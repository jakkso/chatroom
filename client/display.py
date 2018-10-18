"""
Contains display class
"""
import threading
import queue


class CLIDisplay:
    """
    A simple CLI display using the threaded approach to print queue items to the terminal.
    """
    def __init__(self, queue_: queue.Queue):
        self.queue = queue_
        self.thread = threading.Thread(target=self._worker, name='Display worker', daemon=False)
        self.alive = True

    def start(self):
        self.thread.start()

    def _worker(self) -> None:
        """
        Worker target for the threaded interface to use.

        The worker gets items from the queue and prints them to the screen.
        If a poison pill is detected, it quits
        """
        while self.alive:
            item = self.queue.get()
            print(item.payload)
