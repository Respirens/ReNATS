from renats.connection.base import BaseConnection
from renats.protocol.messages.msg import MsgProtocolMessage, HMsgProtocolMessage


async def parse_msg(head: bytes, connection: BaseConnection) -> MsgProtocolMessage:
    pass


async def parse_hmsg(head: bytes, connection: BaseConnection) -> HMsgProtocolMessage:
    pass
