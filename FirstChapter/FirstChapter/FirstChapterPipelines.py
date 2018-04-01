# -*- coding: utf-8 -*-
from Common.Db import Db

#保存管道
class MySQLPipeline(object):
    def process_item(self, item, spider):
        # 写入数据库
        db = Db()
        sql = "insert into zs_chapter_mirror(`b_id`, `m_id`, `m_name`, `b_no`, `last_title`, `last_url`) VALUES (%d, %d, '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE  `m_name`='%s',`b_no`='%s',`last_title`='%s',`last_url`='%s'" % \
              (int(item['b_id']), int(item['m_id']),item['m_name'], item['b_no'], item['last_title'], item['last_url'],item['m_name'], item['b_no'], item['last_title'], item['last_url'])
        print(item)
        db.dml(sql)
        return item
