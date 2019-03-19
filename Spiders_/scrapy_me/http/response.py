#coding=utf-8
# 构造响应对象
class Response(object):
    def __init__(self,url,status_code,body,headers):
        # 响应地址
        self.url=url
        # 响应状态码
        self.status_code=status_code
        # 响应体
        self.body=body
        # 响应头
        self.headers=headers
