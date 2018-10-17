import sys
sys.path.append('..')

from client.message import Message


def test_good() -> None:
    good_message = b'{"id": "123", "timestamp": "123456", "payload": "light on"}'
    good = Message(good_message)
    assert good.error is False
    assert good.get_error_text() == "No errors."


def test_missing_ts() -> None:
    missing_ts = b'{"id": "123", "payload": "light on"}'
    bad = Message(missing_ts)
    assert bad.error is True


def test_missing_id() -> None:
    missing_id = b'{"timestamp": "123456", "payload": "light on"}'
    bad = Message(missing_id)
    assert bad.error is True


def test_missing_payload() -> None:
    missing_payload = b'{"id": "123", "timestamp": "123456"}'
    bad = Message(missing_payload)
    assert bad.error is True


def test_bad_unicode() -> None:
    empty = b''
    bad = Message(empty)
    assert bad.error is True
    malformed = b'{"id": "123"'
    bad = Message(malformed)
    assert bad.error is True
    unicode_msg = ''
    bad = Message(unicode_msg)
    assert bad.error is True
    unicode_msg = 'bob\'s burgers are people'
    bad = Message(unicode_msg)
    assert bad.error is True


def test_class_method() -> None:
    text = 'Testing'
    msg = Message.status_message(text)
    assert msg.error is False
    assert msg.get_error_text() == 'No errors.'
    assert msg.payload == 'Testing'


