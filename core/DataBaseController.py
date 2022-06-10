import datetime

from requests import delete
from core.config import mongo
from typing import List

import motor.motor_asyncio
client = motor.motor_asyncio.AsyncIOMotorClient(mongo)


class DataBaseController:

    _SCORE_BY_LIKE = 1
    _SCORE_BY_COMMENT = 1

    def __init__(self):
        self._db = client.LDPR34
        self._polls = self._db.polls
        self._members = self._db.members
        self._info = self._db.info


    async def check_user(self, id:int) -> bool:
        '''Проверяет на существование пользователя в базе данных'''
        return await self._members.find_one({"_id": id}) is not None

    
    async def add_user(self, id:int):
        '''Добавляет пользователя в базу данных'''
        await self._members.insert_one({"_id": id, "event": 0, "scores": 0, "like": 0, "comment": 0})


    async def scores_update(self, id:int, score:int):
        '''Обновляет количество баллов пользователя'''
        if self.check_user(id): await self.add_user(id)
        await self._members.update_one({"_id": id}, {"$inc": {"scores": score}})


    async def scores_update_event(self, events_members:List[int]):
        '''Обновляет количество баллов пользователя за мероприятие'''
        score = (await self._info.find_one({"_id": 0}))["eventScore"]
        for member in events_members:
            await self.scores_update(member, score)
            await self._members.update_one({"_id": member}, {"$inc": {"event": 1}})
        

    async def scores_update_members(self, members:List[int], score):
        '''Обновляет количество баллов пользователей по списку'''
        for member in members:
            await self.scores_update(member, score)


    async def score_event_update(self, score_event:int):
        '''Обновляет количество баллов за мероприятие'''
        await self._members.update_one({"_id": 0}, {"$set": {"eventScore": score_event}})


    async def addlike(self, id:int):
        '''Добавляет количество лайков пользователя'''
        await self._members.update_one({"_id": id}, {"$inc": {"like": 1}})
        await self.scores_update(id, self._SCORE_BY_LIKE)


    async def removelike(self, id:int):
        '''Уменьшает количество лайков пользователя'''
        await self._members.update_one({"_id": id}, {"$inc": {"like": -1}})
        await self.scores_update(id, -self._SCORE_BY_LIKE)


    async def addcomment(self, id:int):
        '''Добавляет количество комментариев пользователя'''
        await self._members.update_one({"_id": id}, {"$inc": {"comment": 1}})
        await self.scores_update(id, self._SCORE_BY_COMMENT)


    async def removecomment(self, id:int):
        '''Уменьшает количество комментариев пользователя'''
        await self._members.update_one({"_id": id}, {"$inc": {"comment": -1}})
        await self.scores_update(id, -self._SCORE_BY_COMMENT)


    async def getTimeUnix(time:str) -> int:
        '''Конвертирует время в формат unix'''
        return int(datetime.datetime.strptime(time, "%d.%m.%Y %H:%M").timestamp())


    async def add_poll(self, poll_id:int, answer_id:int, time:str):
        '''Добавляет опрос в базу данных'''
        time = await self.getTimeUnix(time).result()
        await self._polls.insert_one({'_id': poll_id, 'answer': answer_id, 'members': [], 'time': time})


    async def edit_time_poll(self, poll_id:int, time:str):
        '''Изменяет время опроса'''
        time = await self.getTimeUnix(time).result()
        await self._polls.update_one({"_id": poll_id}, {"$set": {"time": time}})


    async def add_members_in_poll(self, poll_id:int, member:int):
        '''Добавляет пользователя в опрос'''
        await self._polls.update_one({"_id": poll_id}, {"$push": {"members": member}})


    async def top_members(self, count:int) -> List[int]:
        '''Возвращает список лучших пользователей'''
        return await self._members.find({"scores": {"$gt": 0}}).sort("scores", -1).limit(count)


    async def top_member_count_id(self, count:int) -> int:
        '''Возращает id пользователя на count месте в топе по scores'''
        return (await self._members.find({"scores": {"$gt": 0}}).sort("scores", -1).to_list(count))[-1]["_id"]


    async def get_score(self, id:int) -> int:
        '''Возвращает количество баллов пользователя'''
        return (await self._members.find_one({"_id": id}))["scores"]


    async def get_quntity_like_user(self, id:int) -> int:
        '''Возвращает количество лайков пользователя'''
        return (await self._members.find_one({"_id": id}))["like"]

    
    async def get_quntity_comment_user(self, id:int) -> int:
        '''Возвращает количество комментариев пользователя'''
        return (await self._members.find_one({"_id": id}))["comment"]


    async def get_quntity_event_user(self, id:int) -> int:
        '''Возвращает количество мероприятий пользователя'''
        return (await self._members.find_one({"_id": id}))["event"]


    async def check_poll_time(self, time:int) -> bool:
        '''Проверяет на время опроса все опросы'''
        return await self._polls.find_one({"time": {"$lt": time}}) is not None


    async def get_event_list(self):
        '''Возвращает все опросы в базе данных'''
        return await self._polls.find().to_list(None)


    async def get_memebers_event(self, id:int) -> List[int]:
        '''Возвращает список пользователей в опросе'''
        return (await self._polls.find_one({"_id": id}))["members"]


    async def delete_poll(self, id:str):
        '''Удаляет опрос'''
        await self._polls.delete_one({"_id": id})


    async def get_events_by_time(self, time:int) -> List[int]:
        '''Возвращает список вопросов у которых время опроса меньше чем time'''
        return await self._polls.find({"time": {"$lt": time}}).to_list(None)

