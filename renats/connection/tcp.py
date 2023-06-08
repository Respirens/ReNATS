import asyncio
from asyncio import StreamReader, StreamWriter

from .base import BaseConnection


class TcpConnection(BaseConnection):
    def __init__(self):
        self._reader: StreamReader | None = None
        self._writer: StreamWriter | None = None
        self._closed: bool = True

    async def connect(self, host: str, port: int, timeout: float):
        self._reader, self._writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        self._closed = False

    async def read(self, size: int) -> bytes:
        return await self._reader.read(size)

    async def readexactly(self, size: int) -> bytes:
        return await self._reader.readexactly(size)

    async def readline(self) -> bytes:
        return await self._reader.readline()

    def write(self, data: bytes):
        self._writer.write(data)

    async def drain(self):
        await self._writer.drain()

    async def close(self):
        self._writer.close()
        await self._writer.wait_closed()
        self._closed = True

    @property
    def closed(self) -> bool:
        return self._closed
