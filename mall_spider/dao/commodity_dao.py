# coding: utf-8
from mall_spider.dao.abstract_dao import AbstractDao
from mall_spider.model.cmm_sys_commodity import CmmSysCommodity


class CommodityDao(AbstractDao):
    def __init__(self, session):
        super(CommodityDao, self).__init__(CmmSysCommodity, session)


def get_commodity_dao(session):
    return CommodityDao(session=session)
