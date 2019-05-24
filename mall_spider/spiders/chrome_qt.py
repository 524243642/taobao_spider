#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''使用 PyQt5 内嵌浏览器浏览网页，并注入 Javascript 脚本实现自动化操作。'''
import sys
from http.cookies import SimpleCookie

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QVBoxLayout
from requests.cookies import RequestsCookieJar


class ChromeQt(QWidget):
    def cookie_added(self, cookie):
        raw_form = bytes(cookie.toRawForm()).decode()
        simple_cookie = SimpleCookie(raw_form)

        for cookie in simple_cookie.values():
            self.cookies.set(cookie.key, cookie)

    def __init__(self):
        super().__init__()
        self.init_ui()
        # 脚本
        self.profile = QWebEngineProfile.defaultProfile()
        # requests cookies
        self.cookies = RequestsCookieJar()

        # qt cookies
        self.profile.setPersistentCookiesPolicy(0)
        self.cookie_store = self.profile.cookieStore()
        self.cookie_store.cookieAdded.connect(self.cookie_added)

        # exit
        # self.webView.loadFinished.connect(self.load_finished)

    def load_finished(self):
        self.close()

    def init_ui(self):
        self.webView = QWebEngineView()
        # 主界面
        layout = QVBoxLayout(self)
        layout.addWidget(self.webView)
        self.show()
        self.resize(1024, 800)
        self.center()

    def center(self):
        # frameGeometry() 方法允许我们创建一个无形矩形并根据主窗口的宽高设置自身的宽度与高度。简单理解就是将这个控件(QWidget)的几何内容(宽高位置等)，赋值给qr
        qr = self.frameGeometry()
        # 计算出你的显示器的屏幕分辨率。根据得到的分辨率我们得到屏幕的中心点。
        cp = QDesktopWidget().availableGeometry().center()
        # 我们的矩形(qr)已有宽度和高度，现在设置移动矩形的中心(moveCenter)到屏幕的中心点(cp)，矩形的尺寸是不变的。
        qr.moveCenter(cp)
        # 移动应用程序窗口的左上角到qr矩形的左上角，从而使应用程序窗口显示在屏幕的中心。
        self.move(qr.topLeft())

    def load(self, url):
        self.webView.load(QUrl(url))


def chrome_qt_bootstrap(url=None):
    sys.argv.append('--disable-web-security')
    sys.argv.append('--allow-file-access-from-files')
    sys.argv.append('--allow-file-access')
    app = QApplication(sys.argv)
    b = ChromeQt()
    b.load(url)
    app.exec_()
    return b.cookies


if __name__ == '__main__':
    url = 'https://main.m.taobao.com/mytaobao/index.html'
    cookies = chrome_qt_bootstrap(url)
    print(cookies)
