# coding=utf-8
# 下载器组件
# 根据请求对象(Request)，发起HTTP、HTTPS网络请求，拿到HTTP、HTTPS响应，构建响应对象(Response)
# 并返回

from Spiders_.text_package_.scrapy_me.http.response import Response
import requests

class Downloader(object):
    # 1. 根据请求对象，发起请求，获取响应
    def get_response(self,request):
        if request.method.upper()=='GET':
            resp=requests.get(url=request.url,headers=request.headers)

        elif request.method.upper()=='POST':
            resp=requests.post(url=request.url,headers=request.headers,data=request.data)

        else:
            # 如果方法不是get或者post，抛出一个异常
            raise Exception ('暂时不支持method其他请求方式')
        """
        # 响应地址
        resp.url
        # 响应状态码
        resp.status_code
        # 响应体
        resp.body
        # 响应头
        resp.headers
        """
        # 2. 构建响应对象,并返回
        return Response(url=resp.url,status_code=resp.status_code,body=resp.content,headers=resp.headers)