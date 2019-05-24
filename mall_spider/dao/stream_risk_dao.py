# coding: utf-8
from mall_spider.dao.abstract_dao import AbstractDao
from mall_spider.model.cmm_sys_stream_risk import CmmSysStreamRisk


class StreamRiskDao(AbstractDao):
    def __init__(self, session):
        super(StreamRiskDao, self).__init__(CmmSysStreamRisk, session)


def get_stream_risk_dao(session):
    return StreamRiskDao(session=session)
