from typing_extensions import Self

from pydantic import validator

from .base import BaseServerProtocolMessage


class MsgProtocolMessage(BaseServerProtocolMessage):
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
    def load(cls, params: tuple, body: bytes = None, headers: dict[bytes, bytes] = None) -> Self:
        pass
