# coding: utf-8
from sqlalchemy import BigInteger, Column, String, Integer
from sqlalchemy.schema import FetchedValue

from common.column import JSONEncodedLongColumn
from mall_spider import model
from mall_spider.model.base import VersionMixedIn


class CmmSysStreamGoodData(model.Base, VersionMixedIn):
    __tablename__ = 'cmm_sys_stream_good_data'

    id = Column(BigInteger, primary_key=True)
    # type = Column(Integer, nullable=False, server_default=FetchedValue())
    raw_data = Column(JSONEncodedLongColumn, nullable=False, server_default=FetchedValue())
    create_by = Column(BigInteger, nullable=False, server_default=FetchedValue())
    update_by = Column(BigInteger, nullable=False, server_default=FetchedValue())

    flag = Column(Integer, nullable=False, server_default=FetchedValue())
    category_name = Column(String(50), nullable=False, server_default=FetchedValue())
    brand_name = Column(String(50), nullable=False, server_default=FetchedValue())
    category_id = Column(String(20), nullable=False, server_default=FetchedValue())
    date = Column(String(10), nullable=False, server_default=FetchedValue())
    model_name = Column(String(50), nullable=False, server_default=FetchedValue())

    # content = Column(String(3000), nullable=False, server_default=FetchedValue())
