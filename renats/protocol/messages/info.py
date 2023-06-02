import re

from typing_extensions import Self

from .base import BaseServerProtocolMessage, BaseProtocolMessageParser, BaseProtocolMessageHandler

HEAD_PATTERN = re.compile(br"^INFO\s+(.+)\r\n$")


class InfoProtocolMessage(BaseServerProtocolMessage):
    """
    NATS protocol message model for INFO message
    """
    server_id: str
    server_name: str
    version: str
    go: str
    host: str
    port: int
    headers: bool
    max_payload: int
    proto: int
    client_id: int | None = None
    auth_required: bool | None = None
    tls_required: bool | None = None
    tls_verify: bool | None = None
    tls_available: bool | None = None
    connect_urls: list[str] | None = None
    ldm: bool | None = None
    git_commit: str | None = None
    jetstream: bool | None = None
    ip: str | None = None
    client_id_str: str | None = None
    client_ip: str | None = None
    nonce: str | None = None
    cluster: str | None = None
    domain: str | None = None

    @classmethod
    def load(cls, params: tuple, body: bytes = None, headers: dict[bytes, bytes] = None) -> Self:
        return cls.parse_raw(params[0])


class InfoProtocolMessageHandler(BaseProtocolMessageHandler):
    async def handle(self, message: BaseServerProtocolMessage):
        pass


class InfoProtocolMessageParser(BaseProtocolMessageParser):
    def parse_head(self, data: bytes):
        self._context["result"] = InfoProtocolMessage.load(re.match(HEAD_PATTERN, data).groups())

    def parse_body(self, data: bytes):
        pass

    @property
    def required(self) -> int:
        return 0

    @property
    def result(self):
        return self._context.get("result")
