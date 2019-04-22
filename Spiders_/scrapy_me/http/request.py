# coding='utf-8'
from Spiders_.scrapy_me.conf.settings import HEADERS
# 构造请求对象
class Request(object):
    def __init__(self,url,method='GET',params=None,headers=HEADERS,data=None,meta={},parse='parse', filter=True):
        # 请求地址
        self.url=url
        # 请求方法
        self.method=method
        # 请求参数
        self.params=params
        # 请求头
        self.headers=headers
        # 请求体
        self.data=data

        self.meta=meta

        self.parse=parse

        self.filter=filter# 是否进行去重，默认是True 表示去重!