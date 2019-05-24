# coding: utf-8
from abc import ABCMeta, abstractmethod


class Executable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, context):
        pass
