# coding: utf-8
from sqlalchemy import BigInteger, Column
from sqlalchemy.schema import FetchedValue

from common.column import JSONEncodedColumn
from mall_spider import model
from mall_spider.model.base import VersionMixedIn


class CmmSysCommodity(model.Base, VersionMixedIn):
    __tablename__ = 'cmm_sys_commodity'

    id = Column(BigInteger, primary_key=True)
    # content = Column(String(3000), nullable=False, server_default=FetchedValue())
    content = Column(JSONEncodedColumn, nullable=False, server_default=FetchedValue())
