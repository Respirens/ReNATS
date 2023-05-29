from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing_extensions import Self


class BaseProtocolMessage(ABC, BaseModel):
    @abstractmethod
    def dump(self) -> bytes:
        """
        Dump NATS protocol message to bytes
        :return: NATS protocol message as bytes
        """
        pass

    @classmethod
    @abstractmethod
    def parse(cls, body: bytes) -> Self:
        """
        Parse NATS protocol message body
        :param body: NATS protocol message body
        :return: instance of ``ProtocolMessage``
        """
        pass
