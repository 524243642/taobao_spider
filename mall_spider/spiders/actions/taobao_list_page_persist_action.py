# coding: utf-8

from common.db import write_session_scope
from mall_spider.common.enums import TaobaoPageType, TaobaoTaskType
from mall_spider.dao.stream_handle_task_dao import get_stream_handle_task_dao
from mall_spider.dao.stream_opt_data_dao import get_stream_opt_data_dao
from mall_spider.dao.stream_unhandle_task_dao import get_stream_unhandle_task_dao
from mall_spider.model.cmm_sys_stream_unhandle_task import CmmSysStreamUnhandleTask
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.default_action import DefaultAction


class TaobaoListPagePersistAction(DefaultAction):

    def build_integrate_infos(self, integrate_result):
        # listItem = integrate_result['listItem']
        listItem = integrate_result.get('listItem', [])
        return list(
            {'itemId': item['item_id'], 'title': item['title'], 'userType': item['userType'],
             'originalPrice': item['originalPrice'], 'price': item['price'], 'priceWap': item['priceWap'],
             'category': item.get('category', '0')} for item in
            listItem)

    def build_sale_infos(self, sale_result):
        # listItem = sale_result['listItem']
        listItem = sale_result.get('listItem', [])
        return list(
            {'itemId': item['item_id'], 'title': item['title'], 'userType': item['userType'],
             'originalPrice': item['originalPrice'], 'price': item['price'], 'priceWap': item['priceWap'],
             'category': item['category']} for item in
            listItem)

    def do_execute(self, context):
        integrate_result = context.get(Context.KEY_TAOBAO_INTERGRATE_RESULT)
        sale_result = context.get(Context.KEY_TAOBAO_SALE_RESULT)

        with write_session_scope() as session:
            good = context.get(Context.KEY_GOOD_DICT)
            stream_opt_data_dao = get_stream_opt_data_dao(session=session)
            stream_unhandle_task_dao = get_stream_unhandle_task_dao(session=session)
            stream_handle_task_dao = get_stream_handle_task_dao(session=session)
            opt_data_entity = {
                'raw_data': {
                    'integrateResult': integrate_result,
                    'saleResult': sale_result,
                    'goodResult': good
                },
                'type': int(TaobaoPageType.taobao_list)
            }
            entity = stream_opt_data_dao.insert(**opt_data_entity)

            unhandle_task_entity = {
                'raw_data': {
                    'integrateInfos': self.build_integrate_infos(integrate_result),
                    'saleInfos': self.build_sale_infos(sale_result),
                    'goodResult': good
                },
                'type': int(TaobaoTaskType.taobao_list),
                'origin_id': entity.id,
                'date': good['date']
            }
            stream_unhandle_task_dao.insert(**unhandle_task_entity)

            task = context.get(Context.KEY_CURRENT_TASK)
            task_entity = stream_unhandle_task_dao.delete(_filter=[CmmSysStreamUnhandleTask.id == task.id])

            stream_handle_task_dao.insert(**{
                'type': task.type,
                'raw_data': task.raw_data,
                'origin_id': task.origin_id,
                'date': good['date']
            })
            # stream_handle_task_dao.insert_entity(entity=task)
            # stream_opt_data_entities = list()
            # # stream_opt_data_entity = CmmSysStreamOptData()
            # # stream_opt_data_entity.raw_data = integrate_result
            #
            # stream_opt_data_entities.append({'raw_data': integrate_result, 'type':})
            # stream_opt_data_entities.append({'raw_data': sale_result})
            #
            # # stream_opt_data_dao.insert_entity()
            # stream_opt_data_dao.bulk_insert(stream_opt_data_entities)
        return True

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
