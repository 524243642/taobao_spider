# -*- coding: utf-8 -*-
from PyQt5.QtNetwork import QNetworkCookie, QNetworkCookieJar


class PickleCookieJar(object):

    def __init__(self) -> None:
        super().__init__()
        self.cookies = list()

    def add_cookie(self, qnetwork_cookie):
        cookie = PickleCookie(qnetwork_cookie=qnetwork_cookie)
        self.cookies.append(cookie)

    def get_cookies(self):
        cookie_jar = QNetworkCookieJar()
        for item in self.cookies:
            cookie_jar.insertCookie(item.get_qnetwork_cookie())
        return cookie_jar.allCookies()


class PickleCookie(object):
    def __init__(self, qnetwork_cookie) -> None:
        super().__init__()
        self.name = qnetwork_cookie.name()
        self.path = qnetwork_cookie.path()
        self.domain = qnetwork_cookie.domain()
        self.http_only = qnetwork_cookie.isHttpOnly()
        self.value = qnetwork_cookie.value()
        self.secure = qnetwork_cookie.isSecure()
        self.expiration_date = qnetwork_cookie.expirationDate()

    def get_qnetwork_cookie(self):
        cookie = QNetworkCookie()
        cookie.setExpirationDate(self.expiration_date)
        cookie.setHttpOnly(self.http_only)
        cookie.setValue(self.value)
        cookie.setSecure(self.secure)
        cookie.setPath(self.path)
        cookie.setDomain(self.domain)
        cookie.setName(self.name)
        return cookie
