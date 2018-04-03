#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Common.Db import Db
import redis
import os
from scrapy.http import Request
from Config.DataBaseConfig import REDIS_CONFIG
from Config.Config import RUNTIME_DIR
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import CrawlSpider
import sys

# 兼容3与2.7
if sys.version_info.major == 3:
    from urllib import parse as parseUrl
else:
    import urlparse as parseUrl


class coreSpider(CrawlSpider):
    name = 'coreSpider'
    allowed_domains = []
    regx_list = []
    start_key = 'fcSpider_urls'
    currKey = 1
    workerFileName = 'core_worker.txt'

    # 重载init
    def __init__(self, *a, **kw):
        super(coreSpider, self).__init__(*a, **kw)
        self.db = Db()
        self.instance()
        self._compile_rules()

    def instance(self):
        # 初始化
        # 从数据库源站表中提取定义所有要爬取的域名(启动脚本只查询一次)
        sql = "SELECT m_domain,m_scheme,m_cp_url_regx from zs_mirror WHERE status=1"
        rows = self.db.query(sql)
        self.db.close()
        if rows:
            for row in rows:
                # 设置运行允许域列表
                self.allowed_domains.append(row['m_domain'])
                # 将域名加入初始爬取列表
                self.start_urls.append(row['m_scheme'] + '://' + row['m_domain'])
            # 将对应书籍章节列表页面链接加入规则列表
            self.regx_list = {row['m_domain']: '.*' + row['m_scheme'] + '://' + row['m_domain'] + row['m_cp_url_regx']
                              for row in rows}
            # 创建链接筛选规则(将匹配(是章节列表)的链接 不跟进)
            # 章节列表页 默认排除 .html后缀页面
            regRule = Rule(LinkExtractor(allow=list(self.regx_list.values())), callback=self.parse_reg)
            # 创建链接筛选规则(将不匹配(不是章节列表)的链接 跟进后再处理)
            noRegRule = Rule(LinkExtractor(deny=list(self.regx_list.values())), callback=self.parse_noReg)
            self.rules = (noRegRule, regRule)

    # 将匹配的章节列表页面加入Redis待采集
    def parse_reg(self, response):
        # 记录检测爬虫状态
        self.writeCurrNum()
        self.addToRedis(response.url)

    # 页面中不匹配的链接 请求页面后爬取页面后再进行筛选
    def parse_noReg(self, response):
        # 记录检测爬虫状态
        self.writeCurrNum()
        # 获取域名
        domain = self.extractDomainFromURL(response.url)
        if domain in self.allowed_domains:
            regx = self.regx_list[domain]
            regLinkExtractor = LinkExtractor(allow=(regx,))
            regLinks = regLinkExtractor.extract_links(response)
            # 将匹配的章节链接在再次加入采集队列 再次分析处理
            for regLink in regLinks:
                yield Request(regLink.url, callback=self.parse_reg, dont_filter=True)
            # 将不匹配的链接在再次加入采集队列 再次分析处理
            noRegLinkExtractor = LinkExtractor(deny=(regx,))
            noRegLinks = noRegLinkExtractor.extract_links(response)
            for noRegLink in noRegLinks:
                yield Request(noRegLink.url, callback=self.parse_noReg, dont_filter=True)

    # 链接添加到redis待采集队列
    def addToRedis(self, url):
        pool = redis.ConnectionPool(host=REDIS_CONFIG['default']['host'], port=int(REDIS_CONFIG['default']['port']),
                                    password=REDIS_CONFIG['default']['pass'])
        r = redis.Redis(connection_pool=pool)
        r.rpush(self.start_key, url)

    def extractDomainFromURL(self, url):
        parsed_uri = parseUrl.urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        return domain

    def writeCurrNum(self):
        self.currKey = self.currKey + 1
        file = open(RUNTIME_DIR + self.workerFileName, 'w')
        file.write(str(self.currKey))
        file.close()
