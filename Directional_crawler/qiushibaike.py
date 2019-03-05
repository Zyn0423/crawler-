#-*-coding=utf8-*-
import requests
from lxml import etree
from queue import Queue
import threading
# 多线程队列

class Qiubai(object):
    def __init__(self):
        self.url="https://www.qiushibaike.com/8hr/page/{}/"
        self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        self.s=requests.session()
        # 创建3个队列
        self.url_q=Queue()
        self.resp_q=Queue()
        self.data_q=Queue()

    def getUrl(self):
        for urls in [self.url.format(i) for i in range(1,14)]:
            # 把url放入队列
            self.url_q.put(urls)

    def getHtml(self,):
        try:
            # 取出URL
            while True:
                urls=self.url_q.get()

                Html=self.s.get(url=urls,headers=self.headers)

                print(Html.status_code)
                Html.raise_for_status()
                self.resp_q.put(Html.content.decode())
                self.url_q.task_done()


        except Exception as e:
            print(e,"获取失败")

    def paresHtml(self):
        while True:
            data=self.resp_q.get()
            etree_html=etree.HTML(data)
            # 分组
            etree_div=etree_html.xpath("//div[@class='recommend-article']/ul/li/div")
            # print(etree_div)
            for i in etree_div:
                item={}
                item['text']=i.xpath('./a/text()')
                item['name']=i.xpath('./div/a/span/text()')
                self.data_q.put(item)
            self.resp_q.task_done()

    def printData(self):
        while True:
            data=self.data_q.get()
            print(data)
            self.data_q.task_done()


    def main(self):
        list_=[]
        url_thread=threading.Thread(target=self.getUrl)
        list_.append(url_thread)
        html_thread=threading.Thread(target=self.getHtml)
        list_.append(html_thread)
        pares_thread=threading.Thread(target=self.paresHtml)
        list_.append(pares_thread)
        print_thread=threading.Thread(target=self.printData)
        list_.append(print_thread)
        for i in list_:
            # i.setD
            i.setDaemon(True) #让所有子线程变成守护线程
            i.start()   #让子线程开始执行
        for x in [self.url_q,self.resp_q,self.data_q]:
            x.join() #阻塞主线程
if __name__ == '__main__':
    qiubai=Qiubai()
    qiubai.main()
