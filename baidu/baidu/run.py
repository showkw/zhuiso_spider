# -*- coding: utf-8 -*-
import time
from scrapy import cmdline

cmd = "scrapy crawl bdSpider -s LOG_FILE=./baidu/logs/Bd-%f.log -s LOG_LEVEL=ERROR" % time.time()
cmdline.execute(cmd.split())