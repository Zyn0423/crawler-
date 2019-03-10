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
            item={}
            item['职位名称']=i.xpath("./td/a/text()").extract_first()
            print(item)
        next_=response.xpath("//*[@id='next']/@href").extract_first()
        print(next_)

        if next_ !='javascript:;':
            time.sleep(2)
            url_next='http://hr.tencent.com/'+ next_
            yield scrapy.Request(url=url_next,callback=self.parse)


        pass
