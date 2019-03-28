# coding=utf-8
from Spiders_.scrapy_me.core.downloader import Downloader
from Spiders_.scrapy_me.core.pipeline import Pipeline
from Spiders_.scrapy_me.core.spider import Spider
from Spiders_.scrapy_me.core.scheduler import Scheduler
from Spiders_.scrapy_me.http.request import Request
from Spiders_.scrapy_me.middlewares.downloader_middlewares import DownloaderMiddleware
from Spiders_.scrapy_me.middlewares.spider_middlewares import Spider_middlewares
# 添加log
from datetime import datetime
from Spiders_.scrapy_me.utility.log import logger

# 引擎组件
# 负责驱动各大组件，通过调用各自对外提供的API接口，实现它们之间的交互和协作
# 提供整个框架的启动入口

"""
构造spider中start_urls中的请求
传递给调取器进行保存，之后从中取出
取出的request对象交给下载的进行下载，返回response
response交给爬虫模块进行解析，提取结果
如果结果是request对象，重新交给调度器，如果结果是item对象，交给管道处理
"""


class Engine(object):
    def __init__(self):
        self.downloader = Downloader()
        self.pipeline = Pipeline()
        self.spider = Spider()
        self.scheduler = Scheduler()
        self.downloaderMiddleware = DownloaderMiddleware()
        self.spider_middlewares = Spider_middlewares()

    def start(self):
        '''启动整个引擎'''
        start = datetime.now()  # 起始时间
        logger.info("开始运行时间：%s" % start)  # 使用日志记录起始运行时间
        self._start_engine()
        stop = datetime.now()  # 结束时间
        logger.info("开始运行时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start).total_seconds())  # 使用日志记录运行耗时

    def _start_engine(self):
        # 获取ＵＲＬ
        # 1.爬虫模块发出初始请求
        start_request = self.spider.start_requests()
        # 1.1利用爬虫中间件预处理请求对象
        start_request = self.spider_middlewares.process_request(start_request)
        # 2.把初始请求添加给调度器
        self.scheduler.add_request(start_request)
        # 3.从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        request = self.scheduler.get_request()
        # 3.1利用下载器中间件预处理请求对象

        request = self.downloaderMiddleware.process_request(request)
        # 4.利用下载器发起请求
        response = self.downloader.get_response(request)
        # 4.1利用下载器中间件预处理响应对象
        response = self.downloaderMiddleware.process_response(response)
        # 4.2利用爬虫中间件预处理响应对象
        self.spider_middlewares.process_response(response)
        # 5．利用爬虫的解析响应的方式，处理响应，得到结果
        resp = self.spider.parse(response)
        # ６.判断结果对象
        # 如果是请求对象，那么就在交给调度器
        if isinstance(resp, Request):
            # 6.1利用爬虫中间件预处理请求对象
            resp = self.spider_middlewares.process_request(resp)

            self.scheduler.add_request(resp)
        # 否则，就交给管道处理
        else:

            self.pipeline.process_item(resp)


if __name__ == '__main__':
    eng = Engine()
    eng.start()
