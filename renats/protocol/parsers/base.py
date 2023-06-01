from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

from ..messages.base import BaseServerProtocolMessage


@dataclass
class ProtocolMessageParserContext:
    params: dict[str, Any] = field(default_factory=dict)
    required: int = -1
    result: BaseServerProtocolMessage | None = None


class BaseProtocolMessageParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(data: bytes, context: ProtocolMessageParserContext):
        raise NotImplementedError()

    @staticmethod
    @contextmanager
    def context():
        return ProtocolMessageParserContext()
