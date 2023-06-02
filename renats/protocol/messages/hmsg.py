from typing_extensions import Self

from .base import BaseProtocolMessageHandler, BaseProtocolMessageParser
from .msg import MsgProtocolMessage


class HMsgProtocolMessage(MsgProtocolMessage):
    headers_length: int
    headers: dict[str, str]

    @classmethod
    def load(cls, params: tuple, body: bytes = None, headers: dict[bytes, bytes] = None) -> Self:
        pass


class HMsgProtocolMessageHandler(BaseProtocolMessageHandler):
    pass


class HMsgProtocolMessageParser(BaseProtocolMessageParser):
    pass
