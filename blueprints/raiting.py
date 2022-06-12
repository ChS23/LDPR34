import random
from typing import List
from vkbottle import Bot, GroupEventType, GroupTypes, LoopWrapper, User, VKAPIError
from vkbottle.bot import Blueprint, Message
from core.config import widget, user
from datetime import datetime
from core.DataBaseController import DataBaseController
from core.PermisionRule import PermisionRule
PREFIX="."

bp = Blueprint()

lw = LoopWrapper()

db = DataBaseController()

from core.config1 import user
user = User(user)


# Добавляет баллы пользователю, за лайк
@bp.on.raw_event(GroupEventType.LIKE_ADD, dataclass=GroupTypes.LikeAdd)
async def add_like(event:GroupTypes.LikeAdd):
    await db.addlike(event.object.liker_id)


# Забирает баллы у пользователя, за снятие лайка
@bp.on.raw_event(GroupEventType.LIKE_REMOVE, dataclass=GroupTypes.LikeRemove)
async def remove_like(event:GroupTypes.LikeRemove):
    await db.removelike(event.object.liker_id)


# Добавляет баллы пользователю, за комментарий
@bp.on.raw_event(GroupEventType.WALL_REPLY_NEW, dataclass=GroupTypes.WallReplyNew)
async def add_reply(event:GroupTypes.WallReplyNew):
    await db.addcomment(event.object.from_id)


# Забирает баллы у пользователя, за комментарий
@bp.on.raw_event(GroupEventType.WALL_REPLY_DELETE,dataclass=GroupTypes.WallReplyDelete)
async def remove_reply(event:GroupTypes.WallReplyDelete):
    await db.removecomment(event.object.deleter_id)


async def parser_id(members:List[str]) -> List[int]:
    ''''''
    # https://vk.com/evenifulietome
    # https://vk.com/id457045924
    result=[]
    for member in members:
        if member.find("https://vk.com/") != -1: member = member.replace("https://vk.com/", "")
        if member.find("[id") != -1: member = (member.split('id')[1]).split('|')[0]
        if member.isdigit(): result.append(int(member))
        else: result.append(int((await bp.api.users.get(user_ids=member))[0].id))
    return result
        

@bp.on.message(PermisionRule(), text=f"{PREFIX}мероприятие <members>")
async def add_score_event(message:Message):
    try:
        members = message.text.split(" ")[1:]
        members = await parser_id(members)
        await db.scores_update_event(members)
        await message.answer("Баллы добавлены")
    except:
        await message.answer("Ошибка при добавлении баллов")

    # .мероприятие @id23423542 @dasfgrges https://vk.com/id2344523
    # @dfsdfge -> [id23423542|dasfgrges]


@bp.on.message(PermisionRule(), text=f"{PREFIX}баллы <score> <members>")
async def add_score_members(message:Message):
    try:
        members = message.text.split(" ")[2:]
        members = await parser_id(members)
        score = int(message.text.split(" ")[1])
        await db.scores_update_members(members, score)
        await message.answer("Баллы добавлены")
    except Exception as e:
        await message.answer("Ошибка при добавлении баллов")
        print(e)


@bp.on.message(PermisionRule(), text=(f"{PREFIX}снять <score> <member>"))
async def remove_score_member(message:Message):
    member = message.text.split(" ")[2]
    member = await parser_id(member)
    score = int(message.text.split(" ")[1])
    await db.scores_update(member, -score)
    await message.answer(f"У пользователя @id{member} снято {score} баллов")


# Обновить виджет без ожидания обновления
@bp.on.message(PermisionRule(), text=f"{PREFIX}обновитьвиджет")
async def update_widget(message:Message):
    await rating_update()




# @bp.on.message(text=['!баллы <score> <members>'])
# async def add_scores(message:Message):
# 	try:
# 		score = int(message.text.split(' ')[1])
# 		members = message.text.split(' ')[2].split(',')
# 	except:
# 		await message.answer('Неверный формат ввода')
# 		return
# 	for member in members:
# 		try:
# 			if 'vk.com' in member:
# 				member = member.split('/')[-1]
# 				id = bp.api.utils.resolve_screen_name(screen_name=member)['object_id']
# 			else:
# 				id = (member.split('id')[1]).split('|')[0]
# 			# print(id)
# 			match score:
# 				case 'м': await scores_update_event(id, True)
# 				case _: await scores_update_event(id, False, score)
# 		except:
# 			await message.answer('Неверный формат ввода')
# 			return
# 	await message.answer('Баллы добавлены')


