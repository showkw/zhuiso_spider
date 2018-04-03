# -*- coding: utf-8 -*-
# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
from Config.DataBaseConfig import MYSQL_CONFIG,REDIS_CONFIG

COMMANDS_MODULE = 'FirstChapter.commands'
SPIDER_MODULES = ['FirstChapter.spiders']
NEWSPIDER_MODULE = 'FirstChapter.spiders'

FEED_EXPORT_ENCODING = 'utf-8'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY=0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

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
    'Common.Tool.RandomUserAgent':1
}
DOWNLOAD_TIMEOUT = 5

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
    'FirstChapter.extensions.RedisSpiderSmartIdleClosedExensions': 500,
}

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#使用scrapy_redis.scheduler调度
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = {
   'FirstChapter.FirstChapterPipelines.MySQLPipeline': 1,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

LOG_LEVEL = 'ERROR'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
# DOWNLOAD_DELAY =

#MYSQL
MYSQL_HOST = MYSQL_CONFIG['default']['host']
MYSQL_PORT = MYSQL_CONFIG['default']['port']
MYSQL_DBNAME = MYSQL_CONFIG['default']['db']
MYSQL_USER = MYSQL_CONFIG['default']['user']
MYSQL_PASSWD = MYSQL_CONFIG['default']['pass']
MYSQL_CHARSET = MYSQL_CONFIG['default']['charset']

#Redis
# Specify the full Redis URL for connecting (optional).
# If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
REDIS_URL = 'redis://root:'+REDIS_CONFIG['default']['pass']+'@'+REDIS_CONFIG['default']['host'] +':'+REDIS_CONFIG['default']['port']
# Specify the host and port to use when connecting to Redis (optional).
# REDIS_HOST = '127.0.0.1'
# REDIS_PORT = 6379
#REDIS_PASS = '19940225'

# REDIRECT_ENABLED = True

HTTPERROR_ALLOWED_CODES = [302, 301]

DEPTH_LIMIT = 3

MYEXT_ENABLED = True  # 开启扩展
IDLE_NUMBER = 360  # 配置空闲持续时间单位为 360个 ，一个时间单位为5s
