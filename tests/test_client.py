import queue
import sys
sys.path.append('..')


from client.mqtt_sub import Subscription


def test_client():
    """
    tests imports running correctly
    """
    c = Subscription()
    assert c is not None


def test_queue_creation():
    """
    Tests that Queue is correctly added to client.client
    """
    q = queue.Queue()
    host = '192.168.1.64'
    port = 1883
    keep_alive = 60
    c = Subscription(client_id="Bob123", queue_=q)
    assert c.client.queue is not None
    c.client.connect(host, port, keep_alive)
    c.client.subscribe(topic="test")
    c.client.loop_forever()


if __name__ == '__main__':
    test_queue_creation()

