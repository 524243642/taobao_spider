# coding: utf-8

from mall_spider.spiders.actions.default_action import DefaultAction


class DetailMPageAction(DefaultAction):

    def do_execute(self, context):
        """
        :param context:
        :return:
        """
        # http_request = context.get(Context.KEY_DETAIL_M_HTTP_REQUEST)
        # cookies = chrome_qt_bootstrap(http_request.url)
        # request_cookies = context.get(Context.KEY_COOKIES)
        # request_cookies.update(cookies)
        # response = self.execute_in_retry(context=context, http_request=http_request)
        # result = self.unmarshal(context=context, response=response)

        # context.attach(Context.KEY_DETAIL_M_RESULT, result)
        return True

    # def unmarshal(self, context, response):
    #     result = response.text
    #     return result

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
