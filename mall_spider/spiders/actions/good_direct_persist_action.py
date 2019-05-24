# coding: utf-8
from common.db import write_session_scope
from common.mongo_ import mongo_collection_scope
from mall_spider.common.enums import GoodDataType
from mall_spider.dao.stream_good_data_dao import get_stream_good_data_dao
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.default_action import DefaultAction


class GoodDirectPersistAction(DefaultAction):

    def do_execute(self, context):
        with write_session_scope() as session:
            good = context.get(Context.KEY_GOOD_DICT)
            stream_good_data_dao = get_stream_good_data_dao(session=session)

            good['flag'] = int(GoodDataType.direct)
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
