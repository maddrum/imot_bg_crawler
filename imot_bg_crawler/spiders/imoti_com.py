import re
from urllib.parse import urlparse

from scrapy.utils.project import get_project_settings

from imot_bg_crawler.spiders.base_spiders import BaseSpider
from imot_bg_crawler.utils.tools import get_html_tag_text


class ImotiComSpider(BaseSpider):
    name = 'imoti.com'
    allowed_domains = ['imoti.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.start_urls = settings['INPUT_DATA'][self.allowed_domains[0]]

    def parse(self, response, **kwargs):
        items = response.css('.layout1 > .main')
        yield from response.follow_all(items, self.parse_item)
        pages = response.css('.pageNavigation.see_more_last > span > a')
        yield from response.follow_all(pages, self.parse_page)

    def parse_page(self, response):
        items = response.css('div.list > div.item > a')
        yield from response.follow_all(items, self.parse_item)

    def parse_item(self, response):
        url = response.url
        ad_id = urlparse(url).path.split('/')[2]
        metadata_raw = response.css('.params > div:not([class])').getall()
        metadata = {}
        pattern = re.compile(r'<i>(?P<key>.+):</i><span>(?P<value>.+)</span>')
        for item in metadata_raw:
            if '<a' in item:
                continue
            if get_html_tag_text(item) == '':
                continue
            match = pattern.search(item)
            metadata[match.group('key')] = match.group('value')

        price = response.css('.params > div.price > span').get()
        price = get_html_tag_text(price).split('\n')[0].strip()
        descr = response.css('.main > div.info ').get()
        descr = get_html_tag_text(descr).strip()
        address = response.css('.location').get()
        address = get_html_tag_text(address)
        raw_images = response.css('.photoGallery p > img').getall()
        pattern = re.compile(r'src=\"(?P<src>[\d+\w+./]+)\"')
        images = []
        for item in raw_images:
            match = pattern.search(item)
            images.append(f'http:{match.group("src")}')

        self.fill_in_scraped_data(
            ad_id=ad_id,
            url=url,
            descr=descr,
            address=address,
            price=price,
            images=images,
            source=self.allowed_domains[0],
            metadata=metadata
        )

        result = self.generate_result()

        return result
