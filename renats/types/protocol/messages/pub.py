from . import message
from .base import BaseClientProtocolMessage


class PubProtocolMessage(BaseClientProtocolMessage):
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
        head = message.build_head(
            message.PUB,
            self.subject.encode(),
            b"" if self.reply_to is None else self.reply_to.encode(),
            str(len(self.payload)).encode()
        )
        return head + message.CRLF + self.payload + message.CRLF