@lw.interval(seconds=15)
async def rating_update():
    widgetRating = {
        "title": "Рейтинг на "+datetime.now().strftime("%H:%M %d.%m.%Y"),
        "more": "v." + " " + (await db.get_version())[:(await db.get_version()).find("-")],
        "more_url": "https://vk.com/chs23",
        "head": [
            {
                "text": "Участник",
                "align": "left"
            },
            {
                "text": "❤",
                "align": "left"
            },
            {
                "text": "💬",
                "align": "left"
            },
            {
                "text": "🎉",
                "align": "left"
            },
            {
                "text": "Баллы",
                "align": "left"
            }
        ],
        "body": [
            [
                {
                    "text": (await bp.api.users.get(await db.top_member_count_id(1)))[0].first_name + " " + (await bp.api.users.get(await db.top_member_count_id(1)))[0].last_name,
                    "icon_id": "id"+str(await db.top_member_count_id(1)),
                },
                {
                    "text": await db.get_quntity_like_user(await db.top_member_count_id(1)),
                },
                {
                    "text": await db.get_quntity_comment_user(await db.top_member_count_id(1)),
                },
                {
                    "text": await db.get_quntity_event_user(await db.top_member_count_id(1)),
                },
                {
                    "text": await db.get_score(await db.top_member_count_id(1))
                }
            ],
            [
                {
                    "text": (await bp.api.users.get(await db.top_member_count_id(2)))[0].first_name + " " + (await bp.api.users.get(await db.top_member_count_id(2)))[0].last_name,
                    "icon_id": "id"+str(await db.top_member_count_id(2)),
                },
                {
                    "text": await db.get_quntity_like_user(await db.top_member_count_id(2)),
                },
                {
                    "text": await db.get_quntity_comment_user(await db.top_member_count_id(2)),
                },
                {
                    "text": await db.get_quntity_event_user(await db.top_member_count_id(2)),
                },
                {
                    "text": await db.get_score(await db.top_member_count_id(2))
                }
            ],
            [
                {
                    "text": (await bp.api.users.get(await db.top_member_count_id(3)))[0].first_name + " " + (await bp.api.users.get(await db.top_member_count_id(3)))[0].last_name,
                    "icon_id": "id"+str(await db.top_member_count_id(3)),
                },
                {
                    "text": await db.get_quntity_like_user(await db.top_member_count_id(3)),
                },
                {
                    "text": await db.get_quntity_comment_user(await db.top_member_count_id(3)),
                },
                {
                    "text": await db.get_quntity_event_user(await db.top_member_count_id(3)),
                },
                {
                    "text": await db.get_score(await db.top_member_count_id(3))
                }
            ],
            [
                {
                    "text": (await bp.api.users.get(await db.top_member_count_id(4)))[0].first_name + " " + (await bp.api.users.get(await db.top_member_count_id(4)))[0].last_name,
                    "icon_id": "id"+str(await db.top_member_count_id(4)),
                },
                {
                    "text": await db.get_quntity_like_user(await db.top_member_count_id(4)),
                },
                {
                    "text": await db.get_quntity_comment_user(await db.top_member_count_id(4)),
                },
                {
                    "text": await db.get_quntity_event_user(await db.top_member_count_id(4)),
                },
                {
                    "text": await db.get_score(await db.top_member_count_id(4))
                }                
            ],
            [
                {
                    "text": (await bp.api.users.get(await db.top_member_count_id(5)))[0].first_name + " " + (await bp.api.users.get(await db.top_member_count_id(5)))[0].last_name,
                    "icon_id": "id"+str(await db.top_member_count_id(5)),
                },
                {
                    "text": await db.get_quntity_like_user(await db.top_member_count_id(5)),
                },
                {
                    "text": await db.get_quntity_comment_user(await db.top_member_count_id(5)),
                },
                {
                    "text": await db.get_quntity_event_user(await db.top_member_count_id(5)),
                },
                {
                    "text": await db.get_score(await db.top_member_count_id(5))
                }
            ]
        ]
    }
        
    code = f"return {widgetRating};"

    await Bot(widget).api.app_widgets.update(code=code, type='table')


# Сравнивает время опроса с текущим временем
# Когда осталось 12 часов до начала мероприятия, отправляет всем пользователям напоминание
# lw.interval(60*29)
@lw.interval(seconds=30)
async def event_time_reminder():
    if await db.check_poll_time(datetime.now().timestamp()):
        events = await db.get_events_by_time(datetime.now().timestamp())
        for event in events:
            event_time = datetime.fromtimestamp(event["time"]).strftime('%H:%M %d.%m.%Y')
            members = event['members']
            for member in members:
                try:
                    await bp.api.messages.send(peer_id=member, message=f"Напоминаем, что начало мероприятия в {event_time}", random_id=random.randint(0, 2**64))
                except:
                    try:
                        await user.api.messages.send(user_id=member, message=f"Напоминаем, что начало мероприятия в {event_time}", random_id=random.randint(0, 2**64))
                    except:
                        pass
            await db.delete_poll(event['_id'])


# @lw.interval(seconds=10)
# async def check_time_polls():
#     time_now = int(datetime.now().timestamp())
#     new_polls = polls.find()
#     async for poll in new_polls:
#         if int(poll['time']) - time_now < 60*60*12:
# 			# Отправляем всем пользователям напоминание
#             members=(await polls.find_one({'_id': poll['_id']}))['members']
#             for member in members:
#                 try:
#                     await bp.api.messages.send(peer_id=member, message='До начала мероприятия осталось 12 часов', random_id=0)
#                     await asyncio.sleep(0.5)
#                 except VKAPIError as e:
#                     print('Ошибка отправки напоминания для {}'.format(member))
#             # Удаляем опрос
#             await polls.delete_one({'_id': poll['_id']})
#             print('Опрос удалён')


@bp.on.message(text='test <member>')
async def test(message:Message):
    member = message.text.split(' ')[1]
    print(message.text)