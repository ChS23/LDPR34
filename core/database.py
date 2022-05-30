from core.config import mongo

import motor.motor_asyncio
client = motor.motor_asyncio.AsyncIOMotorClient(mongo)

db = client.LDPR34
polls = db.polls
members = db.members
info = db.info
# polls.insert_one({"_id": 234445, "name": 'vot'})


async def scores_update_event(id:int, event:bool=False, score:int=0):
    count = await members.count_documents({"_id": id})
    if count==0:
        match event:
            case True:
                await members.insert_one({"_id": id, "event": 1, "scores": (await info.find_one({"_id": "0"}))["event"]})
            case False:
                await members.insert_one({"_id": id, "event": 0, "scores": score})   
    else:
        scores:int = (await members.find_one({"_id": id}))["scores"]
        events:int = (await members.find_one({"_id": id}))["event"]
        match event:
            case True:
                await members.update_one({"_id": id}, {"$set": {"scores": scores + (await info.find_one({"_id": "0"}))["event"]}})
                await members.update_one({"_id": id}, {"$set": {"event": events + 1}})
            case False:
                await members.update_one({"_id": id}, {"$set": {"scores": scores+int(score)}})


async def scores_update(id:int, math:str, score:int):
    """add or remove score"""
    count = await members.count_documents({"_id": id})
    match math:
        case '+':
            match count:
                case 0:
                    await members.insert_one({"_id": id, "event": 0, "scores": score})
                case _:
                    scores=(await members.find_one({"_id": id}))["scores"]
                    await members.update_one({"_id": id}, {"$set": {"scores": scores+score}})
        case '-':
            match count:
                case 0:
                    await members.insert_one({"_id": id, "event": 1, "scores": score})
                case _:
                    scores = (await members.find_one({"_id": id}))["scores"]
                    await members.update_one({"_id": id}, {"$set": {"scores": scores-score}})