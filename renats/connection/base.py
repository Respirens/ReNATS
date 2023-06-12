from abc import ABC, abstractmethod


class Connection(ABC):
    @abstractmethod
    async def connect(self, host: str, port: int, timeout: float):
        raise NotImplementedError()

    @abstractmethod
    async def read(self, size: int) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    async def readline(self) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    async def readexactly(self, size: int) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def write(self, data: bytes):
        raise NotImplementedError()

    @abstractmethod
    async def drain(self):
        raise NotImplementedError()

    async def send(self, data: bytes):
        self.write(data)
        await self.drain()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    async def closed(self) -> bool:
        raise NotImplementedError()
