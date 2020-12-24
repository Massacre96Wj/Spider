# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'douban_movie'
    # 序号
    serial_number = Field()
    # 电影名称
    movie_name = Field()
    # 电影介绍
    introduce = Field()
    # 电影星级
    star = Field()
    # 电影的评论
    evaluate = Field()
    # 电影描述
    describe = Field()
