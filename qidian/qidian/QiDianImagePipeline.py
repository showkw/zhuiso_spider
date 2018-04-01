# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class QiDianImagePipeline(ImagesPipeline):
    #通过抓取的图片url获取一个Request用于下载
    def get_media_requests(self, item, info):
        #返回Request根据图片图片url下载
        yield scrapy.Request('https:'+item['bookAvator'])
    #当下载请求完成后执行该方法
    def item_completed(self, results, item, info):
        #获取下载地址
        image_path = [x['path'] for ok, x in results if ok]
        #判断是否成功
        if image_path:
            #将地址存入item
            item['bookAvator'] = image_path[0]
        else:
            item['bookAvator'] = ''
        return item