from pydantic import ValidationError, validator
from typing_extensions import Self

from . import message
from .base import BaseServerProtocolMessage
from ..exceptions import InvalidProtocolMessageBody


class MsgProtocolMessage(BaseServerProtocolMessage):
    """
    NATS protocol message model for MSG message
    """
    subject: str
    sid: str
    reply_to: str | None = None
    payload_length: int
    payload: bytes | None = None

    @validator("payload")
    def check_payload(cls, v, values):
        if len(v) != values.get("payload_length"):
            raise ValueError("Payload length must be equal to payload_length parameter")
        return v

    @classmethod
    def parse(cls, body: bytes) -> Self:
        """
        Parse NATS protocol MSG message body

        Raises ``InvalidProtocolMessageBody`` if message body is invalid
        :param body: bytes of JSON-encoded NATS protocol INFO message body
        :return: instance of ``MsgProtocolMessage``
        """
        head = body[:body.find(message.CRLF)]
        payload = body[body.find(message.CRLF) + len(message.CRLF):body.rfind(message.CRLF)]
        head_params = head.split(b" ")
        try:
            return cls(
                subject=head_params[0],
                sid=head_params[1],
                reply_to=head_params[2] if len(head_params) == 4 else None,
                payload_length=int(head_params[3]) if len(head_params) == 4 else int(head_params[2]),
                payload=payload
            )
        except (ValidationError, ValueError):
            raise InvalidProtocolMessageBody(body)
