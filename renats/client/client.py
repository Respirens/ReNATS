from .base import BaseNatsClient
from ..connection.base import BaseConnection
from ..connection.connection import ConnectionType
from ..connection.tcp import TcpConnection
from renats.protocol.processors.client.base import BaseProtocolMessageProcessor
from ..protocol.protocol import MESSAGE_PROCESSORS


class NatsClient(BaseNatsClient):
    def __init__(self):
        self.connection: BaseConnection | None = None
        self.processors: dict[bytes, BaseProtocolMessageProcessor] = {k: v(self) for k, v in MESSAGE_PROCESSORS.items()}

    async def connect(self, host: str, port: int, connection_type: ConnectionType = ConnectionType.TCP):
        if connection_type is ConnectionType.TCP:
            self.connection = TcpConnection()
            return
        raise ValueError(f"Unknown connection type: {connection_type}")

    async def publish(
            self,
            subject: str,
            payload: bytes = None,
            reply_subject: str = None,
            headers: dict[str, str] = None
    ):
        if headers is not None and len(headers) > 0:
            message_model = HPubProtocolMessage()
