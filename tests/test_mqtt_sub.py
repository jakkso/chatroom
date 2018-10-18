from difflib import SequenceMatcher as Seq
import json
import pytest
import queue
import sys
import time

sys.path.append('..')

from client.mqtt_sub import Subscription, SubscriptionError


def test_client() -> None:
    """
    tests imports running correctly
    """
    c = Subscription()
    assert c is not None


def test_sub_creation_with_sub() -> None:
    """
    Tests that Queue is correctly added to client.client
    Requires that the machine running this test has mosquitto running on localhost.
    """
    q = queue.Queue()
    host = 'localhost'
    port = 1883
    keep_alive = 60
    with pytest.raises(SubscriptionError):
        c = Subscription(client_id="Bob1")
        c.client.connect(host, port, keep_alive)
        c.client.loop_forever()
    c.disconnect()

    with pytest.raises(SubscriptionError):
        c = Subscription(client_id="Bob1", queue_=q, topic=None)
        c.client.connect(host, port, keep_alive)
        c.client.loop_forever()
    c.disconnect()

    c = Subscription(client_id="Bob123", queue_=q, topic="chat_test")
    assert c.client.queue is not None
    assert c.client.topic is not None
    c.client.connect(host, port, keep_alive)
    c.client.loop_start()
    while True:
        try:
            c.client.queue.get(timeout=0.25)
        except queue.Empty:
            break
    c.client.loop_stop()
    c.client.disconnect()


def test_create_payload() -> None:
    """
    Tests that Subscription._create_payload returns the correctly formatted string object.
    """
    id_ = 123
    message = 'Hello, world!'
    timestamp = time.time()
    payload = Subscription._create_payload(message, id_)
    expected = f'{{"id": {id_}, "timestamp": {timestamp}, "payload": "{message}" }}'
    assert isinstance(payload, str)
    # This is to account for two non-simultaneous calls to time.time()
    diff: float = Seq(a=payload, b=expected).ratio()
    assert diff > 0.90
    load = json.loads(payload)
    assert isinstance(load, dict)
    assert load['id'] == id_
    assert load['payload'] == message


def test_publish_payload() -> None:
    """
    Tests publishing functionality
    """
    q = queue.Queue()
    host = 'localhost'
    port = 1883
    keep_alive = 60
    c = Subscription(client_id="Bob123", queue_=q, topic="chat_test")
    c.client.connect(host, port, keep_alive)
    c.client.loop_start()
    message = 'Hello, world!'
    message_id = 5000
    c.publish(message, message_id)
    for i in range(5):
        c.publish("Hi there!", i)
    items = []
    while True:
        try:
            item = c.client.queue.get(timeout=0.25)
            items.append(item)
        except queue.Empty:
            break
    c.client.loop_stop()
    c.disconnect()
    assert len(items) > 5


if __name__ == '__main__':
    test_sub_creation_with_sub()
