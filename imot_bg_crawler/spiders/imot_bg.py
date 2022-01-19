import datetime
import re
from urllib.parse import parse_qs, urlparse

import scrapy
from bs4 import BeautifulSoup

from imot_bg_crawler.input_files.imot_bg_spider import URLS


class ImotBgSpider(scrapy.Spider):
    name = 'imot.bg'
    allowed_domains = ['imot.bg']
    start_urls = URLS

    @staticmethod
    def get_text(text):
        soup = BeautifulSoup(text)
        return soup.get_text()

    def parse(self, response, **kwargs):
        items = response.css('.lnk2')
        yield from response.follow_all(items, self.parse_item)
        pages = response.css('a.pageNumbers')
        yield from response.follow_all(pages, self.parse_page)

    def parse_page(self, response):
        items = response.css('.lnk2')
        yield from response.follow_all(items, self.parse_item)

    def parse_item(self, response):
        url = response.url
        ad_id = parse_qs(urlparse(url).query).get('adv')[0]
        metadata_raw = response.css('div[style*="inline-block; float:left; margin-top:15px;"] > ul >li').getall()
        metadata = {}
        index = 0
        for item in metadata_raw:
            if index % 2 == 0:
                metadata[self.get_text(item)] = ''
            else:
                metadata[self.get_text(metadata_raw[index - 1])] = self.get_text(item)
            index += 1

        price = response.css('#cena').get()
        price = self.get_text(price).strip()
        descr_base = response.css('#description_div').get()
        descr_base = self.get_text(descr_base).strip()
        descr_extra = response.css('#dots_less').get()
        descr_extra = self.get_text(descr_extra).strip()
        descr = descr_base + descr_extra
        descr.replace('Виж повече', '')
        descr.replace('Виж по-малко', '')
        images = response.css('a::attr(data-link)').getall()
        images = [f'https:{item}' for item in images if re.search(r'/big/', item) is not None]

        result = {
            ad_id: {
                'url': url,
                'description': descr,
                'metadata': metadata,
                'price': price,
                'images': images,
                'added': datetime.datetime.now().isoformat(),
            }
        }

        return result
