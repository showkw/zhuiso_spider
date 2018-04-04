#!/usr/bin/env python

# -*- coding: utf-8 -*-
import time
from scrapy import cmdline

# 只记录ERROR错误信息
cmd = "scrapy crawl coreSpider -s LOG_FILE=./core/logs/%f-scrapy.log -s LOG_LEVEL=ERROR" % time.time()
cmdline.execute(cmd.split())
