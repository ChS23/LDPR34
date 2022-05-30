from vkbottle.bot import Blueprint
from vkbottle import API, Bot, GroupEventType, GroupTypes, VKAPIError
from core.database import polls


bp = Blueprint()


@bp.on.raw_event(GroupEventType.WALL_POST_NEW, dataclass=GroupTypes.WallPostNew)
async def check_newpost(event:GroupTypes.WallPostNew):
	print(str(event.object.attachments[0].poll.embed_hash)[0:9])


#
# TODO:Добавить возможность редактировать время напоминания
#  
 
# list=await api.polls.get_voters(poll_id=727652138, answer_ids=[2047972605])
# access_key=None album=None app=None audio=None doc=None event=None graffiti=None group=None link=None market=None market_album=None note=None page=None photo=None poll=PollsPoll(anonymous=False, answer_id=None, answer_ids=[], answers=[PollsAnswer(id=2053489271, rate=0.0, text='1', votes=0), PollsAnswer(id=2053489272, rate=0.0, text='2', votes=0)], author_id=-213296666, background=None, can_edit=True, can_report=False, can_share=True, can_vote=True, closed=False, created=1653060306, disable_unvote=False, embed_hash='730025275_471ca656017d2dddca', end_date=0, friends=None, id=730025275, is_board=False, multiple=False, owner_id=-213296666, photo=None, question='в', votes=0) posted_photo=None type=<WallWallpostAttachmentType.POLL: 'poll'> video=None