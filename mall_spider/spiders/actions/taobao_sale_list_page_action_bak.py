# coding: utf-8
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.http_action import HttpAction


class TaobaoSaleListPageAction(HttpAction):

    def do_execute(self, context):
        """
        :param context:
        :return:
        """
        http_request = context.get(Context.KEY_TAOBAO_SALE_LIST_HTTP_REQUEST)
        response = self.execute_in_retry(context=context, http_request=http_request)
        self.unmarshal(context=context, response=response)
        return True

    def unmarshal(self, context, response):
        result = response.json()
        context.attach(Context.KEY_TAOBAO_SALE_RESULT, result)

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
