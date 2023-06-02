from pydantic import validator

from .base import BaseClientProtocolMessage
from .. import utils, protocol


class UnsubProtocolMessage(BaseClientProtocolMessage):
    """
    NATS protocol message model for UNSUB message
    """
    sid: str
    max_msgs: int | None = None

    @validator("sid")
    def check_sid(cls, v):
        if len(v) == 0:
            raise ValueError("Sid can't be empty string")
        if " " in v:
            raise ValueError("Sid can't contain whitespaces")
        return v

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
