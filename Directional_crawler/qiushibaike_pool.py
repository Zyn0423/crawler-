# -*-coding=utf8-*-
import requests
from queue import Queue
from multiprocessing.dummy import Pool
from lxml import etree


class Qiubai(object):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X \
        10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
        self.url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.s = requests.session()
        self.is_runing = True
        self.q = Queue()
        self.p = Pool(3)
        self.count_request_number = 0
        self.count_responst_number = 0

    # 1.获取url
    def url_(self):
        for i in range(1, 14):
            # 把URL放到队列里
            self.q.put(self.url.format(i))
            # 计数请求数量
            self.count_request_number += 1
        # 2.请求数据

    def get_url(self, urls):
        try:
            # 请求
            html_data = self.s.get(url=urls, headers=self.headers)
            print(html_data.status_code)
            html_data.raise_for_status()
            return html_data.content.decode()
        except Exception as e:
            print(e, "获取失败")
        # 3.解析数据

    def pares_html(self, Html_data):
        etree_html = etree.HTML(Html_data)
        etree_div = etree_html.xpath("//div[@class='recommend-article']/ul/li/div")
        # print(etree_div)
        # 进行分组
        # 创建列表并逐步添加进去
        list_data = []
        for i in etree_div:
            item = {}
            item['text'] = i.xpath('./a/text()')
            item['name'] = i.xpath('./div/a/span/text()')
            list_data.append(item)
        return list_data

    # 3.1.保存数据
    def save_data(self, list_data):
        for i in list_data:
            print(i)
            # 3.2.执行逻辑，一次请求获取响应并解析保存

    def logic_save(self):
        # 从队里取出URL
        urls = self.q.get()
        Html_data = self.get_url(urls)
        list_data = self.pares_html(Html_data)
        self.save_data(list_data)
        self.count_responst_number += 1

    # 4._clack函数
    def _cllback(self, data):
        if self.is_runing:
            self.p.apply_async(self.logic_save, callback=self._cllback)

        # 5.run方法

    def run(self):
        self.url_()
        for i in range(2):
            self.p.apply_async(self.logic_save, callback=self._cllback)
        while True:
            if self.count_responst_number >= self.count_request_number:
                self.is_runing = False
                break


if __name__ == '__main__':
    qiubai = Qiubai()
    qiubai.run()
