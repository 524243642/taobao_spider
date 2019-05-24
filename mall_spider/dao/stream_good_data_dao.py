# coding: utf-8
from mall_spider.dao.abstract_dao import AbstractDao
from mall_spider.model.cmm_sys_stream_good_data import CmmSysStreamGoodData


class StreamGoodDataDao(AbstractDao):
    def __init__(self, session):
        super(StreamGoodDataDao, self).__init__(CmmSysStreamGoodData, session)


def get_stream_good_data_dao(session):
    return StreamGoodDataDao(session=session)
