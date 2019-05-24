# coding: utf-8

import re

from bs4 import BeautifulSoup

from config.config_loader import logger
from mall_spider.common.constants import SpiderUrls
from mall_spider.common.enums import HttpMethod
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.http_action import HttpAction
from mall_spider.spiders.actions.url_info import HttpRequest


class TaobaoPresearchAction(HttpAction):

    def do_execute(self, context):
        """
        :param context:
        :return:
        """
        good = context.get(Context.KEY_GOOD_DICT)
        # brand_name = good.get_brand_name()
        # model_name = good.get_model_name()
        query = good.get_query()
        url = SpiderUrls.get_taobao_presearch_url(query=query)
        http_request = HttpRequest(url=url, method=HttpMethod.GET)
        context.attach(Context.KEY_TAOBAO_PRESEARCH_HTTP_REQUEST, http_request)
        http_request = context.get(Context.KEY_TAOBAO_PRESEARCH_HTTP_REQUEST)
        response = self.execute_in_retry(context=context, http_request=http_request)
        result = self.unmarshal(context=context, response=response)
        context.attach(Context.KEY_TAOBAO_PRESEARCH_RESULT, result)
        return True

    def unmarshal(self, context, response):
        params_dict = self.__get_list_api_params(html=response.text)
        logger.info('list api params:%s', params_dict)
        return params_dict

    def __get_list_api_params(self, html):
        soup = BeautifulSoup(html, "html.parser")
        m = self.__get_list_api_param(html=html, soup=soup, param_name='m')
        token4h5 = self.__get_list_api_param(html=html, soup=soup, param_name='token4h5')
        abtest = self.__get_list_api_param(html=html, soup=soup, param_name='abtest')
        wlsort = self.__get_list_api_param(html=html, soup=soup, param_name='wlsort')
        return {
            'm': m,
            'token4h5': token4h5,
            'abtest': abtest,
            'wlsort': wlsort
        }

    def __get_list_api_param(self, html, soup, param_name):
        try:
            pattern = re.compile(param_name + ":'(.*?)'", re.MULTILINE | re.DOTALL)
            script = soup.find("script", text=pattern)
            return pattern.search(script.text).group(1)
        except Exception as e:
            logger.error('list api params error,param_name%s,origin response:%s,exp:%s', param_name, html, e)
            raise e

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
