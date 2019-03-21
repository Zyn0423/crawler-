# # coding=utf-8
from Spiders_.scrapy_me.core.downloader import Downloader
from Spiders_.scrapy_me.core.pipeline import Pipeline
# from Spiders_.scrapy_me.core.spider import Spider
from Spiders_.scrapy_me.core.scheduler import Scheduler
from Spiders_.scrapy_me.http.request import Request
from Spiders_.scrapy_me.middlewares.downloader_middlewares import DownloaderMiddleware
from Spiders_.scrapy_me.middlewares.spider_middlewares import Spider_middlewares
# 添加log
from datetime import datetime
from Spiders_.scrapy_me.utility.log import logger
import time

# 引擎组件
# 负责驱动各大组件，通过调用各自对外提供的API接口，实现它们之间的交互和协作
# 提供整个框架的启动入口

"""
构造spider中start_urls中的请求
传递给调取器进行保存，之后从中取出
取出的request对象交给下载的进行下载，返回response
response交给爬虫模块进行解析，提取结果
如果结果是request对象，重新交给调度器，如果结果是item对象，交给管道处理


将代码拆分为两个方法，便于维护，提高代码可读性
统计总共完成的响应数
设置程序退出条件：当总响应数等于总请求数时，退出
实现处理start_requests方法返回多个请求的功能
实现处理parse解析函数返回多个对象的功能
"""


class Engine(object):
    def __init__(self, spiders):  # 接收外部传入的爬虫对象
        self.spiders = spiders  # 爬虫对象
        self.downloader = Downloader()
        self.pipeline = Pipeline()
        self.scheduler = Scheduler()
        self.downloaderMiddleware = DownloaderMiddleware()
        self.spider_middlewares = Spider_middlewares()

        self.total_request_nums = 0
        self.total_response_nums = 0

    def start(self):
        '''启动整个引擎'''
        start = datetime.now()  # 起始时间
        logger.info("开始运行时间：%s" % start)  # 使用日志记录起始运行时间
        self._start_engine()
        stop = datetime.now()  # 结束时间
        logger.info("开始运行时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start).total_seconds())  # 使用日志记录运行耗时
        logger.info("总的请求数量:{}".format(self.total_request_nums))
        logger.info("总的响应数量:{}".format(self.total_response_nums))


        # 此处新增

    def _start_request(self):
        # 获取ＵＲＬ
        # 1.爬虫模块发出初始请求
        # 1.1.1.1 遍历字典取出k ,v
        for spider_name,spider  in self.spiders.items():
            # v:spider
            for start_request in spider.start_requests():
                # 1.1利用爬虫中间件预处理请求对象
                start_request = self.spider_middlewares.process_request(start_request)
                # 1.1.1.2:为请求对象绑定它所属的爬虫的名称
                start_request.spider_name=spider_name
                # 2.把初始请求添加给调度器
                self.scheduler.add_request(start_request)

                self.total_request_nums += 1

    def _execute_request_response_item(self):
        # 3.从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        request = self.scheduler.get_request()
        # 判断从调度器取出来后是不是空
        if request is None:
            return

        # 3.1利用下载器中间件预处理请求对象
        request = self.downloaderMiddleware.process_request(request)
        # 4.利用下载器发起请求
        response = self.downloader.get_response(request)
        # 4.1利用下载器中间件预处理响应对象
        response = self.downloaderMiddleware.process_response(response)
        # 4.1.1　获取请求对象属性传递meta赋值给响应对象
        response.meta = request.meta
        # 4.2利用爬虫中间件预处理响应对象
        self.spider_middlewares.process_response(response)
        # 2.1.1.1:根据request的spider_name属性，获取对应的爬虫对象
        spider=self.spiders[request.spider_name]


        # 5．利用爬虫的解析响应的方式，处理响应，得到结果
        # 5.1.1　getattr()函数　　类＋类方法名的字符串＝类方法对象
        # 此处返回的变量parse是self.spider类当中的一个函数对象此时该函数还没有被调用!
        # getattr(实例化的类对象, 该类当中包含的方法名的字符串)
        # parse = getattr(self.spider, request.parse) 2.1.1.2: 修改前
        # 2.1.1.2:
        parse = getattr(spider, request.parse)   # 修改后


        # for resp in self.spider.pares(response):  修改前
        for resp in parse(response):  # 修改后
            # ６.判断结果对象
            # 如果是请求对象，那么就在交给调度器
            if isinstance(resp, Request):
                # 6.1利用爬虫中间件预处理请求对象
                # 在解析函数得到request对象之后，使用process_request进行处理
                resp = self.spider_middlewares.process_request(resp)
                # 3.1.1.1: 给request对象增加一个spider_name属性
                resp.spider_name=request.spider_name

                self.scheduler.add_request(resp)
                self.total_request_nums += 1
            # 7.如果不是，调用pipeline的process_item方法处理结果
            else:

                self.pipeline.process_item(resp)
        self.total_response_nums += 1

    def _start_engine(self):

        self._start_request()

        while True:
            time.sleep(0.001)
            self._execute_request_response_item()
            # 程序退出条件
            if self.total_response_nums >= self.total_request_nums:
                break



