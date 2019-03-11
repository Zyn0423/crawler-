# -*- coding: utf-8 -*-
import scrapy
import time

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php']

    def parse(self, response):
        data=response.xpath("//*[@class='tablelist']//tr")[1:-1]
        "职位类别	人数	地点	发布时间"
        for i in data:
            title=i.xpath("./td/a/text()").extract_first()
            # 获取工作职责：获取url链接并拼接
            urls = 'http://hr.tencent.com/'+i.xpath("./td/a/@href").extract_first()
            #  发送请求回滚到parse_detali方法里
            # meta{} 在不同的解析函数中传递
            yield scrapy.Request(url=urls,callback=self.parse_detali,meta={"title":title})


        # 下一页
        next_=response.xpath("//*[@id='next']/@href").extract_first()

        if next_ !='javascript:;':
            time.sleep(2)
            url_next='http://hr.tencent.com/'+ next_
            yield scrapy.Request(url=url_next,callback=self.parse)


        pass

    def parse_detali(self,response):
        item={}
        # 从meta中取出传递的内容
        item['职位类别']=response.meta['title']
        item['工作职责']=response.xpath("//*[@class='squareli']//text()").extract()
        print(item)
        pass