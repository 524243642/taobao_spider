# -*- coding: utf-8 -*-
from unittest import TestCase

from mall_spider.spiders.actions.action_service import get_action_service
from mall_spider.utils.date_util import today, yesterday


class TestJob(TestCase):
    __action_service = get_action_service()

    def test_execute_sycm_category_job_init_actions(self):
        # date_str = yesterday().strftime("%Y-%m-%d")
        date_str = yesterday().strftime("2019-01-29")
        self.__action_service.execute_sycm_category_job_init_actions(date_str)
