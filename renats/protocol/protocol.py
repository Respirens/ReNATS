from typing import Final

from .messages import messages
from .parsers.base import BaseProtocolMessageParser
from .parsers.info import InfoProtocolMessageParser
from .parsers.msg import MsgProtocolMessageParser
from .processors.base import BaseClientMessageProcessor, BaseServerMessageProcessor

MESSAGE_PARSERS: Final[dict[bytes, type[BaseProtocolMessageParser]]] = {
    messages.INFO: InfoProtocolMessageParser,
    messages.MSG: MsgProtocolMessageParser
}

CLIENT_PROCESSORS: Final[dict[bytes, type[BaseClientMessageProcessor]]] = {}

SERVER_PROCESSORS: Final[dict[bytes, type[BaseServerMessageProcessor]]] = {}
