### scrapy搭建的豆瓣电影爬虫框架，爬取前250个电影
`scrapy stratproject douban`

`scrapy genspider douban_spider movie.douban.com`

`scrapy crawl douban_spider -o result.csv`

`scrapy crawl douban_spider`
