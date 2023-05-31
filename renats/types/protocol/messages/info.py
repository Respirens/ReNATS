from pydantic import ValidationError
from typing_extensions import Self

from .base import BaseServerProtocolMessage
from ..exceptions import InvalidProtocolMessageData


class InfoProtocolMessage(BaseServerProtocolMessage):
    """
    NATS protocol message model for INFO message
    """
    _has_message_body = False
    _has_message_headers = False

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

    @classmethod
    def load(cls, head: bytes, body: bytes = None, headers: dict[bytes, bytes] = None) -> Self:
        """
        Load NATS protocol INFO message from head and body

        Raises ``InvalidProtocolMessageData`` if message data is invalid
        :param head: bytes of JSON-encoded NATS protocol INFO message head
        :param body: in this protocol message type it doesn't used
        :param headers: in this protocol message type it doesn't used
        :return: instance of ``InfoProtocolMessage``
        """
        try:
            return cls.parse_raw(head)
        except ValidationError:
            raise InvalidProtocolMessageData(head, body)
