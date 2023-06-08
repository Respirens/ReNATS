import re

from msgspec import Struct

MSG_HEAD_PATTERN = re.compile(br"^MSG\s+(\S+)\s+(\S+)\s+((\S+)\s+)?(\d+)")


class MsgProtocolMessage(Struct):
    reply_to: str | None = None
    payload: bytes | None = None


class HMsgProtocolMessage(Struct):
    subject: str
    sid: str
    payload_length: int
    headers_length: int
    headers: dict[str, str]
    reply_to: str | None = None
    payload: bytes | None = None
