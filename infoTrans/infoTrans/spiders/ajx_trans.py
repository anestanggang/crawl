from scrapy.http import FormRequest
import scrapy
import json
import re
import csv

class Row_transaksi(scrapy.Item):
	shop_id = scrapy.Field()
	success_trans_1 = scrapy.Field()
	transaksi_detail_1 = scrapy.Field()
	success_trans_2 = scrapy.Field()
	transaksi_detail_2 = scrapy.Field()
	success_trans_3 = scrapy.Field()
	transaksi_detail_3 = scrapy.Field()

class ajxSpider(scrapy.Spider):
	name="ajx_trans"
	def start_requests(self):
		url_list = []
		with open('../Data_tokped_2/Data_Request_Tokopedia_01052017.csv', 'rb') as csvfile:
			data_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in  data_reader:
				join = 'https://www.tokopedia.com/'+ row[0] +'/info'
				url_list.append(join)

		allowed_domain = 'www.tokopedia.com'
		for url in url_list:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self,response):
		id_selector = "".join(response.xpath('//input[@id="shop-id"]/@value').extract_first())
		name_selector = response.xpath('//div[@id="gold-info"]/div/div/a/h1/text()').extract_first()
		url = 'https://www.tokopedia.com/ajax/shop/shop-charts.pl'
		form_data = {'action' : 'get_shop_tx_stats','shop_id' : id_selector}
		yield FormRequest(url, callback=self.parse_info_transaksi, formdata=form_data,meta={'shop_id': id_selector})
		
	def parse_info_transaksi(self,response):
		shop_id = response.request.meta['shop_id']
		res = json.loads(response.body_as_unicode())
		body = res["html"]
		sel = scrapy.Selector(text=body)
		item = Row_transaksi()
		transaksi = sel.xpath('//div[@class="mt-5"]')
		if not transaksi:
			yield{
				'shop_id': shop_id,
				'success_trans_1': 0,
				'transaksi_detail_1': 0,
				'success_trans_2': 0,
				'transaksi_detail_2': 0,
				'success_trans_3': 0,
				'transaksi_detail_3': 0,
			}
		else:
			for trans in transaksi:
				trans_1 = trans.xpath('//div[@class="trans data-trans1 open"]/div/div/p/span/text()').extract_first()
				trans_detail_1 = trans.xpath('//div[@class="trans data-trans1 open"]/div/div[@class="chart-description"]/p/text()').extract_first()
				trans_2 = trans.xpath('//div[@class="trans data-trans2"]/div/div/p/span/text()').extract_first()
				trans_detail_2 = trans.xpath('//div[@class="trans data-trans2"]/div/div[@class="chart-description"]/p/text()').extract_first()
				trans_3 = trans.xpath('//div[@class="trans data-trans3"]/div/div/p/span/text()').extract_first()
				trans_detail_3 = trans.xpath('//div[@class="trans data-trans3"]/div/div[@class="chart-description"]/p/text()').extract_first()
				yield{
					'shop_id': shop_id,
					'success_trans_1': trans_1,
					'transaksi_detail_1': trans_detail_1,
					'success_trans_2': trans_2,
					'transaksi_detail_2': trans_detail_2,
					'success_trans_3': trans_3,
					'transaksi_detail_3': trans_detail_3
				}
