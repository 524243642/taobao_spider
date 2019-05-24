# -*- coding: utf-8 -*-
from unittest import TestCase

from config.config_loader import global_config
from mall_spider.common.constants import SpiderUrls
from mall_spider.common.enums import PickleFileType
from mall_spider.spiders.actions.cookie_service import get_cookie_service
from mall_spider.spiders.actions.proxy_service import get_proxy_service
from mall_spider.spiders.spider_qt5 import spider_qt5_bootstrap


class TestSpiderQt5(TestCase):
    __cookie_service = get_cookie_service()
    __proxy_service = get_proxy_service()

    def test_login(self):
        url = SpiderUrls.get_sycm_login_url()
        # account = global_config.s_accounts[1]
        # proxy = __proxy_service.get_origin_static_proxy(account['username'])
        account = global_config.accounts[0]
        proxy = None
        cookies, origin_cookies = spider_qt5_bootstrap(url, account, True, proxy)
        self.__cookie_service.dump(cookies=cookies, account=account)
        print(cookies)

    def test_app_login(self):
        url = SpiderUrls.get_app_taobao_login_url()
        # account = global_config.s_accounts[1]
        # proxy = __proxy_service.get_origin_static_proxy(account['username'])
        account = global_config.s_accounts[0]
        proxy = None
        cookies, origin_cookies = spider_qt5_bootstrap(url, account, True, proxy)
        self.__cookie_service.dump(cookies=cookies, account=account)
        print(cookies)


    def test_spider_qt5(self):
        url = 'https://s.m.taobao.com/h5?q=Flyco%2BFR5218&search=%E6%8F%90%E4%BA%A4&tab=all'
        account = global_config.s_accounts[0]
        proxy = self.__proxy_service.get_origin_static_proxy(account['username'])
        cookies = self.__cookie_service.load(account=account, type_=PickleFileType.origin_cookie)
        cookies, origin_cookies = spider_qt5_bootstrap(url=url, account=account, risk=True,
                                                       proxy=proxy, cookies=cookies)
        self.__cookie_service.dump(cookies=cookies, account=account)
        self.__cookie_service.dump(cookies=origin_cookies, account=account, type_=PickleFileType.origin_cookie)
