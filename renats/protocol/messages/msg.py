import re

from pydantic import validator, BaseModel

MSG_HEAD_PATTERN = re.compile(br"^MSG\s+(\S+)\s+(\S+)\s+((\S+)\s+)?(\d+)")


class MsgProtocolMessage(BaseModel):
    subject: str
    sid: str
    reply_to: str | None = None
    payload_length: int
    payload: bytes | None = None

    @validator("payload")
    def check_payload(cls, v, values):
        if len(v) != values.get("payload_length"):
            raise ValueError("Payload length must be equal to payload_length parameter")
        return v

    @validator("subject")
    def check_subject(cls, v):
        if len(v) == 0:
            raise ValueError("Subject can't be empty string")
        if " " in v:
            raise ValueError("Subject can't contain whitespaces")
        return v

    @validator("reply_to")
    def check_reply_to(cls, v):
        if v is None:
            return v
        if len(v) == 0:
            raise ValueError("Reply to can't be empty string, use None instead")
        if " " in v:
            raise ValueError("Reply to can't contain whitespaces")
        return v

    @validator("sid")
    def check_sid(cls, v):
        if len(v) == 0:
            raise ValueError("Sid can't be empty string")
        if " " in v:
            raise ValueError("Sid can't contain whitespaces")
        return v


class HMsgProtocolMessage(MsgProtocolMessage):
    headers_length: int
    headers: dict[str, str]
