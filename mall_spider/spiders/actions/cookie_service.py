# coding: utf-8
import pickle
from pathlib import Path

from config.config_loader import logger
from mall_spider.common.enums import PickleFileType
from mall_spider.utils.fnvhash import fnv1a_32

__cookie_service = None


class CookieService(object):
    COOKIE_PREFIX = 'cookies'
    ORIGIN_COOKIE_PREFIX = 'origin_cookies'
    LEGALITY_TOKEN_PREFIX = 'legality_token'

    cookies_dict = {}

    def gen_by_account(self, account, type_):
        if type_ == PickleFileType.cookie:
            return '_'.join([self.COOKIE_PREFIX, str(fnv1a_32(bytes(account, 'utf-8')))])
        elif type_ == PickleFileType.origin_cookie:
            return '_'.join([self.ORIGIN_COOKIE_PREFIX, str(fnv1a_32(bytes(account, 'utf-8')))])
        else:
            return '_'.join([self.LEGALITY_TOKEN_PREFIX, str(fnv1a_32(bytes(account, 'utf-8')))])

    def dump(self, cookies, account, path=None, type_=PickleFileType.cookie):
        if not path:
            path = '../../data/'
        account = account['username']
        data = pickle.dumps(cookies)
        data_dir = Path(__file__).parent.joinpath(path)
        data_dir.mkdir(exist_ok=True)
        key = self.gen_by_account(account=account, type_=type_)
        data_file = data_dir.joinpath(key)
        data_file.write_bytes(data)
        logger.info('dump data success,account:[%s],type:[%s]', account, type_)
        # if type_ == PickleFileType.cookie:
        #     self.cookies_dict[key] = cookies

    def remove(self, account):
        account = account['username']
        key = self.gen_by_account(account=account, type_=PickleFileType.cookie)
        self.cookies_dict.pop(key, None)

    def load(self, account, path=None, type_=PickleFileType.cookie):
        if not path:
            path = '../../data/'
        account = account['username']
        key = self.gen_by_account(account=account, type_=type_)

        if type_ == PickleFileType.cookie:
            # cookies = self.cookies_dict.get(key, None)
            # if cookies:
            #     logger.info('load mem cookies success,account:[%s]', account)
            #     return cookies

            data_file = Path(__file__).parent.joinpath(path + self.gen_by_account(account=account, type_=type_))
            if not data_file.exists():
                return None
            try:
                bytes = data_file.read_bytes()
                cookies = pickle.loads(bytes)
                logger.info('load cookies success,account:[%s]', account)
                self.cookies_dict[key] = cookies
                return cookies
            except Exception as e:
                logger.error('load cookies error,account:[%s],exp:%s', account, e)
                raise e
        elif type_ == PickleFileType.origin_cookie:
            data_file = Path(__file__).parent.joinpath(path + self.gen_by_account(account=account, type_=type_))
            if not data_file.exists():
                return None
            try:
                bytes = data_file.read_bytes()
                cookies = pickle.loads(bytes)
                logger.info('load origin cookies success,account:[%s]', account)
                return cookies
            except Exception as e:
                logger.error('load lorigin cookies error,account:[%s],exp:%s', account, e)
                raise e
        else:
            data_file = Path(__file__).parent.joinpath(path + self.gen_by_account(account=account, type_=type_))
            if not data_file.exists():
                return None
            try:
                bytes = data_file.read_bytes()
                legality_token = pickle.loads(bytes)
                logger.info('load legality_token success,account:[%s]', account)
                return legality_token
            except Exception as e:
                logger.error('load legality_token error,account:[%s],exp:%s', account, e)
                return ''


def get_cookie_service():
    global __cookie_service
    if not __cookie_service:
        __cookie_service = CookieService()
    return __cookie_service
