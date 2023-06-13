from io import BytesIO

from renats.connection.base import Connection


class MockConnection(Connection):
    def __init__(self, data: bytes):
        self.io = BytesIO(data)

    async def connect(self, host: str, port: int, timeout: float):
        pass

    async def read(self, size: int) -> bytes:
        return self.io.read(size)

    async def readline(self) -> bytes:
        return self.io.readline()

    async def readexactly(self, size: int) -> bytes:
        return await self.read(size)

    def write(self, data: bytes):
        self.io.write(data)

    async def drain(self):
        self.io.flush()

    async def close(self):
        pass

    @property
    async def closed(self) -> bool:
        return False
