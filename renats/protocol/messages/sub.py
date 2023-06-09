from msgspec import Struct

from .base import SerializableProtocolMessage
from .. import utils, protocol


class SubProtocolMessage(Struct):
    """
    NATS protocol message model for SUB message
    """
    subject: str
    sid: str
    queue_group: str | None = None

    def dump(self) -> bytes:
        """
        Dump NATS protocol SUB message to bytes
        :return: NATS protocol SUB message as bytes-encoded string
        """
        head = utils.build_head(
            protocol.SUB,
            self.subject.encode(),
            b"" if self.queue_group is None else self.queue_group.encode(),
            self.sid.encode()
        )
        return head + utils.CRLF


class UnsubProtocolMessage(Struct):
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
        head = utils.build_head(
            protocol.UNSUB,
            self.sid.encode(),
            b"" if self.max_msgs is None else str(self.max_msgs).encode()
        )
        return head + utils.CRLF
