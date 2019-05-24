# -*- coding: utf-8 -*-
from unittest import TestCase

from config.config_loader import global_config
from mall_spider.common.constants import Category
from mall_spider.spiders.actions.action_service import get_action_service


class TestActionService(TestCase):
    __action_service = get_action_service()

    def test_execute_sycm_product_actions(self):
        cate_id = '50008552'
        cate_name = '电熨斗'
        account = global_config.accounts[0]
        self.__action_service.execute_sycm_product_actions(cate_id, cate_name, account)

    def test_execute_taobao_integrate_list_actions(self):
        self.__action_service.execute_taobao_integrate_list_actions(1)

    def test_execut_taobao_detail_actions(self):
        self.__action_service.execut_taobao_detail_actions()

    def test_get_cates_by_account(self):
        result = Category.get_cates_by_account(global_config.accounts[1]['username'])
        print(len(result))
