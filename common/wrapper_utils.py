# -*- coding: utf-8 -*-
"""
    wrapper_ex
    feature 1：
    Supports compatible parametric decorators and parametric decorators.

    @wrapper_ex
    def log(func, level=2):
        @wraps(func)
        def wrap(*args, **kwargs):
          try:
            func(*args,**kwargs)
          finally:
            logging.info('hello')
        return wrap

    # try normal
    @log
    def a(x):
        return x + 1

    # try args
    @log(level=1)
    def f2(x, y):
        return x*y
    feature 2：rewrite wraps and getargspec can keep origin function's sign
    don't use getargspec of inspect,and this is deprecated in py3
"""
from _functools import partial

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__')
WRAPPER_UPDATES = ('__dict__',)


def update_wrapper(wrapper,
                   wrapped,
                   assigned=WRAPPER_ASSIGNMENTS,
                   updated=WRAPPER_UPDATES):
    for attr in assigned:
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    wrapper.wrap_func = wrapped
    return wrapper


def wraps(wrapped,
          assigned=WRAPPER_ASSIGNMENTS,
          updated=WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)


def wrapper_extend(func):
    """
    :param func:
    :return:
    """

    @wraps(func)
    def _de_wrapper(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return func(args[0])
        else:
            return lambda real_func: func(real_func, *args, **kwargs)

    return _de_wrapper


import sys
import inspect
import collections

if sys.version >= '3':
    from inspect import getfullargspec


    def get_init(cls):
        return cls.__init__
else:
    FullArgSpec = collections.namedtuple(
        'FullArgSpec', 'args varargs varkw defaults '
                       'kwonlyargs kwonlydefaults')


    def getfullargspec(f):
        "A quick and dirty replacement for getfullargspec for Python 2.X"
        return FullArgSpec._make(inspect.getfullargspec(f) + ([], None))


    def get_init(cls):
        return cls.__init__.__func__

# getargspec has been deprecated in Python 3.5
ArgSpec = collections.namedtuple(
    'ArgSpec', 'args varargs varkw defaults')


def getargspec(f):
    """A replacement for inspect.getargspec"""
    while hasattr(f, 'wrap_func'):
        f = f.wrap_func
    spec = getfullargspec(f)
    return ArgSpec(spec.args, spec.varargs, spec.varkw, spec.defaults)
