from renats.connection.base import BaseConnection
from renats.protocol.messages.info import InfoProtocolMessage
from renats.protocol.parsers.base import BaseProtocolMessageParser


class InfoProtocolMessageParser(BaseProtocolMessageParser):
    @classmethod
    def parse(cls, head: bytes, connection: BaseConnection) -> InfoProtocolMessage:
        pass
