from pydantic import validator

from .base import BaseClientProtocolMessage
from .. import utils, protocol


class SubProtocolMessage(BaseClientProtocolMessage):
    """
    NATS protocol message model for SUB message
    """
    subject: str
    queue_group: str | None = None
    sid: str

    @validator("subject")
    def check_subject(cls, v):
        if " " in v:
            raise ValueError("Subject can't contain whitespaces")
        if len(v) == 0:
            raise ValueError("Queue group can't be empty string")
        return v

    @validator("queue_group")
    def check_queue_group(cls, v):
        if v is None:
            return v
        if len(v) == 0:
            raise ValueError("Queue group can't be empty string, use None instead")
        if " " in v:
            raise ValueError("Queue group can't contain whitespaces")
        return v

    @validator("sid")
    def check_sid(cls, v):
        if len(v) == 0:
            raise ValueError("Sid can't be empty string")
        if " " in v:
            raise ValueError("Sid can't contain whitespaces")
        return v

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
