# -*- coding: utf-8 -*-
import time

from config.config_loader import logger
from mall_spider.job.smorf import Smorf
from mall_spider.spiders.actions.action_service import ActionService
from mall_spider.spiders.actions.executor_service import ExecutorService


class SycmJob(ActionService, Smorf):
    def __init__(self, pool_size):
        super().__init__()
        self._executor = ExecutorService(pool_size)

    def execute(self, num, date_str=None):
        # if not date_str:
        #     date_str = yesterday()
        tasks = self.execute_sycm_product_actions()
        logger.info("start to execute sycm tasks,tasks length:%s", len(tasks))
        i = 0
        for task in tasks:
            if i < num:
                self._execute_sycm_product_actions(task)
                # self._executor.submit(self._execute_sycm_product_actions, task)
                i += 1
                time.sleep(15)

    def init(self):
        super().init()

    def init_argparse(self, parser):
        super().init_argparse(parser)

    def process(self):
        # return super().process()
        self.execute(10)
        time.sleep(10)

    # def run(self):
    #     self.execute(self, maxInt)


if __name__ == "__main__":
    s = SycmJob(1)
    logger.info("start to execute sycm job")
    s.run()
    logger.error("exit sycm job")
