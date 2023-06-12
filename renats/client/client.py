import asyncio
import logging
from asyncio import Task
from typing import Final

import msgspec.json
from typing_extensions import Self

from . import parser
from .subscription import Subscription, SubscriptionManager, SubscriptionCallbackType
from ..connection.base import Connection
from ..connection.tcp import TcpConnection
from ..protocol import protocol
from ..protocol.messages.msg import MsgProtocolMessage, HMsgProtocolMessage
from ..protocol.messages.pub import PubProtocolMessage, HPubProtocolMessage
from ..protocol.messages.service import InfoProtocolMessage, ConnectProtocolMessage
from ..protocol.messages.sub import SubProtocolMessage

DEFAULT_CONNECTION_TIMEOUT: Final[float] = 2
DEFAULT_INFO_WAITING_TIMEOUT: Final[float] = 2

CLIENT_LANGUAGE: Final[str] = "python3"
CLIENT_VERSION: Final[str] = "0.2.1-alpha"

CLIENT_CONNECTION_VERBOSE: Final[bool] = False
CLIENT_CONNECTION_PEDANTIC: Final[bool] = True

HeadersType = dict[str, str]


class NATSClient:
    def __init__(self):
        self._logger: logging.Logger = logging.getLogger(__name__)
        self._connection: Connection | None = None
        self._connection_info: InfoProtocolMessage | None = None
        self._handler_task: Task | None = None
        self._subscriptions: SubscriptionManager = SubscriptionManager()

    @property
    def available(self):
        return all(
            (
                self._connection is not None,
                not self._connection.closed,
                self._connection_info is not None
            )
        )

    @property
    def logger(self):
        return self._logger

    @property
    def connection(self):
        return self._connection

    @property
    def connection_info(self):
        return self._connection_info

    async def _process_connection_init(self):
        info = msgspec.json.decode(
            (await self._connection.readline()).split(b" ", 1)[1].decode(),
            type=InfoProtocolMessage
        )
        self._connection_info = info
        await self._connection.send(
            ConnectProtocolMessage(
                verbose=CLIENT_CONNECTION_VERBOSE,
                pedantic=CLIENT_CONNECTION_PEDANTIC,
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
                    await self._connection.send(protocol.PONG_MESSAGE)
                case protocol.ERR:
                    self.logger.error("Received NATS Error: %s", head[1])
                case protocol.MSG:
                    await self._process_msg(await parser.parse_msg(line, self.connection))
                case protocol.HMSG:
                    await self._process_hmsg(await parser.parse_hmsg(line, self.connection))
                case _:
                    self.logger.warning(f"Received unknown NATS protocol message: %s", line)

    async def connect(self, host: str, port: int) -> Self:
        self._connection = TcpConnection()
        await self.connection.connect(host, port, DEFAULT_CONNECTION_TIMEOUT)
        await self._process_connection_init()
        self._handler_task = asyncio.get_running_loop().create_task(self._handler())
        return self

    async def close(self):
        self._handler_task.cancel()
        await self.connection.close()

    async def publish(self, subject: str, payload: bytes = b"", reply_subject: str = None, headers: HeadersType = None):
        if self._connection_info.headers and headers is not None:
            message = HPubProtocolMessage(
                subject=subject,
                payload=payload,
                reply_to=reply_subject,
                headers=headers
            )
        else:
            message = PubProtocolMessage(
                subject=subject,
                payload=payload,
                reply_to=reply_subject
            )
        await self._connection.send(message.dump())

    async def subscribe(self, subject: str, callback: SubscriptionCallbackType) -> Subscription:
        subscription = self._subscriptions.create(subject, callback)
        message = SubProtocolMessage(
            subject=subscription.subject,
            sid=subscription.id
        )
        await self._connection.send(message.dump())
        return subscription
