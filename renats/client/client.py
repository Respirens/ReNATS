import asyncio
import logging
from asyncio import Task
from typing import Final

import msgspec.json
from typing_extensions import Self

from . import parser
from .subscription import Subscription
from .types import Server
from ..connection.base import BaseConnection
from ..connection.tcp import TcpConnection
from ..protocol import protocol
from ..protocol.messages.msg import MsgProtocolMessage, HMsgProtocolMessage
from ..protocol.messages.pub import PubProtocolMessage, HPubProtocolMessage
from ..protocol.messages.service import InfoProtocolMessage, ConnectProtocolMessage

DEFAULT_CONNECTION_TIMEOUT: Final[float] = 2
DEFAULT_INFO_TIMEOUT: Final[float] = 2
CLIENT_LANGUAGE: Final[str] = "python3"
CLIENT_VERSION: Final[str] = "0.0.1-alpha"


class NATSClient:
    def __init__(self):
        self._logger: logging.Logger = logging.getLogger(__name__)
        self._connection: BaseConnection | None = None
        self._server: Server | None = None
        self._handler_task: Task | None = None
        self._subscriptions: dict[str, Subscription] = {}

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

    async def send(self, message: bytes):
        self._connection.write(message)
        await self._connection.drain()

    async def _process_connection_init(self):
        info = msgspec.json.decode(
            (await self.connection.readline()).split(b" ", 1)[1].decode(),
            type=InfoProtocolMessage
        )
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
            ).dump()
        )

    async def _process_msg(self, msg: MsgProtocolMessage):
        pass

    async def _process_hmsg(self, msg: HMsgProtocolMessage):
        pass

    async def _handler(self):
        while True:
            line = await self.connection.readline()
            head = line.split(b" ", 1)
            match head[0].strip():
                case protocol.PING:
                    await self.send(protocol.PONG_MESSAGE)
                case protocol.ERR:
                    self.logger.error("Received NATS Error: %s", head[1])
                case protocol.MSG:
                    await self._process_msg(await parser.parse_msg(line, self.connection))
                case protocol.HMSG:
                    await self._process_hmsg(await parser.parse_hmsg(line, self.connection))
                case _:
                    self.logger.warning(f"Received unknown NATS protocol message: %s", line)

    async def connect(self, host: str, port: int) -> Self:
        self.connection = TcpConnection()
        await self.connection.connect(host, port, DEFAULT_CONNECTION_TIMEOUT)
        await self._process_connection_init()
        self._handler_task = asyncio.get_running_loop().create_task(self._handler())
        return self

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
                ).dump()
            )
            return
        await self.send(
            PubProtocolMessage(
                subject=subject,
                payload=data,
                reply_to=reply
            ).dump()
        )
