# -*- coding: utf-8 -*-
import urllib.parse
from Common.Db import Db
from scrapy import Selector
from Config.Config import RUNTIME_DIR
from scrapy_redis.spiders import RedisSpider
from FirstChapter.FirstChapterItems import FirstChapterLoader
#从redis待采集链接队列中获取链接并采集
class FirstChapterspider(RedisSpider):
    name = 'fcSpider'
    redis_key = 'fcSpider_urls'
    currKey = 1
    workerFileName = 'fc_worker.txt'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(FirstChapterspider, self).__init__(*args, **kwargs)

    def parse(self, response):
        #记录检测爬虫状态
        self.writeCurrNum()
        el = FirstChapterLoader(response=response)
        #根据链接域名查询数据库中的对应规则信息
        db = Db()
        sql = "SELECT * from zs_mirror WHERE m_domain='%s'" % self.extractDomainFromURL(response.url)
        row = db.query(sql, 'one')
        db.close()
        if row:
            #采集获取书籍章节等数据
            return self.contactItemInfo(response,row,el)

    # 获取Url中的域名
    def extractDomainFromURL(self, url):
        parsed_uri = urllib.parse.urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        return domain

    def contactItemInfo(self,response,row,el):
        # 检查书名是否正确
        bookName = self.getBookName(response, row['m_cp_title_rule'])
        if bookName != False:
            db = Db()
            sql = "SELECT id from zs_book where b_name='%s'" % bookName
            find = db.query(sql, 'one')
            db.close()
            if find:
                el = self.getItemInfo(response, row,el)
                if el != None:
                    el.add_value('b_id', str(find['id']))
                    return el.load_item()

    #根据数据库中配置的规则获取书籍名称
    def getBookName(self,response,tags):
         selector = Selector(response)
         try:
             path = selector.xpath(tags)
             if path:
                 bookName = path.xpath('./text()').extract_first('').strip()
                 if bookName != '':
                     return bookName
         except Exception:
             return False
         return False

    #获取源站数据与最新章节信息
    def getItemInfo(self,response,row,el):
        # 获取书籍对应源站链接标识
        bookInfoPath = ((urllib.parse.urlparse(response.url)).path).strip('/')
        if row['m_cp_last_rule'] != '':
            # 获取书籍最新章节信息
            lastChapter = self.getLastChapter(response, row['m_cp_last_rule'])
            if lastChapter:
                el.add_value('m_id',str(row['id']))
                el.add_value('m_name',row['m_name'] + '(' + row['m_domain'] + ')')
                el.add_value('b_no',bookInfoPath)
                el.add_value('last_title',lastChapter['title'])
                el.add_value('last_url',lastChapter['url'])
                return el

    #获取最新章节信息
    def getLastChapter(self,response,tags):
        lastChapter = Selector(response).xpath(tags)
        lastInfo = {}
        lastInfo['title'] = lastChapter.xpath('./text()').extract_first('').strip()
        lastInfo['url'] = lastChapter.xpath('.//@href').extract_first('').strip()
        if lastInfo['title'] != '' and lastInfo['url'] != '' :
            return lastInfo

    def writeCurrNum(self):
        self.currKey = self.currKey+1
        file = open(RUNTIME_DIR+self.workerFileName, 'w')
        file.write(str(self.currKey))
        file.close()
