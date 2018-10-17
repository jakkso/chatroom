"""
Contains Subscription, which contains methods that fetch messages from the mqtt broker
"""
import queue
from typing import Dict

import paho.mqtt.client as mqtt

from client.message import Message


class SubscriptionError(BaseException):
    pass


class Subscription:
    """
    Subscribes to topics, uses Message to convert payloads returned from broker to a usable form,
    and adds them to a FIFO queue to be displayed elsewhere.

    Paho's mqtt implementation uses a callback function model to deal with messages as they
    come in.  Those callbacks are defined as static functions attached to this class.
    """

    def __init__(self, client_id: str = None, queue_: queue.Queue=None, topic: str = None):
        """
        :param topic: string, topic channel to subscribe to.
        :type queue_: queue.Queue
        :param client_id:  If supplied, subscription will subscribe to the broker's topics
            using it.  If it isn't, than a randomly generated one will be used instead.
        """
        self.client = mqtt.Client(client_id=client_id)
        self.client.queue = queue_
        self.client.topic = topic
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @staticmethod
    def on_connect(client: mqtt.Client, user_data, flags: Dict, return_code: int) -> None:
        """

        :type client: mqtt.Client instance for this callback
        :param user_data: the private user data as set in mqtt.Client() or mqtt.Client.user_data_set()
        :param flags: response flags sent by broker
        :param return_code: int, indicates whether connection was successful or not.
        They are:
            0: Connection successful
            1: Connection refused - incorrect protocol version
            2: Connection refused - invalid client identifier
            3: Connection refused - server unavailable
            4: Connection refused - bad username or password
            5: Connection refused - not authorised
            6-255: Currently unused.
        :return: None
        """
        if return_code != 0:
            if return_code == 1:
                raise SubscriptionError('Incorrect protocol version')
            elif return_code == 2:
                raise SubscriptionError('Invalid client identifier')
            elif return_code == 3:
                raise SubscriptionError('Server unavailable')
            elif return_code == 4:
                raise SubscriptionError('Bad username or password')
            elif return_code == 5:
                raise SubscriptionError('Not authorized')
            else:
                raise SubscriptionError(f'Non-specified connection error code: {return_code}')

        # If the message queue is not added correctly the the client instance, than messages
        # cannot be correctly passed
        if client.queue is None:
            raise SubscriptionError('Queue absent from instance. Aborting.')
        if client.topic is None:
            raise SubscriptionError('Topic absent from instance.  Aborting.')
        client.subscribe(client.topic, qos=2)
        status = Message.status_message('Connected.')
        client.queue.put(status)

    @staticmethod
    def on_subscribe(client: mqtt.Client, user_data, message_id: int, granted_qos) -> None:
        """

        :type client: mqtt.Client instance for this callback
        :param user_data: the private user data as set in mqtt.Client() or mqtt.Client.user_data_set()
        :param message_id: integer, the message id
        :param granted_qos:
        :return:
        """
        status = Message.status_message('Subscription active.')
        client.queue.put(status)

    @staticmethod
    def on_message(client: mqtt.Client, user_data, message: mqtt.MQTTMessage) -> None:
        """
        :param client: mqtt.Client instance for this callback
        :param user_data: the private user data as set in mqtt.Client() or mqtt.Client.user_data_set()
        :param message: mqtt.MQTTMessage object
        :return:
        """
        msg = Message(message.payload)
        if msg.error:
            msg.payload = 'Message error.'
        client.queue.put(msg)

    @staticmethod
    def on_disconnect(client: mqtt.Client, user_data, return_code: int) -> None:
        """
        :param client: mqtt.Client instance for this callback
        :param user_data: the private user data as set in mqtt.Client() or mqtt.Client.user_data_set()
        :param return_code:
        :return:
        """
        if return_code != 0:
            msg = Message.status_message('Disconnected unexpectedly.')
        else:
            msg = Message.status_message('Disconnected.')
        client.queue.put(msg)

    def connect(self, hostname: str, port: int = 1883, keep_alive: int = 60) -> None:
        """
        :param hostname:
        :param port: int, defaults to 1883
        :param keep_alive: maximum period in seconds allowed between communications with the broker.
         If no other messages are being exchanged, this controls the rate at which the client will
         send ping messages to the broker.
        :return:
        """
        self.client.connect(hostname, port, keep_alive)

    def disconnect(self) -> None:
        """
        :return: None
        """
        self.client.disconnect()
