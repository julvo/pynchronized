#! /usr/bin/python3
import unittest
import time
from threading import Thread
from multiprocessing import Process

from pynchronized import synchronized, thread_synchronized

class TestStrategyUtils(unittest.TestCase):
    def test_synchronized_class_in_thread(self):
        self._test_synchronized_class(synchronized, Thread)

    def test_synchronized_method_in_thread(self):
        self._test_synchronized_method(synchronized, Thread)

    def test_synchronized_class_in_process(self):
        self._test_synchronized_class(synchronized, Process)

    def test_synchronized_method_in_process(self):
        self._test_synchronized_method(synchronized, Process)

    def test_thread_synchronized_class_in_thread(self):
        self._test_synchronized_class(thread_synchronized, Thread)

    def test_thread_synchronized_method_in_thread(self):
        self._test_synchronized_method(thread_synchronized, Thread)

    def _test_synchronized_class(self, decorator, executor):
        """test if methods run sequentially in synchronized class"""

        delay = 0.05 # time in seconds to measure if sequentially or concurrent

        @decorator
        class SyncClass:
            def a(self):
                time.sleep(delay)
            def b(self):
                time.sleep(delay)

        c = SyncClass()
        fns_to_run = [c.a, c.b, c.a]

        executors = []
        for m in fns_to_run:
            executors.append(executor(target=m, daemon=True))

        start = time.time()
        for e in executors:
            e.start()

        for e in executors:
            e.join()
        end = time.time()

        self.assertGreater(end - start, len(fns_to_run) * delay)

    def _test_synchronized_method(self, decorator, executor):
        """test if synchronized methods run sequentially"""

        delay = 0.05 # time in seconds to measure if sequentially or concurrent

        class SyncClass:
            @decorator
            def sync_method(self):
                time.sleep(delay)
            def b(self):
                time.sleep(delay)

        c = SyncClass()
        sync_fns_to_run = [c.sync_method, c.sync_method, c.sync_method]
        other_fns_to_run = [c.b, c.b]

        executors = []
        for m in sync_fns_to_run:
            executors.append(executor(target=m, daemon=True))
        for m in other_fns_to_run:
            executors.append(executor(target=m, daemon=True))

        start = time.time()
        for e in executors:
            e.start()

        for e in executors:
            e.join()
        end = time.time()

        self.assertGreater(end - start, len(sync_fns_to_run) * delay)
        self.assertLess(
                end - start,
                (len(sync_fns_to_run) + len(other_fns_to_run)) * delay,
                )

if __name__ == '__main__':
    unittest.main()
