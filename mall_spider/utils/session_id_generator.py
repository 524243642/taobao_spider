# coding: utf-8
from abc import ABCMeta, abstractmethod


class SessionIdGenerator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_id(self, session):
        pass
