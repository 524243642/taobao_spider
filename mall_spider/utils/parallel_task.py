# coding: utf8
import os

import gevent

from config.config_loader import logger

os.environ['GEVENT_RESOLVER'] = 'ares'


class ParallelTask(object):
    # float timeout: If given, the maximum number of seconds to wait.
    def __init__(self, timeout=None, raise_error=False):
        self.timeout = timeout
        self.raise_error = raise_error
        self.tasks = []

    def add_task(self, task, *args):
        self.tasks.append(gevent.spawn(task, *args))

    def run(self):
        try:
            gevent.joinall(self.tasks, timeout=self.timeout, raise_error=self.raise_error)
        except Exception as ex:
            logger.warning("[ParallelTask] run task fail", exc_info=1)
            raise ex
        return [task.value for task in self.tasks]
