from renats.protocol import utils


def test_encode_headers():
    headers = {
        "Foo": "Bar",
        "Bar": "Baz"
    }
    expected_encoded_headers = {
        b"Foo": b"Bar",
        b"Bar": b"Baz"
    }
    assert utils.encode_headers(headers) == expected_encoded_headers


def test_decode_headers():
    encoded_headers = {
        b"Foo": b"Bar",
        b"Bar": b"Baz"
    }
    expected_decoded_headers = {
        "Foo": "Bar",
        "Bar": "Baz"
    }
    assert utils.decode_headers(encoded_headers) == expected_decoded_headers


def test_build_head():
    method = b"PUB"
    params = (b"foo.bar", b"foo.bar.baz", b"11")
    expected_head = b"PUB foo.bar foo.bar.baz 11"
    assert utils.build_head(method, *params) == expected_head


def test_build_headers():
    headers = {
        b"Foo": b"Bar",
        b"Bar": b"Baz"
    }
    headers_version = b"NATS/1.0"
    expected_built_headers = b"NATS/1.0\r\nFoo: Bar\r\nBar: Baz"
    assert utils.build_headers(headers, headers_version) == expected_built_headers
