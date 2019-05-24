# coding: utf-8
import time
from datetime import datetime

from requests.cookies import RequestsCookieJar

from config.config_loader import logger
from mall_spider.common.constants import SpiderUrls, SpiderHttp, Category
from mall_spider.common.enums import HttpMethod, TaobaoTaskType, GoodDataType, PickleFileType
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.cookie_service import get_cookie_service
from mall_spider.spiders.actions.detail_m_page_action import DetailMPageAction
from mall_spider.spiders.actions.exception import RetryException, CookieExpiredException, InterruptException, \
    CookieNeedUpdateException, ProxyException, CookieNotFoundException, ExitException
from mall_spider.spiders.actions.good_direct_persist_action import GoodDirectPersistAction
from mall_spider.spiders.actions.good_persist_action import GoodPersistAction
from mall_spider.spiders.actions.pojo import Good
from mall_spider.spiders.actions.sycm_category_job_init_action import SycmCategoryJobInitAction
from mall_spider.spiders.actions.sycm_home_htm_token_action import SycmHomeHtmTokenAction
from mall_spider.spiders.actions.sycm_product_get_brands_action import SycmProductGetBrandsAction
from mall_spider.spiders.actions.sycm_product_prod_hot_rank_action import SycmProductProdHotRankAction
from mall_spider.spiders.actions.sycm_product_prod_hot_rank_persist_action import SycmProductProdHotRankPersistAction
from mall_spider.spiders.actions.taobao_detail_page_action import TaobaoDetailPageAction
from mall_spider.spiders.actions.taobao_integrate_list_page_action import TaobaoIntegrateListPageAction
from mall_spider.spiders.actions.taobao_list_page_persist_action import TaobaoListPagePersistAction
from mall_spider.spiders.actions.taobao_presearch_action import TaobaoPresearchAction
from mall_spider.spiders.actions.taobao_sale_list_page_action import TaobaoSaleListPageAction
from mall_spider.spiders.actions.task_collect_action import TaskCollectAction
from mall_spider.spiders.actions.task_direct_collect_action import TaskDirectCollectAction
from mall_spider.spiders.actions.thread_sleep_action import ThreadSleepAction
from mall_spider.spiders.actions.url_info import HttpRequest
from mall_spider.spiders.spider_qt5 import spider_qt5_bootstrap
from mall_spider.utils.money_util import yuan_2_cent

__action_service = None


