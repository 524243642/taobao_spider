# coding: utf-8
from pathlib import Path

import execjs

from config.config_loader import logger


def get_sign_js():
    data_file = Path(__file__).parent.joinpath('../../../js/' + 'sign.js')
    if not data_file.exists():
        return None
    try:
        text = data_file.read_text()
        return text
        # ctx = execjs.compile(text)
        # print(ctx.call('p', 'aaa'))
        logger.info('load sign.js success')
    except Exception as e:
        logger.error('load sign.js error,exp:%s', e)
        raise e


def get_sign(token, timestamps, appKey, data):
    a = timestamps
    s = appKey
    target = "&".join([token, timestamps, appKey, data])

    js = get_sign_js()
    ctx = execjs.compile(js)
    return ctx.call('h', target)


if __name__ == '__main__':
    # 58ab1253975a50cf5c02ba54a9c8738f
    sign = get_sign('7f15cb4c79c9ce7dafc46c37403966a0', '1546606545959', '12574478', '{"q":"Flyco/飞科FR5218","search":"提交","tab":"all","sst":"1","n":20,"buying":"buyitnow","m":"api4h5","token4h5":"","abtest":"27","wlsort":"27","page":1}')
    print(sign)
