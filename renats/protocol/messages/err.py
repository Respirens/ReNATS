from pydantic import ValidationError
from typing_extensions import Self

from .base import BaseServerProtocolMessage
from ..exceptions import InvalidProtocolMessageData


class ErrProtocolMessage(BaseServerProtocolMessage):
    """
    NATS protocol message model for ERR message
    """

    _has_message_body = False
    _has_message_headers = False

    error_message: str

    @classmethod
    def load(cls, head: bytes, body: bytes = None, headers: dict[bytes, bytes] = None) -> Self:
        try:
            return cls(error_message=head.decode())
        except ValidationError:
            raise InvalidProtocolMessageData(head, body)
