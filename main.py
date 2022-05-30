from vkbottle import Bot
from blueprints import bps
from core.config import token
from blueprints.raiting import lw


bot=Bot(token)

for bp in bps:
    bp.load(bot)


from core.database import polls
async def check_polls():
	return [i for i in polls.find()]


@bot.on.message()
async def test(text=['test']):
    print(await check_polls())


bot.loop_wrapper = lw
bot.run_forever()