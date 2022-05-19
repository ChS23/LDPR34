from vkbottle import Bot

from blueprints import bps
from config import GroupAPIToken


bot=Bot(api=GroupAPIToken)

for bp in bps:
    bp.load(bot)

bot.run_forever()