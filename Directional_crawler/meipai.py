# coding=utf-8
#今日头条街拍,组图爬取


"""
1.首先分析进入街拍的url,首先分析是不是html数据,发现请求的页面对应的url的响应没有数据
2.点击xhr,发现刷新了两个js,从js中找到了json数据,其中有一个是图片详情的url
"""""
import json
import time
import jsonpath
import requests
from urllib.parse import urlencode
class Meipai(object):
    def __init__(self):
        # self.url = 'https://www.toutiao.com/search_content/?offset={}&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=3&from=search_tab'
        self.url="https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={}&format=json&keyword=%E8%A1%97%E6%8B%8D&en_qc=1&cur_tab=1pd=synthesis"
        "https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1554133442518"

        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
                        }
        self.offset = 0

    def get_data(self,url):
        response = requests.get(url,headers = self.headers)
        return response.content

    def parse_data(self,data):
        dict_data = json.loads(data.decode())
        detail_url_list = jsonpath.jsonpath(dict_data,'$..image_url')
        return detail_url_list

    def get_dateil_data(self,detail_url_list):
        detail_data_list = []
        for url in detail_url_list:
            img_name=url.split('/')[-1].split('.')[0]
            detail_data = self.get_data(url)
            with open(img_name+'.jpg','wb') as f:
                f.write(detail_data)
            # detail_data_list.append(detail_data)

        return detail_data_list


    # def parse_detail_data(self,detail_data_list):
    #
    #     for detail_data in detail_data_list:
    #
    #
    #         pass

    def run(self):
        # while True:

        url = self.url.format(self.offset)
        data = self.get_data(url)
        detail_url_list = self.parse_data(data)
        self.get_dateil_data(detail_url_list)
            # self.parse_detail_data(detail_data_list)


if __name__ == '__main__':
    meipai = Meipai()
    meipai.run()