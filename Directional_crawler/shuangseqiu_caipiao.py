#coding:utf-8

import requests
from lxml import etree

class Xinlang:
    def __init__(self):
        self.url = 'http://zst.aicai.com/ssq/openInfo/'
        self.headers = {
            'User-Agent': '"Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0) ",'
        }


    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content


    def parse_data(self,data):
        #创建对象
        html = etree.HTML(data)

        # 提取标题节点列表
        ball_list = html.xpath('//html/body/div[7]/form/div[2]/table/tbody/tr')
        data_list = []
        for ball in ball_list:
            temp = {}
            temp['date'] = ball.xpath('./td[1]/text()')
            temp['red_b'] = ball.xpath('./td[@class="redColor sz12"]/text()')
            temp['blue_b'] = ball.xpath('./td[9]/text()')

            data_list.append(temp)

        return data_list





    def run(self,input_str):
        url = self.url
        input_str = input('请输入您要查询的期号:')
        ll = []
        ll.append(input_str)
        data = self.get_data(url)
        data_list = self.parse_data(data)

        for data in data_list:

            if ll == data['date']:
                print('本期红球中奖号码为:%s'% data['red_b'][:-1])
                print('本期蓝秋中奖号码为:%s'% data['blue_b'])


if __name__ == '__main__':
    bb = Xinlang()
    bb.run(str)