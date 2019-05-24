# coding: utf-8
import time
import traceback
from abc import ABCMeta, abstractmethod

from requests.cookies import RequestsCookieJar
from requests.exceptions import ReadTimeout, ConnectTimeout, ProxyError
from urllib3.exceptions import ConnectTimeoutError

from config.config_loader import logger
from mall_spider.common.enums import HttpMethod
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.default_action import DefaultAction
from mall_spider.spiders.actions.exception import StatusCodeException, ProxyException
from mall_spider.utils import default_retry, default_retry_interval, default_connect_timeout
from mall_spider.utils.requests_client import post, get


class HttpAction(DefaultAction):
    __metaclass__ = ABCMeta

    @abstractmethod
    def unmarshal(self, context, response):
        pass

    def execute_in_retry(self, context, http_request, data=None):
        method = http_request.method
        is_update_cookies = context.get(Context.KEY_IS_UPDATE_COOKIES, False)
        headers = context.get(Context.KEY_HEADERS, '')
        cookies = context.get(Context.KEY_COOKIES, RequestsCookieJar())
        start_time = time.time()
        retry = int(default_retry)
        retry_interval = float(default_retry_interval)
        timeout = 25.0
        connect_time_out = int(default_connect_timeout)

        proxies = context.get(Context.KEY_CURRENT_PROXY, '')
        account = context.get(Context.KEY_CURRENT_TASK_ACCOUNT, {})
        while retry > 0:
            retry = retry - 1
            response = None
            try:
                if proxies:
                    logger.info('context key:[%s],proxy inject,[%s]->[%s]', context.context_key, account, proxies)
                if method == HttpMethod.GET:
                    response = get(url=http_request.url, params=None, headers=headers, cookies=cookies, proxies=proxies)
                elif method == HttpMethod.POST:
                    response = post(url=http_request.url, data=data, headers=headers, cookies=cookies, proxies=proxies,
                                    connect_timeout=connect_time_out, timeout=timeout)
                logger.debug(u'context key:[%s],action:[%s] execute result:%s',
                             context.context_key, self.__class__.__name__, response.text)
                if response.status_code != 200:
                    raise StatusCodeException(response.status_code)
                return response
            except ProxyError as e:
                logger.error('proxy error,[%s]->[%s],exp:%s', account, proxies, e)
                raise ProxyException(e)
            except ConnectTimeoutError as e:
                logger.error('proxy error,[%s]->[%s],exp:%s', account, proxies, e)
                raise ProxyException(e)
            except ReadTimeout as e:
                import sys
                exc_info = sys.exc_info()
                if time.time() - start_time > timeout or retry == 0:
                    raise e
                    # raise exc_info[0], exc_info[1], exc_info[2]
                logger.error(u'context key:[%s],action:[%s] execute read time out,exception:%s',
                             context.context_key, self.__class__.__name__, traceback.format_exc())
            except ConnectTimeout as e:
                import sys
                exc_info = sys.exc_info()
                if time.time() - start_time > timeout or retry == 0:
                    raise e
                    # raise exc_info[0], exc_info[1], exc_info[2]
                logger.error(u'context key:[%s],action:[%s] execute connect time out,exception:%s',
                             context.context_key, self.__class__.__name__, traceback.format_exc())
            except Exception as e:
                import sys
                exc_info = sys.exc_info()
                if time.time() - start_time > timeout or retry == 0:
                    raise e
                    # raise exc_info[0], exc_info[1], exc_info[2]
                logger.error(u'context key:[%s],action:[%s] execute error,exception:%s',
                             context.context_key, self.__class__.__name__, traceback.format_exc())
            finally:
                if is_update_cookies and response:
                    cookies.update(response.cookies)

            time.sleep(retry_interval)
