from Spiders_.scrapy_me.core.engines import Engine    # 导入引擎
# from Spiders_.scrapy_me.core.test.baidu_spider import BaiduSpider     #百度爬虫
# from Spiders_.scrapy_me.core.test.douban_spider import DoubanSpider   #豆瓣爬虫
# from Spiders_.scrapy_me.core.test.pipelines import BaiduPipeline,DoubanPipeline#
# from Spiders_.scrapy_me.core.test.downloader_middlewares import TestDownloaderMiddleware1,TestDownloaderMiddleware2  #下载中间件
# from Spiders_.scrapy_me.core.test.spider_middlewares import TestSpiderMiddleware1,TestSpiderMiddleware2   #爬虫中间件

if __name__ == '__main__':

    # baiduSpider = BaiduSpider()
    # doubanSpider = DoubanSpider()  # 实例化爬虫对象
    #
    # spiders={BaiduSpider.name:baiduSpider,DoubanSpider.name:doubanSpider}
    # pipelines=[BaiduPipeline(),DoubanPipeline()]  #管道
    # spider_mids=[TestDownloaderMiddleware1(),TestDownloaderMiddleware2()]   #爬虫中间件
    # downloader_mids=[TestSpiderMiddleware1(),TestSpiderMiddleware2()]#下载中间件
    # engine = Engine(spiders,pipelines=pipelines,spider_mids=spider_mids,downloader_mids=downloader_mids)  # 传入爬虫对象
    # engine.start()  # 启动

    engine = Engine()  # 传入爬虫对象
    engine.start()