# -*- coding: utf-8 -*-

import time
from concurrent.futures import as_completed

from config.config_loader import logger
from mall_spider.job.smorf import Smorf
from mall_spider.spiders.actions.action_service import ActionService
from mall_spider.spiders.actions.executor_service import ExecutorService
from mall_spider.spiders.actions.proxy_service import ProxyService


class TaobaoDetailPageJob(ActionService, Smorf):
    def __init__(self, pool_size):
        super().__init__()
        self._executor = ExecutorService(pool_size)
        self._proxy = ProxyService()

    def execute(self, num):
        tasks = self.execut_taobao_detail_actions()
        i = 0
        future_tasks = {}

        for task in tasks:
            proxy = self._proxy.get_proxy()
            if i < num:
                future_tasks[self._executor.submit(self._execut_taobao_detail_actions, task, proxy)] = task
            i += 1
        for future in as_completed(future_tasks):
            try:
                proxy = future.result()
                if proxy:
                    self._proxy.remove_proxy(url=proxy['https'])
            except Exception as e:
                logger.error(e)

    def init(self):
        super().init()

    def init_argparse(self, parser):
        super().init_argparse(parser)

    def process(self):
        # return super().process()
        self.execute(5)
        time.sleep(3)


if __name__ == "__main__":
    s = TaobaoDetailPageJob(40)
    logger.info("start to execute taobao_detail_page job")
    s.run()
    # s.process()
    logger.error("exit taobao_detail_page job")
