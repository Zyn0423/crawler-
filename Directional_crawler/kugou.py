import os

import requests
from lxml import etree
import json
import jsonpath
import hashlib
"""
一. 首先进入酷狗音乐飙升榜,http://www.kugou.com/yy/rank/home/1-6666.html?from=rank  发现1-6666 1 是可以变的,最多到5 ,后面的酷狗不显示
二.进入这个url获取数据,为html数据,此处用xpath来得出song名字和下载的url
三.进入这个下载的url,发现为js代码 ,找到这个代码,url为http://www.kugou.com/song/#hash=93F7D2FC6E95424739448218B591AEAF&album_id=9019462,
    把后面删除还可以访问,hash不能删除
四.蛋疼的就是这个hash值,找了半天也没找到,js代码完全没有找到在哪里生成的(问题点)
五.本来选择放弃,查资料的时候发现了这个api   http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword={}=1&pagesize=20&showtype=1'
keyword 输入歌曲名,是一个json数据,里面有这首歌曲的hash值
六.所以峰会路转,拿到这个hash值后再访问下载url,将从第一个url中得到的歌曲名字传过来就ok了,
七.下载过程会出错,原因为有的歌曲名字可能在这个api中查不到,所以进行判断,不存在的就不要了,也不差这一首歌,
八.下载成功
反扒手段:爬取下载地址和歌曲名没有反扒手段
爬取二进制歌曲的时候有个url中需要传hash,无法解决,解决方法为另一个api可以获取,具体在哪看到的没找到,网上查询资料得到的

"""""

class Kugou():
    def __init__(self):
        self.url = "http://www.kugou.com/yy/rank/home/{}-6666.html?from=rank"
        self.hash_url = 'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword={}=1&pagesize=20&showtype=1'
        self.download_url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash={}'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        }
        self.offset = 2
    def get_data(self,url):
        response = requests.get(url,headers = self.headers)
        return response.content.decode()

    def get_data_byte(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_data(self,data):
        html = etree.HTML(data)

        el_list = html.xpath('//*[@id="rankWrap"]/div[2]/ul/li/a')
        song_list = []
        for el in el_list:
            song_dict = {}
            song_name  = el.xpath('./text()')[0]
            song_url = el.xpath('./@href')[0]
            song_dict['name'] = song_name
            song_dict['url'] = song_url
            song_list.append(song_dict)
        return song_list


    def parse_mp3_data(self,song_list):
        for song in song_list:
            song_name = song['name']
            # print(song_name)
            hash_json_data = self.get_data(self.hash_url.format(song_name))
            hash_dict_data = json.loads(hash_json_data)
            # print(hash_dict_data)
            # print(hash_json_data)

            # hash = jsonpath.jsonpath(hash_dict_data,'$..hash')[0]

            hash_start = hash_dict_data['data']['info']
            if hash_start == []:
                continue
            hash = hash_start[0]['hash']
            #下载
            download_json_data = self.get_data(self.download_url.format(hash))
            download_dict_data = json.loads(download_json_data)
            download_url = download_dict_data['data']['play_url']

            if not os.path.exists('musics'):
                os.makedirs('musics')
            filename = 'musics' + os.sep + song_name + '.mp3'
            data = self.get_data_byte(download_url)
            with open(filename, 'wb') as f:
                f.write(data)
                print(filename)

    def run(self):
        while True:
            url = self.url.format(self.offset)
            #获取数据
            data= self.get_data(url)
            #解析数据
            song_list = self.parse_data(data)
            self.parse_mp3_data(song_list)
            self.offset += 1
            if self.offset >= 6 :
                break

if __name__ == '__main__':
    kugou = Kugou()
    kugou.run()

