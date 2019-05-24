# coding: utf-8
from datetime import datetime

from mall_spider.common.constants import SpiderUrls
from mall_spider.common.enums import HttpMethod
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.exception import CookieNeedUpdateException
from mall_spider.spiders.actions.http_action import HttpAction
from mall_spider.spiders.actions.sign import get_sign
from mall_spider.spiders.actions.url_info import HttpRequest


class TaobaoBaichuanAction(HttpAction):

    def __build_data(self, context):
        return ''

    def __build_token(self, context):
        cookies = context.get(Context.KEY_COOKIES)
        _m_h5_tk = cookies.get('_m_h5_tk')
        if not _m_h5_tk:
            return ''
            # raise CookieExpiredException('cookie is expired,msg:_m_h5_tk is not exist')
        return str(_m_h5_tk).split('_')[0]

    def do_execute(self, context):
        """
        :param context:
        :return:
        """
        timestamps = int(datetime.now().timestamp() * 1000)
        data = self.__build_data(context=context)
        token = self.__build_token(context=context)
        sign = get_sign(token=token, timestamps=str(timestamps), appKey='12574478', data=data)
        # data = data.replace(':', '%3A')

        sale_url = SpiderUrls.get_taobao_baichuan_url(timestamps=timestamps, sign=sign)
        sale_http_request = HttpRequest(url=sale_url, method=HttpMethod.GET)
        context.attach(Context.KEY_TAOBAO_BAICHUAN_HTTP_REQUEST, sale_http_request)
        http_request = context.get(Context.KEY_TAOBAO_BAICHUAN_HTTP_REQUEST)
        response = self.execute_in_retry(context=context, http_request=http_request)
        self.unmarshal(context=context, response=response)
        return True

    def unmarshal(self, context, response):
        result = response.text
        if result.find('FAIL_SYS_TOKEN_EMPTY') != -1:
            raise CookieNeedUpdateException('cookies need update,msg:taobao baichuan page')

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
