# -*- coding: utf-8 -*-
import redis

from config.config_loader import global_profile

redisInfo = {
    'host': global_profile.REDIS_HOST,
    'password': global_profile.REDIS_PASSWORD,
    'port': global_profile.REDIS_PORT,
    'db': global_profile.REDIS_DB
}


class PoolingRedisClient(object):

    def __init__(self):
        if not hasattr(PoolingRedisClient, 'pool'):
            PoolingRedisClient.getRedisCoon()  # 创建redis连接
        # self.connection = redis.Redis(connection_pool=PoolingRedisClient.pool)

    @staticmethod
    def getRedisCoon():
        PoolingRedisClient.pool = redis.ConnectionPool(host=redisInfo['host'], password=redisInfo['password'],
                                                       port=redisInfo['port'], db=redisInfo['db'])


redis_pool = PoolingRedisClient()


def get_redis_client():
    return redis.Redis(connection_pool=redis_pool.pool)
