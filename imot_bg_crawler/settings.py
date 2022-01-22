import os

import yaml

BOT_NAME = 'imot_bg_crawler'

SPIDER_MODULES = ['imot_bg_crawler.spiders']
NEWSPIDER_MODULE = 'imot_bg_crawler.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
    'imot_bg_crawler.pipelines.ImotBgCrawlerPipeline': 300,
}

BASE_PATH = os.path.dirname(__file__)
INPUT_FILE = os.path.join(BASE_PATH, 'input.yaml')
with open(INPUT_FILE, 'r') as input_file:
    INPUT_DATA = yaml.load(input_file, Loader=yaml.FullLoader)
    input_file.close()

# PIPELINE_SETTINGS
SKIP_EXISTING = True
PER_ITEM_RESULT = True
PER_ITEM_DOWNLOAD_IMAGES = True
