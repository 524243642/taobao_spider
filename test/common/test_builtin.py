# -*- coding: utf-8 -*-
from unittest import TestCase
import sys


class TestBuiltin(TestCase):

    def test_bytes(self):
        print(bytes('中文', 'utf-8'))

    def test_max_int(self):
        print(sys.maxsize)
