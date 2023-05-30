from pydantic import Field

from .base import BaseClientProtocolMessage


class ConnectProtocolMessage(BaseClientProtocolMessage):
    """
    NATS protocol message model for CONNECT message
    """
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
        :return: NATS protocol CONNECT message as bytes-encoded string
        """
        return f"CONNECT {self.json(skip_defaults=True)}\r\n".encode()
