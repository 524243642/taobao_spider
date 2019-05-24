# coding:utf-8
"""
所有来自于client的接口都支持如下的配置参数，所列为默认值:
    connect_timeout=1, "connect_timeout" # float. 单次连接超时，单位秒
    timeout=2, "timeout" # float. 读写超时/最大重连超时，单位秒
    retry=2, "retry"          # int. 重试次数
    retry_interval=0.1 "retry_interval" # float. 重连间隔的秒数

如果调用的时候，需要临时指定，可以在发送的kwargs中，直接说明
"""

import warnings

import requests
from urllib3.exceptions import InsecureRequestWarning

from mall_spider.utils import default_connect_timeout, default_timeout


class XSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.verify = False


# Requests 似乎不能使用系统的证书系统, 方便起见, 不验证 HTTPS 证书, 便于使用代理工具进行网络调试...
# http://docs.python-requests.org/en/master/user/advanced/#ca-certificates
requests.Session = XSession
warnings.simplefilter('ignore', InsecureRequestWarning)


def get(url, params=None, headers=None, cookies=None, proxies=None, **kwargs):
    session = requests.Session()
    if headers:
        session.headers.update(headers)
    if cookies:
        session.cookies = cookies
    if proxies:
        session.proxies = proxies
    return execute(session.get, url, params=params, **kwargs)


def post(url, data=None, json=None, headers=None, cookies=None, proxies=None, **kwargs):
    session = requests.Session()
    if headers:
        session.headers.update(headers)
    if cookies:
        session.cookies = cookies
    if proxies:
        session.proxies = proxies
    return execute(session.post, url, data=data, json=json, **kwargs)


def execute(request, url, **kwargs):
    connect_timeout = float(kwargs.pop('connect_timeout', default_connect_timeout))
    timeout = float(kwargs.pop('timeout', default_timeout))

    return request(url, timeout=(connect_timeout, timeout), **kwargs)

    # timeout = float(kwargs.pop('timeout', default_timeout))
    # retry = int(kwargs.pop('retry', default_retry))
    # retry_interval = float(kwargs.pop('retry_interval', default_retry_interval))
    # start_time = time.time()
    # response = None
    #
    # while retry > 0:
    #     try:
    #         response = request(url, *args, timeout=connect_timeout, **kwargs)
    #     except ReadTimeout as e:
    #         logging.error(u'request url %s read time out,exp:%s' % (url, e))
    #     except RequestException as e:
    #         logging.error(u'request url %s execute time out' % url)
    #
    # while retry > 0:
    #     try:
    #         response = request(url, *args, timeout=connect_timeout, **kwargs)
    #     except RequestException as e:
    #         logging.info("Failed to get %s, exception: %s", url, e.message)
    #     if time.time() - start_time > timeout or response is not None:
    #         break
    #     retry -= 1
    #     time.sleep(retry_interval)
    # if response is None:
    #     raise RequestException("Failed to request %s, request_body: %r" % (url, args))
    # return response
