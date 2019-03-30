# # coding=utf-8
import importlib
import time
from datetime import datetime
from Spiders_.scrapy_me.utility.log import logger

from Spiders_.scrapy_me.core.test.setting import SPIDERS, PIPELINES, SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES, \
    MAX_ASYNC_THREAD_NUMBER, ASYNC_TYPE

# 异步并发的方式 thread or coroutine 线程 或 协程
if ASYNC_TYPE == 'thread':
    from multiprocessing.dummy import Pool

    logger.info('异步线程模式')
elif ASYNC_TYPE == 'coroutine':
    from Spiders_.scrapy_me.core.async.coroutine import Pool

    logger.info('异步协程模式')
else:
    raise Exception("不支持的异步类型：{}, 只能是'thread'或者'coroutine'".format(ASYNC_TYPE))
    # 注意：
    # 由于打patch补丁是为了替换掉socket为非阻塞的
    # 而下载器中正好使用了requests模块，如果在这之后导入协程池，会导致requests中使用的socket没有被替换成功
    # 从而有可能导致使用出现问题
    # 所以在导入并发池对象之后再导入框架的各种类对象

from Spiders_.scrapy_me.core.downloader import Downloader
from Spiders_.scrapy_me.core.scheduler import Scheduler
from Spiders_.scrapy_me.http.request import Request

