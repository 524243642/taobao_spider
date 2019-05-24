# -*- coding: utf-8 -*-
from unittest import TestCase

from common.db import write_session_scope
from common.redis_ import get_redis_client
from mall_spider.dao.commodity_dao import get_commodity_dao
from mall_spider.model.cmm_sys_commodity import CmmSysCommodity
from mall_spider.spiders.actions.pojo import Good


class TestDb(TestCase):
    redis_client = get_redis_client()

    def test_db(self):
        entity = CmmSysCommodity()
        entity.content = {
            'category': u'冰箱',
            'brand': u'海尔',
            'model': 'abcd-abcd',
            'price': '12.30',
            'sales': '123',
            'date': '2018-10-10'
        }

        with write_session_scope() as session:
            commodity_dao = get_commodity_dao(session=session)
            entity = commodity_dao.insert_entity(entity)
            delete = {
                'id': entity.id
            }
            commodity_dao.delete(**delete)

    def test_dict(self):
        good = {
            'model':'ccc'
        }
        c_good = Good(good)
        c_good.set_flag('1111')
        print(good)
        print(c_good)
