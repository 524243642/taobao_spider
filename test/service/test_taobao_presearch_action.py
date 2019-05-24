# -*- coding: utf-8 -*-
from unittest import TestCase

from requests.cookies import RequestsCookieJar

from mall_spider.common.constants import SpiderUrls, SpiderHttp
from mall_spider.common.enums import HttpMethod
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.taobao_presearch_action import TaobaoPresearchAction
from mall_spider.spiders.actions.url_info import HttpRequest


class TestTaobaoPresearchAction(TestCase):

    def test(self):
        url = SpiderUrls.get_taobao_presearch_url(u'三星s9')
        http_request = HttpRequest(url=url, method=HttpMethod.GET)
        context = Context()
        context.attach(Context.KEY_TAOBAO_PRESEARCH_HTTP_REQUEST, http_request)
        context.attach(Context.KEY_IS_UPDATE_COOKIES, False)
        context.attach(Context.KEY_HEADERS, SpiderHttp.get_taobao_headers('https://s.m.taobao.com/h5'))
        context.attach(Context.KEY_COOKIES, RequestsCookieJar())
        action = TaobaoPresearchAction()
        action.execute(context=context)
