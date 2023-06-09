import re

import msgspec.json
from msgspec import Struct, field

from .base import SerializableProtocolMessage

INFO_HEAD_PATTERN = re.compile(br"^INFO\s+(.+)\r\n$")


class InfoProtocolMessage(Struct):
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


class ConnectProtocolMessage(Struct, omit_defaults=True):
    """
    NATS protocol message model for CONNECT message
    """
    verbose: bool
    pedantic: bool
    tls_required: bool
    lang: str
    version: str
    auth_token: str | None = None
    user: str | None = None
    password: str | None = field(default=None, name="pass")
    name: str | None = None
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
        return b"CONNECT " + msgspec.json.encode(self) + b"\r\n"


class ErrProtocolMessage(Struct):
    """
    NATS protocol message model for ERR message
    """
    error_message: str
