from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from typing_extensions import Self


class BaseClientProtocolMessage(ABC, BaseModel):
    """
    Base NATS protocol message model for messages sent by client
    """

    @abstractmethod
    def dump(self) -> bytes:
        """
        Dump NATS protocol message to bytes
        :return: NATS protocol message as bytes-encoded string
        """
        raise NotImplementedError()


class BaseServerProtocolMessage(ABC, BaseModel):
    """
    Base NATS protocol message model for messages sent by server
    """

    @classmethod
    @abstractmethod
    def load(cls, params: tuple, body: bytes = None, headers: dict[bytes, bytes] = None) -> Self:
        """
        Load NATS protocol message from head and body
        :param params: NATS protocol message params
        :param body: NATS protocol message body
        :param headers: NATS protocol message headers
        :return: instance of ``ProtocolMessage``
        """
        raise NotImplementedError()


class BaseProtocolMessageParser(ABC):
    def __init__(self):
        self._context: dict[str, Any] = {}

    @abstractmethod
    def parse_head(self, data: bytes):
        raise NotImplementedError()

    @abstractmethod
    def parse_body(self, data: bytes):
        raise NotImplementedError()

    @property
    @abstractmethod
    def required(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def result(self):
        raise NotImplementedError()

    def __enter__(self):
        self._context = {}

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._context = {}


class BaseProtocolMessageHandler(ABC):
    @abstractmethod
    async def handle(self, message: BaseServerProtocolMessage):
        raise NotImplementedError()
