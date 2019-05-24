# -*- coding: utf-8 -*-
from unittest import TestCase

from common.db import write_session_scope
from common.retry import retry
from mall_spider.common.constants import Category
from mall_spider.common.enums import TaobaoTaskType
from mall_spider.dao.stream_unhandle_task_dao import get_stream_unhandle_task_dao
from mall_spider.model.cmm_sys_stream_unhandle_task import CmmSysStreamUnhandleTask
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.pojo import Good
from mall_spider.spiders.actions.task_collect_action import TaskCollectAction


class TestUtil(TestCase):

    @retry
    def _retry(self):
        print('retry')
        raise Exception()

    def test_retry(self):
        self._retry()

    def test_category(self):
        rst = Category.check_cate_id(50015558, 50015560)
        self.assertEqual(True, rst)

    def test_get_tasks(self):
        """
        get main category id that have sub category id
        :return:
        """
        accounts_category_ids_dict = Category.accounts_category_ids_dict
        for key, value in accounts_category_ids_dict.items():
            if value:
                print(key)

    def test_init_unhandle_tasks(self):
        context = Context()
        context.attach(Context.KEY_CURRENT_TASK_TYPE, TaobaoTaskType.sycm_init)
        action = TaskCollectAction()
        action.execute(context=context)
        tasks = context.get(Context.KEY_CURRENT_TASKS, [])
        for task in tasks:
            id_ = task.id
            raw_data = task.raw_data
            date = raw_data['dateStr']
            with write_session_scope() as session:
                stream_unhandle_task_dao = get_stream_unhandle_task_dao(session=session)
                mod_dict = {
                    'date': date
                }
                stream_unhandle_task_dao.update(mod_dict=mod_dict, _filter=[CmmSysStreamUnhandleTask.id == id_])

        context = Context()
        context.attach(Context.KEY_CURRENT_TASK_TYPE, TaobaoTaskType.sycm_list)
        action = TaskCollectAction()
        action.execute(context=context)
        tasks = context.get(Context.KEY_CURRENT_TASKS, [])
        for task in tasks:
            id_ = task.id
            raw_data = task.raw_data
            good = Good(raw_data['goodResult'])
            date = good.get_date()
            with write_session_scope() as session:
                stream_unhandle_task_dao = get_stream_unhandle_task_dao(session=session)
                mod_dict = {
                    'date': date
                }
                stream_unhandle_task_dao.update(mod_dict=mod_dict, _filter=[CmmSysStreamUnhandleTask.id == id_])

        context = Context()
        context.attach(Context.KEY_CURRENT_TASK_TYPE, TaobaoTaskType.taobao_list)
        action = TaskCollectAction()
        action.execute(context=context)
        tasks = context.get(Context.KEY_CURRENT_TASKS, [])
        for task in tasks:
            id_ = task.id
            raw_data = task.raw_data
            good = Good(raw_data['goodResult'])
            date = good.get_date()
            with write_session_scope() as session:
                stream_unhandle_task_dao = get_stream_unhandle_task_dao(session=session)
                mod_dict = {
                    'date': date
                }
                stream_unhandle_task_dao.update(mod_dict=mod_dict, _filter=[CmmSysStreamUnhandleTask.id == id_])
