from ..connection.base import BaseConnection


class ProtocolMessageParser:
    def __init__(self, connection: BaseConnection):
        self.connection = connection
