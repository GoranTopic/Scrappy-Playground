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
        self.error_file = open('errored_words.json', 'w')

    def close_spider(self, spider):
        self.file.close()
        self.error_file.close()

    def process_item(self, item, spider):
        item = ItemAdapter(item)
        if item['word'] is None:
        # if word could not be extracted wirte to errored file
            line = json.dumps(item.asdict(), indent=4, sort_keys=True)
            self.error_file.write(line)
        elif item['definitions'] is None:
        # if definition could not be extracted write to errored file
            line = json.dumps(item.asdict(), indent=4, sort_keys=True)
            self.error_file.write(line)
        else:
            # write to normal file
            line = json.dumps(item.asdict(), indent=4, sort_keys=True)
            self.file.write(line)
        return item

