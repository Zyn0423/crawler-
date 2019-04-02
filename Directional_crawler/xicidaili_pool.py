#coding:utf-8
# 搭建自己的ip代理池
# 免费代理网站有：无忧代理ip，芝麻代理ip，西刺代理ip，云连代理ip
# 以西刺代理ip为例爬取可用的高匿Ip代理
import socket
import threading
import urllib

import requests
from lxml import etree
import csv
import random
import time
import telnetlib

class GenerateProxyPool(object):
    def __init__(self):
        self.base_url = 'http://www.xicidaili.com/nn/{}'

    def construct_headers(self, num):
        """更换ＵＡ，构造请求头"""
        useragent_list = [

            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",

            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",

            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",

            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",

            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",

            "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",

            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",

            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",

            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",

            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",

            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",

            "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",

            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",

            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",

            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",

            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",

            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",

            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",

            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",

        ]
        headers = {
            'User-Agent': random.choice(useragent_list),
            'Referer': 'Referer:http://www.xicidaili.com/nn/%d' % num,
            'Accept-Language':'zh-CN,zh;q=0.9'
        }
        return headers

    def get_data(self, url, headers):
        response = requests.get(url, headers=headers)
        # 减缓爬取速度
        time.sleep(random.randint(5, 10))
        try:
            data = response.content.decode()
        except:
            data = response.content.decode('GBK')
        return data

    def parse_page(self, data):
        info = []
        html = etree.HTML(data)
        for i in range(2, 102):
            temp = {}
            try:
                temp['ip'] = html.xpath('//*[@id="ip_list"]/tr[%s]/td[2]/text()' % i)[0].strip()
                temp['port'] = html.xpath('//table[@id="ip_list"]/tr[%s]/td[3]/text()' % i)[0].strip()
                temp['location'] = html.xpath('//table[@id="ip_list"]/tr[%s]/td[4]/a/text()' % i)[0].strip()
                temp['type'] = html.xpath('//table[@id="ip_list"]/tr[%s]/td[6]/text()' % i)[0].strip()
                temp['speed'] = html.xpath('//table[@id="ip_list"]/tr[%s]/td[7]/div/@title' % i)[0].strip()
                temp['connect_time'] = html.xpath('//table[@id="ip_list"]/tr[%s]/td[8]/div/@title' % i)[0].strip()
                temp['survival_time'] = html.xpath('//table[@id="ip_list"]/tr[%s]/td[9]/text()' % i)[0].strip()
                temp['test_time'] = html.xpath('//table[@id="ip_list"]/tr[%s]/td[10]/text()' % i)[0].strip()
                info.append(temp)
            except:
                pass
        return info

    # 单线程验证
    def validate_ip(self, target_url, info):
        validated_ip_list = []
        for element in info:
            proxies = {element['type']: element['type'] + "://" + element['ip'] + ":" + element['port']}
            try:
               requests.get(target_url, proxies=proxies, timeout=2)
            except:
                print('connect failed' + ":" + element['ip'])
            else:
                print('success' + ":" + element['ip'])
                validated_ip_list.append(element)
        return validated_ip_list

    # 多线程验证
    # def test(i):
    #     socket.setdefaulttimeout(5)  # 设置全局超时时间
    #     url = "http://quote.stockstar.com/stock"  # 打算爬取的网址
    #     try:
    #         proxy_support = urllib.request.ProxyHandler(proxys[i])
    #         opener = urllib.request.build_opener(proxy_support)
    #         opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64)")]
    #         urllib.request.install_opener(opener)
    #         res = urllib.request.urlopen(url).read()
    #         lock.acquire()  # 获得锁
    #         print(proxys[i], 'is OK')
    #         proxy_ip.write('%s\n' % str(proxys[i]))  # 写入该代理IP
    #         lock.release()  # 释放锁
    #     except Exception as e:
    #         lock.acquire()
    #         print(proxys[i], e)
    #         lock.release()
    #
    # threads = []
    # for i in range(len(proxys)):
    #     thread = threading.Thread(target=test, args=[i])
    #     threads.append(thread)
    #     thread.start()
    # # 阻塞主进程，等待所有子线程结束
    # for thread in threads:
    #     thread.join()



    def write_to_file(self, validated_ip_list):
        with open('ip_proxy_pool.csv', 'a', newline='') as f:
            fieldnames = ['ip', 'port','location', 'type', 'speed', 'connect_time', 'survival_time', 'test_time']
            writer = csv.DictWriter(f,fieldnames=fieldnames)
            # writer.writeheader()
            try:
                writer.writerows(validated_ip_list)
            except:
                pass

    def run(self):
        page_num = 3  # 定义开始爬取的页码数
        while page_num <= 6:  # 定义要爬取到多少页
            print(page_num)
            url = self.base_url.format(page_num)
            headers = self.construct_headers(page_num+1)

            data = self.get_data(url, headers)
            info = self.parse_page(data)
            validated_ip_list = self.validate_ip("http://quote.stockstar.com/stock", info)
            self.write_to_file(validated_ip_list)
            page_num += 1

if __name__ == '__main__':
    proxy_pool = GenerateProxyPool()
    proxy_pool.run()