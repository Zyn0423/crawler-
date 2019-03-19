# 调度器组件
# 缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度
# 对请求对象进行去重判断

# coding=utf-8
from queue import Queue
# from six.moves.queue import Queue
class Scheduler(object):
    def __init__(self):
        self.q=Queue()

    def add_request(self,request):
        """
        添加url放入队列
        :param request: url
        :return:
        """
        self.q.put(request)

    def get_request(self):
        """
        从队列里取出并返回
        :return:
        """
        request=self.q.get()
        return request

    def _filter_request(self):
        """
        请求去重
        :return:
        """
        pass
