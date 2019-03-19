# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider
# from scrapy.linkextractor import LinkExtractor   链接提取器

import re
class DangdangSpider(RedisCrawlSpider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://book.dangdang.com/']
    redis_key = 'dangdang_start_url'
    # redis_key='start_urls　'
    # 在redis中lpush dangdang_start_url 'http://book.dangdang.com/'

    def parse(self, response):

        """
        抓取当当图书又有图书的名字、封面图片地址、图书url地址、作者、出版社、出版时间、价格、图书所属大分类、图书所属小的分类、分类的url地址
        """
        # 大分类
        # with open('t.html','w') as f:
        #     f.write(response.body.decode('gbk'))
        level_data=response.xpath('//dl/dd')
        "/dl/dt/span/text()"
        for i in level_data:
            item={}
            item['span_data']=i.xpath('./a/text()').extract_first()
            if item['span_data'] is not None:
               item['href']=i.xpath('./a/@href').extract_first()
               # item['data']=re.findall(r"(.*html$)",item['href'])
               # print(item['data'])

               yield scrapy.Request(url=item['href'],callback=self.parse_books,meta={'item':item})


    def parse_books(self,response):
        item=response.meta.get('item')
        html_data=response.xpath("//ul[@class='bigimg']//li")
        print(len(html_data))
        if len(html_data) is not 0:
            for i in html_data:
                item['book_name']=i.xpath("./p[@class='name']/a/text()").extract_first()
                item['price']=i.xpath("./p[@class='price']/span[@class='search_now_price']/text()").extract_first()
                item['name']=i.xpath("./p[@class='search_book_author']/span[1]/a/text()").extract_first()
                item['search_star_line']=i.xpath("./p[@class='search_star_line']/a/text()").extract_first() #评价
                print(item)

            # 拼接ＵＲＬ　　因为没有下一页，找规律每个网页都是１００页
            "http://category.dangdang.com/pg2-cp01.18.01.00.00.00.html"
            url="http://category.dangdang.com"
            # 获取网页请求第二页的参数，并替换２，{}
            next_params=response.xpath("//*[@id='12810']/div[3]/div[2]/div/ul/li[3]/a/@href").extract_first()
            # 新的ＵＲＬ
            if next_params is not None:
                new_next_=next_params.replace('2-','{}-')
                for i in range(2,101):
                    url_next=url+new_next_.format(i)
                    yield scrapy.Request(url=url_next,callback=self.parse_books,meta={'item':item})

