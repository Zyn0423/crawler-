from Spiders_.scrapy_me.core.spider import Spider

# 继承框架的爬虫基类
class BaiduSpider(Spider):

    start_urls = ['http://www.baidu.com']    # 设置初始请求url