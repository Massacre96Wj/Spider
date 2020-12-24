# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from qq_music.items import QqMusicItem


class QqMusicPipeline:
    def process_item(self, item, spider):
        return item

class MongoPipline(object):
    """
    保存到Mongo数据库
    """
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
        if isinstance(item, QqMusicItem):
            data = dict(item)
            self.db[item.collection].insert(data)

        return item

    def close_spider(self, spider):
        self.client.close()

class lrcText(object):
    """
    获取的歌词需要清洗
    """

    def __init__(self):
        pass

    def process_item(self, item, spider):
        """
        进行正则匹配获取的单词
        :param item:
        :param spider:
        :return:
        """
        if isinstance(item, QqMusicItem):
            if item.get('lrc'):
                result = re.findall(r'[\u4e00-\u9fa5]+', item['lrc'])
                item['lrc'] = ' '.join(result)
                return item
            else:
                return DropItem('Missing Text')
