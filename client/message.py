"""
Contains Message implementation
"""
import json
import time
from typing import Type, TypeVar

msg = TypeVar('msg', bound='Message')  # Used for type-hinting Message.status_message()


class Message:
    """
    Converts raw message bytes to a usable message object
    """
    def __init__(self, raw_message: bytes):
        self.raw_message: bytes = raw_message
        self.error: bool = False
        self._error_text: str = None
        self.msg_id: str = None
        self.timestamp: int = None
        self.payload: str = None
        self._convert()

    def _convert(self) -> None:
        """
        Decodes self.raw_message to utf-8 string, then to json, then adds the converted
        JSON to the message object as attributes.

        If there are errors, such as JSON being improperly structured or a missing attribute,
        self.error is set to True, which signals whichever class that is using Message that the
        message is bad

        Correctly assembled example message:

         '{"id": "example_id", "timestamp": 512331, "payload": "hello, I am a payload"}'


        """
        try:
            message = self.raw_message.decode('utf-8')
            json_ = json.loads(message)
            self.msg_id = json_['id']
            self.timestamp = json_['timestamp']
            self.payload = json_['payload']
            self.timestamp = time.time()
        except AttributeError as e:
            self.error = True
            self._error_text = f'{AttributeError}: {e}'
        except UnicodeDecodeError as e:
            self.error = True
            self._error_text = f'{UnicodeDecodeError}: {e}'
        except json.decoder.JSONDecodeError as e:
            self.error = True
            self._error_text = f'{json.decoder.JSONDecodeError}: {e}'
        except KeyError as e:
            self.error = True
            self._error_text = f'{KeyError}: {e}'

    def get_error_text(self) -> str:
        """
        :return: Error text string
        """
        if not self.error:
            return 'No errors.'
        return self._error_text

    @classmethod
    def status_message(cls: Type[msg], message_body: str) -> msg:
        """
        Alternative constructor used to make status messages, rather than
        text messages from chat clients.

        Given that this method instantiates the object from None rather than bytes, which
        sets the error attributes, this method includes statements which clear the error state
        of the object.
        :return: message.Message
        """
        rv = cls(None)
        rv.error, rv._error_text, rv.msg_id = False, None, None
        rv.timestamp, rv.payload = time.time(), message_body
        return rv
