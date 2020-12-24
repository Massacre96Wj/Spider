# -*- coding: UTF-8 -*-
"""
@Author ：WangJie
@Date   ：2020/12/1 8:59 
@Desc   ：
"""

from selenium import webdriver
import time
from log import logger

class AutoLogin(object):
    def __init__(self, url):
        self.driver = webdriver.Chrome("../chromedriver.exe")
        self.url = url

    def login(self):
        self.driver.get(self.url)
        self.driver.find_element_by_xpath('//div[@class="u_menu_item"]/a').click()
        time.sleep(2)
        self.driver.find_element_by_class_name('tang-pass-footerBarULogin').click()
        
        time.sleep(1)
        self.driver.find_element_by_id('TANGRAM__PSP_11__userName').send_keys("13772137174")
        self.driver.find_element_by_id('TANGRAM__PSP_11__password').send_keys("**********")
        self.driver.find_element_by_id('TANGRAM__PSP_11__submit').click()

        # 一键签到支持会员
        # time.sleep(5)
        # self.driver.find_element_by_name('onekey_btn').click()
        # time.sleep(1)
        # self.driver.find_element_by_class_name('j_sign_btn sign_btn sign_btn_nonmember').click()

        time.sleep(20)
        url_chi = self.driver.find_elements_by_xpath('//a[@class="u-f-item unsign"]')
        for eve_url in url_chi:
            # print(eve_url.get_attribute('href'))
            eve_url = eve_url.get_attribute('href')
            self.driver.get(eve_url)
            print(self.driver.current_url)
            time.sleep(5)
            self.driver.find_element_by_xpath('//div[@id="signstar_wrapper"]/a').click()
            try:
                self.driver.find_element_by_xpath('//div[@id="signstar_wrapper"]/a').click()
            except Exception as e:
                logger.info(e)
            # 切换窗口
            # self.driver.switch_to.window(self.driver.window_handles(0))
        time.sleep(10)
        self.driver.quit()
if __name__ == '__main__':
    url = 'https://tieba.baidu.com/index.html?traceid=#'
    autoLogin = AutoLogin(url)
    autoLogin.login()

