from typing_extensions import Self

from .message import ProtocolMessage


class InfoProtocolMessage(ProtocolMessage):
    
    @classmethod
    def parse(cls) -> Self:
        pass
