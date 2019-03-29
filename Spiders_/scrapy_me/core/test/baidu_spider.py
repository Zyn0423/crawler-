from Spiders_.scrapy_me.core.spider import Spider
from Spiders_.scrapy_me.http.request import Request
import time
# 继承框架的爬虫基类
class BaiduSpider(Spider):

    name = 'baidu'
    start_urls = ['http://www.baidu.com']

    total = 0

    def parse(self, response):
        self.total += 1
        if self.total > 10:
            return
        yield Request(self.start_urls[0], filter=False, parse='parse')
