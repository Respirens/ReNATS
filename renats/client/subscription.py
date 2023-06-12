import uuid
from datetime import datetime
from typing import Callable, Any, Final

from renats.client.message import Message
from renats.connection.base import Connection

SubscriptionCallbackType = Callable[[Message], Any]

MICROSECONDS_IN_SECOND: Final[int] = 1_000_000


def generate_subscription_id() -> str:
    total_microseconds = int(datetime.utcnow().timestamp() * MICROSECONDS_IN_SECOND)
    return uuid.uuid4().hex + hex(total_microseconds)


class Subscription:
    def __init__(self, subscription_id: str, subject: str, callback: SubscriptionCallbackType):
        self.id = subscription_id
        self.subject = subject
        self.callback = callback


class SubscriptionManager:
    def __init__(self):
        self._callbacks: dict[str, SubscriptionCallbackType] = {}

    def create(self, subject: str, callback: SubscriptionCallbackType) -> Subscription:
        subscription = Subscription(generate_subscription_id(), subject, callback)
        self._callbacks[subscription.id] = subscription.callback
        return subscription

    def delete(self, subscription_id: str):
        del self._callbacks[subscription_id]

    async def handle(self, message: Message):
        pass
