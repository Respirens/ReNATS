from typing import Callable, Awaitable

from renats.client.message import Message

SubscriptionCallbackType = Callable[[Message], Awaitable]


class Subscription:
    def __init__(self, sid: str, subject: str, callback: SubscriptionCallbackType):
        self.id = sid
        self.subject = subject
        self.callback = callback

    async def __call__(self, message: Message):
        await self.callback(message)
