class InvalidProtocolMessageData(Exception):
    def __init__(self, head: bytes, body: bytes):
        self.head = head
        self.body = body

    def __str__(self):
        return f"Invalid NATS protocol message: {self.head.decode()}"
