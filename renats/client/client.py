from .base import BaseNatsClient
from ..connection.base import BaseConnection
from ..connection.connection import ConnectionType
from ..connection.tcp import TcpConnection


class NatsClient(BaseNatsClient):
    def __init__(self):
        self.connection: BaseConnection | None = None

    async def connect(self, host: str, port: int, connection_type: ConnectionType = ConnectionType.TCP):
        if connection_type is ConnectionType.TCP:
            self.connection = TcpConnection()
            return
        raise ValueError(f"Unknown connection type: {connection_type}")
