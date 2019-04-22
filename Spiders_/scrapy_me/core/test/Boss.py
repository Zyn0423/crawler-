from Spiders_.scrapy_me.core.spider import Spider
from Spiders_.scrapy_me.http.request import Request

import traceback
class BossSpider(Spider):
    name ='Boss'
    # allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=Python']

    def parse(self, response):
        data=response.xpath("//*[@class='job-list']/ul//li")
        print(len(data))
        "职位类别	人数	地点	发布时间"
        for i in data:
            # "//*[@class='job-list']/ul//li/div/div[2]/div/h3/a/text()"
            title=i.xpath("./div/div[2]/div/h3/a/text()")[0]
            # print(title)
            # 获取工作职责：获取url链接并拼接
            #  发送请求回滚到parse_detali方法里
            # meta{} 在不同的解析函数中传递
            urls = 'https://www.zhipin.com/'+i.xpath("./div/div[2]/div/h3/a/@href")[0]
            # print(urls)
            yield Request(url=urls,parse='parse_detali',meta=title)
        next_=response.xpath('//div[@class="page"]/a[5]/@href')[0]
        try:
            if next_ !="javascript:;":
                url_next='https://www.zhipin.com/'+next_
                yield Request(url=url_next,parse='parse')
        except :
            print(next_)
            traceback.format_exc()

    def parse_detali(self,response):
        item={}
        item['title']=response.meta
        item['intro']=response.xpath('//*[@id="main"]/div[3]/div/div[2]/div/div[1]/div/text()')[0]
        print(item)
        yield item
