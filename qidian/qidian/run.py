#!/usr/bin/env python

# -*- coding: utf-8 -*-
import time
from scrapy import cmdline

cmd = "scrapy crawl QiDianSpider -s LOG_FILE=./qidian/logs/%f-scrapy.log -s LOG_LEVEL=ERROR" % time.time()
cmdline.execute(cmd.split())