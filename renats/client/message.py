class Message:
    def __init__(self, subject: str, payload: bytes, reply_to: str = None, headers: dict[str, str] = None):
        self.subject = subject
        self.payload = payload
        self.reply_to = reply_to
        self.headers = headers
