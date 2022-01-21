To use:

1. Create virtual environment for the project using Python 3.8+
2. Install requirements with `pip install -r requirements.txt`
3. Update search `URLS` in file `./input_files/imot_bg_spider.py`
   `URLS` are obtained by visiting imot.bg and perform a search with your criteria. 
   Could have as many searches as you wish.
4. Run spider with `scrapy crawl imot.bg`. If you do not want logs run with `scrapy crawl imot.bg --nolog`
5. When finished, check the `./imot_bg_crawler/output_files` folder for the results.
6. Enjoy.

Settings

`SKIP_EXISTING` - does not save data if already saved, default `True`

`PER_ITEM_RESULT` - saves every item in a separate folder, default `True`

`PER_ITEM_DOWNLOAD_IMAGES` - if PER_ITEM_RESULT is enabled, marks if crawler will download item images, default `True`