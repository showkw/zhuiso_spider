# -*- coding: utf-8 -*-

# Scrapy settings for yuedu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import datetime
import os


SPIDER_MODULES = ['qidian.spiders']
NEWSPIDER_MODULE = 'qidian.spiders'

# dir = os.path.dirname(os.path.realpath(__file__))
# log_file = '\%s_logs.txt'%str(datetime.date.today())
# if not os.path.exists('%s\logs'%dir):
#     os.mkdir('%s\logs'%dir)
# if not os.path.exists('%s\logs%s'%(dir,log_file)):
#     f = open('%s\logs%s'%(dir,log_file), 'w')
#     f.close()
# LOG_FILE = '%s\logs%s'%(dir,log_file)
#MYSQl
MYSQL_CONFIG = {
    'host':'127.0.0.1',
    'port': 3306,
    'user':'root',
    'pass':'',
    'charset':'utf8',
    'db':'bookSpider'
}

FEED_EXPORT_ENCODING = 'utf-8'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'yuedu (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Pragma':'no-cache',
    'Upgrade-Insecure-Requests':'1'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'yuedu.middlewares.YueduSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   #'yuedu.middlewares.YueduDownloaderMiddleware': 543,
    'Common.Tool.RandomUserAgent': 1
}
DOWNLOAD_TIMEOUT = 5

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
IMAGES_STORE = './imgs/'
# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'qidian.QiDianImagePipeline.QiDianImagePipeline': 1,
    'qidian.QiDianPipeline.QiDianPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
