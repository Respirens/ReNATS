from msgspec import Struct


class MsgProtocolMessage(Struct):
    subject: str
    sid: str
    payload_length: int
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
