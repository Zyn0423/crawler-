# coding='utf-8'

# 构造请求对象
class Request(object):
    def __init__(self,url,method='GET',params=None,headers=None,data=None):
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
