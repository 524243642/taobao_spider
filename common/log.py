#!/usr/bin/env python
# encoding: utf-8

import logging
import logging.config
import platform


def generate_log_config(category, log_format, log_level):
    category = 'mall_spider_' + category
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            "simple": {
                'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
            'default': {
                'format': log_format
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "default": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": log_level,
                "formatter": "default",
                "filename": '/var/log/tiger/%s.log' % category if platform.system() != 'Windows' else 'c:/log/tiger/%s.log' % category,
                'when': 'D',
                "interval": 1,
                "backupCount": 30
            }
            # "default": {
            #     "class": "logging.handlers.RotatingFileHandler",
            #     "level": "INFO",
            #     "formatter": "simple",
            #     "filename": os.path.join(LOG_DIR, LOG_FILE),
            #     'mode': 'w+',
            #     "maxBytes": 1024 * 1024 * 5,  # 5 MB
            #     "backupCount": 20,
            #     "encoding": "utf8"
            # },
        },
        "root": {
            'handlers': ['default'],
            'level': log_level,
            'propagate': False
        }
    }


class SingletonMetaClass(type):
    def __init__(cls, *args, **kwargs):
        cls._instance = None
        super(SingletonMetaClass, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instance


class Log(object):
    __metaclass__ = SingletonMetaClass

    def __init__(self):
        self._logger = logging

    def init(self, config):
        log_conf = generate_log_config(config.CATEGORY, config.LOG_FORMAT, config.LOG_LEVEL)
        logging.config.dictConfig(log_conf)
        # self._logger = logging.getLogger(config.LOG_NAME)
        self._logger = logging.getLogger()
        # self._logger.setLevel(config.LOG_LEVEL)

    def __getattr__(self, item):
        return getattr(self._logger, item)
