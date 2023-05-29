class UnknownProtocolMessage(Exception):
    def __init__(self, message_type: bytes):
        self.message_type = message_type

    def __str__(self):
        return f"Unknown NATS protocol message type: {self.message_type.decode()}"


class InvalidProtocolMessageBody(Exception):
    def __init__(self, body: bytes):
        self.body = body

    def __str__(self):
        return f"Invalid NATS protocol message: {self.body.decode()}"
