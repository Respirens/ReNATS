from . import message
from .base import BaseClientProtocolMessage


class UnsubProtocolMessage(BaseClientProtocolMessage):
    """
    NATS protocol message model for UNSUB message
    """
    sid: str
    max_msgs: int | None = None

    def dump(self) -> bytes:
        """
        Dump NATS protocol UNSUB message to bytes
        :return: NATS protocol UNSUB message as bytes-encoded string
        """
        head = message.build_head(
            message.UNSUB,
            self.sid.encode(),
            b"" if self.max_msgs is None else str(self.max_msgs).encode()
        )
        return head + message.CRLF
