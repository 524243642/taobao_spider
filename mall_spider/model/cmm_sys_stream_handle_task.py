# coding: utf-8
from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.schema import FetchedValue

from common.column import JSONEncodedLongColumn
from mall_spider import model
from mall_spider.model.base import VersionMixedIn


class CmmSysStreamHandleTask(model.Base, VersionMixedIn):
    __tablename__ = 'cmm_sys_stream_handle_task'

    id = Column(BigInteger, primary_key=True)
    type = Column(Integer, nullable=False, server_default=FetchedValue())
    raw_data = Column(JSONEncodedLongColumn, nullable=False, server_default=FetchedValue())
    create_by = Column(BigInteger, nullable=False, server_default=FetchedValue())
    update_by = Column(BigInteger, nullable=False, server_default=FetchedValue())
    # content = Column(String(3000), nullable=False, server_default=FetchedValue())
    origin_id = Column(BigInteger, nullable=False, server_default=FetchedValue())
    date = Column(String(10), nullable=False, server_default=FetchedValue())
