# -*- coding: utf-8 -*-
from common.db import write_session_scope
from config.config_loader import logger, global_config
from mall_spider.dao.stream_risk_dao import get_stream_risk_dao
from mall_spider.job.smorf import Smorf
from mall_spider.model.cmm_sys_stream_risk import CmmSysStreamRisk
from mall_spider.spiders.actions.action_service import ActionService
from mall_spider.spiders.actions.proxy_service import get_proxy_service


class LoginJob(ActionService, Smorf):
    def __init__(self, num):
        super().__init__()
        self.account_num = num
        self._proxy_service = get_proxy_service()

    def execute(self):
        with write_session_scope() as session:
            _stream_risk_dao = get_stream_risk_dao(session=session)
            rsts = _stream_risk_dao.base_query.limit(self.account_num).all()
            if rsts:
                for item in rsts:
                    username = item.raw_data
                    account = global_config.s_accounts_dict[username]
                    proxy = self._proxy_service.get_origin_static_proxy(account['username'])
                    self._login(account=account, force=True, risk=True, proxy=proxy)
                    _stream_risk_dao.delete(_filter=[CmmSysStreamRisk.id == item.id])
                    session.commit()

    def init(self):
        super().init()

    def init_argparse(self, parser):
        super().init_argparse(parser)

    def process(self):
        self.execute()


if __name__ == "__main__":
    s = LoginJob(1)
    logger.info("start to execute login job")
    s.process()
    logger.error("exit login job")
