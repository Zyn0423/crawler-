# -*- coding: utf-8 -*-
import scrapy


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php']

    def parse(self, response):
        data=response.xpath('')
        for i in data:
            item={}
            i.xpath('')

        pass
