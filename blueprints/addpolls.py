from distutils.sysconfig import PREFIX
from email import message
import random
from time import sleep
from vkbottle.bot import Blueprint, Message
from vkbottle import GroupEventType, GroupTypes, Keyboard, KeyboardButtonColor, Text, User
from core.config import user
from core.DataBaseController import DataBaseController


bp = Blueprint()
db = DataBaseController()

# Проверяет пост на наличее опроса
# Если опрос есть, то добавляет всех ответивших на опрос в базу данных
# Если опроса нет, то пропускает пост
@bp.on.raw_event(GroupEventType.WALL_POST_NEW, dataclass=GroupTypes.WallPostNew)
async def check_newpost(event:GroupTypes.WallPostNew):
    if event.object.attachments[0].type.value == 'poll':
        if event.object.attachments[0].poll.answers[0].text == '+':
            poll_id:int = int(str(event.object.attachments[0].poll.embed_hash)[0:9])
            answer_id:int = event.object.attachments[0].poll.answers[0].id
            time:str = event.object.attachments[0].poll.question
            try:
                await db.add_poll(poll_id, answer_id, time)
                print('Опрос добавлен')
            except Exception as e:
                print('Приозошла ошибка при добавлении опроса в базу данных')
                print(e)


# Команда для изменения времени опроса в базе данных
# Пример использования:
# .poll_time id опроса дд.мм.гггг чч:мм
@bp.on.message(text=f'{PREFIX}времяопроса <poll_id> <time>')
async def poll_time(message:Message):
	try:
		poll_id = message.text.split(' ')[1]
		time = message.text.split(' ')[2] + ' ' + message.text.split(' ')[3]
		db.edit_time_poll(poll_id, time)
		await message.answer('Время опроса изменено')
	except:
		await message.answer('Неверный формат времени')


# Определяет наличие новых ответов на опрос
# Если ответ есть, то добавляет его в базу данных
# Если ответа нет, то пропускает пост
@bp.on.raw_event(GroupEventType.POLL_VOTE_NEW, dataclass=GroupTypes.PollVoteNew)
async def check_new_answer(event:GroupTypes.PollVoteNew):
    poll_id = int(str(event.object.poll_id)[0:9])
    try:
        await db.add_members_in_poll(poll_id, event.object.user_id)
        print('Ответ добавлен')
    except Exception as e:
        print(e)
        print('Приозошла ошибка при добавлении пользователя в базу данных')


# При нажатии на кнопку с надписью "Начать"
# Выводит кнопку с текстом "Разрешить отправку сообщений"
@bp.on.chat_message(text=['Начать'])
async def start_poll(message: Message):
    keyboard=(
            Keyboard(one_time=False)
            .add(Text('Разрешить отправку сообщений'), {'request_contact': 'allow'}, color=KeyboardButtonColor.POSITIVE)
            )
    await message.answer(
        message="Нажмите на кнопку, чтобы разрешить отправку сообщений",
        keyboard=keyboard.get_json()
    )


# Подписаться на рассылку сообщений 
@bp.on.private_message(payload={'request_contact':'allow'})
async def allow_send_message(message: Message):
    keyboard=(
        Keyboard(one_time=False)
        .add(Text('Подписаться на рассылку сообщений'), {'request_contact': 'send'}, color=KeyboardButtonColor.POSITIVE)
        )
    await message.answer(
        message="Вы успешно дали разрешение на отправку сообщений",
        keyboard=keyboard.get_json()
    )


@bp.on.private_message(payload={'request_contact':'send'})
async def send_message(message: Message):
    keyboard=(
        Keyboard(one_time=False)
        .add(Text('Подписаться на рассылку сообщений'), {'request_contact': 'send'}, color=KeyboardButtonColor.POSITIVE)
        )
    await message.answer(
        message="Рассылка сообщений пока недоступна",
        keyboard=keyboard.get_json()
    )


# # Отправить напоминание о мероприятии через n часов
# async def send_reminder(id:int, n: int):
# 	name = bp.api.users.users_get(user_ids=id)[0].first_name
# 	message = f"{name}, напоминаем о мероприятии через {n} часов."
# 	try:
# 		await user.api.messages.send(user_id=id, message=message, random_id=random.randint(0, 2**64))
# 	except:
# 		try:
# 			await bp.api.messages.send(user_id=id, message=message, random_id=random.randint(0, 2**64))
# 		except:
# 			print('Не удалось отправить сообщение')