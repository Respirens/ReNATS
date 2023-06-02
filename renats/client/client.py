import asyncio
from typing import Final

from .info import Server
from ..connection.base import BaseConnection
from ..connection.connection import ConnectionType
from ..connection.tcp import TcpConnection
from ..protocol import protocol, utils
from ..protocol.exceptions import UnknownProtocolMessage
from ..protocol.messages.base import BaseProtocolMessageHandler, BaseProtocolMessageParser
from ..protocol.messages.connect import ConnectProtocolMessage
from ..protocol.messages.hpub import HPubProtocolMessage
from ..protocol.messages.info import InfoProtocolMessageHandler, InfoProtocolMessageParser
from ..protocol.messages.msg import MsgProtocolMessageHandler, MsgProtocolMessageParser
from ..protocol.messages.pub import PubProtocolMessage

DEFAULT_CONNECTION_TIMEOUT: Final[float] = 2
DEFAULT_INFO_TIMEOUT: Final[float] = 2
CLIENT_LANGUAGE: Final[str] = "python3"
CLIENT_VERSION: Final[str] = "0.0.1-alpha"


class NatsClient:
    def __init__(self):
        self._connection: BaseConnection | None = None
        self._server: Server | None = None
        self._handlers: dict[bytes, BaseProtocolMessageHandler] = {
            protocol.INFO: InfoProtocolMessageHandler(),
            protocol.MSG: MsgProtocolMessageHandler()
        }
        self._parsers: dict[bytes, BaseProtocolMessageParser] = {
            protocol.INFO: InfoProtocolMessageParser(),
            protocol.MSG: MsgProtocolMessageParser()
        }

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, value: BaseConnection):
        if not self._connection.closed:
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

    async def _handle_messages(self):
        while True:
            data = await self._connection.readline()
            method = data[:data.find(b" ")].strip()
            print(method)

            if method not in protocol.MESSAGES:
                raise UnknownProtocolMessage(method)
            if method == protocol.PING:
                await self._connection.send(protocol.PONG + utils.CRLF)
                continue
            if method == protocol.OK:
                continue

            parser = self._parsers[method]
            with parser:
                parser.parse_head(data)
                if parser.required > 0:
                    parser.parse_body(await self._connection.readexactly(parser.required))
                message = parser.result
            asyncio.create_task(self._handlers[method].handle(message))

    async def _handle_connection(self):
        raw_info = await asyncio.wait_for(self._connection.readline(), DEFAULT_INFO_TIMEOUT)
        info_parser = self._parsers[protocol.INFO]
        with info_parser:
            info_parser.parse_head(raw_info)
            info = info_parser.result
        self._server = Server(
            id=info.server_id,
            name=info.server_name,
            version=info.version,
            protocol=info.proto,
            max_payload=info.max_payload,
            headers_support=info.headers
        )
        await self._connection.send(
            ConnectProtocolMessage(
                verbose=True,
                pedantic=True,
                tls_required=False,
                lang=CLIENT_LANGUAGE,
                version=CLIENT_VERSION
            ).dump()
        )

    async def connect(self, host: str, port: int, connection_type: ConnectionType = ConnectionType.TCP):
        if connection_type is ConnectionType.TCP:
            self._connection = TcpConnection()
            await self._connection.connect(host, port, DEFAULT_CONNECTION_TIMEOUT)
        else:
            raise ValueError(f"Unknown connection type {connection_type}")
        await self._handle_connection()
        asyncio.create_task(self._handle_messages())

    async def publish(
            self,
            subject: str,
            payload: bytes = b"",
            reply_subject: str = None,
            headers: dict[str, str] = None
    ):
        if not self.available:
            raise RuntimeError("Client unavailable")

        if headers is None or len(headers) == 0:
            message = PubProtocolMessage(subject=subject, reply_to=reply_subject, payload=payload)
        else:
            message = HPubProtocolMessage(subject=subject, reply_to=reply_subject, payload=payload, headers=headers)
        await self._connection.send(message.dump())
