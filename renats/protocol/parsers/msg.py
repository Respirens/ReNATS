import re

from .base import BaseProtocolMessageParser

HEAD_PATTERN = re.compile(br"^MSG\s+(\S+)\s+(\S+)\s+((\S+)\s+)?(\d+)")


class MsgProtocolMessageParser(BaseProtocolMessageParser):
    pass
