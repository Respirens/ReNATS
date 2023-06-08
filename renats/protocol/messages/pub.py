from msgspec import Struct

from .base import SerializableProtocolMessage
from .. import utils, protocol


class PubProtocolMessage(Struct, SerializableProtocolMessage):
    """
    NATS protocol message model for PUB message
    """
    subject: str
    reply_to: str | None = None
    payload: bytes = b""

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


class HPubProtocolMessage(Struct, SerializableProtocolMessage):
    """
    NATS protocol message model for HPUB message
    """
    subject: str
    headers: dict[str, str]
    reply_to: str | None = None
    payload: bytes = b""

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
