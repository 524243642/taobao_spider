# coding: utf-8
from copy import deepcopy

from common.db import write_session_scope
from config.config_loader import logger
from mall_spider.common.enums import TaobaoPageType, TaobaoTaskType
from mall_spider.dao.stream_handle_task_dao import get_stream_handle_task_dao
from mall_spider.dao.stream_opt_data_dao import get_stream_opt_data_dao
from mall_spider.dao.stream_unhandle_task_dao import get_stream_unhandle_task_dao
from mall_spider.model.cmm_sys_stream_unhandle_task import CmmSysStreamUnhandleTask
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.default_action import DefaultAction
from mall_spider.spiders.actions.pojo import Good


class SycmProductProdHotRankPersistAction(DefaultAction):

    def build_integrate_infos(self, integrate_result):
        listItem = integrate_result['listItem']
        return list({'itemId': item.item_id, 'title': item.title} for item in listItem)

    def build_sale_infos(self, sale_result):
        listItem = sale_result['listItem']
        return list({'itemId': item.item_id, 'title': item.title} for item in listItem)

    def on_error(self, context, exp):
        task = context.get(Context.KEY_CURRENT_TASK, '')
        good = context.get(Context.KEY_GOOD_DICT, dict())
        hot_rank_result = context.get(Context.KEY_SYCM_PRODUCT_PROD_HOT_RANK_RESULT)
        task_id = None
        data = None
        if task:
            task_id = task.id
            data = task.raw_data

        logger.error(
            u'context key:[%s],action:[%s],task_id:[%s],good:[%s],execute error,data:%s,origin data:%s,exception:%s',
            context.context_key, self.__class__.__name__, task_id, good, data, hot_rank_result, exp)

    def do_execute(self, context):
        account = context.get(Context.KEY_CURRENT_TASK_ACCOUNT)
        # brands_result = context.get(Context.KEY_SYCM_PRODUCT_GET_BRANDS_RESULT)
        hot_rank_result = context.get(Context.KEY_SYCM_PRODUCT_PROD_HOT_RANK_RESULT)
        hot_rank_result = hot_rank_result['data']
        task = context.get(Context.KEY_CURRENT_TASK)
        with write_session_scope() as session:
            good = context.get(Context.KEY_GOOD_DICT)
            stream_opt_data_dao = get_stream_opt_data_dao(session=session)
            stream_unhandle_task_dao = get_stream_unhandle_task_dao(session=session)
            stream_handle_task_dao = get_stream_handle_task_dao(session=session)
            opt_data_entity = {
                'raw_data': {
                    'hotRankResult': hot_rank_result,
                    'goodResult': good
                },
                'type': int(TaobaoPageType.sycm_list)
            }
            entity = stream_opt_data_dao.insert(**opt_data_entity)

            unhandle_task_entities = []
            for item in hot_rank_result:
                c_good = Good(deepcopy(good))
                c_good.set_brand_id(item['brandId'])
                c_good.set_brand_name(item['brandName'])
                c_good.set_model_id(item['modelId'])
                c_good.set_model_name(item['modelName'])
                c_good.set_sell_count(item['payItmCnt'])
                unhandle_task_entities.append(
                    {
                        'raw_data': {
                            'hotRankInfo': item,
                            'goodResult': c_good,
                            'account': account
                        },
                        'type': int(TaobaoTaskType.sycm_list),
                        'origin_id': entity.id,
                        'date': good['date']
                    }
                )
            stream_unhandle_task_dao.bulk_insert(unhandle_task_entities)
            entity = stream_unhandle_task_dao.delete(_filter=[CmmSysStreamUnhandleTask.id == task.id])
            stream_handle_task_dao.insert(**{
                'type': task.type,
                'raw_data': task.raw_data,
                'origin_id': task.origin_id,
                'date': good['date']
            })
        return True

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
