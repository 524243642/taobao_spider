# -*- coding: utf-8 -*-
from unittest import TestCase

from common.redis_ import get_redis_client


class TestRedis(TestCase):
    redis_client = get_redis_client()

    def test_redis(self):
        self.redis_client.set('spider_test', 'spider_test1')
        print(self.redis_client.get('spider_test'))
        self.redis_client.delete('spider_test')
