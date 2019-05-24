# coding: utf-8

class HttpRequest(object):
    def __init__(self, url, method) -> None:
        super().__init__()
        self.url = url
        self.method = method
