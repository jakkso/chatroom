"""
Entry point for the program
"""
import queue

from client.shell import Shell


def run() -> None:
    """
    Run the program
    """
    client_id = 'Bob123!'
    queue_ = queue.Queue()
    topic = "chat_test"
    hostname = "localhost"
    shell = Shell(client_id, queue_, topic, hostname)


if __name__ == '__main__':
    run()
