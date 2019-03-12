# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from pymongo import MongoClient
class TenxunPipeline(object):
    """将数据保存到文件"""
    def open_spider(self,spider):
        if spider.name == 'tencent':
            self.f=open('tencent.json','w+')
        if spider.name =='Boss':
            self.f1=open('Boss.json','w+')

    def process_item(self, item, spider):
        print(item)
        if spider.name == 'tencent':
            self.f.write(json.dumps(item)+'\n')
        if spider.name =='Boss':
            self.f1.write(json.dumps(item)+'\n')
            return item
    def close_spider(self,spider):
        if spider.name == 'tencent':
            self.f.close()
        if spider.name =='Boss':
            self.f1.close()
        pass
#
class MongoPipeline(object):
    def open_spider(self,spider):
        client=MongoClient()
        self.collection=client.test.data

    def process_item(self,item,spider):
        self.collection.inseat(item)
