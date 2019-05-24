#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''使用 PyQt5 内嵌浏览器浏览网页，并注入 Javascript 脚本实现自动化操作。'''
import os
import sys
import time
from datetime import datetime
from http.cookies import SimpleCookie
from pathlib import Path

from PyQt5 import QtNetwork
from PyQt5.QtCore import QUrl, pyqtSlot, QObject, pyqtProperty, pyqtSignal
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineScript
from PyQt5.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout,
    QDesktopWidget, QTextEdit, QLabel, QLineEdit, QPushButton,
    QFileDialog, QProgressBar)
from requests.cookies import RequestsCookieJar

from config.config_loader import logger, global_config
from mall_spider.common.constants import SpiderUrls, SpiderHttp
from mall_spider.common.enums import PickleFileType
from mall_spider.dto.pickle_cookie import PickleCookieJar
from mall_spider.spiders.actions.context import Context
from mall_spider.spiders.actions.cookie_service import get_cookie_service
from mall_spider.spiders.actions.proxy_service import get_proxy_service
from mall_spider.spiders.actions.sycm_home_htm_token_action import SycmHomeHtmTokenAction

__cookie_service = get_cookie_service()
__proxy_service = get_proxy_service()
__app = None


class SmsVerifyCode(QObject):
    mySignal = pyqtSignal(str)
    resultSignal = pyqtSignal(str)

    def __init__(self, parent=None, value=None):
        super().__init__(parent)
        self.value = value
        self.result = None

    @pyqtSlot(result=str)
    def getStrValue(self):
        return self.value

    def setStrValue(self, value):
        self.value = value
        self.mySignal.emit(value)

    @pyqtSlot(result=str)
    def getResultValue(self):
        return self.result

    def setResultValue(self, value):
        self.result = value
        self.resultSignal.emit(value)

    strValue = pyqtProperty(str, getStrValue, setStrValue)
    resultValue = pyqtProperty(str, getResultValue, setResultValue)


