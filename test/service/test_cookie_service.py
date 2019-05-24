# -*- coding: utf-8 -*-
from unittest import TestCase

from config.config_loader import global_config
from mall_spider.dto.pickle_cookie import PickleCookieJar
from mall_spider.spiders.actions.cookie_service import get_cookie_service


class TestCookieService(TestCase):
    __cookie_service = get_cookie_service()

    def test_load(self):
        account = global_config.accounts[0]
        cookies = self.__cookie_service.load(account=account)

    def test_dump(self):
        account = global_config.accounts[1]
        cookie = PickleCookieJar()
        self.__cookie_service.dump(cookie, account)
