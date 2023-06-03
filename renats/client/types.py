from pydantic import BaseModel


class Server(BaseModel):
    id: str
    name: str
    version: str
    protocol: int
    max_payload: int
    headers_support: bool
