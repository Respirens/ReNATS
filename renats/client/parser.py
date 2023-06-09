import re

from renats.connection.base import BaseConnection
from renats.protocol import utils
from renats.protocol.exceptions import InvalidProtocolMessage
from renats.protocol.messages.msg import MsgProtocolMessage, HMsgProtocolMessage

MSG_HEAD_PATTERN = re.compile(br"^MSG\s+(\S+)\s+(\S+)\s+((\S+)\s+)?(\d+)")


async def parse_msg(head: bytes, connection: BaseConnection) -> MsgProtocolMessage:
    match = re.match(MSG_HEAD_PATTERN, head)
    if match is None:
        raise InvalidProtocolMessage(head)
    subject, sid, _, reply_to, payload_length = match.groups()
    payload = await connection.readexactly(int(payload_length) + utils.CRLF_SIZE)
    return MsgProtocolMessage(
        subject=subject,
        sid=sid,
        reply_to=reply_to,
        payload_length=int(payload_length),
        payload=payload
    )


async def parse_hmsg(head: bytes, connection: BaseConnection) -> HMsgProtocolMessage:
    pass
