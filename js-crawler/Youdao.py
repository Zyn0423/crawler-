import random
import requests
import time
import hashlib
import json
import jsonpath

class Youdao(object):
    def __init__(self,word):
        self.word = word
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Referer': 'http://fanyi.youdao.com/?keyfrom=dict2.index',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=1846080727@121.69.48.150; OUTFOX_SEARCH_USER_ID_NCOO=1766857866.5452132;'
                      ' P_INFO=zxnyn0423@163.com|1531119785|0|other|00&99|bej&1530685538&mail163#bej&null#10#0#0|&0|mail163&unireg|zxnyn0423@163.com'
        }
        self.post_data = None
    def generate_post_data(self):
        # r = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10))
        tempTime = int(time.time()*1000)
        tempRandom = random.randint(0,9)
        r = str(tempRandom + tempTime)

        # o = u.md5(S + n + r + D)
        S = "fanyideskweb"
        D = "ebSeFb%=XZ%T[KZ)c(sy!"
        n = self.word
        tempStr = S + n + r + D
        md5 = hashlib.md5()
        md5.update(tempStr.encode())
        o = md5.hexdigest()

        self.post_data = {
        'i': self.word,
        'from': 'AUTO',
        'to': 'AUTO',
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": r,
        "sign": o,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTIME",
        "typoResult": False,
        }
    def get_data(self):
        response = requests.post(self.url,headers=self.headers,data = self.post_data)
        return response.content.decode()
    def parse_data(self,data):
        dict_data = json.loads(data)
        print(jsonpath.jsonpath(dict_data,'$..tgt')[0])
    def run(self):
        self.generate_post_data()
        print(self.post_data)
        data = self.get_data()
        self.parse_data(data)
if __name__ == '__main__':
    youdao = Youdao('人生苦短,及时行乐')
    youdao.run()