# coding: utf-8
from common.db import write_session_scope
from mall_spider.common.constants import Category
from mall_spider.common.enums import TaobaoTaskType
from mall_spider.dao.stream_unhandle_task_dao import get_stream_unhandle_task_dao
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.default_action import DefaultAction
from mall_spider.utils.date_util import yesterday


class SycmCategoryJobInitAction(DefaultAction):

    def do_execute(self, context):
        date_str = yesterday().strftime("%Y-%m-%d")
        date_str = context.get(Context.KEY_SYCM_SPECIFIC_DATE, date_str)

        tasks = Category.get_tasks(date_str, Category.sys_category)
        entities = list()

        for task in tasks:
            entities.append({
                'type': int(TaobaoTaskType.sycm_init),
                'raw_data': task,
                'date': date_str
            })
        if entities:
            with write_session_scope() as session:
                stream_unhandle_task_dao = get_stream_unhandle_task_dao(session=session)
                stream_unhandle_task_dao.bulk_insert(entities)
        return True

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
