from typing import Final

from .processing.base import BaseProtocolMessageProcessor
from ..types.protocol.messages import messages
from ..types.protocol.messages.base import BaseClientProtocolMessage, BaseServerProtocolMessage
from ..types.protocol.messages.connect import ConnectProtocolMessage
from ..types.protocol.messages.err import ErrProtocolMessage
from ..types.protocol.messages.hpub import HPubProtocolMessage
from ..types.protocol.messages.info import InfoProtocolMessage
from ..types.protocol.messages.msg import MsgProtocolMessage
from ..types.protocol.messages.pub import PubProtocolMessage
from ..types.protocol.messages.sub import SubProtocolMessage
from ..types.protocol.messages.unsub import UnsubProtocolMessage

CLIENT_MESSAGES: Final[dict[bytes, type[BaseClientProtocolMessage]]] = {
    messages.CONNECT: ConnectProtocolMessage,
    messages.PUB: PubProtocolMessage,
    messages.HPUB: HPubProtocolMessage,
    messages.SUB: SubProtocolMessage,
    messages.UNSUB: UnsubProtocolMessage
}

SERVER_MESSAGES: Final[dict[bytes, type[BaseServerProtocolMessage]]] = {
    messages.INFO: InfoProtocolMessage,
    messages.MSG: MsgProtocolMessage,
    messages.ERR: ErrProtocolMessage
}

MESSAGE_PROCESSORS: Final[dict[bytes, type[BaseProtocolMessageProcessor]]] = {}
