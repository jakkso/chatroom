import queue
import sys
sys.path.append('..')


from client.mqtt_sub import Subscription


def test_client() -> None:
    """
    tests imports running correctly
    """
    c = Subscription()
    assert c is not None


def test_queue_creation() -> None:
    """
    Tests that Queue is correctly added to client.client
    Requires that the machine running this test has mosquitto running on localhost.
    """
    q = queue.Queue()
    host = 'localhost'
    port = 1883
    keep_alive = 60
    c = Subscription(client_id="Bob123", queue_=q, topic="chat_test")
    assert c.client.queue is not None
    assert c.client.topic is not None
    c.client.connect(host, port, keep_alive)
    # c.client.subscribe("chat_test", 2)
    c.client.loop_start()
    # The below is an attempt to mock a display class example, which isn't really relevant to
    # testing the subscription client, which is why it's commented out.
    # try:
    #     while True:
    #         item = c.client.queue.get()
    #         if item is None:
    #             break
    #         print(item.payload)
    #         # if c.client.queue.empty() -> None:
    #         #     break
    # except KeyboardInterrupt:
    #     c.disconnect()
    c.client.loop_stop()
    c.client.disconnect()


if __name__ == '__main__':
    test_queue_creation()
