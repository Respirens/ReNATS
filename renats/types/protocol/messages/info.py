from pydantic import ValidationError
from typing_extensions import Self

from .message import BaseProtocolMessage
from ..exceptions import InvalidProtocolMessageBody


class InfoProtocolMessage(BaseProtocolMessage):
    server_id: int
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

    def dump(self) -> bytes:
        """
        Dump NATS protocol INFO message to bytes
        :return: NATS protocol INFO message as bytes
        """
        return f"INFO {self.json(skip_defaults=True)}".encode()

    @classmethod
    def parse(cls, body: bytes) -> Self:
        """
        Parse NATS protocol INFO message body

        Raises ``InvalidProtocolMessageBody`` if message body is invalid
        :param body: bytes of JSON-encoded NATS protocol INFO message body
        :return: instance of ``InfoProtocolMessage``
        """
        try:
            return cls.parse_raw(body)
        except ValidationError:
            raise InvalidProtocolMessageBody(body)

