# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TaobaoSPipeline(object):
    def open_spider(self,spider):
        self.f = open('淘宝店铺数据.txt','w')
    def process_item(self, item, spider):
        data = {}
        data['tmall'] = item['tmall']
        data['url'] = item['url']
        data['title'] = item['title']
        data['type'] = item['type']
        data['brand'] = item['brand']
        data['model'] = item['model']
        data['name'] = item['name']
        data['price'] = item['price']
        data['sales'] = item['sales']
        data['shop_name'] = item['shop_name']
        self.f.write(str(data)+'\n')
        return item
    def close_spider(self,spider):
        self.f.close()
