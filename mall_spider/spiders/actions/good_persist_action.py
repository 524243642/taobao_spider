# coding: utf-8
from common.db import write_session_scope
from common.mongo_ import mongo_collection_scope
from mall_spider.dao.stream_good_data_dao import get_stream_good_data_dao
from mall_spider.dao.stream_handle_task_dao import get_stream_handle_task_dao
from mall_spider.dao.stream_unhandle_task_dao import get_stream_unhandle_task_dao
from mall_spider.model.cmm_sys_stream_unhandle_task import CmmSysStreamUnhandleTask
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.default_action import DefaultAction


class GoodPersistAction(DefaultAction):

    def do_execute(self, context):
        task = context.get(Context.KEY_CURRENT_TASK)
        with write_session_scope() as session:
            good = context.get(Context.KEY_GOOD_DICT)
            # stream_opt_data_dao = get_stream_opt_data_dao(session=session)
            stream_unhandle_task_dao = get_stream_unhandle_task_dao(session=session)
            stream_handle_task_dao = get_stream_handle_task_dao(session=session)
            stream_good_data_dao = get_stream_good_data_dao(session=session)

            good_entity = {
                'raw_data': good,
                'flag': int(good['flag']),
                'category_name': good['categoryName'],
                'brand_name': good['brandName'],
                'category_id': good['categoryId'],
                'model_name': good['modelName'],
                'date': good['date']
            }
            stream_good_data_dao.insert(**good_entity)
            entity = stream_unhandle_task_dao.delete(_filter=[CmmSysStreamUnhandleTask.id == task.id])
            # stream_handle_task_dao.insert_entity(entity=task)
            stream_handle_task_dao.insert(**{
                'type': task.type,
                'raw_data': task.raw_data,
                'origin_id': task.origin_id,
                'date': good['date']
            })
            with mongo_collection_scope(collection_name='stream_good_data') as collection:
                collection.insert(good)
        return True

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
