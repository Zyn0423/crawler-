from Spiders_.scrapy_me.core.engines import Engine    # 导入引擎

from Spiders_.scrapy_me.spiders import BaiduSpider




if __name__ == '__main__':
    spider = BaiduSpider()    # 实例化爬虫对象
    engine = Engine(spider)    # 传入爬虫对象
    engine.start()    # 启动引擎