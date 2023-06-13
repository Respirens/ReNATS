import pytest

from mocks.connection import MockConnection
from renats.client import parser
from renats.protocol.messages.msg import MsgProtocolMessage


@pytest.mark.asyncio
async def test_msg_protocol_message_parsing():
    connection = MockConnection(b"MSG foo.bar 9 foo.bar.baz 11\r\nHello World\r\n")

    head = await connection.readline()
    expected_head = b"MSG foo.bar 9 foo.bar.baz 11\r\n"
    assert head == expected_head

    protocol_message = await parser.parse_msg(head, connection)
    expected_protocol_message = MsgProtocolMessage(
        subject="foo.bar",
        sid="9",
        reply_to="foo.bar.baz",
        payload_length=11,
        payload=b"Hello World"
    )
    assert protocol_message == expected_protocol_message
