BOT_NAME = 'imot_bg_crawler'

SPIDER_MODULES = ['imot_bg_crawler.spiders']
NEWSPIDER_MODULE = 'imot_bg_crawler.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
    'imot_bg_crawler.pipelines.ImotBgCrawlerPipeline': 300,
}

# PIPELINE_SETTINGS
SKIP_EXISTING = True
PER_ITEM_RESULT = True
PER_ITEM_DOWNLOAD_IMAGES = True
