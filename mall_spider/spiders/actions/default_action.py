# coding: utf-8
from abc import ABCMeta

from config.config_loader import logger
from mall_spider.spiders.actions.action import Action
from mall_spider.spiders.actions.context import Context


class DefaultAction(Action):
    __metaclass__ = ABCMeta

    def on_error(self, context, exp):
        task = context.get(Context.KEY_CURRENT_TASK, '')
        good = context.get(Context.KEY_GOOD_DICT, dict())
        task_id = None
        data = None
        if task:
            task_id = task.id
            data = task.raw_data

        logger.error(u'context key:[%s],action:[%s],task_id:[%s],good:[%s],execute error,data:%s,exception:%s',
                     context.context_key, self.__class__.__name__, task_id, good, data, exp)
