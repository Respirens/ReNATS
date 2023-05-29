from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing_extensions import Self


class ProtocolMessage(ABC, BaseModel):
    @classmethod
    @abstractmethod
    def parse(cls, body: bytes) -> Self:
        """
        Parse NATS protocol message body
        :param body: NATS protocol message body
        :return: instance of ``ProtocolMessage``
        :r
        """
        pass
