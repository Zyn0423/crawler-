from Spiders_.scrapy_me.core.engines import Engine    # 导入引擎

# from Spiders_.scrapy_me.core.test.baidu_spider import BaiduSpider
from Spiders_.scrapy_me.core.test.douban_spider import DoubanSpider

spider = DoubanSpider()  # 实例化爬虫对象
engine = Engine(spider)  # 传入爬虫对象
engine.start()  # 启动