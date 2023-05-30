from . import message
from .base import BaseClientProtocolMessage


class SubProtocolMessage(BaseClientProtocolMessage):
    """
    NATS protocol message model for SUB message
    """
    subject: str
    queue_group: str | None = None
    sid: str

    def dump(self) -> bytes:
        """
        Dump NATS protocol SUB message to bytes
        :return: NATS protocol SUB message as bytes-encoded string
        """
        head = message.build_head(
            message.SUB,
            self.subject.encode(),
            b"" if self.queue_group is None else self.queue_group.encode(),
            self.sid.encode()
        )
        return head + message.CRLF
