# coding: utf-8
from mall_spider.dao.abstract_dao import AbstractDao
from mall_spider.model.cmm_sys_stream_unhandle_task import CmmSysStreamUnhandleTask


class StreamUnhandleTaskDao(AbstractDao):
    def __init__(self, session):
        super(StreamUnhandleTaskDao, self).__init__(CmmSysStreamUnhandleTask, session)


def get_stream_unhandle_task_dao(session):
    return StreamUnhandleTaskDao(session=session)
