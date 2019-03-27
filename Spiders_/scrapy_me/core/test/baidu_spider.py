from Spiders_.scrapy_me.core.spider import Spider
from Spiders_.scrapy_me.http.request import Request
# 继承框架的爬虫基类
class BaiduSpider(Spider):
    # 为爬虫命名
    name='baidu'

    # 设置初始请求url
    # start_urls =[]

    def start_requests(self):
        base_url = 'http://www.baidu.com'
        yield Request(base_url)
    #     pass
    #
    def parse(self, response):
        print(response.url)
        yield {}
        pass