# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider

import re
class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://book.dangdang.com/']
    # redis_key='start_urls　'

    def parse(self, response):

        """
        抓取当当图书又有图书的名字、封面图片地址、图书url地址、作者、出版社、出版时间、价格、图书所属大分类、图书所属小的分类、分类的url地址
        """
        # 大分类
        "//div[@class='level_one']/dl/dt/span/text()"
        "//div[@class='level_one']//dl/dt/a"
        """
        特价
        网络文学
        小说
        文艺
        经管
        """
        "//div[@class='level_one']//dl/dd/a"
        """
        清华附小推荐书单
        一年级课外阅读书单
        二年级课外阅读书单
        凯迪克奖获奖作品
        致敬大师-林明子温暖绘本
        给新手爸妈的入门图画书
        纽伯瑞奖获奖作品
        图画书之后读什么？--桥梁书
        二胎时代孩子们需要的书
        央视《朗读者》第二季书单
        """
        "//div[@class='level_one']//dl/dd/a/@href"
        """
        http://baby.dangdang.com/20170721_pby5
        http://store.dangdang.com/gys_0016010_emrs
        """
        # with open('t.html','w') as f:
        #     f.write(response.body.decode('gbk'))
        level_data=response.xpath('//dl/dd')
        "/dl/dt/span/text()"
        print(len(level_data))
        for i in level_data:
            item={}
            item['span_data']=i.xpath('./a/text()').extract_first()
            if item['span_data'] is not None:
               item['href']=i.xpath('./a/@href').extract_first()
               "        tlt = re.findall(r'\"raw_title\"\:\".*?\"', HTml)"
               item['data']=re.findall(r"(.*html$)",item['href'])
               print(item)