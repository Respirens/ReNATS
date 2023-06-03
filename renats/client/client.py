from typing import Final

from .types import Server
from ..connection.base import BaseConnection
from ..connection.connection import ConnectionType
from ..connection.tcp import TcpConnection

DEFAULT_CONNECTION_TIMEOUT: Final[float] = 2
DEFAULT_INFO_TIMEOUT: Final[float] = 2
CLIENT_LANGUAGE: Final[str] = "python3"
CLIENT_VERSION: Final[str] = "0.0.1-alpha"


class NatsClient:
    def __init__(self):
        self._connection: BaseConnection | None = None
        self._server: Server | None = None

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

    async def connect(self, host: str, port: int, connection_type: ConnectionType = ConnectionType.TCP):
        if connection_type is ConnectionType.TCP:
            self._connection = TcpConnection()
            await self._connection.connect(host, port, DEFAULT_CONNECTION_TIMEOUT)
        else:
            raise ValueError(f"Unknown connection type {connection_type}")
