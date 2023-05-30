from . import message
from .pub import PubProtocolMessage


class HPubProtocolMessage(PubProtocolMessage):
    """
    NATS protocol message model for HPUB message
    """
    headers: dict[str, str]

    def dump(self) -> bytes:
        """
        Dump NATS protocol HPUB message to bytes
        :return: NATS protocol HPUB message as bytes-encoded string
        """
        headers = message.build_headers(message.encode_headers(self.headers))
        head = message.build_head(
            message.HPUB,
            self.subject.encode(),
            b"" if self.reply_to is None else self.reply_to.encode(),
            str(len(headers + message.CRLF + message.CRLF)).encode(),
            str(len(headers + message.CRLF + message.CRLF + self.payload)).encode()
        )
        return head + message.CRLF + headers + message.CRLF + message.CRLF + self.payload + message.CRLF
