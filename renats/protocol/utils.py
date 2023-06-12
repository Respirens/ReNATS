import re
from typing import Final

CRLF: Final[bytes] = b"\r\n"
CRLF_SIZE: Final[int] = len(CRLF)


def encode_headers(headers: dict[str, str]) -> dict[bytes, bytes]:
    """
    Encode headers dictionary from string-string to bytes-bytes
    :param headers: string-string headers dictionary
    :return: bytes-encoded headers dictionary
    """
    return {k.encode(): v.encode() for k, v in headers.items()}


def decode_headers(headers: dict[bytes, bytes]) -> dict[str, str]:
    """
    Decode headers dictionary from bytes-bytes to string-string
    :param headers: bytes-bytes headers dictionary
    :return: string-decoded headers dictionary
    """
    return {k.decode(): v.decode() for k, v in headers.items()}


def build_head(method: bytes, *params: bytes) -> bytes:
    """
    Build NATS protocol message head (params are joined and cleaned for multiple whitespaces)
    :param method: protocol message method (like PUB, SUB, etc...) as bytes-encoded string
    :param params: protocol message params as bytes-encoded strings
    :return: protocol message head as bytes-encoded string
    """
    return method + b" " + re.sub(br"\s{2,}", b" ", b" ".join(params))


def build_headers(headers: dict[bytes, bytes], headers_version: bytes) -> bytes:
    """
    Build NATS protocol message headers
    :param headers: dictionary with bytes-encoded headers
    :param headers_version: headers version string (NATS/1.0)
    :return: protocol message headers as bytes-encoded string
    """
    return headers_version + CRLF + CRLF.join([k + b": " + v for k, v in headers.items()])
