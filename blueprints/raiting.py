from typing import List
from vkbottle import Bot, GroupEventType, GroupTypes, LoopWrapper
from vkbottle.bot import Blueprint, Message
from core.config import widget
from core.database import db, scores_update, scores_update_event
from datetime import datetime


bp = Blueprint()

lw = LoopWrapper()

members = db.members
info = db.info


@bp.on.raw_event(GroupEventType.LIKE_ADD, dataclass=GroupTypes.LikeAdd)
async def check_like(event:GroupTypes.LikeAdd):
    await scores_update(event.object.liker_id, '+', 1)


@bp.on.raw_event(GroupEventType.LIKE_REMOVE, dataclass=GroupTypes.LikeRemove)
async def check_like(event:GroupTypes.LikeRemove):
    await scores_update(event.object.liker_id, '-', 1)


@bp.on.message(text=["+баллы <score> <members_msg>"])
async def scores_add(message:Message, score:int or str, members_msg):
    members = members_msg.split(",")
    print(members)
    match score:
        case 'м':
            for member in members:
                id = int(member[3:12])
                await scores_update_event(id,True)
        case _:
            for member in members:
                id = int(member[3:12])
                await scores_update_event(id,False,score)


@lw.interval(seconds=15)
async def rating_update():
    print("Виджет обновлён")

    topMembers=[]
    cursor=members.find().sort("scores", -1).limit(3)
    i:int=0
    async for document in cursor:
        topMembers.append(document)
        ++i

    widgetRating = {
        "title": "Рейтинг на "+datetime.now().strftime("%H:%M"),
        "head": [
            {
                "text": "Участник",
                "align": "left"
            },
            {
                "text": "Мероприятия",
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
                    "text": (await bp.api.users.get(topMembers[0]["_id"]))[0].first_name,
                    "icon_id": "id"+str(topMembers[0]["_id"])
                },
                {
                    "text": topMembers[0]["event"]
                },
                {
                    "text": topMembers[0]["scores"]
                }
            ],
            [
                {
                    "text": (await bp.api.users.get(topMembers[1]["_id"]))[0].first_name,
                    "icon_id": "id"+str(topMembers[1]["_id"])
                },
                {
                    "text": topMembers[1]["event"]
                },
                {
                    "text": topMembers[1]["scores"]
                }
            ],
            [
                {
                    "text": (await bp.api.users.get(topMembers[2]["_id"]))[0].first_name,
                    "icon_id": "id"+str(topMembers[2]["_id"])
                },
                {
                    "text": topMembers[2]["event"]
                },
                {
                    "text": topMembers[2]["scores"]
                }
            ]
        ]
    }
        
    code = f"return {widgetRating};"

    await Bot(widget).api.app_widgets.update(code=code, type='table')

    
    
# members.insert_one({"_id": 112355, "event": 4, "scores": 43})

# await widget.app_widgets.update(code=codeWidget, type='table')