import queue
import sys
import threading
import time

sys.path.append('..')

from client.display import CLIDisplay


class TestObj:
    pass


class DumpIntoQueue:
    """

    """

    def __init__(self, queue_: queue.Queue):
        self.alive = True
        self.queue = queue_
        self.thread: threading.Thread = threading.Thread(target=self._worker,
                                                         name='Queue dumper',
                                                         daemon=False)

    def run(self):
        self.thread.start()

    def _worker(self):
        while self.alive:
            payload = TestObj()
            payload.payload = f'Timestamp: {time.time()}'
            self.queue.put(payload)


def test_cli_display():
    """
    Tests CLI display functionality
    """
    q = queue.Queue()
    display = CLIDisplay(q)
    display.start()
    d = DumpIntoQueue(q)
    d.run()
    for i in range(5):
        test = TestObj()
        test.payload = f"Number {i}"
        q.put(test)
    # killer = TestObj()
    # killer.kill = True
    # q.put(killer)
    display.alive = False
    d.alive = False
