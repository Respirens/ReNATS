from renats.protocol.messages.pub import PubProtocolMessage, HPubProtocolMessage
from renats.protocol.messages.service import ConnectProtocolMessage
from renats.protocol.messages.sub import SubProtocolMessage, UnsubProtocolMessage


def test_connect_protocol_message_serialization():
    connect_protocol_message = ConnectProtocolMessage(
        verbose=False,
        pedantic=True,
        tls_required=False,
        lang="python3",
        version="test-version"
    )
    expected_serialization_result = b'CONNECT {' \
                                    b'"verbose":false,' \
                                    b'"pedantic":true,' \
                                    b'"tls_required":false,' \
                                    b'"lang":"python3",' \
                                    b'"version":"test-version"' \
                                    b'}' \
                                    b'\r\n'
    assert connect_protocol_message.dump() == expected_serialization_result


def test_pub_protocol_message_serialization():
    pub_protocol_message = PubProtocolMessage(
        subject="foo.bar",
        reply_to="foo.bar.baz",
        payload=b"Hello NATS!"
    )
    expected_serialization_result = b'PUB foo.bar foo.bar.baz 11\r\nHello NATS!\r\n'
    assert pub_protocol_message.dump() == expected_serialization_result


def test_hpub_protocol_message_serialization():
    hpub_protocol_message = HPubProtocolMessage(
        subject="foo.bar",
        reply_to="foo.bar.baz",
        headers={"Foo": "Bar"},
        payload=b"Hello NATS!"
    )
    expected_serialization_result = b'HPUB foo.bar foo.bar.baz 22 33\r\nNATS/1.0\r\nFoo: Bar\r\n\r\nHello NATS!\r\n'
    assert hpub_protocol_message.dump() == expected_serialization_result


def test_sub_protocol_message_serialization():
    sub_protocol_message = SubProtocolMessage(
        subject="foo.*",
        sid="test_sid_001"
    )
    expected_serialization_result = b'SUB foo.* test_sid_001\r\n'
    assert sub_protocol_message.dump() == expected_serialization_result


def test_unsub_protocol_message_serialization():
    unsub_protocol_message = UnsubProtocolMessage(
        sid="test_sid_001",
        max_msgs=10
    )
    expected_serialization_result = b'UNSUB test_sid_001 10\r\n'
    assert unsub_protocol_message.dump() == expected_serialization_result

