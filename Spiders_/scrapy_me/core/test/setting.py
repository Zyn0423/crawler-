# 修改默认日志文件名称
DEFAULT_LOG_FILENAME = '日志.log'    # 默认日志文件名称




# 启用的爬虫类
SPIDERS = [
    # 'spiders.baidu.BaiduSpider',
    # 'spiders.douban.DoubanSpider',
    # 'douban_spider.DoubanSpider',
    'baidu_spider.BaiduSpider'
]

# 启用的管道类
PIPELINES = [
    # 'pipelines.BaiduPipeline',
    # 'pipelines.DoubanPipeline'
]

# 启用的爬虫中间件类
SPIDER_MIDDLEWARES = []

# 启用的下载器中间件类
DOWNLOADER_MIDDLEWARES = []