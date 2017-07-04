from scrapy.http import FormRequest
import scrapy
import json
import re
import csv

class Row_satisfaction(scrapy.Item):
	shop_id = scrapy.Field()
	positif_1 = scrapy.Field()
	positif_2 = scrapy.Field()
	positif_3 = scrapy.Field()
	netral_1 = scrapy.Field()
	netral_2 = scrapy.Field()
	netral_3 = scrapy.Field()
	negative_1 = scrapy.Field()
	negative_2 = scrapy.Field()
	negative_3 = scrapy.Field()

class ajxSpider(scrapy.Spider):
	name="ajx_sat"
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
		form_data = {'action' : 'get_shop_satisfaction','shop_id' : id_selector}
		yield FormRequest(url, callback=self.parse_info_satisfaction, formdata=form_data,meta={'shop_id': id_selector})

	def parse_info_satisfaction(self,response):
		shop_id = response.request.meta['shop_id']
		res = response.body_as_unicode()
		res_proces = res.replace("\'"," ")
		res_out = json.loads(res_proces)
		body = res_out['html']
		sel = scrapy.Selector(text=body)

		item = Row_satisfaction()
		satisfaction = sel.css('table tbody')
		for s in satisfaction:
			item = Row_satisfaction()
			temp = s.css('tr td::text').extract()
			yield{
				'shop_id': shop_id,
				'positif_1': temp[0],
				'positif_2': temp[1],
				'positif_3': temp[2],
				'netral_1': temp[3],
				'netral_2': temp[4],
				'netral_3': temp[5],
				'negative_1': temp[6],
				'negative_2': temp[7],
				'negative_3': temp[8]			
			}
