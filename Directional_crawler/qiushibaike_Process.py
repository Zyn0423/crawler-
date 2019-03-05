#-*-coding=utf8-*-
import requests
from lxml import etree
from  multiprocessing import Process

from multiprocessing import JoinableQueue as Queue


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
        url_P=Process(target=self.getUrl)
        list_.append(url_P)
        html_P=Process(target=self.getHtml)
        list_.append(html_P)
        pares_P=Process(target=self.paresHtml)
        list_.append(pares_P)
        print_P=Process(target=self.printData)
        list_.append(print_P)
        for i in list_:
            # i.setD
            i.damon=True #让所有子进程变成守护进程
            i.start()   #让子进程开始执行
        for x in [self.url_q,self.resp_q,self.data_q]:
            x.join() #阻塞主进程
if __name__ == '__main__':
    qiubai=Qiubai()
    qiubai.main()
