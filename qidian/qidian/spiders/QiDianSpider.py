# -*- coding: utf-8 -*-
import scrapy
import os
import re
import requests
from Common.Db import Db
from scrapy import Selector
from lxml import etree
from Config.Config import RUNTIME_DIR
from qidian.BookListItems import BookListItem

#从起点爬取小说基本数据 如 小说名称 作者 字数 分类 简介 等
class QiDianSpider(scrapy.Spider):
    # 爬虫名称
    name = 'QiDianSpider'
    # 允许访问的域
    allowed_hosts = ['qidian.com']
    workerFileName = RUNTIME_DIR+'qd_worker.txt'
    start = 0
    limit = 5

    last_page = 42607

    def start_requests(self):
        if os.path.exists(self.workerFileName):
            file = open( self.workerFileName,'r')
            #重新启动则从最后结束的分页再后退2页 保持数据完整
            page = int(file.read())-2
            if page <= 1:
                page = 1
            file.close()
        else:
            file = open(self.workerFileName,'w')
            file.write('1')
            page = 1
            file.close()
        yield scrapy.Request('https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=%d' % page, dont_filter=False)


    def parse(self,response):
        currPage = int(response.url.split('=')[-1])
        file = open(self.workerFileName, 'w')
        file.write(str(currPage))
        file.close()
        nextPage = currPage + 1
        if int(response.status) >= 400:
            db = Db()
            url = str(response.url)
            db.insert('b_error_url',{'url':url})
            nextUrl = response.urljoin('all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=%d' % nextPage)
            return scrapy.Request(nextUrl, callback=self.parse, dont_filter=False)
        else:
            selector = Selector(response)
            data = {}
            for box in selector.xpath('//ul[@class="all-img-list cf"]'):
                #封面
                data['avatorList'] = box.xpath('./li/div/a/img/@src').extract()
                #书名
                data['nameList'] = box.xpath('./li//h4/a/text()').extract()
                authorBox = box.xpath('./li//p[@class="author"]')
                #作者
                data['authorList'] = authorBox.xpath('./a[1]/text()').extract()
                #一级分类
                data['firstCategory'] = authorBox.xpath('./a[2]/text()').extract()
                #二级分类
                data['twoCategory'] = authorBox.xpath('./a[3]/text()').extract()
                #连载状态
                data['status'] = authorBox.xpath('./span/text()').extract()
                for i in range(len(data['status'])):
                    if data['status'][i] == '连载中':
                        data['status'][i] = 1
                    elif data['status'][i] == '完本':
                        data['status'][i] = 2
                    else:
                        data['status'][i] = 0
                #小说简介
                data['introList'] = box.xpath('./li/div/p[@class="intro"]/text()').extract()
                #更新字数
                #TODO 起点升级了  字数获取不到了
                #data['wordNumberList'] = box.xpath('./li/div/p[@class="update"]/span/text()').extract()
                return self.parse_detail(data,nextPage,response)

    def parse_detail(self,data,nextPage,response):
        for i in range(len(data['avatorList'])):
            item = BookListItem()
            item['bookName'] = data['nameList'][i].strip()
            item['bookAvator'] = data['avatorList'][i]
            item['firstCategory'] = data['firstCategory'][i].strip()
            item['twoCategory'] = data['twoCategory'][i].strip()
            item['bookAuthor'] = data['authorList'][i].strip()
            item['bookStatus'] = data['status'][i]
            dr = re.compile(r'<[^>]+>', re.S)
            intro = (dr.sub('', data['introList'][i].strip())).replace('"','\"').replace("'",'\'')
            item['bookIntro'] = intro
            # TODO 起点升级了  字数获取不到了 暂时不获取字数
            item['wordNumber'] = 0
            # item['wordNumber'] = data['wordNumberList'][i].strip('字')
            # if item['wordNumber'].find('万') != -1:
            #     item['wordNumber'] = item['wordNumber'].strip('万')
            #     print(item['wordNumber'])
            #     os._exit()
            #     item['wordNumber'] = int(float(item['wordNumber'])*10000)
            # else:
            #     item['wordNumber'] = int(item['wordNumber'])
                #如果字数少于1万跳过
            #if item['wordNumber'] < 10000:
                #continue
            yield item
        nextUrl = response.urljoin('all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=%d' % nextPage)
        yield scrapy.Request( nextUrl,callback=self.parse,dont_filter=False)


    def get_lastPageNum(self):
        #从列表获取分页总数
        url = 'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1'
        res = requests.get(url)
        selector = etree.HTML(res.content.decode('utf-8'))
        try:
            res = selector.xpath('//div[@class="lbf-pagination"]/ul[@class="lbf-pagination-item-list"]')
            self.last_page = res[0].xpath('.//li[8]/a/text()')[0]
        except Exception:
            return int(self.last_page)
        return int(self.last_page)