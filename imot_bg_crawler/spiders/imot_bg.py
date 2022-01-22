import datetime
import re
from urllib.parse import parse_qs, urlparse

import scrapy
from scrapy.utils.project import get_project_settings

from imot_bg_crawler.utils.tools import get_html_tag_text


class ImotBgSpider(scrapy.Spider):
    name = 'imot.bg'
    allowed_domains = ['imot.bg']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.start_urls = settings['INPUT_DATA'][self.allowed_domains[0]]

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
                metadata[get_html_tag_text(item)] = ''
            else:
                metadata[get_html_tag_text(metadata_raw[index - 1])] = get_html_tag_text(item)
            index += 1

        price = response.css('#cena').get()
        price = get_html_tag_text(price).strip()
        descr_base = response.css('#description_div').get()
        descr_base = get_html_tag_text(descr_base).strip()
        descr_extra = response.css('#dots_less').get()
        descr_extra = get_html_tag_text(descr_extra).strip()
        address = response.css('span[style*="font-size:14px; margin:8px 0; display:inline-block"]').get()
        address = get_html_tag_text(address)
        descr = descr_base + descr_extra
        descr.replace('Виж повече', '')
        descr.replace('Виж по-малко', '')
        images = response.css('a::attr(data-link)').getall()
        images = [f'https:{item}' for item in images if re.search(r'/big/', item) is not None]

        result = {
            ad_id: {
                'url': url,
                'description': descr,
                'address': address,
                'metadata': metadata,
                'price': price,
                'images': images,
                'added': datetime.datetime.now().isoformat(),
                'source': self.allowed_domains[0],
            }
        }

        return result
