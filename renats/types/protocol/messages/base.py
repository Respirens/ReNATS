import abc
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
    _has_message_body = NotImplemented
    _has_message_headers = NotImplemented

    @classmethod
    @abstractmethod
    def load(cls, head: bytes, body: bytes = None, headers: dict[bytes, bytes] = None) -> Self:
        """
        Load NATS protocol message from head and body
        :param head: NATS protocol message head
        :param body: NATS protocol message body
        :param headers: NATS protocol message headers
        :return: instance of ``ProtocolMessage``
        """
        raise NotImplementedError()
