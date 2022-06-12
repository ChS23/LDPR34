from vkbottle.dispatch.rules import ABCRule
from vkbottle.bot import Message

class PermisionRule(ABCRule):
    async def check(self, message: Message) -> bool:
        return message.from_id in [15895536,326129427]