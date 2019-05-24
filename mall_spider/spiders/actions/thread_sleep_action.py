# coding: utf-8
import time

from mall_spider.spiders.actions.action import Action
from mall_spider.spiders.actions.context import Context


class ThreadSleepAction(Action):

    def execute(self, context):
        interval_secs = context.get(Context.KEY_CURRENT_SLEEP_SECS, 10)
        if interval_secs:
            time.sleep(interval_secs)
        return True

    def do_execute(self, context):
        pass

    def on_create(self, context):
        pass

    def on_start(self, context):
        pass

    def on_error(self, context, exp):
        pass

    def on_complete(self, context):
        pass

    def on_destroy(self, context):
        pass
