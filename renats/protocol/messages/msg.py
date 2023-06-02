import re

from typing_extensions import Self

from pydantic import validator

from .base import BaseServerProtocolMessage, BaseProtocolMessageHandler, BaseProtocolMessageParser
from .. import utils
from ..exceptions import InvalidProtocolMessageData

HEAD_PATTERN = re.compile(br"^MSG\s+(\S+)\s+(\S+)\s+((\S+)\s+)?(\d+)")


class MsgProtocolMessage(BaseServerProtocolMessage):
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

    @classmethod
    def load(cls, params: tuple, body: bytes = None, headers: dict[bytes, bytes] = None) -> Self:
        pass


class MsgProtocolMessageHandler(BaseProtocolMessageHandler):
    async def handle(self, message: BaseServerProtocolMessage):
        print(message)


class MsgProtocolMessageParser(BaseProtocolMessageParser):
    def parse_head(self, data: bytes):
        match = re.match(HEAD_PATTERN, data)
        if match is None:
            raise InvalidProtocolMessageData(data)
        subject, sid, _, reply_to, str_payload_length = match.groups()
        payload_length = int(str_payload_length)

        if payload_length == 0:
            self._context["__result__"] = MsgProtocolMessage(
                subject=subject,
                sid=sid,
                reply_to=reply_to,
                payload_length=payload_length
            )
            return

        self._context["subject"] = subject
        self._context["sid"] = sid
        self._context["reply_to"] = reply_to
        self._context["payload_length"] = payload_length
        self._context["__required__"] = payload_length + len(utils.CRLF)

    def parse_body(self, data: bytes):
        payload = data[:data.find(utils.CRLF)]
        self._context["__result__"] = MsgProtocolMessage(
            subject=self._context["subject"],
            sid=self._context["sid"],
            reply_to=self._context["reply_to"],
            payload_length=self._context["payload_length"],
            payload=payload
        )

    @property
    def required(self) -> int:
        return self._context.get("__required__")

    @property
    def result(self):
        return self._context.get("__result__")
