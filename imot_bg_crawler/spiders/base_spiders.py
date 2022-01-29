import datetime
from dataclasses import asdict

import scrapy

from imot_bg_crawler.items import CommonData, MetaData


class BaseSpider(scrapy.Spider):
    scpraped_data = {
        'ad_id': None,
        'url': None,
        'descr': None,
        'address': None,
        'price': None,
        'images': None,
        'source': None,
        'metadata': None,
    }

    def generate_result(self):
        common_data_obj = CommonData(
            url=self.scpraped_data.get('url'),
            description=self.scpraped_data.get('descr'),
            address=self.scpraped_data.get('address'),
            price=self.scpraped_data.get('price'),
            images=self.scpraped_data.get('images'),
            added=datetime.datetime.now().isoformat(),
            source=self.scpraped_data.get('source'),
        )
        metadata_obj = MetaData(metadata=self.scpraped_data.get('metadata'))

        result = {
            self.scpraped_data.get('ad_id'): {
                **asdict(metadata_obj),
                **asdict(common_data_obj),
            }
        }
        return result

    def fill_in_scraped_data(self, ad_id, url, descr, address, price, images, source, metadata):
        self.scpraped_data['ad_id'] = ad_id
        self.scpraped_data['url'] = url
        self.scpraped_data['price'] = price
        self.scpraped_data['descr'] = descr
        self.scpraped_data['address'] = address
        self.scpraped_data['images'] = images
        self.scpraped_data['source'] = source
        self.scpraped_data['metadata'] = metadata
