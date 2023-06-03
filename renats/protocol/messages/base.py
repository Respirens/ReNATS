from abc import ABC, abstractmethod


class SerializableProtocolMessage(ABC):
    @abstractmethod
    def dump(self) -> bytes:
        """
        Dump class protocol message to bytes
        :return: NATS protocol message as bytes-encoded string
        """
        raise NotImplementedError()
