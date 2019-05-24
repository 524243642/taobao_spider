# -*- coding: utf-8 -*-
from unittest import TestCase

from config.config_loader import logger


class TestLog(TestCase):

    def test_log(self):
        logger.info(u'中文')
