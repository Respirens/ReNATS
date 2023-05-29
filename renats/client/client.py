from ..connection import Connection


class NatsClient:
    def __init__(self):
        self.connection: Connection | None = None