class Browser(QWidget):

    def init_account(self, account):
        self.account = account

    def cookie_added(self, cookie):
        self.origin_cookies.add_cookie(cookie)
        raw_form = bytes(cookie.toRawForm()).decode()
        simple_cookie = SimpleCookie(raw_form)
        for cookie in simple_cookie.values():
            self.cookies.set(cookie.key, cookie)

    def set_cookies(self, cookies=None):
        if cookies is None:
            return
        for item in cookies.get_cookies():
            self.cookie_store.setCookie(item)

    def init_cookie(self, cookies=None):
        self.cookies = RequestsCookieJar()
        self.origin_cookies = PickleCookieJar()

        self.profile.setPersistentCookiesPolicy(0)
        self.cookie_store = self.profile.cookieStore()
        self.cookie_store.deleteAllCookies()
        self.set_cookies(cookies=cookies)
        self.cookie_store.cookieAdded.connect(self.cookie_added)

    def init_script(self):
        self.pre_script = QWebEngineScript()
        try:
            file_name = 'qwebchannel.js'
            qwebchannel = Path(__file__).parent.joinpath('../../js/', file_name)
            if not qwebchannel.exists():
                logger.warning('配置文件不存在,{}".'.format(file_name))
            qwebchannel_file = qwebchannel.resolve()
            qwebchannel_js = qwebchannel_file.read_text(encoding='utf-8')
            self.pre_script.setSourceCode(qwebchannel_js)
            self.pre_script.setName(file_name)
            self.pre_script.setWorldId(QWebEngineScript.MainWorld)
            self.pre_script.setInjectionPoint(QWebEngineScript.DocumentCreation)
            self.pre_script.setRunsOnSubFrames(True)
            self.profile.scripts().insert(self.pre_script)
        except Exception as e:
            sys.exit('# 错误: 配置文件载入失败: {}'.format(e))

        self.channel_script = QWebEngineScript()
        try:
            file_name = 'channel_inject.js'
            channel = Path(__file__).parent.joinpath('../../js/', file_name)
            if not channel.exists():
                logger.warning('配置文件不存在,{}".'.format(file_name))
            channel_file = channel.resolve()
            channel_js = channel_file.read_text(encoding='utf-8')
            self.pre_script.setSourceCode(channel_js)
            self.pre_script.setName(file_name)
            self.pre_script.setWorldId(QWebEngineScript.MainWorld)
            self.pre_script.setRunsOnSubFrames(True)
            self.profile.scripts().insert(self.pre_script)
        except Exception as e:
            sys.exit('# 错误: 配置文件载入失败: {}'.format(e))

        self.script = QWebEngineScript()
        self.app_taobao_script = QWebEngineScript()
        try:
            self.channel_script.setWorldId(QWebEngineScript.MainWorld)
            self.script.setInjectionPoint(QWebEngineScript.Deferred)
            self.script.setRunsOnSubFrames(True)

            self.app_taobao_script.setInjectionPoint(QWebEngineScript.Deferred)
            self.app_taobao_script.setRunsOnSubFrames(True)

            self.user_script()
        except Exception as e:
            sys.exit('# 错误: 配置文件载入失败: {}'.format(e))

    def init_channel(self):
        self.channel = QWebChannel()
        self.handler = SmsVerifyCode()
        self.handler.resultSignal.connect(lambda b: self.smsEdit.setText(b))
        self.channel.registerObject('sms_code', self.handler)
        self.webView.page().setWebChannel(self.channel)

    def __init__(self, account, risk=False, app=None, s_proxy=None, cookies=None):
        super().__init__()
        self.current_url = None
        self.success = False
        self.app = app
        self.risk = risk
        # account
        self.init_account(account=account)
        # ui
        self.init_ui()
        # profile
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setHttpUserAgent(SpiderHttp.UA)
        # cookie
        self.init_cookie(cookies=cookies)
        # script
        self.init_script()

        # 代理的账号名和密码
        def handleProxyAuthReq(url, auth, proxyhost):
            auth.setUser(s_proxy.get('username', ''))
            auth.setPassword(s_proxy.get('password', ''))

        if s_proxy:
            _proxy = QtNetwork.QNetworkProxy()
            _proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
            _proxy.setHostName(s_proxy['ip'])
            _proxy.setPort(int(s_proxy['port']))
            QtNetwork.QNetworkProxy.setApplicationProxy(_proxy)

            # _proxy.setUser('')
            # _proxy.setPassword('')

            self.webView.page().proxyAuthenticationRequired.connect(handleProxyAuthReq)

    @pyqtSlot()
    def load_sms_code(self):
        text = self.smsEdit.text()
        if text:
            self.handler.setStrValue(text)

    @pyqtSlot()
    def close_window(self):
        app = self.app
        self.close()
        app.closingDown()
        app.exit()
        app.quit()
        self.success = True

    def on_done(self):
        if self.risk:
            return
        if str(self.current_url).startswith(
                'https://s.m.taobao.com/h5', 0, len('https://s.m.taobao.com/h5')):
            logger.info('fetch cookie success,account:%s', self.account['username'])
            self.close()
            self.app.closingDown()
            self.app.exit()
            self.app.quit()
            self.success = True

    def on_url_changed(self, i):
        self.addrEdit.setText(i.toDisplayString())
        home_url = SpiderUrls.get_sycm_home_url()
        i = i.toDisplayString()
        self.current_url = i

        if str(i).startswith(home_url + 'portal/home.htm', 0, len(home_url + 'portal/home.htm')) or str(i).startswith(
                home_url + 'custom/no_permission', 0, len(home_url + 'custom/no_permission')):
            self.load('https://s.m.taobao.com/h5?q=Flyco%2BFR5218&search=%E6%8F%90%E4%BA%A4&tab=all')
            logger.info('fetch cookie success,account:%s', self.account['username'])
            if not self.risk:
                self.close()
                self.app.closingDown()
                self.app.exit()
                self.app.quit()
                self.success = True

    def init_ui(self):
        self.webView = QWebEngineView()
        self.webView.loadFinished.connect(self.on_done)

        self.logEdit = QTextEdit()
        self.logEdit.setFixedHeight(100)

        self.addrEdit = QLineEdit()
        self.addrEdit.returnPressed.connect(self.load_url)

        self.webView.urlChanged.connect(self.on_url_changed)

        self.jsEdit = QLineEdit()
        file_name = 'sycm_inject.js'
        path = str(Path(__file__).parent.joinpath('../../js/', file_name).absolute())
        self.jsEdit.setText(path)

        self.smsEdit = QLineEdit()
        self.smsEdit.setText('')

        loadUrlBtn = QPushButton('加载')
        loadUrlBtn.clicked.connect(self.load_url)

        chooseJsBtn = QPushButton('选择脚本文件')
        chooseJsBtn.clicked.connect(self.choose_js_file)

        smsBtn = QPushButton('短信验证码')
        smsBtn.clicked.connect(self.load_sms_code)

        closeBtn = QPushButton('关闭继续执行')
        closeBtn.clicked.connect(self.close_window)

        # 导航/工具
        top = QWidget()
        top.setFixedHeight(120)
        topBox = QVBoxLayout(top)
        topBox.setSpacing(0)
        topBox.setContentsMargins(5, 0, 0, 5)

        progBar = QProgressBar()
        progBox = QHBoxLayout()
        progBox.addWidget(progBar)
        topBox.addLayout(progBox)

        naviBox = QHBoxLayout()
        naviBox.addWidget(QLabel('网址'))
        naviBox.addWidget(self.addrEdit)
        naviBox.addWidget(loadUrlBtn)
        topBox.addLayout(naviBox)

        naviBox = QHBoxLayout()
        naviBox.addWidget(QLabel('注入脚本文件'))
        naviBox.addWidget(self.jsEdit)
        naviBox.addWidget(chooseJsBtn)
        topBox.addLayout(naviBox)

        naviBox = QHBoxLayout()
        naviBox.addWidget(QLabel('注入短信验证码'))
        naviBox.addWidget(self.smsEdit)
        naviBox.addWidget(smsBtn)
        topBox.addLayout(naviBox)

        naviBox = QHBoxLayout()
        naviBox.addWidget(QLabel('关闭继续执行'))
        naviBox.addWidget(closeBtn)
        topBox.addLayout(naviBox)

        self.webView.loadProgress.connect(progBar.setValue)

        # 主界面
        layout = QVBoxLayout(self)
        layout.addWidget(self.webView)
        layout.addWidget(top)
        layout.addWidget(self.logEdit)

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

    @pyqtSlot()
    def load_url(self):
        url = self.addrEdit.text().strip()
        if not url.lower().startswith('http://') \
                and not url.lower().startswith('https://'):
            url = 'http://{}'.format(url)
        self.load(url)

    @pyqtSlot()
    def choose_js_file(self):
        f, _ = QFileDialog.getOpenFileName(filter="Javascript files(*.js)")
        if os.path.isfile(f):
            self.jsEdit.setText(f)
            self.user_script()

    def user_script(self):
        path = self.jsEdit.text().strip()
        user_js = Path(path)
        if not user_js.exists():
            self.log('js file not exist')
            return
        user_js_file = user_js.resolve()
        user_js_text = user_js_file.read_text(encoding='utf-8') % (self.account['username'], self.account['password'])
        self.profile.scripts().remove(self.script)
        self.script.setSourceCode(user_js_text)
        self.profile.scripts().insert(self.script)
        self.log('js load success')

        # app taobao login inject
        file_name = 'app_taobao_inject.js'
        app_taobao = Path(__file__).parent.joinpath('../../js/', file_name)
        if not app_taobao.exists():
            logger.warning('app淘宝登录配置文件不存在,{}".'.format(file_name))
        app_taobao_file = app_taobao.resolve()
        app_taobao_js_text = app_taobao_file.read_text(encoding='utf-8') % (
            self.account['username'], self.account['password'])

        self.profile.scripts().remove(self.app_taobao_script)
        self.app_taobao_script.setSourceCode(app_taobao_js_text)
        self.profile.scripts().insert(self.app_taobao_script)
        self.log('app taobao js load success')

    def log(self, msg, *args, **kwargs):
        m = msg.format(*args, **kwargs)
        self.logEdit.append('{} {}'.format(
            datetime.now().strftime('%H:%M:%S'), m))

    def load(self, url):
        self.log(f'loading {url}')
        self.addrEdit.setText(url)
        self.webView.load(QUrl(url))


