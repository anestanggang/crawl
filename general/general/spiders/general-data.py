import scrapy
import csv
import urllib2
import simplejson as json

class generalSpider(scrapy.Spider):
	name = "general-data"
		
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
		#Scrap general
		domain_selector = response.xpath('//html/head/link[@rel="canonical"]/@href').extract_first()
		merchant_status = 'Gold Merchant'
		name_selector = response.xpath('//div[@id="gold-info"]/div/div/a/h1/text()').extract_first()
		opening_date_temp = " ".join(response.xpath('//li[@class="mr-20"]/small/text()').re(r'\w+')).split(' ')
		id_selector = "".join(response.xpath('//input[@id="shop-id"]/@value').extract_first())		
		
		if name_selector is None or opening_date_temp is None:
			name_selector = response.xpath('//div[@class="span10"]/div/div/h1/a/span/text()').extract_first()
			opening_date_temp = " ".join(response.xpath('//div[@id="s_shop_info"]/div/ul/li/text()').re(r'\w+')).split(' ') 
			merchant_status = 'Regular Merchant'
			slogan_2_selector = " ".join(response.xpath('//div[@class="span10"]/div/text()').re(r'\w+'))

		if len(opening_date_temp)>2:
			opening_date_selector = opening_date_temp[2]+" "+opening_date_temp[3]
		else :
			opening_date_selector = " ".join(opening_date_temp)

		slogan_2_selector = response.css('.slogan p small::text').re(r'\w+') 
		slogan_selector = response.css('.shop-slogan::text').re(r'\w+')
		shop_owner_selector = response.xpath('//div[@class="shop-owner-wrapper"]/h3/a/text()').extract_first()
		trans_statistik = " ".join(response.xpath('//div[@class="row-fluid shop-statistics"]/ul/li/div/strong/text()').extract()).split(" ")
		location_selector = response.xpath('//span[@itemprop="location"]/text()').extract_first()

		#Scrap data JSON
		join = "https://js.tokopedia.com/js/shoplogin?id="+ id_selector
		response = urllib2.urlopen(join)
		data = json.load(response)

		yield{		
			'shop_id': id_selector,
			'domain': domain_selector,
			'name_shop': "".join(name_selector),
			'merchant_status': merchant_status,
			'slogan': " ".join(slogan_selector),
			'slogan_2': " ".join(slogan_2_selector),
			'shop_owner': "".join(shop_owner_selector),
			'opening_date': opening_date_selector,
			'location': "".join(location_selector),
			'succes_trans_total': trans_statistik[0],
			'sold_product': trans_statistik[1],
			'total_etalase': trans_statistik[2],
			'total_product': trans_statistik[3],

				#data JSON
			'UID': data['UID'],
			'ItemSoldCount': data['ItemSoldCount'],
			'Timestamp': data['Timestamp'],
			'Responship': data['Responship'],
			'Active': data['Active'],
			'FavoriteCount': data['FavoriteCount'],
		}

