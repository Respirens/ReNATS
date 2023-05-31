from abc import ABC, abstractmethod

from ...client.base import BaseNatsClient
from ...types.protocol.messages.base import BaseServerProtocolMessage


class BaseProtocolMessageProcessor(ABC):
    def __init__(self, client: BaseNatsClient):
        self.client = client

    @abstractmethod
    def process(self, model: BaseServerProtocolMessage):
        raise NotImplementedError()
