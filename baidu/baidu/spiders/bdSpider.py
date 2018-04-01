# -*- coding: utf-8 -*-

import re
import os
import scrapy
import redis
import requests
import hashlib
import sys

if sys.version_info.major == 3:
    from urllib import parse as parseUrl
else:
    import urlparse as parseUrl
from Common.Db import Db
from scrapy import Selector
from scrapy_redis.spiders import Spider
from Config.DataBaseConfig import REDIS_CONFIG
from Config.Config import RUNTIME_DIR


# Master爬虫(可负制项目,开启多个运行)爬取小说百度搜索结果爬虫 用于生产待采集requests_url
class BdSpider(Spider):
    name = 'bdSpider'
    allowed_domains = ['baidu.com']
    replace_key = 'bdSpider_replace'
    start_key = 'fcSpider_urls'
    page = 1
    limit = 100
    curr_url = dict(
        curr_books=[],
        curr_bookNames=[],
        curr_charset=[],
        curr_mirr=[],
        curr_domain=[],
    )
    pageFileName = 'bd_chapter.txt'
    workerFileName = 'bd_worker.txt'
    currKey = 0
    db = Db()

    #生产初始百度搜索链接
    def start_make_url(self):
        self.start_urls = []
        self.curr_url = dict(
            curr_books=[],
            curr_bookNames=[],
            curr_charset=[],
            curr_mirr=[],
            curr_domain=[],
        )
        # 记录页码
        self.writePageNum()
        begin = (self.page - 1) * self.limit
        db = Db()
        #从zs_book表查询 limit 条小说数据(小说id, 小说名称)
        sqlSelect = 'SELECT id,b_name FROM zs_book order by id limit %d,%d' % (begin, self.limit)
        rows = db.query(sqlSelect)
        #从采集源表 zs_mirror 查询可用的源站规则数据 ( 源站id, 源站域名, 源站页面编码 )
        mirrRows = db.query('SELECT id,m_domain,charset FROM zs_mirror WHERE status=1')
        if rows:
            for row in rows:
                for mirr in mirrRows:
                    self.curr_url['curr_books'].append(row['id'])
                    self.curr_url['curr_bookNames'].append(row['b_name'])
                    self.curr_url['curr_charset'].append(mirr['charset'])
                    self.curr_url['curr_mirr'].append(mirr['id'])
                    self.curr_url['curr_domain'].append(mirr['m_domain'])
                    #使用百度高级查询生成搜索词: (site:搜索域名) intitle: 小说名称 (从指定搜索域名的搜索结果中精确搜索xxx)
                    self.start_urls.append(
                        'https://www.baidu.com/s?ie=utf-8&rn=50&f=8&rsv_bp=1&tn=baidu&wd=(site:' + mirr[
                            'm_domain'] + ')' + ' intitle:' + row['b_name'])

    #生成初始requests请求
    def start_requests(self):
        self.start_make_url()
        for url in self.start_urls:
            key = self.start_urls.index(url)
            request = scrapy.Request(url, callback=self.parse_url, dont_filter=True)
            #使用meta给请求结果response传递必要参数
            request.meta['b_id'] = self.curr_url['curr_books'][key]
            request.meta['b_name'] = self.curr_url['curr_bookNames'][key]
            request.meta['charset'] = self.curr_url['curr_charset'][key]
            request.meta['m_id'] = self.curr_url['curr_mirr'][key]
            request.meta['m_domain'] = self.curr_url['curr_domain'][key]
            yield request

    def parse_url(self, response):
        self.writeCurrNum()
        if not response.xpath('/html/body/noscript'):
                for box in response.xpath('//div[@id="content_left"]'):
                    # 获取搜索结果页列表中的所有链接
                    linkInfo = box.xpath('.//div[@class="c-tools"]//@data-tools').extract()
                    # 链接去重(通过源站id与数据id hash去重)
                    if 'b_id' in response.meta and self.linksReplace(response.meta['m_id'], response.meta['b_id']) == True:
                        yield self.parse_bdSearchResult_links(linkInfo, response)

    # 根据数据库需求筛选需要爬取的链接 进行下一步链接爬取
    def parse_bdSearchResult_links(self, linkInfo, response):
        for link in linkInfo:
            links = eval(link)
            # 将搜索结果中的百度加密链接转换为真实网站链接地址
            realUrl = self.get_bd_realyUrl(links['url'])
            # 获取真实链接的scheme
            scheme = (parseUrl.urlparse(realUrl)).scheme
            # 获取真实网站地址中的域名
            domain = self.extractDomainFromURL(realUrl)
            # #从数据库根据得出的域名获取是否有对应的网页提取规则 没有则跳过
            db = Db()
            sql = "SELECT * FROM zs_mirror WHERE m_domain='%s'" % domain
            rows = db.query(sql)
            if rows:
                for row in rows:
                    # 检查真实链接页面是否是小说章节列表页面
                    result = self.getPageType(realUrl, row, response.meta['charset'])
                    if result == 0:
                        continue
                    else:
                        if result['type'] == 1:  # 是章节页面
                            #将地址压入 redis 队列
                            self.addToRedis(realUrl)
                        elif result['type'] == 2:  # 是内容页面
                            #根据数据库查询得出的源站 内容页面采集规则 获取章节页面链接
                            pageUrl = self.getChapterUrlByContentPage(result['response'], row['m_ct_i_url_rule'])
                            if pageUrl != False:
                                #应对不同站点不同链接组合方式
                                i_rule = int(row['m_ct_i_rule'])
                                if i_rule == 1: #链接需要拼接域名
                                    url = scheme + '://' + domain + '/' + pageUrl.lstrip('/')
                                elif i_rule == 0:#使用链接本身
                                    url = pageUrl
                                elif i_rule == 3:#需要拼接完整真实链接
                                    url = realUrl.rstrip('/') + '/' + pageUrl.lstrip('/')
                                else:
                                    continue
                                # 将地址压入 redis 队列
                                self.addToRedis(url)
                            else:
                                continue
                        else:
                            continue
            else:
                continue

    # 获取百度搜索结果链接的真实跳转网站地址
    def get_bd_realyUrl(self, bdUrl):
        tmpPage = requests.get(bdUrl, allow_redirects=False)
        if tmpPage.status_code == 200:
            urlMatch = re.search(r'URL=\'(.*?)\'', tmpPage.text.encode('utf-8'), re.S)
            return urlMatch.group(1)
        elif tmpPage.status_code == 302:
            return tmpPage.headers.get('location')
        else:
            print('No URL found!!')

    # 获取网站地址中的域名
    def extractDomainFromURL(self, url):
        """Get domain name from url"""
        parsed_uri = parseUrl.urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        return domain

    # 根据数据库配置的规则检查页面类型
    def getPageType(self, url, rules, charset):
        response = requests.get(url)
        response.encoding = charset
        selector = Selector(response)
        ret = {}
        ret['response'] = response
        #标识章节页面的规则
        chapterRule = rules['b_info_url_tags']
        #标识内容页面的规则
        contentRule = rules['m_ct_tags']
        try:
            if selector.xpath(chapterRule):
                ret['type'] = 1
            elif selector.xpath(contentRule):
                ret['type'] = 2
            else:
                return 0
            return ret
        except Exception:
            return 0

    # 从章节内容页面获取章节列表页面链接
    def getChapterUrlByContentPage(self, response, tags):
        selector = Selector(response)
        path = selector.xpath(tags)
        if path:
            pageUrl = path.xpath('.//@href').extract_first('').strip()
            return pageUrl
        return False

    #链接添加到redis待采集队列
    def addToRedis(self,url):
        pool = redis.ConnectionPool(host=REDIS_CONFIG['default']['host'], port=int(REDIS_CONFIG['default']['port']),
                                    password=REDIS_CONFIG['default']['pass'])
        r = redis.Redis(connection_pool=pool)
        r.rpush(self.start_key, url)

    #记录数据库查询分页页码
    def writePageNum(self):
        if os.path.exists(RUNTIME_DIR+self.pageFileName):
            file = open(RUNTIME_DIR+self.pageFileName, 'r')
            self.page = int(file.read())
            if self.page <= 1:
                self.page = 1
            file.close()
        else:
            file = open(RUNTIME_DIR+self.pageFileName, 'w')
            file.write('1')
            self.page = 1
            file.close()
        file = open(RUNTIME_DIR+self.pageFileName, 'w')
        file.write(str(self.page + 1))
        file.close()

    #记录当前执行条数 同时用作监测爬虫状态
    def writeCurrNum(self):
        self.currKey = self.currKey+1
        file = open(RUNTIME_DIR+self.workerFileName, 'w')
        file.write(str(self.currKey))
        file.close()

     #m_id与b_id hash 检查去重
    def linksReplace(self,m_id,b_id):
        string = str(m_id)+str(b_id)
        hl = hashlib.md5()
        hl.update(string.encode(encoding='utf-8'))
        hsh = hl.hexdigest()
        pool = redis.ConnectionPool(host=REDIS_CONFIG['local']['host'], port=int(REDIS_CONFIG['local']['port']),
                                    password=REDIS_CONFIG['local']['pass'])
        r = redis.Redis(connection_pool=pool)
        res = r.sadd(self.replace_key,hsh)
        if res == 0 or res == False :
            return False
        else:
            return True