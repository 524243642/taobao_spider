# -*- coding: utf-8 -*-
from unittest import TestCase

from common.mongo_ import mongo_collection_scope


class TestMongo(TestCase):

    def test_db(self):
        good_dict = {
            "categoryId": 50012101,
            "categoryName": "干衣机",
            "flag": "0",
            "date": "2018-10-29",
            "brandId": 3621586,
            "brandName": "天骏",
            "modelId": 521452867,
            "modelName": "TJ-SM368",
            "sellCount": 540,
            "priceInfo": [
                {
                    "skuId": "0",
                    "price": "8500"
                },
                {
                    "skuId": "4023688523183",
                    "price": "8500"
                },
                {
                    "skuId": "3691488135263",
                    "price": "12500"
                },
                {
                    "skuId": "3691488135264",
                    "price": "14900"
                }
            ]
        }

        with mongo_collection_scope(collection_name='stream_good_data') as collection:
            collection.insert(good_dict)
