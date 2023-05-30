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
        pass


class BaseServerProtocolMessage(ABC, BaseModel):
    """
    Base NATS protocol message model for messages sent by server
    """
    @classmethod
    @abstractmethod
    def parse(cls, body: bytes) -> Self:
        """
        Parse NATS protocol message body
        :param body: NATS protocol message body
        :return: instance of ``ProtocolMessage``
        """
        pass
