from pydantic import validator

from .pub import PubProtocolMessage
from .. import utils, protocol


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
        headers = utils.build_headers(utils.encode_headers(self.headers))
        head = utils.build_head(
            protocol.HPUB,
            self.subject.encode(),
            b"" if self.reply_to is None else self.reply_to.encode(),
            str(len(headers + utils.CRLF + utils.CRLF)).encode(),
            str(len(headers + utils.CRLF + utils.CRLF + self.payload)).encode()
        )
        return head + utils.CRLF + headers + utils.CRLF + utils.CRLF + self.payload + utils.CRLF
