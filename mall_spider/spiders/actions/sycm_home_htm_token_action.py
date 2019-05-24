# coding: utf-8
import re

from config.config_loader import logger
from mall_spider.common.constants import SpiderUrls
from mall_spider.common.enums import HttpMethod
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.exception import CookieExpiredException
from mall_spider.spiders.actions.http_action import HttpAction
from mall_spider.spiders.actions.url_info import HttpRequest


class SycmHomeHtmTokenAction(HttpAction):

    def do_execute(self, context):
        """
        :param context:
        :return:
        """
        http_request = HttpRequest(SpiderUrls.get_sycm_home_htm_url(), HttpMethod.GET)
        context.attach(Context.KEY_SYCM_HOME_HTM_TOKEN_HTTP_REQUEST, http_request)
        http_request = context.get(Context.KEY_SYCM_HOME_HTM_TOKEN_HTTP_REQUEST)
        response = self.execute_in_retry(context=context, http_request=http_request)
        result = self.unmarshal(context=context, response=response)
        context.attach(Context.KEY_SYCM_HOME_HTM_TOKEN_RESULT, result)
        return True

    def unmarshal(self, context, response):
        html = response.text
        try:
            rst = re.search("legalityToken=(.*?);", html).group(1)
            return rst
        except Exception as e:
            logger.error('legalityToken fetch error,origin response:%s,exp:%s', html, e)
            raise CookieExpiredException(e)
        # soup = BeautifulSoup(html, "html.parser")
        # try:
        #     pattern = re.compile("legalityToken=(.*?);", re.MULTILINE | re.DOTALL)
        #     script = soup.find(text=pattern)
        #     return pattern.search(script.text).group(0)
        # except Exception as e:
        #     logger.error('legalityToken fetch error,origin response:%s,exp:%s', html, e)
        #     raise e

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
