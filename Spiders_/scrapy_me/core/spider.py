# coding=utf-8
from Spiders_.scrapy_me.http.request import Request
from Spiders_.scrapy_me.item import Item
# 爬虫组件
# 构建请求信息(初始的)，也就是生成请求对象(Request)
# 解析响应对象，返回数据对象(Item)
# 或者新的请求对象(Request)
class Spider(object):
    '''
    1. 构建请求信息(初始的)，也就是生成请求对象(Request)
    2. 解析响应对象，返回数据对象(Item)或者新的请求对象(Request)
    '''
    name=''
    start_urls = []

    # def start_requests(self):
    #     """
    #     调用request对象发送起始ＵＲＬ
    #     :return:
    #     """
    #     return Request(url=self.urls)

    def start_requests(self):
        '''构建初始请求对象并返回'''
        for url in self.start_urls:
            yield Request(url)

    # def pares(self,response):
    #
    #     """
    #     调用item对象
    #     :param response: 响应参数
    #     :return: 返回响应体
    #     """
    #     return Item(response.body)
    # 利用生成器方式实现，提高程序的资源消耗
    def pares(self,response):
        '''解析请求
        并返回新的请求对象、或者数据对象
        返回值应当是一个容器，如start_requests返回值方法一样，改为生成器即可
        '''
        yield Item(response.body)   # 返回item对象 改为生成器即可