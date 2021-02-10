import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from raphaelsbank.items import Article


class raphaelsSpider(scrapy.Spider):
    name = 'raphaels'
    start_urls = ['https://www.raphaelsbank.com/news']

    def parse(self, response):
        links = response.xpath('//div[@class="post-news"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//p[@class="date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="container"]//p//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[1:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
