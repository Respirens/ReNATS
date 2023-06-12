class Message:
    def __init__(self, subject: str, payload: bytes, reply_subject: str = None, headers: dict[str, str] = None):
        self.subject = subject
        self.payload = payload
        self.reply_subject = reply_subject
        self.headers = headers
