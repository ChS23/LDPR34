from distutils.sysconfig import PREFIX
from time import sleep
from vkbottle.bot import Blueprint, Message
from vkbottle import API, Bot, GroupEventType, GroupTypes, VKAPIError
from core.config import user
import datetime
from blueprints.raiting import lw
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
			poll_id = str(event.object.attachments[0].poll.embed_hash)[0:9]
			answer_id = event.object.attachments[0].poll.answers[0].id
			time:int = event.object.attachments[0].poll.question
			try:
				await db.add_poll(poll_id, answer_id, time)
				print('Опрос добавлен')
			except:
				print('Приозошла ошибка при добавлении опроса в базу данных')


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
	poll_id = str(event.object.poll_id)[0:9]
	try:
		await db.add_members_in_poll(poll_id, event.object.user_id)
		print('Ответ добавлен')
	except:
		print('Приозошла ошибка при добавлении пользователя в базу данных')