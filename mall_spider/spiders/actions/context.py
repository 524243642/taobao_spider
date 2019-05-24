# coding: utf-8


from mall_spider.spiders.actions.exception import IllegalArgumentException
from mall_spider.utils.id_gen import IdGen


class Context(object):
    # KEY_TAOBAO_LIST_PAGE_QUERY = 'key_taobao_list_page_query'
    # KEY_TAOBAO_LIST_PAGE_NO = 'key_taobao_list_page_number'
    KEY_TAOBAO_PRESEARCH_HTTP_REQUEST = 'key_taobao_presearch_http_request'
    KEY_TAOBAO_PRESEARCH_RESULT = 'key_taobao_presearch_result'

    KEY_TAOBAO_INTERGRATE_LIST_HTTP_REQUEST = 'key_taobao_integrate_list_http_request'
    KEY_TAOBAO_INTERGRATE_RESULT = 'key_taobao_integrate_result'
    KEY_TAOBAO_SALE_LIST_HTTP_REQUEST = 'key_taobao_sale_list_http_request'
    KEY_TAOBAO_SALE_RESULT = 'key_taobao_sale_result'
    KEY_TAOBAO_BAICHUAN_HTTP_REQUEST = 'key_taobao_baichuan_http_request'
    KEY_TAOBAO_BAICHUAN_RESULT = 'key_taobao_baichuan_result'
    KEY_IS_UPDATE_COOKIES = 'key_is_update_cookies'
    KEY_COOKIES = 'key_cookies'
    KEY_HEADERS = 'key_headers'
    KEY_CURRENT_SLEEP_SECS = 'key_current_sleep_secs'

    KEY_GOOD_DICT = 'key_good_dict'

    # KEY_CURRENT_POLICY_SUCCESS_NUM = 'key_current_policy_success_num'

    KEY_CURRENT_TASK_TYPE = 'key_current_task_type'
    KEY_CURRENT_TASKS = 'key_current_tasks'
    KEY_ACTION_DICT = 'key_action_dict'

    KEY_DETAIL_M_HTTP_REQUEST = 'key_detail_m_http_request'
    KEY_DETAIL_M_RESULT = 'key_detail_m_result'

    KEY_TAOBAO_DETAIL_HTTP_REQUEST = 'key_taobao_detail_http_request'
    KEY_TAOBAO_DETAIL_RESULT = 'key_taobao_detail_result'
    KEY_CURRENT_TASK = 'key_current_task'

    KEY_SYCM_PRODUCT_GET_BRANDS_HTTP_REQUEST = 'key_sycm_product_get_brands_http_request'
    KEY_SYCM_PRODUCT_GET_BRANDS_RESULT = 'key_sycm_product_get_brands_result'

    KEY_SYCM_PRODUCT_PROD_HOT_RANK_HTTP_REQUEST = 'key_sycm_product_prod_hot_rank_http_request'
    KEY_SYCM_PRODUCT_PROD_HOT_RANK_RESULT = 'key_sycm_product_prod_hot_rank_result'

    KEY_SYCM_HOME_HTM_TOKEN_HTTP_REQUEST = 'key_sycm_home_htm_token_http_request'
    KEY_SYCM_HOME_HTM_TOKEN_RESULT = 'key_sycm_home_htm_token_result'

    KEY_SYCM_SPECIFIC_DATE = 'key_sycm_specific_date'
    KEY_DIRECT_COLLECT_DATE = 'key_direct_collect_date'

    KEY_CURRENT_TASK_ACCOUNT = 'key_current_task_account'
    KEY_CURRENT_PROXY = 'key_current_proxy'

    KEY_PROXY_HTTP_REQUEST = 'key_proxy_http_request'
    KEY_PROXY_RESULT = 'key_proxy_result'

    def __init__(self):
        super(Context, self).__init__()
        self.key_map = {}
        self.context_key = IdGen.uuid()
        self.__init_action_dict()

    def __init_action_dict(self):
        policy_dict = {
        }
        self.key_map.setdefault(self.KEY_ACTION_DICT, policy_dict)

    def attach(self, key, value):
        # self.key_map.setdefault(key, value)
        self.key_map[key] = value

    def get(self, key, default=None):
        value = self.key_map.get(key, default)
        if value is None and default is None:
            raise IllegalArgumentException(
                u'context key:[%s]:context map value not exist,key:%s' % (self.context_key, key))
        return value

    def has_key(self, key):
        return self.key_map.has_key(key)
