import re
from typing import Final

from .base import BaseClientProtocolMessage, BaseServerProtocolMessage
from .connect import ConnectProtocolMessage
from .err import ErrProtocolMessage
from .hpub import HPubProtocolMessage
from .info import InfoProtocolMessage
from .pub import PubProtocolMessage
from .sub import SubProtocolMessage
from .unsub import UnsubProtocolMessage

HEADERS_VERSION: Final[bytes] = b"NATS/1.0"

CRLF: Final[bytes] = b"\r\n"

INFO: Final[bytes] = b"INFO"
CONNECT: Final[bytes] = b"CONNECT"
PUB: Final[bytes] = b"PUB"
HPUB: Final[bytes] = b"HPUB"
SUB: Final[bytes] = b"SUB"
UNSUB: Final[bytes] = b"UNSUB"
MSG: Final[bytes] = b"MSG"
HMSG: Final[bytes] = b"HMSG"
PING: Final[bytes] = b"PING"
PONG: Final[bytes] = b"PONG"
OK: Final[bytes] = b"+OK"
ERR: Final[bytes] = b"-ERR"

CLIENT_MESSAGES: Final[dict[bytes, type[BaseClientProtocolMessage]]] = {
    CONNECT: ConnectProtocolMessage,
    PUB: PubProtocolMessage,
    HPUB: HPubProtocolMessage,
    SUB: SubProtocolMessage,
    UNSUB: UnsubProtocolMessage
}

SERVER_MESSAGES: Final[dict[bytes, type[BaseServerProtocolMessage]]] = {
    INFO: InfoProtocolMessage,
    ERR: ErrProtocolMessage
}


def encode_headers(headers: dict[str, str]) -> dict[bytes, bytes]:
    """
    Encode headers dictionary from string-string to bytes-bytes
    :param headers: string-string headers dictionary
    :return: bytes-encoded headers dictionary
    """
    return {k.encode(): v.encode() for k, v in headers.items()}


def build_head(method: bytes, *params: bytes) -> bytes:
    """
    Build NATS protocol message head (params are joined and cleaned for multiple whitespaces)
    :param method: protocol message method (like PUB, SUB, etc...) as bytes-encoded string
    :param params: protocol message params as bytes-encoded strings
    :return: protocol message head as bytes-encoded string
    """
    return method + b" " + re.sub(br"\s{2,}", b" ", b" ".join(params))


def build_headers(headers: dict[bytes, bytes]) -> bytes:
    """
    Build NATS protocol message headers
    :param headers: dictionary with bytes-encoded headers
    :return: protocol message headers as bytes-encoded string
    """
    return HEADERS_VERSION + CRLF + CRLF.join([k + b": " + v for k, v in headers.items()])
