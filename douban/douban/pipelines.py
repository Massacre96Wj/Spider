# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class DoubanPipeline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        data = dict(item)
        self.db[item.collection].insert(data)
        return item

    def close_spider(self, item):
        self.client.close()