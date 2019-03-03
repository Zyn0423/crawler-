#-*-coding=utf8-*-
import requests
import json
class Douban(object):
    def __init__(self):
        self.headers_1={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"

        }
        self.headers_2 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host":"m.douban.com",
            "Pragma":"no - cache",
            "Referer":"https://m.douban.com/tv/american"

        }

        self.url1="https://m.douban.com/tv"
        self.url2=self.headers_2['Referer']
        self.url3="https://m.douban.com/rexxar/api/v2/subject_collection/tv_american/items?os=android&for_mobile=1&start={}&count=18&loc_id=108288&_=0"
        self.s=requests.session()
        self.s.headers=self.headers_1
        self.s.get(url=self.url1)
        self.s.get(url=self.url2)


 # 获取HTML数据
    def getHtml(self,url):
        try:
            Html=self.s.get(url=url,headers=self.headers_2)
            print(Html.status_code)
            Html.raise_for_status()
            return Html.content.decode()
        except:
            print("获取失败")


# 解析数据
    def parse_html(self,json_str):
        # 提取数据
        # json转换为python类型并返回
        content_list=json.loads(json_str)['subject_collection_items']

        return content_list

    def save_content_list(self, content_lsit):  # 保存
        with open("douban.txt", "a", encoding="utf-8") as f:
            for content in content_lsit:

                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")
        print("保存成功")
    def main(self):
        for i in range(2):
            json_str=self.getHtml(url=self.url3.format(i*18))
            content_list=self.parse_html(json_str)
            self.save_content_list(content_list)

if __name__ == '__main__':
    dou=Douban()
    dou.main()