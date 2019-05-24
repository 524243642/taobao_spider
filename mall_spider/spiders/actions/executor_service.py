# coding: utf-8
from concurrent.futures.thread import ThreadPoolExecutor


class ExecutorService(object):
    executor = None

    def __init__(self, pool_size) -> None:
        super().__init__()
        self.executor = ThreadPoolExecutor(pool_size)

    def submit(self, task, *args):
        return self.executor.submit(task, *args)
