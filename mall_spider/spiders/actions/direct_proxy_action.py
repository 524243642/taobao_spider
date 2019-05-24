# coding: utf-8

from config.config_loader import logger
from mall_spider.common.enums import HttpMethod
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.http_action import HttpAction
from mall_spider.spiders.actions.url_info import HttpRequest


class DirectProxyAction(HttpAction):

    def do_execute(self, context):
        """
        :param context:
        :return:
        """
        from mall_spider.spiders.actions.proxy_service import ProxyService
        url = ProxyService.proxy_fetch_url
        http_request = HttpRequest(url=url, method=HttpMethod.GET)
        context.attach(Context.KEY_PROXY_HTTP_REQUEST, http_request)
        http_request = context.get(Context.KEY_PROXY_HTTP_REQUEST)
        response = self.execute_in_retry(context=context, http_request=http_request)
        result = self.unmarshal(context=context, response=response)
        context.attach(Context.KEY_PROXY_RESULT, result)
        return True

    def unmarshal(self, context, response):
        result = response.json()
        logger.info('proxy result:%s', result)
        return result['data']

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
