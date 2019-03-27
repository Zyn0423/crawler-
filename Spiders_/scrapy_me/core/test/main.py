from Spiders_.scrapy_me.core.engines import Engine    # 导入引擎

from Spiders_.scrapy_me.core.test.baidu_spider import BaiduSpider
from Spiders_.scrapy_me.core.test.douban_spider import DoubanSpider

from Spiders_.scrapy_me.core.test.pipelines import BaiduPipeline,DoubanPipeline


if __name__ == '__main__':

    baiduSpider = BaiduSpider()
    doubanSpider = DoubanSpider()  # 实例化爬虫对象

    spiders={BaiduSpider.name:baiduSpider,DoubanSpider.name:doubanSpider}
    pipelines=[BaiduPipeline(),DoubanPipeline()]
    engine = Engine(spiders,pipelines=pipelines)  # 传入爬虫对象
    engine.start()  # 启动

