# coding :utf-8
import logging


class DevelopConfig(object):
    # env
    ENV = 'dev'

    # db
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@127.0.0.1:3306/mall_spider_test?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI_R = 'mysql+mysqlconnector://root:@127.0.0.1:3306/mall_spider_test?charset=utf8mb4'

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'
    REDIS_DB = '0'
    REDIS_PASSWORD = ''

    # mongo
    MONGO_DATABASE_URI = 'mongodb://test:test@127.0.0.1:27017/test?authMechanism=SCRAM-SHA-1'
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = '27017'
    MONGO_USERNAME = 'test'
    MONGO_PASSWORD = 'test'
    MONGO_DB = 'test'

    # log
    LOG_NAME = 'suc.cmm.mall_spider'
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '[%(asctime)s]-[%(threadName)s:%(thread)d]-[%(name)s:%(levelname)s(%(lineno)d)]-[%(pathname)s.%(funcName)s]:%(message)s'
    # LOG_FORMAT = "[%(thread)d]-[%(asctime)s]-%(levelname)s-[%(pathname)s.%(funcName)s] %(message)s"
    CATEGORY = 'site_test'


class ProdConfig(object):
    # env
    ENV = 'prod'

    # db
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@127.0.0.1:3306/mall_spider?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI_R = 'mysql+mysqlconnector://root:@127.0.0.1:3306/mall_spider?charset=utf8mb4'

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'
    REDIS_DB = '0'
    REDIS_PASSWORD = ''

    # mongo
    MONGO_DATABASE_URI = 'mongodb://test:test@127.0.0.1:27017/test?authMechanism=SCRAM-SHA-1'
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = '27017'
    MONGO_USERNAME = 'test'
    MONGO_PASSWORD = 'test'
    MONGO_DB = 'test'

    # log
    LOG_NAME = 'suc.cmm.mall_spider'
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = '[%(asctime)s]-[%(threadName)s:%(thread)d]-[%(name)s:%(levelname)s(%(lineno)d)]-[%(pathname)s.%(funcName)s]:%(message)s'
    # LOG_FORMAT = "[%(thread)d]-[%(asctime)s]-%(levelname)s-[%(pathname)s.%(funcName)s] %(message)s"
    CATEGORY = 'site'


profiles = {
    "dev": DevelopConfig,
    "prod": ProdConfig
}

# _env = os.getenv('PRODUCT_ENV', 'dev')
# print(_env)
