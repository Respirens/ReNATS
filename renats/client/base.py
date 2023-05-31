from abc import ABC, abstractmethod


class BaseNatsClient(ABC):
    @abstractmethod
    async def connect(self, host: str, port: int):
        raise NotImplementedError()

    @abstractmethod
    async def publish(
            self,
            subject: str,
            payload: bytes = None,
            reply_subject: str = None,
            headers: dict[str, str] = None
    ):
        raise NotImplementedError()
