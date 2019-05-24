# coding: utf-8
import ast
import json
from datetime import datetime

from mall_spider.common.constants import SpiderUrls, SpiderParams
from mall_spider.common.enums import TaobaoSearchType, HttpMethod
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.cookie_service import get_cookie_service
from mall_spider.spiders.actions.exception import InterruptException, CookieExpiredException, CookieNeedUpdateException
from mall_spider.spiders.actions.http_action import HttpAction
from mall_spider.spiders.actions.sign import get_sign
from mall_spider.spiders.actions.url_info import HttpRequest


class TaobaoIntegrateListPageAction(HttpAction):
    __cookie_service = get_cookie_service()

    def __build_data(self, context):
        good = context.get(Context.KEY_GOOD_DICT)
        # brand_name = good.get_brand_name()
        # model_name = good.get_model_name()
        query = good.get_query()
        page = 1
        extra = context.get(Context.KEY_TAOBAO_PRESEARCH_RESULT)
        # data = SpiderParams.build_taobao_search_data(query, page, 'list', 'nav,selecthot,onesearch', None, **extra)
        data = SpiderParams.build_taobao_search_data(query, page, None, None, None, **extra)
        datastr = json.dumps(data, ensure_ascii=False)
        datastr = datastr.replace(' ', '')
        return datastr

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
        s_data = data.replace('+', ' ')
        token = self.__build_token(context=context)
        # sign = '' if not token else get_sign(token=token, timestamps=str(timestamps), appKey='12574478', data=data)
        sign = get_sign(token=token, timestamps=str(timestamps), appKey='12574478', data=s_data)
        integrate_url = SpiderUrls.get_taobao_serarch_url(type=TaobaoSearchType.integrate, timestamps=timestamps,
                                                          sign=sign, data=data)
        integrate_http_request = HttpRequest(url=integrate_url, method=HttpMethod.GET)
        context.attach(Context.KEY_TAOBAO_INTERGRATE_LIST_HTTP_REQUEST, integrate_http_request)
        http_request = context.get(Context.KEY_TAOBAO_INTERGRATE_LIST_HTTP_REQUEST)
        response = self.execute_in_retry(context=context, http_request=http_request)
        self.unmarshal(context=context, response=response)

        cookies = context.get(Context.KEY_COOKIES)
        account = context.get(Context.KEY_CURRENT_TASK_ACCOUNT)
        self.__cookie_service.dump(cookies, account)
        return True

    def unmarshal(self, context, response):
        result = response.text
        if result.find('请稍后重试') != -1:
            raise InterruptException(u'happen to risk,value:%s' % (result))
        if result.find('login.m.taobao.com') != -1:
            raise CookieExpiredException('cookie is expired,msg:taobao integrate list page')
        if result.find('FAIL_SYS_TOKEN_EMPTY') != -1:
            raise CookieNeedUpdateException('cookies need update,msg:taobao integrate list page')
        result = result.replace('mtopjsonp1(', '')
        result = ast.Str(result.replace(')', ''))
        result = self.parse_js(result)
        result = json.loads(result)
        result = result['data']
        # context.attach(Context.KEY_TAOBAO_INTERGRATE_RESULT, result)
        # result = response.json()
        context.attach(Context.KEY_TAOBAO_INTERGRATE_RESULT, result)

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass

    def parse_js(self, expr):
        """
        解析非标准JSON的Javascript字符串，等同于json.loads(JSON str)
        :param expr:非标准JSON的Javascript字符串
        :return:Python字典
        """
        import ast
        m = ast.parse(expr)
        a = ast.Str(m.s)

        def parse(node):
            if isinstance(node, ast.Expr):
                return parse(node.value)
            elif isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Str):
                return node.s
            elif isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Dict):
                return dict(zip(map(parse, node.keys), map(parse, node.values)))
            elif isinstance(node, ast.List):
                return map(parse, node.elts)
            else:
                raise NotImplementedError(node.__class__)

        result = parse(a)
        return result
