# -*- coding: utf-8 -*-
from unittest import TestCase
import platform
# from scrapy import cmdline


class TestCmdline(TestCase):

    def test_cmdline(self):
        pass
        # cmdline.execute("Scrapy list".split())
        # cmdline.execute("Scrapy crawl spider_alimall".split())

    def test_for(self):
        for i in range(0, 2):
            print(i)

    def test_platform(self):
        print(platform.system())
