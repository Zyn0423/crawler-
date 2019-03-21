from Spiders_.scrapy_me.core.engines import Engine    # 导入引擎

from Spiders_.scrapy_me.core.test.baidu_spider import BaiduSpider
from Spiders_.scrapy_me.core.test.douban_spider import DoubanSpider


if __name__ == '__main__':
    baiduSpider = BaiduSpider()
    doubanSpider = DoubanSpider()  # 实例化爬虫对象

    spiders={BaiduSpider.name:baiduSpider,DoubanSpider.name:doubanSpider}

    engine = Engine(spiders)  # 传入爬虫对象
    engine.start()  # 启动

