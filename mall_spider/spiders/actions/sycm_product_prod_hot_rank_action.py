# coding: utf-8

from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.exception import CookieExpiredException
from mall_spider.spiders.actions.http_action import HttpAction


class SycmProductProdHotRankAction(HttpAction):

    def do_execute(self, context):
        """
        :param context:
        :return:
        """
        http_request = context.get(Context.KEY_SYCM_PRODUCT_PROD_HOT_RANK_HTTP_REQUEST)
        response = self.execute_in_retry(context=context, http_request=http_request)
        result = self.unmarshal(context=context, response=response)
        self.check_result(context, result)
        context.attach(Context.KEY_SYCM_PRODUCT_PROD_HOT_RANK_RESULT, result)
        return True

    def check_result(self, context, result):
        if result.get('code', 0) == 5810 or result.get('msg', '') == 'You must login system first' or result.get(
                'message',
                '') == '类目无权限':
            raise CookieExpiredException('cookie is expired,origin msg:%s' % result)
        # if result.get('code', 0) == 1000 or result.get('msg', '') == '系统出错，未知异常':
        #     raise CookieExpiredException('system exception')

    def unmarshal(self, context, response):
        return response.json()

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
