import json

import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import EasybanknoItem
from itemloaders.processors import TakeFirst


class EasybanknoSpider(scrapy.Spider):
	name = 'easybankno'
	start_urls = ["https://www.mynewsdesk.com/services/pressroom/list/6CZMLF3EFRllXIoKobLvSQ/?format=json&offset=0&limit=99999"]

	def parse(self, response):
		data = json.loads(response.text)
		for item in data['items']['item']:
			date = item['published_at']
			title = item['header']
			summary = remove_tags(item['body'])

			item = ItemLoader(item=EasybanknoItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', summary)
			item.add_value('date', date)

			yield item.load_item()
