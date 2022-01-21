import datetime
import json
import os
import shutil

import requests
from scrapy.exceptions import DropItem
from slugify import slugify

from .settings import PER_ITEM_DOWNLOAD_IMAGES, PER_ITEM_RESULT, SKIP_EXISTING


class ImotBgCrawlerPipeline:
    results_file = None
    start_time = None
    output_path = None
    result = []
    existing_items = []

    @staticmethod
    def get_filename(prefix='result_'):
        return f'{prefix}{datetime.datetime.now().strftime("%d-%m-%Y@%H:%M")}.json'

    @staticmethod
    def get_item_dir_name(item):
        item_id = list(item)[0]
        folder_name = f'{slugify(item[item_id]["address"].split(",")[-1].strip())}_{item_id}'
        return folder_name

    def check_existing(self, item):
        folder_name = self.get_item_dir_name(item)
        absolute_folder = os.path.join(self.output_path, folder_name)
        return os.path.isdir(absolute_folder)

    def get_all_results_file(self):
        file_path = os.path.dirname(__file__)
        filename = self.get_filename()
        self.output_path = os.path.join(file_path, 'output_files')
        return os.path.join(self.output_path, filename)

    def get_create_item_dir(self, item):
        folder_name = self.get_item_dir_name(item)
        filepath = os.path.join(self.output_path, folder_name)
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
        return filepath

    def write_item_result_file(self, item):
        item_id = list(item)[0]
        filename = self.get_filename(prefix=f'ad-id_{item_id}_result_')
        filepath = self.get_create_item_dir(item)
        absolute_filename = os.path.join(filepath, filename)
        with open(absolute_filename, 'w') as file:
            file.write(json.dumps(item, ensure_ascii=False).encode('utf8').decode())
            file.close()

    def download_item_pictures(self, item):
        image_dir = os.path.join(self.get_create_item_dir(item), 'images')
        if not os.path.isdir(image_dir):
            os.makedirs(image_dir)
        ad_id = list(item)[0]
        images = item[ad_id]['images'] if item[ad_id].get('images') is not None else []
        for counter, image_url in enumerate(images):
            r = requests.get(image_url, stream=True)
            if r.status_code == 200:
                filepath = os.path.join(image_dir, f'image_{counter}.png')
                with open(filepath, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    f.close()

    def open_spider(self, spider):
        filename = self.get_all_results_file()
        self.results_file = open(filename, 'a')
        self.start_time = datetime.datetime.now()

    def process_item(self, item, spider):
        if SKIP_EXISTING and self.check_existing(item):
            self.existing_items.append(item)
            raise DropItem(f'Item id: {list(item)[0]} already scrapped, skipping...')
        self.result.append(item)
        if PER_ITEM_RESULT:
            self.write_item_result_file(item)
            if PER_ITEM_DOWNLOAD_IMAGES:
                self.download_item_pictures(item)
        return item

    def close_spider(self, spider):
        end_time = datetime.datetime.now()
        dropped_data = [list(item)[0] for item in self.existing_items]
        crawled_data = {
            'total_found': len(self.result),
            'existing_number': len(dropped_data),
            'existing_ids': dropped_data,
            'stated': self.start_time.isoformat(),
            'ended': end_time.isoformat(),
            'tookSeconds': (end_time - self.start_time).seconds,
        }
        self.result.append(crawled_data)
        self.results_file.write(json.dumps(self.result, ensure_ascii=False).encode('utf8').decode())
        self.results_file.close()
