# -*- coding: utf-8 -*-
import time

from config.config_loader import logger
from mall_spider.job.smorf import Smorf
from mall_spider.spiders.actions.action_service import ActionService
from mall_spider.spiders.actions.executor_service import ExecutorService
from mall_spider.utils.date_util import yesterday


class DirectSyncJob(ActionService, Smorf):
    def __init__(self, pool_size):
        super().__init__()
        self._executor = ExecutorService(pool_size)

    def execute(self, num, date_str=None):
        # date_str = yesterday().strftime("%Y-%m-%d")
        date_str = '2019-01-17'
        self.execute_direct_good_actions(date_str=date_str)

    def init(self):
        super().init()

    def init_argparse(self, parser):
        super().init_argparse(parser)

    def process(self):
        self.execute(10)
        time.sleep(10)


if __name__ == "__main__":
    s = DirectSyncJob(1)
    logger.info("start to execute direct sync job")
    s.process()
    logger.info("exit direct sync job")
