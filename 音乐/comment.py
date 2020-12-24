# -*- coding: UTF-8 -*-
"""
@Author ：WangJie
@Date   ：2020/11/30 17:55
@Desc   ：
"""

import time
from selenium import webdriver
from log import logger

class YunSpider(object):
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome("../chromedriver.exe")

    def get_content(self, pages):
        self.driver.get(self.url)
        # 先进入Iframe
        self.driver.switch_to.frame(0)
        js = "window.scrollBy(0, 8000)"
        self.driver.execute_script(js)

        # 翻页
        for _ in range(pages):
            selectors = self.driver.find_elements_by_xpath('//div[@class="cmmts j-flag"]/div')
            for selector in selectors:
                comment = selector.find_element_by_xpath('.//div[@class="cnt f-brk"]').text
                # logger.info(comment)
                self.saveData(comment)
                # YunSpider.saveData(comment)
            # 获取下一页
            # 获取文本链接，模糊匹配
            nextPage = self.driver.find_element_by_partial_link_text('下一页')
            nextPage.click()
            time.sleep(.5)

    @staticmethod
    def saveData(text):
        with open('comments.txt', 'a', encoding="utf-8") as f:
            f.write(text + '\n')

if __name__ == '__main__':
    url = "https://music.163.com/#/song?id=1495058484"
    yunSpider = YunSpider(url)
    yunSpider.get_content(5)