# 此处新增
from Spiders_.scrapy_me.utility.stats_collector import ReidsStatsCollector, NormalStatsCollector
from Spiders_.scrapy_me.conf.settings import SCHEDULER_PERSIST

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
    # def __init__(self, spiders,pipelines=[],spider_mids=[],downloader_mids=[]):
    def __init__(self):  # 接收外部传入的爬虫对象

        self.spiders = self._auto_import_instances(SPIDERS, isspider=True)  # 爬虫对象
        if SCHEDULER_PERSIST:
            self.collector=ReidsStatsCollector()
        else:
            self.collector=NormalStatsCollector()
        self.scheduler = Scheduler(self.collector)
        self.downloader = Downloader()
        self.pipelines = self._auto_import_instances(PIPELINES)
        self.downloaderMiddlewares = self._auto_import_instances(DOWNLOADER_MIDDLEWARES)
        self.spider_middlewaress = self._auto_import_instances(SPIDER_MIDDLEWARES)

        self.p = Pool()
        self.running = False
        self.total_request_nums = 0
        self.total_response_nums = 0

    def start(self):
        """启动引擎"""
        t_start = datetime.now()
        logger.info("爬虫开始启动：{}".format(t_start))
        logger.info("爬虫运行模式：{}".format(ASYNC_TYPE))
        logger.info("最大并发数：{}".format(MAX_ASYNC_THREAD_NUMBER))
        logger.info("启动的爬虫有：{}".format(list(self.spiders.keys())))
        logger.info("启动的下载中间件有：\n{}".format(DOWNLOADER_MIDDLEWARES))
        logger.info("启动的爬虫中间件有：\n{}".format(SPIDER_MIDDLEWARES))
        logger.info("启动的管道有：\n{}".format(PIPELINES))
        self._start_engine()
        t_end = datetime.now()
        logger.info("爬虫结束：{}".format(t_end))
        logger.info("耗时：%s" % (t_end - t_start).total_seconds())
        logger.info("一共获取了请求：{}个".format(self.collector.request_nums))
        logger.info("重复的请求：{}个".format(self.collector.repeat_request_nums))
        logger.info("成功的请求：{}个".format(self.collector.response_nums))
        self.collector.clear() # 清除redis中所有的计数的值,但不清除指纹集合




    def _auto_import_instances(self, path=[], isspider=False):

        """
        通过配置文件，动态导入类并实例化
        :param path: 表示配置文件中配置的导入类的路径
        :param isspider: 由于爬虫需要返回的是一个字典，因此对其做对应的判断和处理
        :return:
        """

        instances = {} if isspider else []
        for p in path:
            module_name = p.rsplit('.', 1)[0]  # 取出模块名称
            cla_name = p.rsplit('.', 1)[1]  # 取出类名称
            ret = importlib.import_module(module_name)  # 动态导入爬虫模块
            cls = getattr(ret, cla_name)  # 根据类名称获取类对象

            if isspider:
                instances[cls.name] = cls()  # 组装成爬虫字典{spider_name:spider(),}
            else:
                instances.append(cls())  # 实例化类对象
                # 把管道中间件分别组装成 管道列表=[管道类1(),管道类2()] / 中间件列表 = [中间件类1(),中间件类2()

        return instances  # 返回类对象字典或列表

    def _start_request(self):
        # 获取ＵＲＬ
        # 1.爬虫模块发出初始请求
        # 1.1.1.1 遍历字典取出k ,v

            # v:spider
        def func(spider_name,spider):
            for start_request in spider.start_requests():
                # 1.1利用爬虫中间件预处理请求对象
                for spider_middlewares in self.spider_middlewaress:  # 遍历爬虫对象１．１．１．１．１
                    start_request = spider_middlewares.process_request(start_request)
                # 1.1.1.2:为请求对象绑定它所属的爬虫的名称
                start_request.spider_name = spider_name
                # 2.把初始请求添加给调度器
                self.scheduler.add_request(start_request)

                self.collector.incr(self.collector.request_nums_key)

        for spider_name, spider in self.spiders.items():
            # 把执行每个爬虫的start_requests方法，设置为异步的
            self.p.apply_async(func=func,args=(spider_name,spider),error_callback=self._error_callback)

    def _execute_request_response_item(self):
        # 3.从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        request = self.scheduler.get_request()
        # 判断从调度器取出来后是不是空
        if request is None:
            return

        # 3.1利用下载器中间件预处理请求对象
        for downloaderMiddleware in self.downloaderMiddlewares:  # 1.1.1.1.1.2
            request = downloaderMiddleware.process_request(request)
        # 4.利用下载器发起请求
        response = self.downloader.get_response(request)
        # 4.1利用下载器中间件预处理响应对象
        for downloaderMiddleware in self.downloaderMiddlewares:  # 1.1.1.1.1.3
            response = downloaderMiddleware.process_response(response)
        # 4.1.1　获取请求对象属性传递meta赋值给响应对象
        response.meta = request.meta
        # 4.2利用爬虫中间件预处理响应对象
        for spider_middlewares in self.spider_middlewaress:  # 1.1.1.1.1.4
            spider_middlewares.process_response(response)
        # 2.1.1.1:根据request的spider_name属性，获取对应的爬虫对象
        spider = self.spiders[request.spider_name]

        # 5．利用爬虫的解析响应的方式，处理响应，得到结果
        # 5.1.1　getattr()函数　　类＋类方法名的字符串＝类方法对象
        # 此处返回的变量parse是self.spider类当中的一个函数对象此时该函数还没有被调用!
        # getattr(实例化的类对象, 该类当中包含的方法名的字符串)
        # parse = getattr(self.spider, request.parse) 2.1.1.2: 修改前
        # 2.1.1.2:
        results = getattr(spider, request.parse)  # 修改后
        if results is not None:
            # 如果项目中爬虫的解析函数不返回可迭代对象就会报错1.1.1.1.1.1.1
            # for resp in self.spider.parse(response):  修改前
            for resp in results(response):  # 修改后
                # ６.判断结果对象
                # 如果是请求对象，那么就在交给调度器
                if isinstance(resp, Request):
                    # 6.1利用爬虫中间件预处理请求对象
                    # 在解析函数得到request对象之后，使用process_request进行处理
                    for spider_middlewares in self.spider_middlewaress:  # 1.1.1.1.1.5
                        resp = spider_middlewares.process_request(resp)
                    # 3.1.1.1: 给request对象增加一个spider_name属性
                    resp.spider_name = request.spider_name

                    self.scheduler.add_request(resp)
                    self.collector.incr(self.collector.request_nums_key)
                # 7.如果不是，调用pipeline的process_item方法处理结果
                else:
                    # 修改后，遍历管道　　 # 就通过process_item()

                    # 传递数据给管道
                    for pipeline in self.pipelines:
                        pipeline.process_item(resp, spider)  # 添加spider对象
        # 改用collector进行数据的收集
        self.collector.incr(self.collector.response_nums_key)

    def _call_back(self, temp):  # 这是异步线程池的callback参数指向的函数,temp参数为固定写法
        if self.is_running:
            self.p.apply_async(self._execute_request_response_item, callback=self._call_back,
                               error_callback=self._error_callback)

    def _error_callback(self, exception):
        """异常回调函数"""
        try:
            raise exception  # 抛出异常后，才能被日志进行完整记录下来
        except Exception as e:
            logger.exception(e)

    def _start_engine(self):
        '''
        具体的实现引擎的细节
        :return:
        '''
        self.is_running = True  # 启动引擎，设置状态为True
        # 处理strat_urls产生的request
        # self._start_request()
        self.p.apply_async(self._start_request, error_callback=self._error_callback)  # 使用异步线程池中的线程执行指定的函数

        # 不断的处理解析过程中产生的request
        for i in range(MAX_ASYNC_THREAD_NUMBER):  # 控制最大并发数
            self.p.apply_async(self._execute_request_response_item, callback=self._call_back,
                               error_callback=self._error_callback)

        timed_task_sum = sum([spider.timed_task for spider in self.spiders.values()])  # 对[False,True]求和
        start_urls_nums = sum([len(spider.start_urls) for spider in self.spiders.values()])
        # 控制判断程序何时中止
        while True:
            time.sleep(0.001)  # 避免cpu空转,避免性能消耗
            # self._execute_request_response_item()
            # if self.collector.request_nums != 0:  # 因为异步，需要增加判断，响应数不能为0
            # 有定时爬虫时,一直不退出程序; 没有定时增量爬虫,才判断是否退出!
            if self.collector.request_nums+self.collector.repeat_request_nums >= start_urls_nums and timed_task_sum == 0:
                # 成功的响应数+重复的数量>=总的请求数量 程序结束
                # if self.total_response_nums + self.scheduler.repeat_request_num >= self.total_request_nums:
                # 这个地方不能用response_nums作为判断标准了
                if self.collector.response_nums + self.collector.repeat_request_nums >= self.collector.request_nums:
                    self.is_running = False
                    break
