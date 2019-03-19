# coding=utf-8
from Spiders_.text_package_.scrapy_me.http.request import Request
from Spiders_.text_package_.scrapy_me.item import Item
# 爬虫组件
# 构建请求信息(初始的)，也就是生成请求对象(Request)
# 解析响应对象，返回数据对象(Item)
# 或者新的请求对象(Request)
class Spider(object):
    urls = 'http://www.baidu.com'

    def start_requests(self):
        """
        调用request对象发送起始ＵＲＬ
        :return:
        """
        return Request(url=self.urls)

    def pares(self,response):

        """
        调用item对象
        :param response: 响应参数
        :return: 返回响应体
        """
        return Item(response.body)