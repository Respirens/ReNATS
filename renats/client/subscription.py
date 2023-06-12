import inspect
from typing import Callable, Any

import uuid6

from renats.client.base import NATS
from renats.client.message import Message

SubscriptionCallbackType = Callable[[Message], Any]


def generate_subscription_id() -> str:
    return uuid6.uuid7().hex


class Subscription:
    def __init__(self, subscription_id: str, subject: str, callback: SubscriptionCallbackType, client: NATS):
        self.id = subscription_id
        self.subject = subject
        self.callback = callback
        self._client = client

    async def unsubscribe(self, messages_left: int = 0):
        await self._client.unsubscribe(self.id, messages_left)


class SubscriptionManager:
    def __init__(self):
        self._messages_left: dict[str, int] = {}
        self._callbacks: dict[str, SubscriptionCallbackType] = {}

    def create(self, subject: str, callback: SubscriptionCallbackType, client: NATS) -> Subscription:
        subscription = Subscription(generate_subscription_id(), subject, callback, client)
        self._callbacks[subscription.id] = subscription.callback
        return subscription

    def delete(self, subscription_id: str, messages_left: int):
        if messages_left > 0:
            self._messages_left[subscription_id] = messages_left
            return
        del self._callbacks[subscription_id]

    def __contains__(self, item: str):
        return item in self._callbacks

    async def handle(self, subscription_id: str, message: Message):
        callback = self._callbacks[subscription_id]
        if inspect.iscoroutinefunction(callback):
            await callback(message)
        else:
            callback(message)
