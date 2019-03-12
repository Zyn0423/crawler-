# -*- coding: utf-8 -*-
import scrapy
import time
# from tenxun.items import BossItem
import traceback
class BossSpider(scrapy.Spider):
    name ='Boss'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=Python']

    def parse(self, response):
        data=response.xpath("//*[@class='job-list']/ul//li")
        "职位类别	人数	地点	发布时间"
        for i in data:
            # "//*[@class='job-list']/ul//li/div/div[2]/div/h3/a/text()"
            title=i.xpath("./div/div[2]/div/h3/a/text()").extract_first()
            # 获取工作职责：获取url链接并拼接
            #  发送请求回滚到parse_detali方法里
            # meta{} 在不同的解析函数中传递
            urls = 'https://www.zhipin.com/'+i.xpath("./div/div[2]/div/h3/a/@href").extract_first()
            yield scrapy.Request(url=urls,callback=self.parse_detali,meta={'title':title})
        next_=response.xpath('//*[@id="main"]/div/div[3]/div[2]/a[5]/@href').extract_first()
        try:
            if next_ !="javascript:;":
                url_next='https://www.zhipin.com/'+next_
                time.sleep(2)
                yield scrapy.Request(url=url_next,callback=self.parse)
        except :
            print(next_)
            traceback.format_exc()

    def parse_detali(self,response):
        item={}
        item['title']=response.meta.get('title')
        item['intro']=response.xpath('//*[@id="main"]/div[3]/div/div[2]/div/div[1]/div/text()').extract()
        yield item
        pass


    # def parse_detali(self,response):
    #     item=TenxunItem()
    #     # 从meta中取出传递的内容
    #     item['title']=response.meta['title']
    #     item['workeduty']=response.xpath("//*[@class='squareli']//text()").extract()
    #     pass