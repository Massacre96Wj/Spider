# -*- coding: UTF-8 -*-
"""
@Author ：WangJie
@Date   ：2020/12/1 18:59 
@Desc   ：
"""
import json
import time

import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from log import logger
import os
from tkinter import *

class TaoBaoSpider(object):
    def __init__(self,  url, shop):
        self.url = url
        self.shop = shop
        self.driver = webdriver.Chrome("../chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        self.driver.get(self.url)
        usar_name = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#fm-login-id'))
        )
        usar_name.send_keys("13772137174")
        self.driver.find_element_by_id('fm-login-password').send_keys("415563X@wangjie")
        submit = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-form > div.fm-btn > button'))
        )
        submit.click()
        time.sleep(3)
        index_url = self.driver.find_element_by_xpath('//*[@id="J_SiteNavHome"]/div/a').get_attribute('href')
        self.driver.get(index_url)

    def search(self, shop=None):
        logger.info("开始搜索")
        try:
            # 判断输入框是否加载完成
            input = self.wait.until(
                # (#)表示通过  id    属性来定位元素
                # (.)表示通过 class  属性来定位元素
                EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
            )
            input.send_keys(u'{}'.format(shop))
            submit = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
            )
            submit.click()
            time.sleep(2)
        except TimeoutException as e:
            logger.info(e)
            return self.search(shop)

    def get_shop_info(self, pages):
        products = []
        for _ in range(pages):
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'))
            )
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            items = soup.find('div', class_='m-itemlist').find_all('div', class_='item')
            for item in items:
                product = {
                    'image': item.find('a').find('img')['src'],
                    'price': item.find('div', class_='price g_price g_price-highlight').text.strip(),
                    'num': item.find('div', class_='deal-cnt').text[:-3].strip(),
                    'title': item.find('div', class_='row row-2 title').text.strip(),
                    'location': item.find('div', class_='location').text.strip(),
                }
                # logger.info(product)
                products.append(json.dumps(product))
            try:
                nextPage = self.driver.find_element_by_partial_link_text('下一页')
                nextPage.click()
                time.sleep(.5)
            except Exception as e:
                return
        return products

    def run(self, pages):
        self.login()
        self.search(self.shop)
        products = self.get_shop_info(pages)
        # 退出
        time.sleep(5)
        self.driver.quit()
        return products

def main():
    # shop = input("请输入要搜索的商品名字：")
    shop = entry.get()
    url = 'https://login.taobao.com/'
    taobaoSpider = TaoBaoSpider(url, shop)
    while 1:
        try:
            pages = int(entry1.get())
            break
        except:
            logger.info("输入正整数")
            continue
    products = taobaoSpider.run(pages)
    # for product in products:
    #     text.insert(END, product)
    #     # 文本框滑动
    #     text.see(END)
    #     # 更新
    #     text.update()

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client.spider
    taobao = db.taobao
    for i, product in enumerate(products):
        product = json.loads(product)
        taobao.insert_one(product)

        text.insert(END, "第{}条写入完成".format(i+1))
        # 文本框滑动
        text.see(END)
        # 更新
        text.update()


# 界面
# 1.创建画布
root = Tk()
# 2.标题
root.title("淘宝商品搜索")
# 3.设置大小
root.geometry('560x450+400+200')
# 4.创建标签组件
label = Label(root, text='请输入爬取商品名称：', font=("华文行楷", 20))
# 5.定位标签布局在画面上
label.grid()
# 6.创建输入框组件
entry = Entry(root, font=("隶书", 20))
entry.grid(row=0, column=1)

label1 = Label(root, text='请输入爬取页数：', font=("华文行楷", 20))
label1.grid(row=1, column=0)
entry1 = Entry(root, font=("隶书", 20))
entry1.grid(row=1, column=1)

# 7.列表框
text = Listbox(root, font=("隶书", 16), width=50, height=15)
text.grid(row=2, columnspan=2)
# 8.下载按钮
button1 = Button(root, text='开始下载', font=("隶书", 15), command=main)
button1.grid(row=3, column=0)
button2 = Button(root, text='退出程序', font=("隶书", 15), command=root.quit)
button2.grid(row=3, column=1)
# 显示界面
root.mainloop()
