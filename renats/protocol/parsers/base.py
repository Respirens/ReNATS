from abc import ABC, abstractmethod

from ..messages.base import BaseServerProtocolMessage
from ...connection.base import BaseConnection


class BaseProtocolMessageParser(ABC):
    @classmethod
    @abstractmethod
    def parse(cls, head: bytes, connection: BaseConnection) -> BaseServerProtocolMessage:
        raise NotImplementedError()
