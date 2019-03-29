# 修改默认日志文件名称
DEFAULT_LOG_FILENAME = '日志.log'    # 默认日志文件名称




# 启用的爬虫类
SPIDERS = [
    # 'spiders.baidu.BaiduSpider',
    # 'spiders.douban.DoubanSpider',
    'douban_spider.DoubanSpider',
    'baidu_spider.BaiduSpider'
]

# 启用的管道类
PIPELINES = [
    'pipelines.BaiduPipeline',
    'pipelines.DoubanPipeline'
]

# 启用的爬虫中间件类
SPIDER_MIDDLEWARES = []

# 启用的下载器中间件类
DOWNLOADER_MIDDLEWARES = []
# 控制最大并发数
MAX_ASYNC_THREAD_NUMBER=3

# 异步并发的方式 thread or coroutine 线程 或 协程
ASYNC_TYPE = 'coroutine' # 覆盖为协程的方式

# 量个值：True和False
# 如果是True，那么就是使用分布式，同时也是基于请求的增量式爬虫
# 如果是False, 不使用redis队列，会使用python的set存储指纹和请求

SCHEDULER_PERSIST = True