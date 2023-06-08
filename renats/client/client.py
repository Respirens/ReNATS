import asyncio
import logging
from asyncio import Task
from typing import Final

import msgspec.json

from .types import Server
from ..connection.base import BaseConnection
from ..connection.tcp import TcpConnection
from ..protocol import protocol, utils
from ..protocol.messages.base import SerializableProtocolMessage
from ..protocol.messages.pub import PubProtocolMessage, HPubProtocolMessage
from ..protocol.messages.service import InfoProtocolMessage, ConnectProtocolMessage

DEFAULT_CONNECTION_TIMEOUT: Final[float] = 2
DEFAULT_INFO_TIMEOUT: Final[float] = 2
CLIENT_LANGUAGE: Final[str] = "python3"
CLIENT_VERSION: Final[str] = "0.0.1-alpha"


class NatsClient:
    def __init__(self):
        self._connection: BaseConnection | None = None
        self._server: Server | None = None
        self._logger: logging.Logger = logging.getLogger(__name__)
        self._handler_task: Task | None = None

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, value: BaseConnection):
        if self._connection is not None and not self._connection.closed:
            raise RuntimeError("Replacing non-closed connection is not allowed")
        self._connection = value

    @property
    def available(self):
        return (
                self._connection is not None
                and
                not self._connection.closed
                and
                self._server is not None
        )

    @property
    def server(self):
        return self._server

    @property
    def logger(self):
        return self._logger

    async def send_raw(self, message: bytes):
        self._connection.write(message)
        await self._connection.drain()
        self.logger.info(f"Protocol message sent: {message}")

    async def send(self, protocol_message: SerializableProtocolMessage):
        await self.send_raw(protocol_message.dump())

    async def _process_connection_init(self):
        info = msgspec.json.decode(
            (await self.connection.readline()).split(b" ", 1)[1].decode(),
            type=InfoProtocolMessage
        )
        self.logger.info(f"Received INFO: {info}")
        self._server = Server(
            id=info.server_id,
            headers_support=info.headers,
            max_payload=info.max_payload,
            name=info.server_name,
            protocol=info.proto,
            version=info.version
        )
        await self.send(
            ConnectProtocolMessage(
                verbose=False,
                pedantic=True,
                tls_required=False,
                lang=CLIENT_LANGUAGE,
                version=CLIENT_VERSION,
                headers=True
            )
        )

    async def _handler(self):
        while True:
            line = await self.connection.readline()
            self.logger.info(f"Received protocol message line: {line}")
            if line == protocol.PING + utils.CRLF:
                await self.send_raw(protocol.PONG + utils.CRLF)

    async def connect(self, host: str, port: int):
        self.connection = TcpConnection()
        await self.connection.connect(host, port, DEFAULT_CONNECTION_TIMEOUT)
        await self._process_connection_init()
        self._handler_task = asyncio.get_running_loop().create_task(self._handler())

    async def close(self):
        self._handler_task.cancel()
        await self.connection.close()

    async def publish(self, subject: str, data: bytes = b"", reply: str = None, headers: dict[str, str] = None):
        if self.server.headers_support and headers is not None:
            await self.send(
                HPubProtocolMessage(
                    subject=subject,
                    payload=data,
                    reply_to=reply,
                    headers=headers
                )
            )
            return
        await self.send(
            PubProtocolMessage(
                subject=subject,
                payload=data,
                reply_to=reply
            )
        )


async def connect(host: str = "127.0.0.1", port: int = 4222) -> NatsClient:
    client = NatsClient()
    await client.connect(host, port)
    return client
