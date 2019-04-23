# coding=utf-8
import requests
from lxml import etree
import json


class Sogou(object):
    def __init__(self):
        self.url = "http://xz.sogou.com/ranking.html?uID=2EE5F877E32E940A000000005B5B9CEB"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        self.top3_file = open("top3.json", "w")
        self.general_file = open("general.json", "w")

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_top3_data(self, data):

        html = etree.HTML(data)

        top3_list = html.xpath('//*[@id="bangList"]/div')

        top3_data_list = []
        for el in top3_list:
            temp = {}
            temp["name"] = el.xpath('./span/a/text()')[0].strip()
            temp["url"] = "http://xz.sogou.com" + el.xpath('./span/a/@href')[0]
            top3_data_list.append(temp)
            # print(top3_data_list)
        return top3_data_list

    def parse_general_data(self, data):
        html = etree.HTML(data)
        general_list = html.xpath('//*[@id="recListBox"]/div[1]/div')

        general_data_list = []
        for el in general_list:
            temp = {}
            temp["name"] = el.xpath('./span/a/text()')[0].strip()
            temp["url"] = "http://xz.sogou.com" + el.xpath('./span/a/@href')[0]
            general_data_list.append(temp)

        return general_data_list

    def save_top3_data(self, top3_data_list):
        for top3_data in top3_data_list:
            top3_json_data = json.dumps(top3_data, ensure_ascii=False) + ",\n"
            self.top3_file.write(top3_json_data)

    def save_general_data(self, general_data_list):
        for general_data in general_data_list:
            general_json_data = json.dumps(general_data, ensure_ascii=False) + ",\n"
            self.general_file.write(general_json_data)

    def __del__(self):
        self.top3_file.close()
        self.general_file.close()

    def run_top3(self):
        while True:
            url = self.url
            data = self.get_data(url)
            top3_data_list = self.parse_top3_data(data)
            self.save_top3_data(top3_data_list)
            if len(top3_data_list) == 3:
                break

    def run_general(self):
        while True:
            url = self.url
            data = self.get_data(url)
            general_data_list = self.parse_general_data(data)
            self.save_general_data(general_data_list)

    def run(self):
        self.run_top3()
        self.run_general()


if __name__ == '__main__':
    sogou = Sogou()
    sogou.run()
