# coding: utf-8
import ast
import json

from requests.exceptions import ProxyError
from urllib3.exceptions import ConnectTimeoutError

from config.config_loader import logger
from mall_spider.common.enums import GoodDataType
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.exception import RetryException, InterruptException, ProxyException
from mall_spider.spiders.actions.http_action import HttpAction


class TaobaoDetailPageAction(HttpAction):

    def do_execute(self, context):
        """
        :param context:
        :return:
        """
        http_request = context.get(Context.KEY_TAOBAO_DETAIL_HTTP_REQUEST)
        try:
            response = self.execute_in_retry(context=context, http_request=http_request)
        except ProxyError as e:
            # logger.exception(e)
            raise ProxyException(e)
        except ConnectTimeoutError as e:
            # logger.exception(e)
            raise ProxyException(e)
        result = self.unmarshal(context=context, response=response)
        self.check_result(context=context, result=result)
        context.attach(Context.KEY_TAOBAO_DETAIL_RESULT, result)
        return True

    def check_result(self, context, result):
        good = context.get(Context.KEY_GOOD_DICT)
        task = context.get(Context.KEY_CURRENT_TASK)
        task_id = task.id

        detail_brand_id = result['data']['item'].get('brandValueId', '')
        brand_id = good.get_brand_id()
        if str(detail_brand_id) != str(brand_id):
            raise RetryException(
                u'brand_id not match,task_id:%s,value:%s,expect:%s' % (
                    str(task_id), str(detail_brand_id), str(brand_id)))

        groupProps = result['data']['props']['groupProps']
        if not groupProps:
            raise RetryException('groupProps not exist,task_id:%s' % (task_id))

        prop = groupProps[0]
        base_infos = prop.get('基本信息', '')
        if not base_infos:
            raise RetryException('baseInfo not exist,task_id:%s' % (task_id))
        model_name = None
        for base_info in base_infos:
            for key, value in base_info.items():
                if str(key).find('型号') != -1:
                    model_name = value
                    break
                if str(key).find('货号') != -1:
                    model_name = value
                    break
            if model_name:
                break
        # brand_name = base_info.get('品牌', '')
        # if not brand_name:
        #     raise RetryException('brandName not exist,task_id:%s' % (task_id))
        if not model_name:
            raise RetryException('modelName not exist,task_id:%s' % (task_id))
        if str(model_name).upper().find(str(good.get_model_name()).upper()) == -1:
            raise RetryException(
                u'model not match,task_id:%s,value:%s,expect:%s' % (task_id, model_name, good.get_model_name()))
        sku2info = result['data']['apiStack'][0]['value']['skuCore']['sku2info']
        price_info = []
        for key, value in sku2info.items():
            price_info.append({
                'skuId': key,
                'price': value['price']['priceMoney']
            })
        good['priceInfo'] = price_info

        good['flag'] = str(int(GoodDataType.detail_success))
        sku_base = result['data']['skuBase']
        good['skuBase'] = sku_base
        # good.set_price_info(price_info=price_info)
        # good.set_flag(str(int(GoodDataType.success)))

    def unmarshal(self, context, response):
        result = response.text
        if result.find('请稍后重试') != -1:
            raise InterruptException(u'happen to risk,value:%s' % (result))
        if result.find('apiStack') == -1:
            raise RetryException(u'may happen to risk,value:%s' % (result))
        result = result.replace('mtopjsonp3(', '')
        result = ast.Str(result.replace(')', ''))
        result = self.parse_js(result)
        # print(result)
        # result = result.replace(':"\\"', ':"')
        # result = result.replace('\\""', '"')
        # result = result.replace('mtopjsonp2(', '')
        # result = result.replace(')', '')
        # result = result.replace('\\', '')
        # result = result.replace('"{', '{')
        # result = result.replace('}"', '}')
        # result = result.replace('"[', '[')
        # result = result.replace(']"', ']')
        result = json.loads(result)
        try:
            value_str = result['data']['apiStack'][0]['value']
            result['data']['apiStack'][0]['value'] = json.loads(value_str)
        except Exception as e:
            logger.error('taobao detail page unmarshal error,result:%s', result)
            raise e
        return result

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

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
