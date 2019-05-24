# coding: utf-8
from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.schema import FetchedValue

from mall_spider import model
from mall_spider.model.base import VersionMixedIn


class CmmSysStreamRisk(model.Base, VersionMixedIn):
    __tablename__ = 'cmm_sys_stream_risk'

    id = Column(BigInteger, primary_key=True)
    raw_data = Column(String(50), nullable=False, server_default=FetchedValue())
    type = Column(Integer, nullable=False, server_default=FetchedValue())
