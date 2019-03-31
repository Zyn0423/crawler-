import requests
from lxml import etree
import json
import time

class TencentVIPMovie(object):
    def __init__(self):
        self.url = 'https://v.qq.com/x/list/movie'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
        }
        self.file = open('tencent_movie.json', 'w')

    def get_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content.decode()
        except:
            print('获取失败')


    def parse_data(self,data):
        html = etree.HTML(data)
        data_list = []
        el_list = html.xpath('/html/body/div[3]/div/div/div[1]/div[2]/div/ul/li/div[1]/strong/a')
        for el in el_list:
            temp = {}
            temp['url'] = el.xpath('./@href')[0]
            temp['title'] = el.xpath('./text()')[0]

            data_list.append(temp)

        try:
            next_url = 'https://v.qq.com/x/list/movie' + html.xpath('//a[@class="page_next"]/@href')[0]
            print(next_url)
        except:
            print('error')
            next_url = None
        return data_list, next_url

    def save_data(self, data_list):
        for data in data_list:
            json_data = json.dumps(data, ensure_ascii=False) + ',\n'
            self.file.write(json_data)

    def __del__(self):
        self.file.close()

    def run(self):
        url = self.url
        while True:
            time.sleep(2)
            data = self.get_data(url)

            data_list,url = self.parse_data(data)
            print(data_list)
            self.save_data(data_list)

            if not url:
                break



if __name__ == '__main__':
    movie = TencentVIPMovie()
    movie.run()
