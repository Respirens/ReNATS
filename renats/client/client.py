import asyncio
import logging
from asyncio import Task
from typing import Final

import msgspec.json
from typing_extensions import Self

from . import parser
from .base import NATS, HeadersType
from .message import Message
from .subscription import Subscription, SubscriptionManager, SubscriptionCallbackType
from ..connection.base import Connection
from ..connection.tcp import TcpConnection
from ..protocol import protocol
from ..protocol.messages.msg import MsgProtocolMessage, HMsgProtocolMessage
from ..protocol.messages.pub import PubProtocolMessage, HPubProtocolMessage
from ..protocol.messages.service import InfoProtocolMessage, ConnectProtocolMessage
from ..protocol.messages.sub import SubProtocolMessage, UnsubProtocolMessage

DEFAULT_CONNECTION_TIMEOUT: Final[float] = 2
DEFAULT_INFO_WAITING_TIMEOUT: Final[float] = 2

CLIENT_LANGUAGE: Final[str] = "python3"
CLIENT_VERSION: Final[str] = "0.2.2-alpha-3"

CLIENT_CONNECTION_VERBOSE: Final[bool] = False
CLIENT_CONNECTION_PEDANTIC: Final[bool] = True
CLIENT_SUPPORT_HEADERS: Final[bool] = False


class NATSClient(NATS):

    def __init__(self):
        self._logger: logging.Logger = logging.getLogger(__name__)
        self._connection: Connection | None = None
        self._connection_info: InfoProtocolMessage | None = None
        self._handler_task: Task | None = None
        self._subscriptions: SubscriptionManager = SubscriptionManager()

    @property
    def available(self) -> bool:
        return all(
            (
                self._connection is not None,
                not self._connection.closed,
                self._connection_info is not None
            )
        )

    @property
    def connection(self) -> Connection:
        return self._connection

    @property
    def connection_info(self) -> InfoProtocolMessage:
        return self._connection_info

    async def _init_connection(self):
        # Wait for INFO protocol message and parse it
        info = msgspec.json.decode(
            (await self._connection.readline()).split(b" ", 1)[1].decode(),
            type=InfoProtocolMessage
        )

        # Save INFO protocol message in the client class
        self._connection_info = info

        # Send CONNECT protocol message
        await self._connection.send(
            ConnectProtocolMessage(
                verbose=CLIENT_CONNECTION_VERBOSE,
                pedantic=CLIENT_CONNECTION_PEDANTIC,
                tls_required=False,
                lang=CLIENT_LANGUAGE,
                version=CLIENT_VERSION,
                headers=CLIENT_SUPPORT_HEADERS
            ).dump()
        )

    async def _handle_message(self, protocol_message: MsgProtocolMessage | HMsgProtocolMessage):
        # Skip message if its subscription id not registered in subscription manager
        if protocol_message.sid not in self._subscriptions:
            return

        # Create Message class instance from MsgProtocolMessage or HMsgProtocolMessage
        message = Message(
            subject=protocol_message.subject,
            payload=protocol_message.payload,
            reply_subject=protocol_message.reply_to,
            headers=protocol_message.headers if isinstance(protocol_message, HMsgProtocolMessage) else None
        )

        # Create message handler task (message handled by subscription manager)
        asyncio.create_task(self._subscriptions.handle(protocol_message.sid, message))

    async def _handle_connection_input(self):
        while True:
            # Wait for "head" line and read it
            # The "head" is the first line of the protocol message.
            head_line = await self.connection.readline()

            # Split the "head" line to method and params line
            head = head_line.split(b" ", 1)
            method = head[0].strip()

            if method == protocol.PING:
                await self._connection.send(protocol.PONG_MESSAGE)
            elif method == protocol.ERR:
                self._logger.error("Received NATS error: %s", head[1])
            elif method == protocol.MSG:
                protocol_message = await parser.parse_msg(head_line, self._connection)
                await self._handle_message(protocol_message)
            elif method == protocol.HMSG:
                protocol_message = await parser.parse_hmsg(head_line, self._connection)
                await self._handle_message(protocol_message)
            else:
                self._logger.warning("Received unknown NATS protocol message: %s", head_line)

    async def connect(self, servers: tuple[tuple[str, int]]) -> Self:
        # Temporary. This will be updated for using multiserver connection
        host, port = servers[0]

        self._connection = TcpConnection()
        await self.connection.connect(host, port, DEFAULT_CONNECTION_TIMEOUT)
        await self._init_connection()
        self._handler_task = asyncio.get_running_loop().create_task(self._handle_connection_input())
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
        subscription = self._subscriptions.create(subject, callback, self)
        message = SubProtocolMessage(
            subject=subscription.subject,
            sid=subscription.id
        )
        await self._connection.send(message.dump())
        return subscription

    async def unsubscribe(self, subscription_id: str, messages_left: int = 0):
        message = UnsubProtocolMessage(
            sid=subscription_id,
            max_msgs=messages_left
        )
        await self._connection.send(message.dump())
        self._subscriptions.delete(subscription_id, messages_left)

    async def request(self, subject: str, payload: bytes, headers: HeadersType = None, timeout: float = None):
        raise NotImplementedError()
