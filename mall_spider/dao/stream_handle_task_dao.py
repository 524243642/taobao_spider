# coding: utf-8
from mall_spider.dao.abstract_dao import AbstractDao
from mall_spider.model.cmm_sys_stream_handle_task import CmmSysStreamHandleTask


class StreamHandleTaskDao(AbstractDao):
    def __init__(self, session):
        super(StreamHandleTaskDao, self).__init__(CmmSysStreamHandleTask, session)


def get_stream_handle_task_dao(session):
    return StreamHandleTaskDao(session=session)
