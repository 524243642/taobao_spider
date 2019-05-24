# -*- coding: utf-8 -*-
from flufl.enum import IntEnum


def labels(cls):
    @classmethod
    def to_str(c, val):
        if hasattr(c, '__labels__'):
            return c.__labels__.get(int(val))
        return val

    cls.label = to_str
    return cls


class HttpMethod(IntEnum):
    POST = 1
    GET = 2


class TaobaoSearchType(IntEnum):
    integrate = 1
    sale = 2

    __labels__ = {
        integrate: u'综合排序',
        sale: u'销量优先'
    }


class TaobaoPageType(IntEnum):
    sycm_init = 50
    sycm_list = 100
    taobao_list = 200
    taobao_detail = 300

    __labels__ = {
        sycm_init: u'生意参谋单品类',
        sycm_list: u'生意参谋列表页',
        taobao_list: u'淘宝搜索列表页',
        taobao_detail: u'淘宝商品详情页'
    }


class TaobaoTaskType(IntEnum):
    sycm_init = 50
    sycm_list = 100
    taobao_list = 200
    taobao_detail = 300

    __labels__ = {
        sycm_init: u'生意参谋单品类',
        sycm_list: u'生意参谋列表页',
        taobao_list: u'淘宝搜索列表页',
        taobao_detail: u'淘宝商品详情页'
    }


class AliUserType(IntEnum):
    taobao = 0
    tmall = 1
    __labels__ = {
        taobao: u'淘宝',
        tmall: u'天猫'
    }


class GoodDataType(IntEnum):
    initial = 10
    not_found = 20
    success = 0
    detail_success = 30
    direct = 40
    __labels__ = {
        initial: u'初始化状态',
        not_found: u'列表页未查询到结果',
        success: u'成功',
        detail_success: u'详情页查询成功',
        direct: u'无价格数据直接导入'
    }


class RiskType(IntEnum):
    sycm = 1
    taobao_search = 2

    __labels__ = {
        sycm: u'生意参谋',
        taobao_search: u'淘宝搜索页'
    }


class PickleFileType(IntEnum):
    cookie = 1
    legality_token = 2
    origin_cookie = 3
    __labels__ = {
        cookie: u'淘宝cookie',
        legality_token: u'生意参谋首页token',
        origin_cookie: u'QNetworkCookieJar'
    }
