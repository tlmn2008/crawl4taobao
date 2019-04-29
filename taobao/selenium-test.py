# -*- coding: utf-8 -*-

from taobao_s.tools import data_cleaning,register
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

url = 'https://detail.tmall.com/item.htm?spm=a230r.1.14.183.71566aa2cwOQtg&id=591737862952&ns=1&abbucket=17'
url = 'https://item.taobao.com/item.htm?spm=a230r.1.14.93.71566aa2cwOQtg&id=588753956023&ns=1&abbucket=17#detail'
# browser, c_list = register()
browser = webdriver.FirefoxOptions()
browser = webdriver.Firefox(firefox_options=browser)
browser.get(url)
main_handle = browser.current_window_handle

# js = 'window.open("{}");'.format(url)
# browser.execute_script(js)
# for handle in browser.window_handles:
#     if handle != main_handle:
#         browser.switch_to.window(handle)

wait = WebDriverWait(browser, 6)
try:
    # wait.until(
    #     EC.presence_of_element_located((By.XPATH, '//span[@class="tm-count"]'))
    # )
    time.sleep(3)
    # print(browser.find_elements_by_xpath('//span[@class="tm-count"]')[0].text)
    # for i in browser.find_elements(By.XPATH, '//*[@id="J_AttrUL"]/li'):
    #     if u'品牌' in i.text:
    #         print(i.text)
    # print(browser.find_elements(By.XPATH, '//li[@class="tm-ind-item tm-ind-sellCount"]/div/span[@class="tm-count"]')[0].text)
    # taobao销量
    print(browser.find_elements(By.ID, 'J_SellCounter')[0].text)
    for param in browser.find_elements(By.XPATH, '//ul[@class="attributes-list"]/li'):
        if param.text.startswith(u'品牌'):
            print(param.text)
        if param.text.startswith(u'型号'):
            print(param.text)



except():
    # pass
    print(Exception)
    # browser.close()
finally:
    browser.close()


# print('all handler are {}'.format(browser.window_handles))
# time.sleep(2)
# all_handler = browser.window_handles
# for h in all_handler:
#     if h == main_handle:
#         continue
#     browser.switch_to.window(h)
#     browser.close()
# time.sleep(2)
# browser.switch_to.window(main_handle)

async def abc():
    pass
