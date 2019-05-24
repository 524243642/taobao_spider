# coding: utf-8
from mall_spider.dao.abstract_dao import AbstractDao
from mall_spider.model.cmm_sys_stream_opt_data import CmmSysStreamOptData


class StreamOptDataDao(AbstractDao):
    def __init__(self, session):
        super(StreamOptDataDao, self).__init__(CmmSysStreamOptData, session)


def get_stream_opt_data_dao(session):
    return StreamOptDataDao(session=session)
