# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler

from config.config_loader import logger
from mall_spider.spiders.actions.action_service import ActionService


class SycmScheduleJob(ActionService, BlockingScheduler):

    def __init__(self):
        super().__init__()

    def handle(self):
        # self.execute_sycm_category_job_init_actions()
        self.add_job(self.execute_sycm_category_job_init_actions, 'cron', day_of_week='0-6', hour=10, minute=30,
                     second=0)

    def run(self):
        self.handle()
        self.start()


if __name__ == "__main__":
    s = SycmScheduleJob()
    logger.info("start to execute sycm_schedule job")
    s.run()
    # jobs = s.get_jobs()
    # print(jobs)
    logger.error("exit sycm_schedule job")
