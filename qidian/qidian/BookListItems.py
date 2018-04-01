# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #小说名称
    bookName= scrapy.Field()
    #小说所属一级分类
    firstCategory = scrapy.Field()
    #小说所属二级分类
    twoCategory = scrapy.Field()
    #小说作者
    bookAuthor = scrapy.Field()
    #小说封面图片地址
    bookAvator = scrapy.Field()
    #小说连载状态
    bookStatus = scrapy.Field()
    #小说简介
    bookIntro = scrapy.Field()
    #小说更新字数
    wordNumber = scrapy.Field()
    # pass
