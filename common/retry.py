# coding: utf-8

import logging
import random
import time

from common.wrapper_utils import wrapper_extend, wraps
from config.config_loader import logger

DEFAULT_RETRY_COUNT = 3


class Retry(object):
    def __init__(self, func, tries=DEFAULT_RETRY_COUNT, exceptions=Exception, delay=0, max_delay=None, wait_delta=0):
        """
        :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
        :param tries: the maximum number of attempts. default: 3.
        :param delay: initial delay between attempts. default: 0.
        :param max_delay: the maximum value of delay. default: None (no limit).
        :param wait_delta: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
        """
        self.func = func
        self.exceptions = exceptions if exceptions else Exception
        self.tries = tries
        self.delay = delay
        self.max_delay = max_delay
        self.wait_delta = wait_delta

    def __call__(self, *args, **kwargs):
        _tries, _delay = self.tries, self.delay
        while _tries:
            try:
                return self.func(*args, **kwargs)
            except self.exceptions:
                logger.exception(u'Call func %s failed, retry it.' % self.func.__name__)
                _tries -= 1
                if not _tries:
                    raise
                time.sleep(_delay)
                if isinstance(self.wait_delta, tuple):
                    _delay += random.uniform(*self.wait_delta)
                else:
                    _delay += self.wait_delta
                if self.max_delay is not None:
                    _delay = min(_delay, self.max_delay)


@wrapper_extend
def retry(func, tries=DEFAULT_RETRY_COUNT, exceptions=Exception, delay=0, max_delay=None, wait_delta=0):
    retry_proxy = Retry(func, tries, exceptions, delay, max_delay, wait_delta)

    @wraps(func)
    def retry_decorator(*args_, **kwargs_):
        return retry_proxy(*args_, **kwargs_)

    return retry_decorator
