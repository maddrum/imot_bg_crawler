# To use

1. Create virtual environment for the project using Python 3.8+
2. Install requirements with `pip install -r requirements.txt`
3. Update search URLs in file `./input_files/input.yaml`
   When done, check with `http://www.yamllint.com/` if the input file is okay.
4. Run spider for the desired website. If you do not want logs add `--nolog` in the end of the command
5. When finished, check the `./imot_bg_crawler/output_files` folder for the results.
6. Enjoy.

---

# Spiders

1. Imot.bg - `scrapy crawl imot.bg`
2. Imoti.com - `scrapy crawl imoti.com`'

---

# Settings

`SKIP_EXISTING` - does not save data if already saved, default `True`

`PER_ITEM_RESULT` - saves every item in a separate folder, default `True`

`PER_ITEM_DOWNLOAD_IMAGES` - if PER_ITEM_RESULT is enabled, marks if crawler will download item images, default `True`