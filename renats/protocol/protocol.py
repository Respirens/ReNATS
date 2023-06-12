from typing import Final

from renats.protocol import utils

HEADERS_VERSION: Final[bytes] = b"NATS/1.0"

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

PONG_MESSAGE = PONG + utils.CRLF
OK_MESSAGE = OK + utils.CRLF

MESSAGES: Final[list[bytes]] = [
    INFO,
    MSG,
    HMSG,
    CONNECT,
    PUB,
    HPUB,
    SUB,
    UNSUB,
    PING,
    PONG,
    OK,
    ERR
]
