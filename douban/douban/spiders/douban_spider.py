import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']
    # 入口url，扔到调度器中，自己添加后买呢的top250
    start_urls = ['https://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        # 循环电影条目
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")  # 编写Xpath规则
        for i_item in movie_list:
            # 导入item文件
            douban_item = DoubanItem()
            # 写详细的xpath，数据分析
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(
                ".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            douban_item['introduce'] = [" ".join(i.split()) for i in content]
            douban_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
            # 将数据yield到piplines进行数据清洗和存储
            yield douban_item
        # 解析下一页规则，取后一页的xpath
        next_link = response.xpath("//span[@class='next']/link/@href").extract_first()
        if next_link:
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)
