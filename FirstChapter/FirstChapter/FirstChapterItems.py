# -*- coding: utf-8 -*-
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

#item
class FirstChapterItem(Item):
    #书籍id
    b_id = Field()
    #源站id
    m_id = Field()
    #源站名称
    m_name = Field()
    #书籍对应源站标识
    b_no =  Field()
    #书籍最新更新章节名称
    last_title = Field()
    #书籍最新更新章节链接
    last_url = Field()


class FirstChapterLoader(ItemLoader):
    default_item_class = FirstChapterItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()