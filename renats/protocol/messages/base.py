from abc import ABC, abstractmethod

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
