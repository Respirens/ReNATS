from msgspec import Struct


class Server(Struct):
    id: str
    name: str
    version: str
    protocol: int
    max_payload: int
    headers_support: bool
