from .base import BaseProtocolMessageParser
from ..messages.msg import MsgProtocolMessage
from ...connection.base import BaseConnection

HEAD_PATTERN = r"^MSG\s+(\w+)\s+(\d+)\s+(\d+)\s+(\d+)"


class MsgProtocolMessageParser(BaseProtocolMessageParser):
    @classmethod
    def parse(cls, head: bytes, connection: BaseConnection) -> MsgProtocolMessage:
        pass
