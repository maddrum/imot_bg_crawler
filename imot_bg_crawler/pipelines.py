# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
import json
import os


class ImotBgCrawlerPipeline:
    filename = None
    file = None
    result = []
    start_time = None

    def open_spider(self, spider):
        self.filename = self.get_results_file()
        self.file = open(self.filename, 'a')
        self.start_time = datetime.datetime.now()

    def get_results_file(self):
        file_path = os.path.dirname(__file__)
        filename = f'result_{datetime.datetime.now().strftime("%d-%m-%Y@%H:%M")}.json'
        return os.path.join(file_path, 'output_files', filename)

    def process_item(self, item, spider):
        self.result.append(item)
        return item

    def close_spider(self, spider):
        end_time = datetime.datetime.now()
        crawled_data = {
            'totalFound': len(self.result),
            'stated': self.start_time.isoformat(),
            'ended': end_time.isoformat(),
            'tookSeconds': (end_time - self.start_time).seconds,

        }
        self.result.append(crawled_data)
        self.file.write(json.dumps(self.result, ensure_ascii=False).encode('utf8').decode())
        self.file.close()
