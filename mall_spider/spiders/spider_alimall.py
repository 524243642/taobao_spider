# # -*- coding: utf-8 -*-
#
# import scrapy
# from scrapy.http.cookies import CookieJar
#
#
# class SpiderAlimallSpider(scrapy.Spider):
#     name = "spider_alimall"
#     allowed_domains = ["sycm.taobao.com"]
#     start_urls = ['https://sycm.taobao.com/custom/login.htm']
#
#     cookie_jar = CookieJar()
#
#     common_headers = {
#         ':method': 'GET',
#         ':authority': 'sycm.taobao.com',
#         ':scheme': 'https',
#         ':path': '/custom/login.htm',
#         'cache-control': 'max-age=0',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'accept-encoding': 'gzip, deflate, br',
#         'accept-language': 'zh-CN,zh;q=0.9'
#     }
#
#     def start_requests(self):
#         return [scrapy.Request(url='https://sycm.taobao.com/custom/login.htm', callback=self.store_cookie, method='GET',
#                                headers=self.common_headers, meta={'cookiejar': self.cookie_jar},
#                                )]
#
#     def store_cookie(self, response):
#         self.cookie_jar.extract_cookies(response, response.request)
#         with open('cookies.txt', 'w') as f:
#             for cookie in self.cookie_jar:
#                 f.write(str(cookie) + '\n')
#
#         # return super(SpiderAlimallSpider, self).start_requests()
#
#     def parse(self, response):
#         pass
