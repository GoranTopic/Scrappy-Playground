# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sqlite3
from itemadapter import ItemAdapter


class MerriamWebsterScraperPipeline:

    def open_spider(self, spider):
        self.file = open('dictionary.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), indent=4, sort_keys=True)
        self.file.write(line)
        return item

