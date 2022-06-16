from core.config import mongo
from typing import List

import motor.motor_asyncio

from core.functions import get_unix_time
client = motor.motor_asyncio.AsyncIOMotorClient(mongo)


class DataBaseController:

    _SCORE_BY_LIKE = 1
    _SCORE_BY_COMMENT = 1
    _TIME_NOTIFY = 60*60*12

    def __init__(self):
        self._db = client.LDPR34
        self._polls = self._db.polls
        self._members = self._db.members
        self._info = self._db.info


    async def check_user(self, id:int) -> bool:
        '''Проверяет на существование пользователя в базе данных'''
        return await self._members.find_one({"_id": id}) is None

    
    async def add_user(self, id:int):
        '''Добавляет пользователя в базу данных'''
        await self._members.insert_one({"_id": id, "event": 0, "scores": 0, "like": 0, "comment": 0})


    async def scores_update(self, id:int, score:int):
        '''Обновляет количество баллов пользователя'''
        if (await self.check_user(id)): await self.add_user(id)
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


    async def add_poll(self, poll_id:int, answer_id:int, time:str):
        '''Добавляет опрос в базу данных'''
        time = get_unix_time(time)
        try:
            await self._polls.insert_one({"_id": poll_id, "answer": answer_id, "members": [], "time": time})
        except Exception as e:
            print(e)


    async def edit_time_poll(self, poll_id:int, time:str):
        '''Изменяет время опроса'''
        time = get_unix_time(time)
        await self._polls.update_one({"_id": poll_id}, {"$set": {"time": time}})


    async def add_members_in_poll(self, poll_id:int, member:int):
        '''Добавляет пользователя в опрос'''
        try:
            await self._polls.update_one({"_id": poll_id}, {"$addToSet": {"members": member}})
        except Exception as e:
            print(e)


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
        time = time + self._TIME_NOTIFY
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
        print("Опрос удален")


    async def get_events_by_time(self, time:int) -> List[int]:
        '''Возвращает список вопросов у которых время опроса меньше чем time'''
        time = time + self._TIME_NOTIFY
        return await self._polls.find({"time": {"$lt": time}}).to_list(None)


    async def get_version(self) -> str:
        '''Возвращает версию базы данных'''
        return (await self._info.find_one({"_id": 0}))["version"]


    async def set_version(self, version:str):
        '''Устанавливает версию бота'''
        await self._info.update_one({"_id": 0}, {"$set": {"version": version}})