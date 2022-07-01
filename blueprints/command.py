from vkbottle.bot import Blueprint, Message
from core.DataBaseController import DataBaseController
from core.PermisionRule import PermisionRule
from typing import List
PREFIX="."


bp = Blueprint()
db = DataBaseController()


async def parser_id(members:List[str]) -> List[int]:
    result=[]
    for member in members:
        if member.find("https://vk.com/") != -1: member = member.replace("https://vk.com/", "")
        if member.find("[id") != -1: member = (member.split('id')[1]).split('|')[0]
        if member.isdigit(): result.append(int(member))
        else: result.append(int((await bp.api.users.get(user_ids=member))[0].id))
    return result


async def get_name(id:int) -> str:
    return (await bp.api.users.get(user_ids=id))[0].first_name + " " + (await bp.api.users.get(user_ids=id))[0].last_name


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


@bp.on.message(PermisionRule(), text=f"{PREFIX}мероприятие <count> <members>")
async def add_event_members(message:Message):
    try:
        members = message.text.split(" ")[2:]
        print(members)
        members = await parser_id(members)
        count = int(message.text.split(" ")[1])
        await db.scores_update_event_count(count, members)
        await message.answer("Баллы добавлены")
    except Exception as e:
        await message.answer("Ошибка при добавлении баллов за мероприятие")
        print(e)


@bp.on.message(PermisionRule(), text=(f"{PREFIX}снять <score> <member>"))
async def remove_score_member(message:Message):
    try:
        member = message.text.split(" ")[2:]
        member = (await parser_id(member))[0]
        score = int(message.text.split(" ")[1])
        await db.scores_update(member, -score)
        await message.answer(f"У пользователя @id{member} снято {score} баллов")
    except Exception as e:
        await message.answer("Ошибка при снятии баллов")
        print(e)


@bp.on.message(PermisionRule(), text=f"{PREFIX}топ <count>")
async def get_top(message:Message):
    try:
        count = int(message.text.split(" ")[1])
        members = await db.get_top_members_by_score(count)
        result = ""
        n=1
        for member in members:
            name = await get_name(member['_id'])
            result += ''.join(f'{n}. @id{member["_id"]} ({name}):   {member["scores"]} баллов \n')
            n+=1      
        await message.answer(f"Топ {count} пользователей:\n{result}")
    except Exception as e:
        await message.answer("Ошибка при получении топа")
        print(e)


@bp.on.message(text=f"{PREFIX}инфо <member>")
async def get_info(message:Message):
    try:
        member = message.text.split(" ")[1:]
        member = (await parser_id(member))[0]
        name = await get_name(member)
        likes=await db.get_likes_by_id(member)
        comment=await db.get_comments_by_id(member)
        event=await db.get_events_by_id(member)
        scores = await db.get_scores_by_id(member)
        await message.answer(f"Информация о пользователе @id{member} ({name}):\n❤ Лайков: {likes}\n💬 Комментариев: {comment}\n🎉 Мероприятий: {event}\n🔥Баллов: {scores}")
    except Exception as e:
        await message.answer("Ошибка при получении информации")
        print(e)


@bp.on.message(PermisionRule(), text=f"{PREFIX}новыймесяц")
async def new_month(message:Message):
    try:
        await db.reset_members()
        await message.answer("Рейтинг сброшен. Удачи в следующем месяце!")
    except Exception as e:
        await message.answer("Ошибка при сбросе баллов")
        print(e)
