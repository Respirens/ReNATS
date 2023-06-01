from abc import ABC, abstractmethod


class BaseNatsClient(ABC):
    @abstractmethod
    async def connect(self, host: str, port: int):
        raise NotImplementedError()
