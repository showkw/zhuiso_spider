#!/usr/bin/env python

# -*- coding: utf-8 -*-
import logging
import time
from scrapy import signals
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


# 爬虫扩展 解决Scrapy-Redis空跑问题，redis_key链接跑完后，自动关闭爬虫的问题
# 1、scrapy内部的信号系统会在爬虫耗尽内部队列中的request时，就会触发spider_idle信号。
# 2、爬虫的信号管理器收到spider_idle信号后，将调用注册spider_idle信号的处理器进行处理。
# 3、当该信号的所有处理器(handler)被调用后，如果spider仍然保持空闲状态， 引擎将会关闭该spider。
# 解决思路：
# 我们知道 爬虫关闭的关键是 spider_idle 信号。
# spider_idle信号只有在爬虫队列为空时才会被触发， 触发间隔为5s。
# 那么我们也可以使用同样的方式，在信号管理器上注册一个对应在spider_idle信号下的spider_idle()方法。
# 在 spider_idle() 方法中，编写自定义的结束条件来结束爬虫

class RedisSpiderSmartIdleClosedExensions(object):

    def __init__(self, idle_number, crawler):
        self.crawler = crawler
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        # 首先检查是否应该启用和提高扩展
        # 否则不配置
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        # 获取配置中的时间片个数，默认为360个，30分钟
        idle_number = crawler.settings.getint('IDLE_NUMBER', 360)

        # 实例化扩展对象
        ext = cls(idle_number, crawler)

        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info("opened spider %s redis spider Idle, Continuous idle limit： %d", spider.name, self.idle_number)

    def spider_closed(self, spider):
        logger.info("closed spider %s, idle count %d , Continuous idle count %d",
                    spider.name, self.idle_count, len(self.idle_list))

    def spider_idle(self, spider):
        self.idle_count += 1  # 空闲计数
        self.idle_list.append(time.time())  # 每次触发 spider_idle时，记录下触发时间戳
        idle_list_len = len(self.idle_list)  # 获取当前已经连续触发的次数

        # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明redis 中还有key
        if idle_list_len > 2 and self.idle_list[-1] - self.idle_list[-2] > 6:
            self.idle_list = [self.idle_list[-1]]

        elif idle_list_len > self.idle_number:
            # 连续触发的次数达到配置次数后关闭爬虫
            logger.info('\n continued idle number exceed {} Times'
                        '\n meet the idle shutdown conditions, will close the reptile operation'
                        '\n idle start time: {},  close spider time: {}'.format(self.idle_number,
                                                                                self.idle_list[0], self.idle_list[0]))
            # 执行关闭爬虫操作
            self.crawler.engine.close_spider(spider, 'closespider_pagecount')
