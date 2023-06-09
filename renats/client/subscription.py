import inspect
from typing import Callable, Any

from renats.client.message import Message

SubscriptionCallbackType = Callable[[Message], Any]


class Subscription:
    def __init__(self, sid: str, subject: str, callback: SubscriptionCallbackType):
        self.id = sid
        self.subject = subject
        self.callback = callback

    async def __call__(self, message: Message):
        if inspect.iscoroutinefunction(self.callback):
            await self.callback(message)
        else:
            self.callback(message)
