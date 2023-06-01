class NotConnected(Exception):
    def __str__(self):
        return "Not connected to server"


class UnknownProtocolMessage(Exception):
    def __init__(self, message_type: bytes):
        self.message_type = message_type

    def __str__(self):
        return f"Unknown NATS protocol message type: {self.message_type.decode()}"


class InvalidProtocolMessageData(Exception):
    def __init__(self, head: bytes, body: bytes = None):
        self.head = head
        self.body = body

    def __str__(self):
        return f"Invalid NATS protocol message: {self.head.decode()}"
