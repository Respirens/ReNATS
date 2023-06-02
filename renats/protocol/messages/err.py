from typing_extensions import Self

from .base import BaseServerProtocolMessage, BaseProtocolMessageParser, BaseProtocolMessageHandler


class ErrProtocolMessage(BaseServerProtocolMessage):
    """
    NATS protocol message model for ERR message
    """
    error_message: str

    @classmethod
    def load(cls, params: tuple, body: bytes = None, headers: dict[bytes, bytes] = None) -> Self:
        pass


class ErrProtocolMessageHandler(BaseProtocolMessageHandler):
    pass


class ErrProtocolMessageParser(BaseProtocolMessageParser):
    pass
