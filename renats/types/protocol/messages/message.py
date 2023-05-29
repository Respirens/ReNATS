from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing_extensions import Self


class ProtocolMessage(ABC, BaseModel):
    @classmethod
    @abstractmethod
    def parse(cls) -> Self:
        pass
