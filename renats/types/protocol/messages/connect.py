from pydantic import Field, ValidationError
from typing_extensions import Self

from .message import BaseProtocolMessage
from ..exceptions import InvalidProtocolMessageBody


class ConnectProtocolMessage(BaseProtocolMessage):
    verbose: bool
    pedantic: bool
    tls_required: bool
    auth_token: str | None = None
    user: str | None = None
    password: str | None = Field(None, alias="pass")
    name: str | None = None
    lang: str
    version: str
    protocol: int | None = None
    echo: bool | None = None
    sig: str | None = None
    jwt: str | None = None
    no_responders: bool | None = None
    headers: bool | None = None
    nkey: str | None = None

    def dump(self) -> bytes:
        """
        Dump NATS protocol CONNECT message to bytes
        :return: NATS protocol CONNECT message as bytes
        """
        return f"CONNECT {self.json(skip_defaults=True)}".encode()

    @classmethod
    def parse(cls, body: bytes) -> Self:
        """
        Parse NATS protocol CONNECT message body

        Raises ``InvalidProtocolMessageBody`` if message body is invalid
        :param body: bytes of JSON-encoded NATS protocol INFO message body
        :return: instance of ``ConnectProtocolMessage``
        """
        try:
            return cls.parse_raw(body)
        except ValidationError:
            raise InvalidProtocolMessageBody(body)
