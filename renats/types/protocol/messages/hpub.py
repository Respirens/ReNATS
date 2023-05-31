from pydantic import validator

from . import messages
from .pub import PubProtocolMessage


class HPubProtocolMessage(PubProtocolMessage):
    """
    NATS protocol message model for HPUB message
    """
    headers: dict[str, str]

    @validator("headers")
    def check_headers(cls, v):
        for key in v:
            if key.strip() != key:
                raise ValueError("Header keys must be stripped")
        return v

    def dump(self) -> bytes:
        """
        Dump NATS protocol HPUB message to bytes
        :return: NATS protocol HPUB message as bytes-encoded string
        """
        headers = messages.build_headers(messages.encode_headers(self.headers))
        head = messages.build_head(
            messages.HPUB,
            self.subject.encode(),
            b"" if self.reply_to is None else self.reply_to.encode(),
            str(len(headers + messages.CRLF + messages.CRLF)).encode(),
            str(len(headers + messages.CRLF + messages.CRLF + self.payload)).encode()
        )
        return head + messages.CRLF + headers + messages.CRLF + messages.CRLF + self.payload + messages.CRLF
