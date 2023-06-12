from abc import ABC, abstractmethod

from typing_extensions import Self

from renats.client.client import HeadersType
from renats.client.subscription import SubscriptionCallbackType, Subscription


class NATS(ABC):
    @abstractmethod
    async def connect(self, servers: tuple[tuple[str, int]]) -> Self:
        raise NotImplementedError()

    @abstractmethod
    async def publish(self, subject: str, payload: bytes = b"", reply_subject: str = None, headers: HeadersType = None):
        raise NotImplementedError()

    @abstractmethod
    async def subscribe(self, subject: str, callback: SubscriptionCallbackType) -> Subscription:
        raise NotImplementedError()

    @abstractmethod
    async def unsubscribe(self, subscription_id: str, messages_left: int = 0):
        raise NotImplementedError()
