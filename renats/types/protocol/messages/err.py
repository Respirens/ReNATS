from pydantic import ValidationError
from typing_extensions import Self

from .base import BaseServerProtocolMessage
from ..exceptions import InvalidProtocolMessageBody


class ErrProtocolMessage(BaseServerProtocolMessage):
    """
    NATS protocol message model for ERR message
    """
    error_message: str

    @classmethod
    def parse(cls, body: bytes) -> Self:
        """
        Parse NATS protocol ERR message body

        Raises ``InvalidProtocolMessageBody`` if message body is invalid
        :param body: bytes of JSON-encoded NATS protocol ERR message body
        :return: instance of ``ErrProtocolMessage``
        """
        try:
            return cls(error_message=body.decode())
        except ValidationError:
            raise InvalidProtocolMessageBody(body)
