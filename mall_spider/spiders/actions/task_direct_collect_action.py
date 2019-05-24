# coding: utf-8
from common.db import write_session_scope
from mall_spider.dao.stream_unhandle_task_dao import get_stream_unhandle_task_dao
from mall_spider.model.cmm_sys_stream_unhandle_task import CmmSysStreamUnhandleTask
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.default_action import DefaultAction


class TaskDirectCollectAction(DefaultAction):

    def do_execute(self, context):
        task_type = int(context.get(Context.KEY_CURRENT_TASK_TYPE))
        date_str = context.get(Context.KEY_DIRECT_COLLECT_DATE)

        with write_session_scope() as session:
            # stream_opt_data_dao = get_stream_opt_data_dao(session=session)
            stream_unhandle_task_dao = get_stream_unhandle_task_dao(session=session)

            tasks = stream_unhandle_task_dao.query(entities=[CmmSysStreamUnhandleTask.id, CmmSysStreamUnhandleTask.type,
                                                             CmmSysStreamUnhandleTask.raw_data,
                                                             CmmSysStreamUnhandleTask.origin_id],
                                                   _filter=[CmmSysStreamUnhandleTask.type == task_type,
                                                            CmmSysStreamUnhandleTask.date == date_str])

            context.attach(Context.KEY_CURRENT_TASKS, tasks)
        return True

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
