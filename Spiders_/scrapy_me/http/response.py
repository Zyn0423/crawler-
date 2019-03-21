#coding=utf-8
# 构造响应对象
import re
import json
from lxml import etree
class Response(object):
    def __init__(self,url,status_code,body,headers,meta={}):
        # 响应地址
        self.url=url
        # 响应状态码
        self.status_code=status_code
        # 响应体
        self.body=body
        # 响应头
        self.headers=headers

        self.meta=meta

    def xpath(self,rule):
        html=etree.HTML(self.body)
        '''提供xpath方法'''
        return html.xpath(rule)



    def json(self):
        # "提供json解析"
        # "如果content是json字符串，是才有效"

        return json.loads(self.body)



    def re_findall(self,rule,data=None):
        '''封装正则的findall方法'''
        if data is None:
            data=self.body
        return re.findall(rule,data)