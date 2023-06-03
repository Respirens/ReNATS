from pydantic import validator, BaseModel

from .. import utils, protocol
from .base import SerializableProtocolMessage


class PubProtocolMessage(BaseModel, SerializableProtocolMessage):
    """
    NATS protocol message model for PUB message
    """
    subject: str
    reply_to: str | None = None
    payload: bytes = b""

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

    def dump(self) -> bytes:
        """
        Dump NATS protocol PUB message to bytes
        :return: NATS protocol PUB message as bytes-encoded string
        """
        head = utils.build_head(
            protocol.PUB,
            self.subject.encode(),
            b"" if self.reply_to is None else self.reply_to.encode(),
            str(len(self.payload)).encode()
        )
        return head + utils.CRLF + self.payload + utils.CRLF


class HPubProtocolMessage(PubProtocolMessage):
    """
    NATS protocol message model for HPUB message
    """
    headers: dict[str, str]

    @validator("headers")
    def check_headers(cls, v):
        for key in v:
            if key.strip() != key:
                raise ValueError("Header keys must be stripped")
        return v

    def dump(self) -> bytes:
        """
        Dump NATS protocol HPUB message to bytes
        :return: NATS protocol HPUB message as bytes-encoded string
        """
        headers = utils.build_headers(utils.encode_headers(self.headers))
        head = utils.build_head(
            protocol.HPUB,
            self.subject.encode(),
            b"" if self.reply_to is None else self.reply_to.encode(),
            str(len(headers + utils.CRLF + utils.CRLF)).encode(),
            str(len(headers + utils.CRLF + utils.CRLF + self.payload)).encode()
        )
        return head + utils.CRLF + headers + utils.CRLF + utils.CRLF + self.payload + utils.CRLF
