#!/usr/bin/env python
# encoding: utf-8
# coding: utf-8
from sqlalchemy import Integer, DateTime, Column, func


class MySQLMixedIn(object):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }


class VersionMixedIn(MySQLMixedIn):
    version = Column(Integer, default=1)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())

    __mapper_args__ = {
        "version_id_col": version
    }
