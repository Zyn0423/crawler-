# coding:utf8
import requests
import json
from collections import Counter
class WeChat(object):
    def __init__(self):
        self.Wxurl="https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact"
        self.cookie=''
        self.headers = {
        'Cookie': self.cookie,
        'Host': 'wx.qq.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
                }
# 微信Url数据获取连接


    def gethtml(self):
        try:
            # 获取JS
            data=requests.get(url=self.Wxurl,headers=self.headers)
            print(data.status_code)
            data.raise_for_status()
            return data.content.decode()
        except:
            print('获取失败')

    def parsing(self,html_data,HeadImgUrls,sexs,Province):

        # js文件装换为python文件
        dict1 = json.loads(html_data)
        listdata = dict1["MemberList"]  # 集合
        for lists in range(0, dict1["MemberCount"]):  # 把全部用户的地址存储
            HeadImgUrls.append(listdata[lists]["HeadImgUrl"])
            sexs.append(listdata[lists]["Sex"])
            # 地址省份                      市
            Province.append(listdata[lists]["Province"] + "" + listdata[lists]["City"])
        return dict1["MemberCount"]
    def statistical_(self,Province,sexs):
        # 统计相同的地方有多少
        RET=Counter(Province)
        # ('去重',sets)
        # '去重后装换列表',countProvin
        countProvin = list(set(Province))
        Countcity=[]
        # 遍历列表
        for iii in range(0, len(countProvin)):
            # # 索引字典values

            Countcity.append([countProvin[iii],RET[countProvin[iii]]])

        try:
            countProvin[0] = "暂未填写地区"
        except   Exception:
            print("登录授权已过期")
        Sexrests = Counter(sexs)
        return Countcity,Sexrests
    def print_data(self,listdata,Countcity, Sexrests):
        # 性别判断
        # 这里是分组
        # 让代码看上去简单一点使用方法封装
        print('公总号和好友合计: {} '.format(listdata))
        print('公众号: {} 男: {} 女: {} '.format(Sexrests[0],Sexrests[1],Sexrests[2]))
        print('-'*20+'地方统计'+"-"*20)
        for i in range(len(Countcity)):
            if i ==0:
                continue
            print(Countcity[i])
        print('-'*60)

    def run(self):
        HeadImgUrls = []       #路径
        sexs = []              #性别
        Province = []          #地方
        html_data=self.gethtml()
        listdata=self.parsing(html_data,HeadImgUrls,sexs,Province)
        Countcity, Sexrests=self.statistical_(Province,sexs)
        self.print_data(listdata,Countcity, Sexrests)

        pass
if __name__ == '__main__':
    wchat=WeChat()
    wchat.run()