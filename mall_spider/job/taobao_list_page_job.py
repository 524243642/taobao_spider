# -*- coding: utf-8 -*-
import time
from concurrent.futures import as_completed

from common.db import read_session_scope, write_session_scope
from config.config_loader import logger, global_config
from mall_spider.common.enums import RiskType, PickleFileType
from mall_spider.dao.stream_risk_dao import get_stream_risk_dao
from mall_spider.job.smorf import Smorf
from mall_spider.model.cmm_sys_stream_risk import CmmSysStreamRisk
from mall_spider.spiders.actions.action_service import ActionService
from mall_spider.spiders.actions.cookie_service import get_cookie_service
from mall_spider.spiders.actions.executor_service import ExecutorService
from mall_spider.spiders.actions.proxy_service import get_proxy_service
from mall_spider.spiders.spider_qt5 import spider_qt5_bootstrap


class TaobaoListPageJob(ActionService, Smorf):

    def __init__(self, pool_size):
        super().__init__()
        self._counter = 0
        self._executor = ExecutorService(pool_size)
        self._proxy_service = get_proxy_service()
        self._cookie_service = get_cookie_service()
        s_accounts = global_config.s_accounts
        self._account_counter = dict()
        for item in s_accounts:
            self._account_counter[item['username']] = 0
        self._fail_account_counter = dict()
        for item in s_accounts:
            self._fail_account_counter[item['username']] = 0

    def execute(self, num):

        cycle_login_num = 0
        tasks = self.execute_taobao_integrate_list_actions()
        i = 0
        future_tasks = {}
        with read_session_scope() as session:
            _stream_risk_dao = get_stream_risk_dao(session=session)
            rsts = _stream_risk_dao.base_query.all()
            risk_usernames = set(item.raw_data for item in rsts)
        s_accounts = global_config.s_accounts
        for task in tasks:
            account = s_accounts[self._counter % len(s_accounts)]
            proxy = self._proxy_service.get_static_proxy(account['username'])
            # raw_data = task.raw_data
            # account = raw_data['account']
            self._counter += 1
            i += 1
            if account['username'] in risk_usernames:
                continue
            if i < num:
                future_tasks[
                    self._executor.submit(self._execute_taobao_integrate_list_actions, task, account, proxy)] = task

        for future in as_completed(future_tasks):
            try:
                account, flag, force = future.result()
                if flag:
                    if force:
                        with write_session_scope() as session:
                            _stream_risk_dao = get_stream_risk_dao(session=session)
                            self._risk(stream_risk_dao=_stream_risk_dao, account=account)
                        # self._login(account=account, force=True if cycle_login_num == 0 else False)
                        cycle_login_num += 1
                    else:
                        self._fail_account_counter[account['username']] += 1
                        if self._fail_account_counter[account['username']] > 2:
                            self._cookie_service.remove(account=account)
                            with write_session_scope() as session:
                                _stream_risk_dao = get_stream_risk_dao(session=session)
                                self._risk(stream_risk_dao=_stream_risk_dao, account=account)
                            # self._login(account=account, force=True if cycle_login_num == 0 else False)
                            cycle_login_num += 1
                        else:
                            url = 'https://s.m.taobao.com/h5?q=Flyco%2BFR5218&search=%E6%8F%90%E4%BA%A4&tab=all'
                            # url = 'https://s.m.taobao.com/h5?q=Flyco%2BFR5218&search=%E6%8F%90%E4%BA%A4&tab=all'
                            proxy = self._proxy_service.get_origin_static_proxy(account['username'])
                            cookies = self._cookie_service.load(account=account, type_=PickleFileType.origin_cookie)
                            time.sleep(5)
                            cookies, origin_cookies = spider_qt5_bootstrap(url=url, account=account, risk=False,
                                                                           proxy=proxy, cookies=cookies)
                            self._cookie_service.dump(cookies=cookies, account=account)
                            self._cookie_service.dump(cookies=origin_cookies, account=account,
                                                      type_=PickleFileType.origin_cookie)
                    self._account_counter[account['username']] = 0
                else:
                    self._fail_account_counter[account['username']] = 0
                    self._account_counter[account['username']] += 1
                    if self._account_counter[account['username']] >= 2:
                        url = 'https://s.m.taobao.com/h5?q=Flyco%2BFR5218&search=%E6%8F%90%E4%BA%A4&tab=all'
                        # url = 'https://s.m.taobao.com/h5?q=Flyco%2BFR5218&search=%E6%8F%90%E4%BA%A4&tab=all'
                        proxy = self._proxy_service.get_origin_static_proxy(account['username'])
                        cookies = self._cookie_service.load(account=account, type_=PickleFileType.origin_cookie)
                        time.sleep(5)
                        cookies, origin_cookies = spider_qt5_bootstrap(url=url, account=account, risk=False,
                                                                       proxy=proxy, cookies=cookies)
                        self._cookie_service.dump(cookies=cookies, account=account)
                        self._cookie_service.dump(cookies=origin_cookies, account=account,
                                                  type_=PickleFileType.origin_cookie)
                        self._account_counter[account['username']] = 0

            except Exception as e:
                logger.error(e)

    def _risk(self, stream_risk_dao, account):
        entity = stream_risk_dao.query_one(_filter=[CmmSysStreamRisk.type == int(RiskType.taobao_search),
                                                    CmmSysStreamRisk.raw_data == account['username']])
        if not entity:
            entity = CmmSysStreamRisk()
            entity.raw_data = account['username']
            entity.type = int(RiskType.taobao_search)
            stream_risk_dao.insert_entity(entity=entity)

    def init(self):
        super().init()

    def init_argparse(self, parser):
        super().init_argparse(parser)

    def process(self):
        # return super().process()
        self.execute(2)
        time.sleep(10)


if __name__ == "__main__":
    s = TaobaoListPageJob(10)
    logger.info("start to execute taobao_list_page job")
    s.run()
    # s.process()
    logger.error("exit taobao_list_page job")
