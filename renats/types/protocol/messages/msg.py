from pydantic import ValidationError, validator
from typing_extensions import Self

from .base import BaseServerProtocolMessage
from ..exceptions import InvalidProtocolMessageData


class MsgProtocolMessage(BaseServerProtocolMessage):
    """
    NATS protocol message model for MSG message
    """
    _has_message_body = True
    _has_message_headers = False

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

    @validator("subject")
    def check_subject(cls, v):
        if len(v) == 0:
            raise ValueError("Subject can't be empty string")
        if " " in v:
            raise ValueError("Subject can't contain whitespaces")
        return v

    @validator("reply_to")
    def check_reply_to(cls, v):
        if v is None:
            return v
        if len(v) == 0:
            raise ValueError("Reply to can't be empty string, use None instead")
        if " " in v:
            raise ValueError("Reply to can't contain whitespaces")
        return v

    @validator("sid")
    def check_sid(cls, v):
        if len(v) == 0:
            raise ValueError("Sid can't be empty string")
        if " " in v:
            raise ValueError("Sid can't contain whitespaces")
        return v

    @classmethod
    def load(cls, head: bytes, body: bytes = None, headers: dict[bytes, bytes] = None) -> Self:
        """
        Load NATS protocol MSG message from head and body

        Raises ``InvalidProtocolMessageData`` if message body is invalid
        :param head: bytes of NATS protocol MSG message head
        :param body: bytes of NATS protocol MSG message body
        :param headers: in this protocol message type it doesn't used
        :return: instance of ``MsgProtocolMessage``
        """
        payload = b"" if body is None else body
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
            raise InvalidProtocolMessageData(head, body)
