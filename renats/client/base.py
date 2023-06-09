from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Any

from typing_extensions import Self

from .message import Message

HeadersType = dict[str, str]
SubscriptionCallbackType = Callable[[Message], Any]
SubscriptionType = TypeVar("SubscriptionType", bound="Subscription")


class NATS(ABC):
    @abstractmethod
    async def connect(self, servers: tuple[tuple[str, int]]) -> Self:
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()

    @abstractmethod
    async def send(self, data: bytes):
        raise NotImplementedError()

    @abstractmethod
    async def publish(self, subject: str, payload: bytes = b"", reply_subject: str = None, headers: HeadersType = None):
        raise NotImplementedError()

    @abstractmethod
    async def subscribe(self, subject: str, callback: SubscriptionCallbackType) -> SubscriptionType:
        raise NotImplementedError()

    @abstractmethod
    async def request(
            self,
            subject: str,
            payload: bytes = b"",
            headers: HeadersType = None,
            timeout: float = None
    ) -> Message:
        raise NotImplementedError()
