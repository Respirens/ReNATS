from typing import Self

from .msg import MsgProtocolMessage


class HMsgProtocolMessage(MsgProtocolMessage):
    headers_length: int
    headers: dict[str, str]

    @classmethod
    def load(cls, params: tuple, body: bytes = None, headers: dict[bytes, bytes] = None) -> Self:
        pass
