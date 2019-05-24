# coding: utf-8
import time

from config.config_loader import global_config
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.direct_proxy_action import DirectProxyAction

__proxy_service = None


class ProxyService(object):
    proxies_set = set()
    proxies_list = ['https://' + item['ip'] + ':' + item['port'] for item in global_config.s_proxy]

    LOW_WATER_MARK = 5

    proxy_fetch_url = "http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=json&ss=5&css=&dt=1&specialTxt=3&specialJson="

    def __init__(self) -> None:
        super().__init__()
        self._counter = 0

    def get_s_proxy(self, username):
        proxy = global_config.s_proxy_dict[username]
        url = 'https://' + proxy['ip'] + ':' + proxy['port']
        return {
            'https': url
        }

    def get_origin_s_proxy(self, username):
        return global_config.s_proxy_dict[username]

    def get_static_proxy(self, username):
        if not global_config.static_proxy:
            return None
        proxy = global_config.static_proxy_dict[username]
        if proxy['username'] and proxy['password']:
            url = 'https://' + proxy['username'] + ':' + proxy['password'] + '@' + proxy['ip'] + ':' + proxy['port']
        else:
            url = 'https://' + proxy['ip'] + ':' + proxy['port']
        return {
            'https': url
        }

    def get_origin_static_proxy(self, username):
        if not global_config.static_proxy:
            return None
        return global_config.static_proxy_dict[username]

    def get_proxy(self):
        if len(self.proxies_list) < self.LOW_WATER_MARK:
            for i in range(0, int(self.LOW_WATER_MARK * 1) - len(self.proxies_list)):
                self.fetch_proxy()
                time.sleep(2)
        proxy = self.proxies_list[self._counter % len(self.proxies_list)]
        self._counter += 1
        return {
            'https': proxy
        }

    def fetch_proxy(self):
        context = Context()
        action = DirectProxyAction()
        action.execute(context=context)
        result = context.get(Context.KEY_PROXY_RESULT, [])
        if result:
            for item in result:
                ip = item['IP']
                port = str(item['Port'])
                url = 'https://' + ip + ':' + port
                if url not in self.proxies_set:
                    self.proxies_set.add(url)
                    self.proxies_list.append(url)

    def remove_proxy(self, url, force=False):
        if force:
            self.proxies_set.remove(url)
            self.proxies_list.remove(url)


def get_proxy_service():
    global __proxy_service
    if not __proxy_service:
        __proxy_service = ProxyService()
    return __proxy_service
