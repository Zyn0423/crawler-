from Spiders_.scrapy_me.core.engines import Engine    # 导入引擎
from Spiders_.scrapy_me.core.spider import Spider

class BaiduSpider(Spider):
    start_urls = ['http://www.baidu.com']


spider = BaiduSpider()  # 实例化爬虫对象
engine = Engine(spider)  # 传入爬虫对象
engine.start()  # 启