# -*- coding: utf-8 -*-
import scrapy
import json

class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    allowed_domains = ['list.jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']
    # "https://book.jd.com/booksort.html"
    # 抓取京东图书包含图书的名字、封面图片地址、图书url地址、
    # 作者、出版社、出版时间、价格、
    # 图书所属大分类、图书所属小的分类、分类的url地址

    def parse(self, response):
        dl_data=response.xpath('//div[@class="mc"]/dl/dt')
        for i in dl_data:
            # 大标题
            item={}
            item['big_']=i.xpath('./a/text()').extract_first()
            # url
            item['Big_url']=i.xpath('./a/@href').extract_first()
            # 兄弟节点
            em_list=i.xpath('./following-sibling::*[1]/em')
            for em in em_list:
                item['em_text']=em.xpath('./a/text()').extract_first()
                item['em_url']='https:'+em.xpath('./a/@href').extract_first()
                "https://list.jd.com/list.html?cat=1713,3258,3297&tid=3297"
                "//list.jd.com/1713-11745-11757.html"
                # 拼接uRL
                # next_url='https:'+item['em_url']
                yield scrapy.Request(item['em_url'],callback=self.parse_books,meta={'item':item})
                # yield scrapy.Request(item['em_url'], callback=self.parse_books)
                # print(item)
    def parse_books(self,response):

        item=response.meta.get('item')
        # print(item)
        # exit()
        # 抓取京东图书包含图书的名字、封面图片地址、图书url地址
        # 作者、出版社、出版时间、价格、
        "//*[@id='plist']/ul/li[1]/div/div[3]/a/em/text()"#图书的名字
        "//*[@id='plist']/ul/li[1]/div/div[1]/a/@href"#  图书url地址
        "//*[@id='plist']/ul/li[1]/div/div[1]/a/img/@src"#封面图片地址
        "//*[@id='plist']/ul/li[1]/div/div[4]/span[1]/span/a"#作者
        "//*[@id='plist']/ul/li[1]/div/div[4]/span[2]/a" #出版社
        "//*[@id='plist']/ul/li[1]/div/div[4]/span[3]" #出版时间
        "//*[@id='plist']/ul/li[1]/div/@data-sku"#价格
        """
        {'name': '\n                中国科幻基石丛书：三体（套装1-3册）      ',
        'book_img_url': '//img14.360buyimg.com/n7/jfs/t1705/189/702227414/177982/cc8c12f0/55dab54dN5271c377.jpg',
        'book_store': '重庆出版社',
        'book_time':    ',
        'book_author_type': ' 刘慈欣 ',
        'book_url': '//item.jd.com/11757834.html',
        'price': '11757834'}

        """
        data_li=response.xpath("//*[@id='plist']/ul//li")
        for data_div in data_li:
            # item={}
            "//*[@id='plist']/ul//li//div[@class='p-name']/a/em/text()"
            item['name']=data_div.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()
            item['book_url']=data_div.xpath('.//div[@class="p-img"]/a/@href').extract_first()
            item['book_img_url']=data_div.xpath(".//div[@class='p-img']/a/img/@src").extract_first()
            item['book_time']=data_div.xpath('.//div[@class="p-bookdetails"]/span[3]/text()').extract_first().strip()
            item['book_store'] = data_div.xpath('.//div[@class="p-bookdetails"]/span[2]/a/text()').extract_first()
            item['book_author_type'] = data_div.xpath('.//div[@class="p-bookdetails"]/span[1]/span/a/text()').extract_first()
            item['price_url']='https://p.3.cn/prices/mgets?skuIds=J_'+data_div.xpath('.//div/@data-sku').extract_first()
            yield scrapy.Request(item['price_url'],callback=self.parse_price,meta={'item':item})



        next_data=response.xpath('//*[@id="J_bottomPage"]/span[1]/a[10]/@href').extract_first()
        if next_data != None:
            next_url="https://list.jd.com/"+next_data
            yield scrapy.Request(next_url,callback=self.parse_books,meta={'item':item})

        pass
    def parse_price(self,response):
        item=response.meta.get('item')
        item['book_price']=json.loads(response.body.decode())[0]['op']
        """
        {'big_': '小说', 'book_img_url': None, 'em_text': '期刊杂志',
        'em_url': 'https://list.jd.com/1713-3258-3321.html',
        'book_price': '37.60',
        'price_url': 'https://p.3.cn/prices/mgets?skuIds=J_10204084',
        'book_store': '江西
        'book_author_type': ' 柯兴 ',
        'name': '秘密战',
        'book_url': '//item.jd.com/10204084.html',
        'Big_url': '//channel.jd.com/1713-3258.html',
        'book_time': '\n        2009-11      '}

        """

        print(item)
        yield item