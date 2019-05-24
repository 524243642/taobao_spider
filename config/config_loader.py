import argparse
import json
import sys
from pathlib import Path

from common.log import Log
from config.config import profiles


class Account(object):
    def __init__(self):
        self.accounts = []
        self.accounts_dict = {}
        self.s_accounts = []
        self.s_accounts_dict = {}
        self.s_proxy = []
        self.s_proxy_dict = {}
        self.static_proxy = {}
        self.static_proxy_dict = {}

    @classmethod
    def load(cls, d):
        the_account = Account()
        accounts = d['accounts']
        the_account.accounts = accounts
        the_account.accounts_dict = {
            item['username']: item for item in accounts
        }
        s_accounts = d['s_accounts']
        the_account.s_accounts = s_accounts
        the_account.s_accounts_dict = {
            item['username']: item for item in s_accounts
        }
        s_proxy = d['s_proxy']
        the_account.s_proxy = s_proxy
        the_account.s_proxy_dict = {
            item['username']: s_proxy[i % len(s_proxy)] for i, item in enumerate(s_accounts)
        }

        static_proxy = d['static_proxy']
        the_account.static_proxy = static_proxy
        if static_proxy:
            the_account.static_proxy_dict = {
                item['username']: static_proxy[i % len(static_proxy)] for i, item in enumerate(s_accounts)
            }
        return the_account


def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file name', default='config.json')
    parser.add_argument('-e', '--env', help='environment', default='dev')
    # args = parser.parse_args()
    args, unknown = parser.parse_known_args()
    env_name = args.env or 'dev'
    global_profile = profiles.get(env_name, 'dev')
    logger = Log()
    logger.init(global_profile)

    config_name = args.config or 'config.json'
    logger.info('使用配置文件 "{}".'.format(config_name))

    config_file = Path(__file__).parent.joinpath('./', config_name)

    if not config_file.exists():
        config_name = 'config.default.json'
        logger.warning('配置文件不存在, 使用默认配置文件 "{}".'.format(config_name))
        config_file = config_file.parent.joinpath(config_name)

    try:
        # 略坑, Path.resolve() 在 3.5 和 3.6 上表现不一致... 若文件不存在 3.5 直接抛异常, 而 3.6
        # 只有 Path.resolve(strict=True) 才抛, 但 strict 默认为 False.
        # 感觉 3.6 的更合理些...
        config_file = config_file.resolve()
        config_dict = json.loads(config_file.read_text(encoding='utf-8'))
    except Exception as e:
        sys.exit('# 错误: 配置文件载入失败: {}'.format(e))

    global_config = Account.load(config_dict)

    return global_profile, global_config, logger


global_profile, global_config, logger = load_config()
