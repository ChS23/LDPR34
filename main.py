from vkbottle import Bot
from blueprints import bps
from core.config import token
from blueprints.raiting import lw


bot=Bot(token)


for bp in bps:
    bp.load(bot)


bot.loop_wrapper = lw
bot.run_forever()