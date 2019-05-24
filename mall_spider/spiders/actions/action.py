# coding: utf-8
import traceback
from abc import ABCMeta, abstractmethod

from mall_spider.spiders.actions.executable import Executable


class Action(Executable):
    __metaclass__ = ABCMeta

    def execute(self, context):
        self.on_create(context=context)
        self.on_start(context=context)

        try:
            result = self.do_execute(context=context)
            self.on_complete(context=context)
            return result
        except Exception as e:
            import sys
            exc_info = sys.exc_info()
            self.on_error(context=context, exp=traceback.format_exc())
            # raise exc_info[0], exc_info[1], exc_info[2]
            raise e
        finally:
            self.on_destroy(context=context)

    @abstractmethod
    def do_execute(self, context):
        pass

    @abstractmethod
    def on_create(self, context):
        pass

    @abstractmethod
    def on_start(self, context):
        pass

    @abstractmethod
    def on_error(self, context, exp):
        pass

    @abstractmethod
    def on_complete(self, context):
        pass

    @abstractmethod
    def on_destroy(self, context):
        pass
