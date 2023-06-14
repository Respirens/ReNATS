import msgspec.json
import pytest

from mocks.connection import MockConnection
from renats.client import parser
from renats.protocol.messages.msg import MsgProtocolMessage
from renats.protocol.messages.service import InfoProtocolMessage


@pytest.mark.asyncio
async def test_info_protocol_message_parsing():
    connection = MockConnection(
        b'INFO {'
        b'"server_id":"test-server-id",'
        b'"server_name":"test-server-name",'
        b'"version":"test-version",'
        b'"go":"test-go",'
        b'"host":"test-host",'
        b'"port":9999,'
        b'"headers":true,'
        b'"max_payload":123456,'
        b'"proto":1'
        b'}'
        b'\r\n'
    )
    expected_protocol_message = InfoProtocolMessage(
        server_id="test-server-id",
        server_name="test-server-name",
        version="test-version",
        go="test-go",
        host="test-host",
        port=9999,
        headers=True,
        max_payload=123456,
        proto=1
    )
    line = await connection.readline()
    method, params = line.split(b" ", 1)
    assert method == b"INFO"
    assert msgspec.json.decode(params, type=InfoProtocolMessage) == expected_protocol_message


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
