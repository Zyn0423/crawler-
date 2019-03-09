#-*-coding=utf8-*-
import requests
import js2py
class RenrenL(object):
    def __init__(self):
        # 1首先获取三个js URL
        self.urls_dict={
              "RSA.js": "http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/RSA.js",
              "BigInt.js":"http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/BigInt.js",
              "Barrett.js":"http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/Barrett.js"

        }
        self.url='http://activity.renren.com/livecell/rKey'  #获取form data
        self.url_post="http://activity.renren.com/livecell/ajax/clog" #post
        self.s=requests.session()
        self.headers= {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36'
}
        self.js=js2py.EvalJs()   #实例化JS解释器

    def saveJs(self):
        """保存登录需要js代码"""
        for name,urls in self.urls_dict.items():
            js_data=requests.get(urls,headers=self.headers).text
            with open(name,'w') as f :
                f.write(js_data)
    def getHtml(self,url):

        data=self.s.get(url,headers=self.headers).json()
        return data['data']
    def parersJS(self,data):
        # 加载3个js文件中的JS代码
        with open('RSA.js','r') as f:
            self.js.execute(f.read())
        with open('BigInt.js', 'r') as f:
            self.js.execute(f.read())
        with open('Barrett.js', 'r') as f:
            self.js.execute(f.read())
        # 给JS解析器添加所需要的变量
        self.js.t={'password':'z5791846'}
        self.js.n=data
        # 再加载关键部位的JS加密代码
        js= 't.password = t.password.split("").reverse().join(""),' \
            'setMaxDigits(130);var o = new RSAKeyPair(n.e,"",n.n), ' \
            'r = encryptedString(o, t.password);'
        # 加载并执行
        self.js.execute(js)

        return self.js.r
    def login(self,data1):

        html=self.s.post(url=self.url_post,data=data1,headers=self.headers).text
        print(html)
        response =self.s.get("http://activity.renren.com/home#profile")
        print(response.content.decode())
    def run(self):
        # 首先保存js代码
        self.saveJs()
        # 获取get请求的参数data :rkey
        data=self.getHtml(self.url)
        # 构造js代码加密
        password_=self.parersJS(data)
        # 构造post请求参数
        data1 = {
            "phoneNum": "15321210423",
            "password": password_,
            "c1": "0",
            "rKey": data['rkey']
        }
        self.login(data1)
if __name__ == '__main__':
    ren=RenrenL()
    ren.run()