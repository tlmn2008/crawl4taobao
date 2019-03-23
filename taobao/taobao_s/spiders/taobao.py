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
from scrapy_splash import SplashRequest


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    # allowed_domains = ['www.taobao.com']
    base_url = ['https://s.taobao.com/search?q=']
    base_url = ['https://s.taobao.com/search?q=%E5%84%BF%E7%AB%A5%E6%99%BA%E8%83%BD%E6%89%8B%E8%A1%A8']
    pages = 100
    re_headers = {
        'user-agent': '"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"',
        'referer': 'https://www.taobao.com/',
        'accept-encoding': 'gzip, deflate, b',
    }
    i = 1

    def start_requests(self):
        keys = self.settings.get('KEYS')
        self.browser,list = register()
        self.browser.get(self.base_url[0])#+keys)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        url_i = self.browser.current_url
        html = self.browser.page_source
        # yield scrapy.Request(url=self.base_url[0], headers=self.re_headers,callback=self.parse,meta={'html':html,'i':self.i,'url':url_i}) #,cookies=list
        yield SplashRequest(url=self.base_url[0],
                            # headers=self.re_headers,
                            callback=self.parse,
                            args={'wait': '0.5'},
                             meta={'html': html, 'i': self.i, 'url': url_i}
                            )

    def parse(self, response):

        # # num = list.select('div[class="deal-cnt"]')[0].get_text()
        # soup = BeautifulSoup(response.body, 'html.parser')
        # print("$$$$$$$$$$$$$$$$$$$$$")
        # a = soup.find_all(attrs={'class': 'tm-count'})  # .get_text())#.strip()
        # print(a)
        # return a

        time.sleep(5)
        html = response.meta.get('html')
        i = response.meta.get("i")
        url_i = response.meta.get("url")
        # i +=1
        # 当搜索所有结果时改成 1 > 100
        if i > 1:
            return
        try:
            i += 1
            soup = BeautifulSoup(html,'html.parser')
            lists = soup.select('#mainsrp-itemlist > div > div > div > div')

            for list in lists:

                url = list.select('a[class="pic-link J_ClickStat J_ItemPicA"]')[0].attrs.get('href','')
                if 'simba' in url:
                    continue
                yield SplashRequest(url="https:"+ url, callback=self.parse_detail)
                break
            time.sleep(10)
            button = self.browser.find_elements(By.XPATH,'//a[@class="J_Ajax num icon-tag"]')[-1]

            button.click()
            time.sleep(random.random()*2)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            html = self.browser.page_source
            yield SplashRequest(url=response.url,headers=self.re_headers,callback=self.parse,meta={'html':html,'i':i,'url':url_i},dont_filter=True)#, errback=self.err)

        except Exception as e:
            time.sleep(2)
            print(e)
            self.browser.close()
            self.browser,list = register()
            self.browser.get(url=url_i)
            time.sleep(random.random()*2)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            html = self.browser.page_source
            yield SplashRequest(url=response.url,headers=self.re_headers,callback=self.parse,meta={'html':html,'i':i,'url':url_i},dont_filter=True)

    def parse_detail(self, response):

        soup = BeautifulSoup(response.body, 'html.parser')

        url = response.url
        tmall = True if 'tmall' in url else False
        title = ''.join(response.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[1]/h1/text()').extract()).strip()
        sales = soup.find_all(attrs={'class':'tm-count'})[0].get_text()
        shop_name = soup.select('a[class="slogo-shopname"] strong')[0].get_text()

        brand = 'brand'
        params = soup.find(attrs={'id': 'J_AttrUL'})
        for param in params:
            print("DDDDDDDDDDDDDDDDDDDDDDDDDD")
            print(param)
            print(type(param))
            # if '品牌' in param.text():
            #     brand = param.text()

        type = 'type'
        model = 'model'
        name = 'name'
        price = 'price'

        item = TaobaoSItem()
        item['tmall'] = tmall
        item['url'] = url
        item['title'] = title
        item['type'] = type
        item['brand'] = brand
        item['model'] = model
        item['name'] = name
        item['price'] = price
        item['sales'] = sales
        item['shop_name'] = shop_name
        yield item

    def close(spider, reason):
        spider.browser.close()