def init_application():
    global __app
    if __app:
        return
    sys.argv.append('--disable-web-security')
    sys.argv.append('--allow-file-access-from-files')
    sys.argv.append('--allow-file-access')
    __app = QApplication(sys.argv)


def spider_qt5_bootstrap(url=None, account=None, risk=False, proxy=None, cookies=None):
    global __app
    sys.argv.append('--disable-web-security')
    sys.argv.append('--allow-file-access-from-files')
    sys.argv.append('--allow-file-access')
    if not __app:
        init_application()
    app = __app
    app.startingUp()
    # app = QApplication(sys.argv)
    # app = QCoreApplication(sys.argv)
    # app.setAttribute(Qt.AA_UseSoftwareOpenGL, True)
    # app.setAttribute(Qt.AA_UseOpenGLES, True)
    # app.setAttribute(Qt.AA_MSWindowsUseDirect3DByDefault, True)
    # app.setAttribute(Qt.AA_UseDesktopOpenGL, True)
    b = Browser(account=account, risk=risk, app=app, s_proxy=proxy, cookies=cookies)
    if not url:
        url = SpiderUrls.get_sycm_login_url()
    b.load(url)
    app.exec_()
    while True:
        time.sleep(2)
        if b.success:
            break
    return b.cookies, b.origin_cookies


if __name__ == '__main__':
    url = SpiderUrls.get_sycm_login_url()
    # account = global_config.s_accounts[1]
    # proxy = __proxy_service.get_origin_static_proxy(account['username'])
    account = global_config.accounts[0]
    proxy = None
    cookies, origin_cookies = spider_qt5_bootstrap(url, account, True, proxy)
    __cookie_service.dump(cookies=cookies, account=account)

    context = Context()
    context.attach(Context.KEY_IS_UPDATE_COOKIES, False)
    context.attach(Context.KEY_HEADERS, SpiderHttp.get_sycm_home_htm_headers())
    cookies = __cookie_service.load(account=account)
    context.attach(Context.KEY_COOKIES, cookies)
    action = SycmHomeHtmTokenAction()
    action.execute(context=context)
    legality_token = context.get(Context.KEY_SYCM_HOME_HTM_TOKEN_RESULT)
    __cookie_service.dump(cookies=legality_token, account=account, type_=PickleFileType.legality_token)
    print(cookies)
    print(legality_token)
