# coding=utf-8
from scrapy_me.core.downloader import Downloader
from scrapy_me.core.pipeline import Pipeline
from scrapy_me.core.spider import Spider
from scrapy_me.core.scheduler import Scheduler
from scrapy_me.http.request import Request
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
        self.downloader=Downloader()
        self.pipeline=Pipeline()
        self.spider=Spider()
        self.scheduler=Scheduler()

    def _start_engine(self):
        # 获取ＵＲＬ
        # 1.爬虫模块发出初始请求
        start_request=self.spider.start_requests()
        # 2.把初始请求添加给调度器
        self.scheduler.add_request(start_request)
        # 3.从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        request=self.scheduler.get_request()
        # 4.利用下载器发起请求
        response=self.downloader.get_response(request)
        # 5．利用爬虫的解析响应的方式，处理响应，得到结果
        resp=self.spider.pares(response)
        # ６.判断结果对象
        # 如果是请求对象，那么就在交给调度器
        if isinstance(resp,Request):
            self.scheduler.add_request(response)
            # 否则，就交给管道处理
        else:

            self.pipeline.process_item(response)



