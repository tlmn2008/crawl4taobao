# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoSItem(scrapy.Item):
    # define the fields for your item here like:
    tmall = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    sales = scrapy.Field()
    shop_name = scrapy.Field()

