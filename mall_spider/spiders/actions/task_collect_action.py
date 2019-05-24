# coding: utf-8
from common.db import write_session_scope
from mall_spider.dao.stream_unhandle_task_dao import get_stream_unhandle_task_dao
from mall_spider.model.cmm_sys_stream_unhandle_task import CmmSysStreamUnhandleTask
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.default_action import DefaultAction


class TaskCollectAction(DefaultAction):

    def do_execute(self, context):
        task_type = int(context.get(Context.KEY_CURRENT_TASK_TYPE))

        with write_session_scope() as session:
            # stream_opt_data_dao = get_stream_opt_data_dao(session=session)
            stream_unhandle_task_dao = get_stream_unhandle_task_dao(session=session)

            tasks = stream_unhandle_task_dao.base_query.with_entities(
                entities=[CmmSysStreamUnhandleTask.id, CmmSysStreamUnhandleTask.type,
                          CmmSysStreamUnhandleTask.raw_data,
                          CmmSysStreamUnhandleTask.origin_id]).filter(
                filters_=[CmmSysStreamUnhandleTask.type == task_type]).limit(1000).all()

            # tasks = stream_unhandle_task_dao.query(entities=[CmmSysStreamUnhandleTask.id, CmmSysStreamUnhandleTask.type,
            #                                                  CmmSysStreamUnhandleTask.raw_data,
            #                                                  CmmSysStreamUnhandleTask.origin_id],
            #                                        _filter=[CmmSysStreamUnhandleTask.type == task_type])
            if tasks:
                context.attach(Context.KEY_CURRENT_TASKS, tasks)

            # opt_data_entity = {
            #     'raw_data': {
            #         'integrateResult': integrate_result,
            #         'saleResult': sale_result,
            #         'goodResult': good
            #     },
            #     'type': int(TaobaoPageType.taobao_list)
            # }
            # entity = stream_opt_data_dao.insert(**opt_data_entity)
            #
            # unhandle_task_entity = {
            #     'raw_data': {
            #         'integrateInfos': self.build_integrate_infos(integrate_result),
            #         'saleInfos': self.build_sale_infos(sale_result),
            #         'goodResult': good
            #     },
            #     'type': int(TaobaoTaskType.taobao_list),
            #     'origin_id': entity.id
            # }
            # stream_unhandle_task_dao.insert(**unhandle_task_entity)
        return True

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