class ActionService(object):
    _cookie_service = get_cookie_service()

    def __init__(self):
        super(ActionService, self).__init__()

    def get_sycm_product_actions(self):
        actions = list()
        actions.append(SycmProductGetBrandsAction())
        actions.append(SycmProductProdHotRankAction())
        actions.append(SycmProductProdHotRankPersistAction())
        return actions

    def get_taobao_integrate_list_actions(self):
        actions = list()
        actions.append(TaobaoPresearchAction())
        actions.append(TaobaoIntegrateListPageAction())
        actions.append(ThreadSleepAction())
        actions.append(TaobaoSaleListPageAction())
        actions.append(TaobaoListPagePersistAction())
        actions.append(ThreadSleepAction())
        return actions

    def get_taobao_http_detail_actions(self):
        actions = list()
        actions.append(DetailMPageAction())
        actions.append(TaobaoDetailPageAction())
        actions.append(ThreadSleepAction())
        actions.append(GoodPersistAction())
        return actions

    def get_taobao_detail_actions(self):
        actions = list()
        actions.append(GoodPersistAction())
        return actions

    def get_task_actions(self):
        actions = list()
        actions.append(TaskCollectAction())
        return actions

    def get_sycm_category_job_init_actions(self):
        actions = list()
        actions.append(SycmCategoryJobInitAction())
        return actions

    def execute_direct_good_actions(self, date_str):
        context = Context()
        context.attach(Context.KEY_DIRECT_COLLECT_DATE, date_str)
        context.attach(Context.KEY_CURRENT_TASK_TYPE, TaobaoTaskType.sycm_list)
        action = TaskDirectCollectAction()
        action.execute(context=context)
        tasks = context.get(Context.KEY_CURRENT_TASKS, [])
        for task in tasks:
            raw_data = task.raw_data
            good = Good(raw_data['goodResult'])
            context.attach(Context.KEY_GOOD_DICT, good)
            action = GoodDirectPersistAction()
            action.execute(context=context)

    def execute_sycm_category_job_init_actions(self, date_str=None):
        actions = self.get_sycm_category_job_init_actions()
        context = Context()
        if date_str:
            context.attach(Context.KEY_SYCM_SPECIFIC_DATE, date_str)
        for action in actions:
            action.execute(context=context)

    def execute_sycm_product_actions(self, date_str=None):
        context = self.execute_task_actions(TaobaoTaskType.sycm_init)
        tasks = context.get(Context.KEY_CURRENT_TASKS, [])
        return tasks

    def _execute_legality_token_actions(self, cookies, account):
        context = Context()
        context.attach(Context.KEY_IS_UPDATE_COOKIES, False)
        context.attach(Context.KEY_HEADERS, SpiderHttp.get_sycm_home_htm_headers())
        context.attach(Context.KEY_COOKIES, cookies)
        action = SycmHomeHtmTokenAction()
        action.execute(context=context)
        legality_token = context.get(Context.KEY_SYCM_HOME_HTM_TOKEN_RESULT)
        self._cookie_service.dump(cookies=legality_token, account=account, type_=PickleFileType.legality_token)

    def _relogin(self, account, cate_id, cate_name):
        for i in range(0, 3):
            try:
                cookies, origin_cookies = spider_qt5_bootstrap(url=SpiderUrls.get_sycm_login_url(), account=account)
                self._execute_legality_token_actions(cookies=cookies, account=account)
                self._cookie_service.dump(cookies, account)
                return
            except CookieExpiredException as e:
                logger.warning('relogin cookie is expired,cate_id:%s,cate_name:%s,account:%s', cate_id, cate_name,
                               account['username'])
                if i == 2:
                    raise ExitException('exit when try login util max 3 times retry')
            except Exception as e:
                logger.error('retry error,retry times,%s,%s', i, e)
                if i == 2:
                    raise ExitException('exit when try login util max 3 times retry')
            time.sleep(5)

    def _execute_sycm_product_actions(self, task):
        raw_data = task.raw_data
        account = raw_data['account']
        cate_id = raw_data['cateId']
        cate_name = raw_data['cateName']

        try:
            for i in range(0, 3):
                try:
                    self.__execute_sycm_product_actions(task)
                    return
                except CookieNotFoundException as e:
                    logger.warning('cookie is not exist,cate_id:%s,cate_name:%s,account:%s', cate_id, cate_name,
                                   account['username'])
                    self._relogin(account=account, cate_id=cate_id, cate_name=cate_name)
                    if i == 2:
                        raise e
                except CookieExpiredException as e:
                    logger.warning('cookie is expired,cate_id:%s,cate_name:%s,account:%s', cate_id, cate_name,
                                   account['username'])
                    self._relogin(account=account, cate_id=cate_id, cate_name=cate_name)
                    if i == 2:
                        raise e
                except Exception as e:
                    logger.exception(e)
                    if i == 2:
                        raise e
                time.sleep(5)
        except Exception as e:
            logger.exception(e)
            raise e

    def __execute_sycm_product_actions(self, task):
        raw_data = task.raw_data
        cate_id = raw_data['cateId']
        cate_name = raw_data['cateName']
        account = raw_data['account']
        date_str = raw_data['dateStr']
        context = Context()
        context.attach(Context.KEY_CURRENT_TASK, task)
        context.attach(Context.KEY_IS_UPDATE_COOKIES, False)
        referer = 'https://sycm.taobao.com/mc/mq/product_insight'
        context.attach(Context.KEY_HEADERS, SpiderHttp.get_sycm_headers(referer))
        requests_cookie_jar = self._cookie_service.load(account)

        if not requests_cookie_jar:
            raise CookieNotFoundException('cookie not found')
            # cookies = spider_qt5_bootstrap(url=SpiderUrls.get_sycm_login_url(), account=account)
            # requests_cookie_jar = cookies
            # self._cookie_service.dump(cookies, account)
        context.attach(Context.KEY_COOKIES, requests_cookie_jar)
        context.attach(Context.KEY_IS_UPDATE_COOKIES, False)
        context.attach(Context.KEY_CURRENT_TASK_ACCOUNT, account)
        good = Good()
        good.set_category_id(cate_id)
        good.set_category_name(cate_name)
        good.set_flag(str(int(GoodDataType.initial)))

        # yesterday_date_str = yesterday().strftime("%Y-%m-%d")
        # yesterday_date_str = day_before_yesterday().strftime("%Y-%m-%d")
        yesterday_date_str = date_str
        good.set_date(yesterday_date_str)
        context.attach(Context.KEY_GOOD_DICT, good)

        sycm_brands_url = SpiderUrls.get_sycm_product_get_brands_url(cate_id)
        token = self._cookie_service.load(account=account, type_=PickleFileType.legality_token)
        sycm_prod_hot_rank_url = SpiderUrls.get_sycm_product_prod_hot_rank(start_data=yesterday_date_str,
                                                                           end_date=yesterday_date_str, cate_id=cate_id,
                                                                           token=token)
        sycm_brands_http_request = HttpRequest(url=sycm_brands_url, method=HttpMethod.GET)
        sycm_prod_hot_rank_http_request = HttpRequest(url=sycm_prod_hot_rank_url, method=HttpMethod.GET)
        context.attach(Context.KEY_SYCM_PRODUCT_GET_BRANDS_HTTP_REQUEST, sycm_brands_http_request)
        context.attach(Context.KEY_SYCM_PRODUCT_PROD_HOT_RANK_HTTP_REQUEST, sycm_prod_hot_rank_http_request)

        for action in self.get_sycm_product_actions():
            action.execute(context=context)
        return

    def _execute_taobao_integrate_list_actions(self, task, account, proxy):
        try:
            self.__execute_taobao_integrate_list_actions(task, account, proxy)
        except ProxyException as e:
            logger.exception(e)
            # return proxy
        except CookieExpiredException as e:
            logger.exception(e)
            # raw_data = task.raw_data
            # default_account = global_config.accounts[0]
            # account = raw_data.get('account', default_account)
            return account, True, True
        except InterruptException as e:
            logger.exception(e)
            # raw_data = task.raw_data
            # default_account = global_config.accounts[0]
            # account = raw_data.get('account', default_account)
            return account, True, False
        except Exception as e:
            logger.exception(e)
        return account, False, False

    def _login(self, account, force, risk=False, proxy=None):
        requests_cookie_jar = self._cookie_service.load(account)
        if not requests_cookie_jar or force:
            cookies, origin_cookies = spider_qt5_bootstrap(url=SpiderUrls.get_sycm_login_url(), account=account,
                                                           risk=risk, proxy=proxy)
            self._cookie_service.dump(cookies, account)
            self._cookie_service.dump(cookies=origin_cookies, account=account, type_=PickleFileType.origin_cookie)

    def __execute_taobao_integrate_list_actions(self, task, account, proxy):

        raw_data = task.raw_data
        # default_account = global_config.accounts[0]
        # account = raw_data.get('account', default_account)
        # account = raw_data.get('account', default_account)
        good = Good(raw_data['goodResult'])

        context = Context()
        context.attach(Context.KEY_CURRENT_TASK, task)
        context.attach(Context.KEY_CURRENT_TASK_ACCOUNT, account)
        context.attach(Context.KEY_CURRENT_PROXY, proxy)
        # query = 'Flyco/飞科 + FR5218'
        # query = brand_name + '+' + model_name
        # page = '1'

        requests_cookie_jar = self._cookie_service.load(account)

        if not requests_cookie_jar:
            raise CookieExpiredException('integrate list need first login')

        context.attach(Context.KEY_IS_UPDATE_COOKIES, True)
        referer = 'https://s.m.taobao.com/h5'
        context.attach(Context.KEY_HEADERS, SpiderHttp.get_taobao_headers(referer))
        context.attach(Context.KEY_COOKIES, requests_cookie_jar)
        context.attach(Context.KEY_CURRENT_SLEEP_SECS, 2)
        context.attach(Context.KEY_GOOD_DICT, good)
        actions = self.get_taobao_integrate_list_actions()
        for action in actions:
            try:
                result = action.execute(context=context)
            except CookieNeedUpdateException as e:
                self._cookie_service.dump(requests_cookie_jar, account)
                raise e
            # except CookieExpiredException as e:
            #     raise e
            # except InterruptException as e:
            #     raise e
            if not result:
                break

    def execute_taobao_integrate_list_actions(self):
        context = self.execute_task_actions(type=TaobaoTaskType.sycm_list)
        tasks = context.get(Context.KEY_CURRENT_TASKS, [])
        return tasks

    def execute_task_actions(self, type):
        context = Context()
        context.attach(Context.KEY_CURRENT_TASK_TYPE, type)
        for action in self.get_task_actions():
            action.execute(context)
        return context

    def _execut_taobao_detail_actions(self, task, proxy=None):
        try:
            self.__execut_taobao_detail_actions(task, proxy)
        except ProxyException as e:
            # logger.exception(e)
            return proxy
        except Exception as e:
            logger.exception(e)

    def __execut_taobao_detail_actions(self, task, proxy=None):
        raw_data = task.raw_data
        good_result = Good(raw_data['goodResult'])
        model_name = good_result.get_model_name()
        cate_id = good_result.get_category_id()
        integrate_infos = raw_data['integrateInfos']
        sale_infos = raw_data['saleInfos']
        i = 0
        j = 1
        length = min(len(integrate_infos), len(sale_infos))
        is_success = False

        context = Context()
        context.attach(Context.KEY_GOOD_DICT, good_result)
        context.attach(Context.KEY_CURRENT_TASK, task)
        context.attach(Context.KEY_CURRENT_PROXY, proxy)

        for x in range(0, length):
            is_need_retry = False
            if i < len(sale_infos):
                sale_info = sale_infos[i]
                sale_item_id = sale_info['itemId']
                sale_title = sale_info['title']
                sale_cate_id = sale_info['category']
                sale_price = sale_info['price']
                # str(sale_title).upper()
                # if str(sale_title).upper().find(str(model_name).upper()) != -1 and str(cate_id) == str(sale_cate_id):
                if str(sale_title).upper().find(str(model_name).upper()) != -1 and Category.check_cate_id(cate_id,
                                                                                                          sale_cate_id):
                    actions = self.get_taobao_detail_actions()
                    is_success = True
                    price_info = [{
                        'skuId': '-1',
                        'price': yuan_2_cent(sale_price)
                    }]
                    good_result.set_price_info(price_info=price_info)
                    good_result.set_flag(str(int(GoodDataType.success)))
                    for action in actions:
                        action.execute(context=context)
                    break
                elif i < 5:
                    actions = self.get_taobao_http_detail_actions()
                    timestamps = int(datetime.now().timestamp() * 1000)
                    # sign = get_sign('414804c1e894540b7f18f703c74346cf', str(timestamps), '12574478',
                    #                 '{"itemNumId":"%s"' % (sale_item_id))
                    sale_detail_url = SpiderUrls.get_taobao_detail_url(timestamps, '', sale_item_id)
                    context = Context()
                    context.attach(Context.KEY_GOOD_DICT, good_result)
                    context.attach(Context.KEY_CURRENT_TASK, task)
                    context.attach(Context.KEY_COOKIES, RequestsCookieJar())
                    context.attach(Context.KEY_IS_UPDATE_COOKIES, True)
                    context.attach(Context.KEY_CURRENT_PROXY, proxy)

                    detail_m_url = SpiderUrls.get_detail_m_url(sale_info['userType'], sale_item_id)
                    detail_m_http_request = HttpRequest(detail_m_url, method=HttpMethod.GET)
                    context.attach(Context.KEY_DETAIL_M_HTTP_REQUEST, detail_m_http_request)

                    sale_http_request = HttpRequest(url=sale_detail_url, method=HttpMethod.GET)
                    context.attach(Context.KEY_TAOBAO_DETAIL_HTTP_REQUEST, sale_http_request)
                    context.attach(Context.KEY_HEADERS, SpiderHttp.get_taobao_headers(detail_m_url))
                    try:
                        for action in actions:
                            action.execute(context=context)
                        is_success = True
                        break
                    except RetryException as e:
                        logger.error(e)
                        time.sleep(5)
                    except InterruptException as e:
                        logger.exception(e)
                        time.sleep(10)
                        is_need_retry = True
                        # raise e
                # if is_success:
                #     break
            if j < len(integrate_infos):
                integrate_info = integrate_infos[j]
                integrate_item_id = integrate_info['itemId']
                integrate_title = integrate_info['title']
                integrate_cate_id = integrate_info['category']
                integrate_price = integrate_info['price']
                # if str(integrate_title).upper().find(
                #         str(model_name).upper()) != -1 and str(cate_id) == str(integrate_cate_id):
                if str(integrate_title).upper().find(
                        str(model_name).upper()) != -1 and Category.check_cate_id(cate_id, integrate_cate_id):
                    actions = self.get_taobao_detail_actions()
                    is_success = True
                    price_info = [{
                        'skuId': '-2',
                        'price': yuan_2_cent(integrate_price)
                    }]
                    good_result.set_price_info(price_info=price_info)
                    good_result.set_flag(str(int(GoodDataType.success)))
                    for action in actions:
                        action.execute(context=context)
                    break
                elif j < 6:
                    actions = self.get_taobao_http_detail_actions()
                    timestamps = int(datetime.now().timestamp() * 1000)
                    integrate_detail_url = SpiderUrls.get_taobao_detail_url(timestamps, '', integrate_item_id)
                    context = Context()
                    # referer = 'https://s.m.taobao.com/h5'
                    # context.attach(Context.KEY_HEADERS, SpiderHttp.get_taobao_headers(referer))
                    context.attach(Context.KEY_GOOD_DICT, good_result)
                    context.attach(Context.KEY_CURRENT_TASK, task)
                    context.attach(Context.KEY_COOKIES, RequestsCookieJar())
                    context.attach(Context.KEY_IS_UPDATE_COOKIES, True)
                    context.attach(Context.KEY_CURRENT_PROXY, proxy)

                    detail_m_url = SpiderUrls.get_detail_m_url(integrate_info['userType'], integrate_item_id)
                    detail_m_http_request = HttpRequest(detail_m_url, method=HttpMethod.GET)
                    context.attach(Context.KEY_DETAIL_M_HTTP_REQUEST, detail_m_http_request)

                    integrate_http_request = HttpRequest(url=integrate_detail_url, method=HttpMethod.GET)
                    context.attach(Context.KEY_TAOBAO_DETAIL_HTTP_REQUEST, integrate_http_request)

                    context.attach(Context.KEY_HEADERS, SpiderHttp.get_taobao_headers(detail_m_url))
                    try:
                        for action in actions:
                            action.execute(context=context)
                        is_success = True
                        break
                    except RetryException as e:
                        logger.exception(e)
                        time.sleep(5)
                    except InterruptException as e:
                        logger.exception(e)
                        time.sleep(10)
                        is_need_retry = True
                        # raise e
            if not is_need_retry:
                i += 1
                j += 1
        if not is_success:
            actions = self.get_taobao_detail_actions()
            good_result.set_flag(str(int(GoodDataType.not_found)))
            for action in actions:
                action.execute(context=context)

    def execut_taobao_detail_actions(self):
        context = self.execute_task_actions(type=TaobaoTaskType.taobao_list)
        tasks = context.get(Context.KEY_CURRENT_TASKS, [])
        return tasks


def get_action_service():
    global __action_service
    if not __action_service:
        __action_service = ActionService()
    return __action_service
