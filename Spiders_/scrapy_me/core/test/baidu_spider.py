from Spiders_.scrapy_me.core.spider import Spider
# 继承框架的爬虫基类
class BaiduSpider(Spider):
    # 为爬虫命名
    name='baidu'

    # 设置初始请求url
    start_urls = ['http://www.baidu.com']


