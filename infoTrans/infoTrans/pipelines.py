# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class InfotransPipeline(object):
	def open_spider(self,spider):
		self.file = open('item-trans-req-010717.json','wb')

	def close_spider(self,spider):
		self.file.close()
	def process_item(self, item, spider):
		line = json.dumps(dict(item))
		self.file.write(line)
		self.file.write(',')
		self.file.write('\n')
		return item
