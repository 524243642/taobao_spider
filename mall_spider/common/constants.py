# -*- coding: utf-8 -*-
from datetime import datetime

from numpy import random

from config.config_loader import global_config
from mall_spider.common.enums import TaobaoSearchType


class Account(object):
    pass


class Category(object):
    a0_category = {
        124252007: '除螨仪',
        50022648: '蒸汽拖把',
        122088002: '擦窗机器人',
        127354001: '洗地机',
        50008555: '扫地机器人',
        50008554: '吸尘器',
        50008553: '蒸汽刷/手持挂烫机',
        50008552: '电熨斗',
        50008557: '电风扇',
        125170007: '空气净化机器人',
        200978002: '电动拖把/电动扫把',
        50012101: '干衣机',
        350404: '暖风机/取暖器',
        350407: '加湿器',
        350402: '空气净化/氧吧',
        50017072: '抽湿器/除湿器',
        127442005: '家用新风机',
        50017589: '空调扇',
        121468015: '蒸汽清洁机',
        200906001: '擦地/拖地机器人',
        50018327: '吊扇',
        50013195: '挂烫机'
    }
    a1_category = {
        121986001: '烘干机',
        201131101: '冰箱',
        50015563: '酒柜',
        50019790: '平板电视',
        127492005: '家用空调',
        201128001: '冰洗套装',
        50015558: '冷柜/便携冷热箱',
        350401: '空调',
        126664001: '洗烘套装',
        350301: '洗衣机',
        50013474: '热水器',
        127926010: '商用电视',
        125610001: '激光电视',
        122014001: '厨房大电',
        201130501: '壁挂洗衣机',
        127628006: '商用冷链'
    }
    a2_category = {
        50003695: '电热水壶',
        50008556: '豆浆机',
        350502: '电磁炉',
        50008543: '其它厨房家电',
        127684027: '破壁机',
        350504: '净水器',
        350507: '咖啡机',
        50002894: '电烤箱',
        50002893: '饮水机',
        50012097: '搅拌/料理机',
        124212007: '原汁机',
        127458001: '厨师机',
        50018218: '榨汁机',
        50005929: '保健/养生/煎药壶',
        50004399: '电动打蛋器',
        50004363: '电饼铛/可丽饼机',
        50002809: '微波炉',
        50013039: '绞肉/碎肉机',
        50013009: '电压力锅',
        50013008: '电饭煲',
        50008330: '电茶炉/煮茶器'
    }
    sys_category = dict()
    sys_category.update(a0_category)
    sys_category.update(a1_category)
    sys_category.update(a2_category)
    # 第二个参数是category_id
    account_0_category = [
        [50012100, 124252007, "除螨仪", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50022648, "蒸汽拖把", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 122088002, "擦窗机器人", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 127354001, "洗地机", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50008563, "对讲机", 2, "pro", "Y", 50012100, "生活电器"],
        [50008544, 50008566, "电子灭蚊器", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50008555, "扫地机器人", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50008554, "吸尘器", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50008553, "蒸汽刷/手持挂烫机", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50000360, "电热毯", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50008552, "电熨斗", 2, "pro", "Y", 50012100, "生活电器"],
        [50012135, 150806, "电话配件", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50008557, "电风扇", 2, "pro", "Y", 50012100, "生活电器"],
        [50012135, 50011872, "净化/加湿抽湿机配件", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50008544, "其它生活家电", 2, "pro", "N", 50012100, "生活电器"],
        [50012100, 50012135, "生活家电配件", 2, "pro", "N", 50012100, "生活电器"],
        [50012100, 125170007, "空气净化机器人", 2, "pro", "Y", 50012100, "生活电器"],
        [50012135, 50011871, "风扇/换气扇配件", 0, "pro", "Y", 50012100, "生活电器"],
        [50012135, 50011870, "缝纫机配件", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50008542, "电话机(有绳/无绳/网络)", 2, "pro", "Y", 50012100, "生活电器"],
        [50012135, 50011869, "吸尘器/扫地机配件", 0, "pro", "Y", 50012100, "生活电器"],
        [50012135, 50011868, "清洁/挂烫机/电熨斗配件", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 200978002, "电动拖把/电动扫把", 2, "pro", "Y", 50012100, "生活电器"],
        [50008544, 50002899, "解毒/活氧机", 0, "pro", "Y", 50012100, "生活电器"],
        [50008544, 50002901, "保温碟/垫", 0, "pro", "Y", 50012100, "生活电器"],
        [50008544, 50002889, "电暖手器/电暖足器", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50012101, "干衣机", 2, "pro", "Y", 50012100, "生活电器"],
        # [0, 50012100, "生活电器", 1, "pro", "N", 50012100, "生活电器"],
        [50012100, 350404, "暖风机/取暖器", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 350407, "加湿器", 2, "pro", "Y", 50012100, "生活电器"],
        [50008544, 350406, "其它日用家电", 0, "pro", "Y", 50012100, "生活电器"],
        [50008544, 50008383, "节电器", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 350402, "空气净化/氧吧", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50017072, "抽湿器/除湿器", 2, "pro", "Y", 50012100, "生活电器"],
        [50008544, 350409, "电子温湿度计", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 127442005, "家用新风机", 2, "pro", "Y", 50012100, "生活电器"],
        [50008544, 350408, "换气扇/排气扇", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50017589, "空调扇", 2, "pro", "Y", 50012100, "生活电器"],
        [50008544, 50008372, "充气泵", 0, "pro", "Y", 50012100, "生活电器"],
        [50012135, 50004394, "其他生活家电配件", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 121468015, "蒸汽清洁机", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 121422058, "擦鞋器", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 121474016, "超声波清洗机", 2, "pro", "Y", 50012100, "生活电器"],
        [50008544, 50005926, "缝纫机", 0, "pro", "Y", 50012100, "生活电器"],
        [50012135, 50012955, "对讲机配件", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 350310, "毛球修剪器", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 125152016, "服务机器人", 2, "pro", "Y", 50012100, "生活电器"],
        [50008544, 350307, "干手器", 0, "pro", "Y", 50012100, "生活电器"],
        [50012100, 200906001, "擦地/拖地机器人", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50018327, "吊扇", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 50013195, "挂烫机", 2, "pro", "Y", 50012100, "生活电器"],
        [50012100, 121434057, "干鞋器", 2, "pro", "Y", 50012100, "生活电器"],
        [50008544, 50006278, "加香机", 0, "pro", "Y", 50012100, "生活电器"]
    ]
    account_1_category = [
        [50013474, 126970001, "热厨套装", 0, "vip", "Y", 50022703, "大家电"],
        [127628006, 127680031, "冷库", 0, "vip", "Y", 50022703, "大家电"],
        [127628006, 127664028, "鲜花保鲜柜", 0, "vip", "Y", 50022703, "大家电"],
        [50013474, 50022268, "锅炉", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 127466003, "中央新风机", 2, "vip", "Y", 50022703, "大家电"],
        [201131101, 201132401, "组合嵌入式冰箱", 0, "vip", "Y", 50022703, "大家电"],
        [127628006, 127664023, "商用冰箱", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 126042001, "中央空调", 2, "vip", "N", 50022703, "大家电"],
        [50022703, 121986001, "烘干机", 2, "vip", "Y", 50022703, "大家电"],
        [50013474, 50025837, "电热水龙头", 0, "vip", "Y", 50022703, "大家电"],
        [50013474, 50025836, "厨宝", 0, "vip", "Y", 50022703, "大家电"],
        [122014001, 124406004, "集成灶", 0, "vip", "Y", 50022703, "大家电"],
        [50022734, 50026084, "空调配件", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 201131101, "冰箱", 2, "vip", "N", 50022703, "大家电"],
        [122014001, 350503, "消毒柜", 0, "vip", "Y", 50022703, "大家电"],
        [201131101, 201131102, "雪茄柜", 0, "vip", "Y", 50022703, "大家电"],
        [127628006, 127652031, "药品阴凉柜", 0, "vip", "Y", 50022703, "大家电"],
        [50022734, 50026077, "电视机遥控器", 0, "vip", "Y", 50022703, "大家电"],
        [50022734, 50022739, "洗衣机配件", 0, "vip", "Y", 50022703, "大家电"],
        [50022734, 50022738, "烟机灶具配件", 0, "vip", "Y", 50022703, "大家电"],
        [50022734, 50022737, "冷柜/便携冷热箱配件", 0, "vip", "Y", 50022703, "大家电"],
        [122014001, 350511, "油烟机", 0, "vip", "Y", 50022703, "大家电"],
        [50022734, 50022736, "冰箱配件", 0, "vip", "Y", 50022703, "大家电"],
        [50022734, 50009808, "电视机架", 0, "vip", "Y", 50022703, "大家电"],
        [201131101, 201131601, "化妆品冰箱", 0, "vip", "Y", 50022703, "大家电"],
        [122014001, 50018263, "烟灶消套装", 0, "vip", "Y", 50022703, "大家电"],
        [122014001, 124472005, "嵌入式电烤箱", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 50015563, "酒柜", 2, "vip", "Y", 50022703, "大家电"],
        [50015558, 50015562, "迷你/便携/车载冷热箱", 0, "vip", "Y", 50022703, "大家电"],
        [50015558, 50015560, "冷柜", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 50022734, "大家电配件", 2, "vip", "N", 50022703, "大家电"],
        [50022703, 50019790, "平板电视", 2, "vip", "Y", 50022703, "大家电"],
        [50022734, 50023117, "其他大家电配件", 0, "vip", "Y", 50022703, "大家电"],
        [201131101, 201132101, "单台嵌入式冰箱", 0, "vip", "Y", 50022703, "大家电"],
        [126042001, 200856002, "商用柜机空调", 0, "vip", "Y", 50022703, "大家电"],
        [201131101, 201131201, "冰吧", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 127492005, "家用空调", 2, "vip", "N", 50022703, "大家电"],
        [50022703, 201128001, "冰洗套装", 2, "vip", "Y", 50022703, "大家电"],
        [50022703, 50015558, "冷柜/便携冷热箱", 2, "vip", "N", 50022703, "大家电"],
        [127628006, 126686003, "商用冷柜", 0, "vip", "Y", 50022703, "大家电"],
        [127628006, 127688028, "圆弧柜", 0, "vip", "Y", 50022703, "大家电"],
        [50013474, 50013499, "空气源热泵热水器", 0, "vip", "Y", 50022703, "大家电"],
        [50013474, 50013498, "太阳能热水器", 0, "vip", "Y", 50022703, "大家电"],
        [50013474, 50013497, "燃气热水器", 0, "vip", "Y", 50022703, "大家电"],
        [127628006, 127656031, "冰鲜台", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 350401, "空调", 2, "vip", "Y", 50022703, "大家电"],
        [201131101, 201131701, "母婴冰箱", 0, "vip", "Y", 50022703, "大家电"],
        [126042001, 200910003, "螺杆机", 0, "vip", "Y", 50022703, "大家电"],
        [126042001, 200894003, "风管机", 0, "vip", "Y", 50022703, "大家电"],
        [126042001, 200878003, "嵌入式空调/天花机", 0, "vip", "Y", 50022703, "大家电"],
        [122014001, 200862003, "嵌入式微蒸烤一体机", 0, "vip", "Y", 50022703, "大家电"],
        [126042001, 200862004, "多联机", 0, "vip", "Y", 50022703, "大家电"],
        [126042001, 125662001, "中央空调套装", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 126664001, "洗烘套装", 2, "vip", "Y", 50022703, "大家电"],
        [122014001, 50005928, "洗碗机", 0, "vip", "Y", 50022703, "大家电"],
        [201131101, 50003881, "厨房冰箱", 0, "vip", "Y", 50022703, "大家电"],
        # [0, 50022703, "大家电", 1, "vip", "N", 50022703, "大家电"],
        [122014001, 124478013, "嵌入式电蒸箱", 0, "vip", "Y", 50022703, "大家电"],
        [50013474, 50498004, "即热式热水器", 0, "vip", "Y", 50022703, "大家电"],
        [201131101, 201131301, "复古冰箱", 0, "vip", "Y", 50022703, "大家电"],
        [50013474, 50013475, "电热水器", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 350301, "洗衣机", 2, "vip", "Y", 50022703, "大家电"],
        [50022703, 201060002, "电子鞋柜", 2, "vip", "Y", 50022703, "大家电"],
        [50022703, 50013474, "热水器", 2, "vip", "N", 50022703, "大家电"],
        [122014001, 200900003, "水槽厨电一体机", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 127640001, "衣物护理机", 2, "vip", "Y", 50022703, "大家电"],
        [127628006, 127694019, "水果保鲜柜", 0, "vip", "Y", 50022703, "大家电"],
        [122014001, 127224010, "嵌入式微蒸烤套装", 0, "vip", "Y", 50022703, "大家电"],
        [126042001, 125652002, "中央空调单品", 0, "vip", "Y", 50022703, "大家电"],
        [122014001, 124480015, "嵌入式微波炉", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 127926010, "商用电视", 2, "vip", "Y", 50022703, "大家电"],
        [127628006, 127692026, "岛柜", 0, "vip", "Y", 50022703, "大家电"],
        [127628006, 127692020, "风幕柜", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 125610001, "激光电视", 2, "vip", "Y", 50022703, "大家电"],
        [122014001, 50015382, "燃气灶", 0, "vip", "Y", 50022703, "大家电"],
        [201131101, 201131401, "茶几冰箱", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 122014001, "厨房大电", 2, "vip", "N", 50022703, "大家电"],
        [50022734, 50025615, "3D电视眼镜", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 201130501, "壁挂洗衣机", 2, "vip", "Y", 50022703, "大家电"],
        [126042001, 200912001, "中央空调离心机", 0, "vip", "Y", 50022703, "大家电"],
        [126042001, 200880003, "模块机", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 200992001, "移动空调", 2, "vip", "Y", 50022703, "大家电"],
        [127492005, 127500005, "家用空调套装", 0, "vip", "Y", 50022703, "大家电"],
        [50022703, 127628006, "商用冷链", 2, "vip", "N", 50022703, "大家电"]
    ]
    account_2_category = [
        [50013021, 126970002, "自动售货机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50003695, "电热水壶", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50008556, "豆浆机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50004204, "冰淇淋机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012099, 50011875, "电煲/电锅类配件", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012099, 50011874, "豆浆/搅拌/研磨机配件", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012099, 50011873, "净水/饮水机配件耗材", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 201068001, "商用制冷电器配件", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012099, 50011876, "酸奶/咖啡机配件及辅料", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 350502, "电磁炉", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50008543, "其它厨房家电", 2, "pro", "N", 50012082, "厨房电器"],
        [50012082, 127684027, "破壁机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50002898, "煮蛋器/蒸蛋器", 2, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50016465, "电蒸炉", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50002896, "食物垃圾处理机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 350504, "净水器", 2, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50002900, "其它厨房家电", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 350507, "咖啡机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50002894, "电烤箱", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50002893, "饮水机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50012099, "厨房家电配件", 2, "pro", "N", 50012082, "厨房电器"],
        [50013021, 127460001, "商用制冷工作台", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50012097, "搅拌/料理机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 121366023, "制冰机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 124212007, "原汁机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 127458001, "厨师机", 2, "pro", "Y", 50012082, "厨房电器"],
        # [0, 50012082, "厨房电器", 1, "pro", "N", 50012082, "厨房电器"],
        [50008543, 50004402, "芝士炉/电烤盘", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 201070001, "商用干果机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50018218, "榨汁机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50013609, "电热炉", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50005929, "保健/养生/煎药壶", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012099, 50003369, "其它厨房家电配件", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50004399, "电动打蛋器", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012099, 50015138, "电热水壶/保健养生壶配件", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50015397, "电陶炉", 2, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 126732001, "商用吸尘器", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 126764001, "蒸饭柜", 0, "pro", "Y", 50012082, "厨房电器"],
        [50562004, 50598004, "净水桶/净水杯", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50004363, "电饼铛/可丽饼机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50000013, "多士炉", 2, "pro", "Y", 50012082, "厨房电器"],
        [125206001, 127404002, "电动醒酒器", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 201072001, "商用制热电器配件", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013051, "商用净水设备", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013050, "商用豆浆机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013049, "商用电磁炉", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013048, "商用消毒柜", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50002809, "微波炉", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 125206001, "智能厨房电器", 2, "pro", "N", 50012082, "厨房电器"],
        [50013021, 50013043, "展示柜", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013042, "蒸炉/蒸包炉", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013041, "棉花糖机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013040, "关东煮机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013047, "商用烘烤炉/烤箱", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013046, "商用咖啡机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013045, "和面机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013044, "章鱼丸机/鱼丸炉", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50013035, "果蔬消毒清洗机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013034, "炒冰/冰粥机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 121412014, "炒冰机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013033, "刨冰/碎冰/冰沙机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013032, "商用制冰机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50013039, "绞肉/碎肉机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013038, "封口/封杯机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50013037, "巧克力喷泉机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013036, "肠粉机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013027, "商用炸锅", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013026, "其他商用厨电", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013025, "商用爆米花机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013024, "冷饮/饮料机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013031, "商用切片机/切肉机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 127488004, "商用厨房电梯", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013030, "扒炉/铁板烧/手抓饼炉", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50002535, "酸奶机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013029, "商用烤饼机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50002532, "爆米花机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013028, "商用打蛋搅拌机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013023, "商用冰淇淋/甜筒/雪糕机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50013022, "商用面条/轧面机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50013021, "商用厨电", 2, "pro", "N", 50012082, "厨房电器"],
        [50012082, 50013011, "电炖/煮粥锅/文火炉", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50013010, "电蒸锅", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50013009, "电压力锅", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50013008, "电饭煲", 2, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 121392018, "刨冰机", 0, "pro", "Y", 50012082, "厨房电器"],
        [125206001, 50011733, "炒菜机/烹饪锅", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50013007, "电热杯", 2, "pro", "Y", 50012082, "厨房电器"],
        [125206001, 125208001, "烹饪机器人", 0, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 126686004, "开水机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50006845, "削皮机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50006844, "面条机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 201054002, "果糖机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50008369, "电热饭盒", 2, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50008368, "烹饪锅", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50018103, "面包机", 2, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50008363, "香肠/热狗机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50008362, "切片机/切肉机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50008361, "豆芽机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50008366, "电烤炉", 2, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 50008365, "磨粉机/药材粉碎机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50562004, "净水设备", 2, "pro", "N", 50012082, "厨房电器"],
        [50012082, 50012960, "电热/火锅", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50003987, "电炸锅", 2, "pro", "Y", 50012082, "厨房电器"],
        [50013021, 201066001, "商用水饮设备配件", 0, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50005270, "筷子消毒机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 350709, "定时器/提醒器", 2, "pro", "Y", 50012082, "厨房电器"],
        [50012082, 50008330, "电茶炉/煮茶器", 2, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50003464, "三明治机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 200768004, "牛排机", 0, "pro", "Y", 50012082, "厨房电器"],
        [50008543, 50003465, "早餐吧", 0, "pro", "Y", 50012082, "厨房电器"]
    ]
    accounts_category = {
        global_config.accounts[0]['username']: account_0_category,
        global_config.accounts[1]['username']: account_1_category,
        global_config.accounts[2]['username']: account_2_category
    }
    accounts_category_ids_dict = {}
    for item in accounts_category.values():
        for c_item in item:
            m_cate_id = c_item[1]
            s_cate_id_set = set()
            for t_item in item:
                p_cate_id = t_item[0]
                if m_cate_id == p_cate_id:
                    s_cate_id_set.add(t_item[1])
            accounts_category_ids_dict[m_cate_id] = s_cate_id_set
    accounts_category_id_dict = {}
    for item in accounts_category.values():
        for c_item in item:
            m_cate_id = c_item[1]
            accounts_category_id_dict[m_cate_id] = c_item

    @staticmethod
    def get_account_by_name(name):
        for item in global_config.accounts:
            if item['username'] == name:
                return item

    @staticmethod
    def get_tasks(date_str, category=None):
        if not category:
            category = Category.sys_category
        tasks = list()
        for key, value in category.items():
            accounts = Category.get_accounts_by_cate_name(value)
            if not accounts:
                continue
            cate = Category.get_cate_by_account(accounts[0], value)
            cate_id = cate[1]
            account = Category.get_account_by_name(accounts[random.randint(0, len(accounts))])
            # tasks.append({
            #     'id': key,
            #     'cateId': cate_id,
            #     'cateName': value,
            #     'account': account,
            #     'dateStr': date_str
            # })
            s_cate_ids_set = Category.accounts_category_ids_dict[int(cate_id)]
            if s_cate_ids_set:
                for s_cate_id in s_cate_ids_set:
                    item = Category.accounts_category_id_dict[s_cate_id]
                    tasks.append({
                        'id': s_cate_id,
                        'cateId': s_cate_id,
                        'cateName': item[2],
                        'account': account,
                        'dateStr': date_str
                    })
            else:
                tasks.append({
                    'id': key,
                    'cateId': cate_id,
                    'cateName': value,
                    'account': account,
                    'dateStr': date_str
                })
        return tasks

    @staticmethod
    def find_cate(cate_name, account_cate_data):
        for item in account_cate_data:
            if item[2] == cate_name:
                return item
        return None

    @staticmethod
    def check_cate_id(m_category_id, s_category_id):
        if int(m_category_id) == int(s_category_id):
            return True
        rst = Category.accounts_category_ids_dict[int(m_category_id)]
        if int(s_category_id) in rst:
            return True
        return False

    @staticmethod
    def get_accounts_by_cate_name(cate_name):
        accounts = list()
        for key, value in Category.accounts_category.items():
            result = Category.find_cate(cate_name=cate_name, account_cate_data=value)
            if not result:
                continue
            accounts.append(key), result[1]
        return accounts

    @staticmethod
    def find_sys_cate(cate_name):
        for key, value in Category.sys_category.items():
            if value == cate_name:
                return key, value
        return None, None

    @staticmethod
    def get_cate_by_account(account, cate_name):
        account_data = Category.accounts_category[account]
        return Category.find_cate(cate_name, account_data)

    @staticmethod
    def get_cates_by_account(account):
        cates = list()
        account_data = Category.accounts_category[account]
        for item in account_data:
            if item[3] == 2:
                key, value = Category.find_sys_cate(item[2])
                if key and value:
                    cates.append([key, value, item[1]])
        return cates


class SpiderParams(object):
    @staticmethod
    def build_taobao_search_data(query, page, style=None, close_modues=None, sort=None, **extra):
        param_dict = {
            # 'event_submit_do_new_search_auction': '1',
            # '_input_charset': 'utf-8',
            # 'topSearch': '1',
            # 'atype': 'b',
            # 'searchfrom': '1',
            # 'action': 'home:redirect_app_action',
            # 'from': '1',
            'q': query,
            'search': '提交',
            'tab': 'all',
            'sst': '1',
            'n': 20,
            'buying': 'buyitnow'
        }
        param_dict.update(extra)
        if style:
            param_dict['style'] = style
        if close_modues:
            param_dict['closeModues'] = close_modues
        if sort:
            param_dict['sort'] = sort
        param_dict['page'] = page
        return param_dict


class SpiderHttp(object):
    UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

    @staticmethod
    def get_sycm_home_htm_headers():
        common_headers = {
            'upgrade-insecure-requests': '1',
            # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'user-agent': SpiderHttp.UA,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9'
        }
        return common_headers

    @staticmethod
    def get_sycm_headers(referer):
        common_headers = {
            # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'user-agent': SpiderHttp.UA,
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9'
        }
        if referer:
            common_headers.setdefault('referer', referer)
        return common_headers

    @staticmethod
    def get_taobao_headers(referer):
        common_headers = {
            # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.10.1 Chrome/61.0.3163.140 Safari/537.36',
            'user-agent': SpiderHttp.UA,
            # 'user-agent': 'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; LG-H850 Build/NRD90U;) AppleWebKit/537.36 (KHTML,like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.8.4.964 Mobile Safari/537.36 AliApp(TUnionSDK/0.3.2.1)',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,en-US;q=0.8'
        }
        common_headers.setdefault('referer', referer)
        return common_headers


class SpiderUrls(object):
    # 淘宝搜索2018-12-29
    _S_M_TAOBAO_PRE_SERARCH_DOMAIN = u'https://s.m.taobao.com'
    # S_M_TAOBAO_PRE_SERARCH_URL = _S_M_TAOBAO_PRE_SERARCH_DOMAIN + u'/h5?q=%s&search=提交&tab=all&sst=1&n=20&buying=buyitnow'
    S_M_TAOBAO_PRE_SERARCH_URL = _S_M_TAOBAO_PRE_SERARCH_DOMAIN + u'/h5?q=%s&search=提交&tab=all'
    # S_M_TAOBAO_PRE_SERARCH_URL = _S_M_TAOBAO_PRE_SERARCH_DOMAIN + u'/h5?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home:redirect_app_action&from=1&q=%s&sst=1&n=20&buying=buyitnow'

    # S_M_TAOBAO_SERARCH_URL_BY_INTERGRATE_TEMPLATE = _S_M_TAOBAO_SERARCH_DOMAIN + u'/search?q=%s&search=提交&tab=all&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=18&wlsort=18&style=list&closeModues=nav,selecthot,onesearch&page=%s'
    # S_M_TAOBAO_SERARCH_URL_BY_SORT_TEMPLATE = _S_M_TAOBAO_SERARCH_DOMAIN + u'/search?q=%s&search=提交&tab=all&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=13&wlsort=13&style=grid&closeModues=nav,selecthot,onesearch&sort=_sale&page=%s'
    _S_M_TAOBAO_SERARCH_DOMAIN = u'https://acs.m.taobao.com'
    S_M_TAOBAO_SERARCH_URL = _S_M_TAOBAO_SERARCH_DOMAIN + u'/h5/mtop.taobao.wsearch.h5search/1.0/?jsv=2.3.16&appKey=12574478&t=%s%s&api=mtop.taobao.wsearch.h5search&v=1.0&H5Request=true&ecode=1&AntiCreep=true&AntiFlool=true&type=jsonp&dataType=jsonp&callback=%s&data=%s'
    S_M_TAOBAO_BAICHUAN_URL = _S_M_TAOBAO_SERARCH_DOMAIN + u'/h5/mtop.taobao.baichuan.smb.get/1.0/?jsv=2.3.16&appKey=12574478&t=%s%s&api=mtop.taobao.baichuan.smb.get&v=1.0&type=originaljson&dataType=jsonp&timeout=10000'
    # S_M_TAOBAO_SERARCH_URL = _S_M_TAOBAO_SERARCH_DOMAIN + u'/h5/mtop.taobao.wsearch.h5search/1.0/?jsv=2.3.16&appKey=12574478&t=%s%s&api=mtop.taobao.wsearch.h5search&v=1.0&H5Request=true&ecode=1&AntiCreep=true&AntiFlool=true&type=jsonp&dataType=jsonp&smToken=as&sm=e&callback=%s&data=%s'
    # S_M_TAOBAO_SERARCH_URL_BY_INTERGRATE_TEMPLATE = _S_M_TAOBAO_SERARCH_DOMAIN + u'/h5?q=%s&search=提交&tab=all&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=18&wlsort=18&style=list&closeModues=nav,selecthot,onesearch&page=%s'
    # S_M_TAOBAO_SERARCH_URL_BY_SORT_TEMPLATE = _S_M_TAOBAO_SERARCH_DOMAIN + u'/search?q=%s&search=提交&tab=all&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=13&wlsort=13&style=grid&closeModues=nav,selecthot,onesearch&sort=_sale&page=%s'

    # 详情页（淘宝和天猫融合）
    DETAIL_M_TEMPLATE = u'https://detail.m.%s.com/item.htm?id=%s'
    _H5API_M_TAOBAO_DOMAIN = u'https://h5api.m.taobao.com'
    H5API_M_TAOBAO_MTOP_TAOBAO_DETAIL_TEMPLAGE = _H5API_M_TAOBAO_DOMAIN + u'/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t=%s&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017@taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp3&data={"itemNumId"%s"%s"}'

    # 生意参谋首页
    # SYCM_HOME = u'https://sycm.taobao.com/portal/home.htm'
    SYCM_HOME = u'https://sycm.taobao.com/'
    # 生意参谋登录页
    # SYCM_LOGIN_TEMPLATE = u'https://login.taobao.com/member/login.jhtml?from=sycm&full_redirect=true&style=minisimple&minititle=&minipara=0,0,0&sub=true&redirect_url=https://sycm.taobao.com/portal/home.htm'
    SYCM_LOGIN_TEMPLATE = u'https://sycm.taobao.com/custom/login.htm?_target=http://sycm.taobao.com/'
    # 生意参谋首页，目前没有风控，返回的html中有legalityToken，如果风控可以尝试加入此值
    SYCM_HOME_HTM = SYCM_HOME + u'portal/home.htm'
    # 生意参谋产品洞察单品类所有品牌
    _SYCM_TAOBAO_DOMAIN = u'https://sycm.taobao.com'
    SYCM_TAOBAO_MC_MQ_PRODUCT_GET_BRANDS = _SYCM_TAOBAO_DOMAIN + u'/mc/mq/product/getBrands.json?keyword=&cateId=%s&_=%s'
    # 生意参谋产品洞察单品类所有品牌的top500型号
    SYCM_TAOBAO_MC_MQ_PRODUCT_PROD_HOT_RANK = _SYCM_TAOBAO_DOMAIN + u'/mc/mq/product/prodHotRank.json?dateRange=%s|%s&dateType=day&pageSize=10&page=1&order=desc&orderBy=payItmCnt&cateId=%s&brandId=&deviceType=0&sellerType=-1&indexCode=tradeIndex,payItmCnt&_=%s&token=%s'

    # 淘宝app登录页
    APP_TAOBAO_LOGIN_TEMPLATE = u'https://main.m.taobao.com/mytaobao/index.html'

    @staticmethod
    def get_sycm_home_htm_url():
        return SpiderUrls.SYCM_HOME_HTM

    @staticmethod
    def get_taobao_presearch_url(query):
        return SpiderUrls.S_M_TAOBAO_PRE_SERARCH_URL % (query)

    @staticmethod
    def get_sycm_home_url():
        return SpiderUrls.SYCM_HOME

    @staticmethod
    def get_sycm_login_url():
        return SpiderUrls.SYCM_LOGIN_TEMPLATE

    @staticmethod
    def get_app_taobao_login_url():
        return SpiderUrls.APP_TAOBAO_LOGIN_TEMPLATE

    @staticmethod
    def get_detail_m_url(type, item_id):
        if type == '0':
            return SpiderUrls.DETAIL_M_TEMPLATE % ('taobao', item_id)
        if type == '1':
            return SpiderUrls.DETAIL_M_TEMPLATE % ('tmall', item_id)
        return None

    @staticmethod
    def get_sycm_product_get_brands_url(cate_id):
        timestamps = int(datetime.now().timestamp() * 1000)
        return SpiderUrls.SYCM_TAOBAO_MC_MQ_PRODUCT_GET_BRANDS % (cate_id, timestamps)

    @staticmethod
    def get_sycm_product_prod_hot_rank(start_data, end_date, cate_id, token=''):
        timestamps = int(datetime.now().timestamp() * 1000)
        return SpiderUrls.SYCM_TAOBAO_MC_MQ_PRODUCT_PROD_HOT_RANK % (start_data, end_date, cate_id, timestamps, token)

    @staticmethod
    def get_taobao_serarch_url(type, timestamps, sign, data):
        if type == TaobaoSearchType.integrate:
            return SpiderUrls.S_M_TAOBAO_SERARCH_URL % (timestamps, '&sign=' + sign if sign else '', 'mtopjsonp1', data)
        if type == TaobaoSearchType.sale:
            return SpiderUrls.S_M_TAOBAO_SERARCH_URL % (timestamps, '&sign=' + sign if sign else '', 'mtopjsonp2', data)
        raise Exception('taobao serarch type is not exist')

    @staticmethod
    def get_taobao_baichuan_url(timestamps, sign):
        return SpiderUrls.S_M_TAOBAO_BAICHUAN_URL % (timestamps, '&sign=' + sign if sign else '')

    # @staticmethod
    # def get_taobao_serarch_url(type, query, page):
    #     if type == TaobaoSearchType.integrate:
    #         return SpiderUrls.S_M_TAOBAO_SERARCH_URL_BY_INTERGRATE_TEMPLATE % (query, page)
    #     if type == TaobaoSearchType.sale:
    #         return SpiderUrls.S_M_TAOBAO_SERARCH_URL_BY_SORT_TEMPLATE % (query, page)
    #     raise Exception('taobao serarch type is not exist')

    @staticmethod
    def get_taobao_detail_url(timestamps, sign, item_id):
        return SpiderUrls.H5API_M_TAOBAO_MTOP_TAOBAO_DETAIL_TEMPLAGE % (timestamps, "%3A", item_id)


if __name__ == '__main__':
    timestamps = int(datetime.now().timestamp() * 1000)
    # print(datetime.now().timestamp() * 1000)
    print(SpiderUrls.H5API_M_TAOBAO_MTOP_TAOBAO_DETAIL_TEMPLAGE % (timestamps, '1234'))
