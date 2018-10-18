"""
Combination of all various elements of the client to one whole program.
"""
import queue

from client.display import CLIDisplay
from client.mqtt_sub import Subscription, SubscriptionError
from client.message import Message


class Shell:
    """
    Combines all the bits into a single working chat program
    """
    def __init__(self,
                 client_id: str,
                 queue_: queue.Queue,
                 topic: str,
                 hostname: str,
                 port: int = 1883,
                 keep_alive: int = 60
                 ):
        """

        """
        self.client_id = client_id
        self.topic = topic
        self.hostname = hostname
        self.port = port
        self.keep_alive = keep_alive
        self.queue = queue_
        self.running = True

        self.display = CLIDisplay(self.queue)
        self.subscriber = Subscription(self.client_id, self.queue, self.topic)
        self.start()

    def start(self) -> None:
        """
        Used to start initial looping, detect SubscriberErrors, and if all is well,
        fire up the threaded loop_start as well as the input loop.
        :return:
        """
        self.subscriber.connect(self.hostname, self.port, self.keep_alive)
        try:
            self.display.start()
            # This is probably a bad assumption, but loop ten times,
            # if SubscriptionError hasn't been raised, assume all is well and call Shell.run()
            loops = 10
            while loops > 0:
                self.subscriber.client.loop()
                loops -= 1
        except SubscriptionError as e:
            print(str(e))
            self.display.alive = False
            return
        self.run()

    def run(self) -> None:
        """
        If start goes well, this is called.  Calls input to get user input to send to broker
        :return: None
        """
        self.subscriber.client.loop_start()
        while self.running:
            try:
                text: str = input('> ')
                if len(text) > 0:
                    self.subscriber.publish(text, 1)
            except KeyboardInterrupt:
                self.shutdown()
            except EOFError:
                self.shutdown()

    def shutdown(self) -> None:
        """
        Gracefully cleanup / shutdown
        """
        self.running = False
        self.subscriber.disconnect()
        self.display.alive = False
        print('\nExiting...')


