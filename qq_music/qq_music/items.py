# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class QqMusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 数据库表名
    collection = 'qqmusic'
    id = Field()
    # 歌手名字
    singer_name = Field()
    # 歌曲名
    song_name = Field()
    # 歌曲地址
    song_url = Field()
    # 歌词
    lrc = Field()
    # 评论
    comment = Field()
