# 调度器组件
# 缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度
# 对请求对象进行去重判断

# coding=utf-8
from queue import Queue
# from six.moves.queue import Queue
class Scheduler(object):
    '''
     1. 缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度
     2. 对请求对象进行去重判断
     '''
    def __init__(self):
        self.q=Queue()
        # 记录总共的请求数
        self.total_request_number = 0
    def add_request(self,request):
        """
        添加url放入队列
        :param request: url
        :return:
        """
        self.q.put(request)
        self.total_request_number +=1
    def get_request(self):
        """
        从队列里取出并返回
        :return:
        """
        '''获取一个请求对象并返回'''
        # 如果程序异常返回None ,如果正常返回request对象
        try:
            request=self.q.get(False) #设置非阻塞
        except:
            return None
        else:
            return request

    def _filter_request(self):
        """
        请求去重
        :return:
        """
        pass
