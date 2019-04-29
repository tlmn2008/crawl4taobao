# -*- coding: utf-8 -*-
import scrapy
import random
from bs4 import BeautifulSoup
import time
from scrapy import Selector
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from taobao_s.tools import data_cleaning,register
from taobao_s.items import TaobaoSItem
#from scrapy_splash import SplashRequest


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    # allowed_domains = ['www.taobao.com']
    base_url = ['https://s.taobao.com/search?q=%E5%84%BF%E7%AB%A5%E6%99%BA%E8%83%BD%E6%89%8B%E8%A1%A8']
    re_headers = {
        'user-agent': '"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"',
        # 'referer': 'https://www.taobao.com/',
        'referer': 'https://detail.tmall.com/',
       # 'accept-encoding': 'gzip, deflate, b',
    }
    i = 1
    cookies = {}

    def start_requests(self):
        # keys = self.settings.get('KEYS')
        self.browser,c_list = register()
        global cookies
        cookies = c_list
        self.cookies = c_list
        self.browser.get(self.base_url[0])#+keys)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        url_i = self.browser.current_url
        html = self.browser.page_source
        # yield SplashRequest(url=self.base_url[0],
        yield scrapy.Request(url=self.base_url[0],
                            callback=self.parse,
                            # args={'wait': '0.5', 'timeout': 3600},
                             meta={'html': html, 'i': self.i, 'url': url_i},
                            cookies=c_list,
                            headers=self.re_headers
                            )

    def parse(self, response):

        time.sleep(1)
        html = response.meta.get('html')
        i = response.meta.get("i")
        url_i = response.meta.get("url")
        main_page_handler = self.browser.window_handles[0]

        # i +=1
        # 当搜索所有结果时改成 1 > 100
        if i > 100:
            return
        try:

            i += 1
            soup = BeautifulSoup(html, 'html.parser')
            products = soup.select('#mainsrp-itemlist > div > div > div > div')
            # n=0
            for product in products:
                # if n > 4:
                #     break
                # n += 1
                item = TaobaoSItem()
                url = "https:"+product.select('a[class="pic-link J_ClickStat J_ItemPicA"]')[0].attrs.get('href','')
                if 'simba' in url:
                    continue
                try:
                    shop_name = product.select('a[class="shopname J_MouseEneterLeave J_ShopInfo"]')[0].get_text().split()[-1]
                except Exception as e:
                    print("$$$ shop name get failed.")
                    print(e)
                try:
                    name = product.select('a[class="J_ClickStat"]')[0].get_text().strip()
                except Exception as e:
                    print("$$$ name get failed.")
                    print(e)
                try:
                    price = product.select('div[class="price g_price g_price-highlight"]')[0].get_text().strip()[1:]
                except Exception as e:
                    print("$$$ price get failed.")
                    print(e)

                brand = None
                type = None
                model = None
                title = None

                self.browser.switch_to.window(main_page_handler)
                goods_page = 'window.open("{}");'.format(url)
                self.browser.execute_script(goods_page)
                time.sleep(3)

                for handle in self.browser.window_handles:
                    if handle != main_page_handler:
                        self.browser.switch_to.window(handle)
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                if 'tmall' in url:
                    mall_name = 'tmall'
                    try:
                        sales = self.browser.find_elements(
                            By.XPATH, '//li[@class="tm-ind-item tm-ind-sellCount"]/*/span[@class="tm-count"]')[0].text
                    except Exception as e:
                        print("$$$ sales get failed.")
                        print(e)

                    for param in self.browser.find_elements(By.XPATH, '//*[@id="J_AttrUL"]/li'):
                        if u'品牌' in param.text:
                            brand = param.text
                        if param.text.startswith(u'型号'):
                            model = param.text
                else:
                    mall_name = 'taobao'
                    try:
                        sales = self.browser.find_elements(By.ID, 'J_SellCounter')[0].text
                    except Exception as e:
                        print("$$$ sales get failed.")
                        print(e)
                    for param in self.browser.find_elements(By.XPATH, '//ul[@class="attributes-list"]/li'):
                        text = param.text
                        if text.startswith(u'品牌'):
                            brand = text
                        if text.startswith(u'型号'):
                            model = text

                self.browser.close()
                item['tmall'] = mall_name
                item['url'] = url
                item['name'] = name
                item['price'] = price
                item['shop_name'] = shop_name
                item['sales'] = sales
                item['title'] = title
                item['type'] = type
                item['brand'] = brand
                item['model'] = model

                yield item

            self.browser.switch_to.window(main_page_handler)
            self.c_url = self.browser.current_url
            time.sleep(4)
            button = self.browser.find_elements(By.XPATH,'//a[@class="J_Ajax num icon-tag"]')[-1]

            button.click()
            time.sleep(random.random()*2)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            html = self.browser.page_source
            # self.url_i = response.url
            yield scrapy.Request(url=self.c_url, headers=self.re_headers, callback=self.parse,
                                meta={'html':html,'i':i,'url':url_i},dont_filter=True,
                                # args={'wait': '0.5', 'timeout': 3600},
                                cookies=self.cookies)#, errback=self.err)

        except Exception as e:
            time.sleep(2)
            print(e)
            self.browser.switch_to.window(main_page_handler)
            self.browser.close()
            self.browser, list = register()
            self.browser.get(url=response.url)
            time.sleep(random.random()*2)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            html = self.browser.page_source
            yield scrapy.Request(url=response.url,headers=self.re_headers,callback=self.parse,
                                meta={'html':html,'i':i,'url':url_i}, dont_filter=True,
                                # args={'wait': '0.5', 'timeout': 3600}
                                 )


    #
    # def parse_detail(self, response):
    #     # item = TaobaoSItem()
    #     item = response.meta.get('result')
    #     brand = 'brand'
    #     type = 'type'
    #     model = 'model'
    #     title = 'title'
    #
    #     soup = BeautifulSoup(response.body, 'html.parser')
    #     # title = response.body
    #     params = soup.find('', {'class': "attributes-list"}).find_all('li')
    #     for param in params:
    #         if str(param.get_text()).startswith('品牌'):
    #             brand = param.get_text()
    #         if str(param.get_text()).startswith('型号'):
    #             model = param.get_text()
    #     url = response.url
    #     tmall = True if 'tmall' in url else False
    #     item['title'] = title
    #     item['type'] = type
    #     item['brand'] = brand
    #     item['model'] = model
    #     yield item

    def close(spider, reason):
        spider.browser.close()
