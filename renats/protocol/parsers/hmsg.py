import re

HEAD_PATTERN = re.compile(br"^HMSG\s+(\S+)\s+(\S+)\s+((\S+)\s+)?(\d+)\s+(\d+)")