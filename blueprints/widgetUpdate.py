# import datetime
# import json
# from core.DataBaseController import DataBaseController
# from vkbottle.bot import Blueprint, Message
# from core.config import widget, user
# from vkbottle import Bot, LoopWrapper, vkscript
# from pytz import timezone

# db = DataBaseController()

# bp = Blueprint()

# @vkscript
# async def get_rating():
#         widgetRating = {
#         "title": "Рейтинг на "+ datetime.datetime.now(timezone("Europe/Moscow")).strftime("%H:%M %d.%m.%Y"),
#         "more": "v." + " " + (await db.get_version())[:(await db.get_version()).find("-")],
#         "more_url": "https://vk.com/chs23",
#         "head": [
#             {
#                 "text": "Участник",
#                 "align": "left"
#             },
#             {
#                 "text": "❤",
#                 "align": "left"
#             },
#             {
#                 "text": "💬",
#                 "align": "left"
#             },
#             {
#                 "text": "🎉",
#                 "align": "left"
#             },
#             {
#                 "text": "Баллы",
#                 "align": "left"
#             }
#         ],
#         "body": [
#             [
#                 {
#                     "text": (await bp.api.users.get(await db.top_member_count_id(1)))[0].first_name + " " + (await bp.api.users.get(await db.top_member_count_id(1)))[0].last_name,
#                     "icon_id": "id"+str(await db.top_member_count_id(1)),
#                 },
#                 {
#                     "text": await db.get_quntity_like_user(await db.top_member_count_id(1)),
#                 },
#                 {
#                     "text": await db.get_quntity_comment_user(await db.top_member_count_id(1)),
#                 },
#                 {
#                     "text": await db.get_quntity_event_user(await db.top_member_count_id(1)),
#                 },
#                 {
#                     "text": await db.get_score(await db.top_member_count_id(1))
#                 }
#             ],
#             [
#                 {
#                     "text": (await bp.api.users.get(await db.top_member_count_id(2)))[0].first_name + " " + (await bp.api.users.get(await db.top_member_count_id(2)))[0].last_name,
#                     "icon_id": "id"+str(await db.top_member_count_id(2)),
#                 },
#                 {
#                     "text": await db.get_quntity_like_user(await db.top_member_count_id(2)),
#                 },
#                 {
#                     "text": await db.get_quntity_comment_user(await db.top_member_count_id(2)),
#                 },
#                 {
#                     "text": await db.get_quntity_event_user(await db.top_member_count_id(2)),
#                 },
#                 {
#                     "text": await db.get_score(await db.top_member_count_id(2))
#                 }
#             ],
#             [
#                 {
#                     "text": (await bp.api.users.get(await db.top_member_count_id(3)))[0].first_name + " " + (await bp.api.users.get(await db.top_member_count_id(3)))[0].last_name,
#                     "icon_id": "id"+str(await db.top_member_count_id(3)),
#                 },
#                 {
#                     "text": await db.get_quntity_like_user(await db.top_member_count_id(3)),
#                 },
#                 {
#                     "text": await db.get_quntity_comment_user(await db.top_member_count_id(3)),
#                 },
#                 {
#                     "text": await db.get_quntity_event_user(await db.top_member_count_id(3)),
#                 },
#                 {
#                     "text": await db.get_score(await db.top_member_count_id(3))
#                 }
#             ],
#             [
#                 {
#                     "text": (await bp.api.users.get(await db.top_member_count_id(4)))[0].first_name + " " + (await bp.api.users.get(await db.top_member_count_id(4)))[0].last_name,
#                     "icon_id": "id"+str(await db.top_member_count_id(4)),
#                 },
#                 {
#                     "text": await db.get_quntity_like_user(await db.top_member_count_id(4)),
#                 },
#                 {
#                     "text": await db.get_quntity_comment_user(await db.top_member_count_id(4)),
#                 },
#                 {
#                     "text": await db.get_quntity_event_user(await db.top_member_count_id(4)),
#                 },
#                 {
#                     "text": await db.get_score(await db.top_member_count_id(4))
#                 }                
#             ],
#             [
#                 {
#                     "text": (await bp.api.users.get(await db.top_member_count_id(5)))[0].first_name + " " + (await bp.api.users.get(await db.top_member_count_id(5)))[0].last_name,
#                     "icon_id": "id"+str(await db.top_member_count_id(5)),
#                 },
#                 {
#                     "text": await db.get_quntity_like_user(await db.top_member_count_id(5)),
#                 },
#                 {
#                     "text": await db.get_quntity_comment_user(await db.top_member_count_id(5)),
#                 },
#                 {
#                     "text": await db.get_quntity_event_user(await db.top_member_count_id(5)),
#                 },
#                 {
#                     "text": await db.get_score(await db.top_member_count_id(5))
#                 }
#             ],
#             [
#                 {
#                     "text": (await bp.api.users.get(Args.uid))[0].first_name + " " + (await bp.api.users.get(await db.top_member_count_id(5)))[0].last_name,
#                     "icon_id": "id"+str(await db.top_member_count_id(5)),
#                 },
#                 {
#                     "text": await db.get_quntity_like_user(await db.top_member_count_id(5)),
#                 },
#                 {
#                     "text": await db.get_quntity_comment_user(await db.top_member_count_id(5)),
#                 },
#                 {
#                     "text": await db.get_quntity_event_user(await db.top_member_count_id(5)),
#                 },
#                 {
#                     "text": await db.get_score(await db.top_member_count_id(5))
#                 }
#             ]
#         ]
#     }
#     return raiting;
# )


# async def update_widget():
#     await Bot(widget).api.app_widgets.update(code=get_rating, type='table')