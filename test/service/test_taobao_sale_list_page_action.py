# -*- coding: utf-8 -*-
from unittest import TestCase

from config.config_loader import global_config
from mall_spider.common.constants import SpiderUrls, SpiderHttp
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.cookie_service import get_cookie_service
from mall_spider.spiders.actions.exception import CookieNeedUpdateException
from mall_spider.spiders.actions.pojo import Good
from mall_spider.spiders.actions.proxy_service import get_proxy_service
from mall_spider.spiders.actions.taobao_presearch_action import TaobaoPresearchAction
from mall_spider.spiders.actions.taobao_sale_list_page_action import TaobaoSaleListPageAction
from mall_spider.spiders.spider_qt5 import spider_qt5_bootstrap


class TestTaobaoSaleListPageAction(TestCase):
    __cookie_service = get_cookie_service()

    __proxy_service = get_proxy_service()
    account = global_config.s_accounts[0]

    def test_login(self):
        cookies, origin_cookies = spider_qt5_bootstrap(url=SpiderUrls.get_sycm_login_url(), account=self.account)
        self.__cookie_service.dump(cookies, self.account)

    def test(self):
        requests_cookie_jar = self.__cookie_service.load(account=self.account)

        context = Context()
        context.attach(Context.KEY_IS_UPDATE_COOKIES, True)
        context.attach(Context.KEY_HEADERS, SpiderHttp.get_taobao_headers('https://s.m.taobao.com/h5'))
        context.attach(Context.KEY_COOKIES, requests_cookie_jar)
        context.attach(Context.KEY_CURRENT_TASK_ACCOUNT, self.account)
        proxy = self.__proxy_service.get_s_proxy(self.account['username'])
        context.attach(Context.KEY_CURRENT_PROXY, proxy)

        good = Good()
        good.set_brand_name('Flyco/飞科')
        good.set_model_name('FR5218')
        context.attach(Context.KEY_GOOD_DICT, good)

        action = TaobaoPresearchAction()
        action.execute(context=context)
        try:
            # action = TaobaoBaichuanAction()
            # action.execute(context=context)
            action = TaobaoSaleListPageAction()
            action.execute(context=context)
        except CookieNeedUpdateException as e:
            self.__cookie_service.dump(requests_cookie_jar, self.account)
