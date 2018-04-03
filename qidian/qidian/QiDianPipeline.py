# -*- coding: utf-8 -*-
import os
from Common.Db import Db
from qidian.settings import IMAGES_STORE

class QiDianPipeline(object):
    def process_item(self, item, spider):
        # TODO 起点升级  字数获取不到
        # if int(item['wordNumber']) < 10000:
        #     file_path = IMAGES_STORE + item['bookAvator']
        #     os.remove(file_path)
        #     return item
        db = Db()
        try:
            #查询书籍是否已存在
            bookSql = "SELECT id,b_img FROM zs_book WHERE b_name='%s'" % item['bookName']
            findBook = db.query(bookSql)
            if findBook:
                # TODO 起点升级  字数获取不到
                # if int(item['wordNumber']) < 10000:
                #     sql = 'DELETE FROM zs_book WHERE id=%d' % findBook[0]['id']
                #     file_path = IMAGES_STORE + item['bookAvator']
                #     os.remove(file_path)
                if findBook[0]['b_img'] == '' :
                    sql = "UPDATE zs_book set b_img='%s' WHERE id=%d" % (item['bookAvator'],findBook[0]['id'])
                    db.dml(sql)
                db.close()
                return item
            else:
                #不存在
                firstCategory = item['firstCategory']
                twoCategory = item['twoCategory']
                #查询一级分类是否存在
                sql = "SELECT * FROM zs_category WHERE c_name='%s'" % firstCategory
                findFirstCate = db.query(sql)
                #已存在一级分类
                if findFirstCate:
                    firstId = findFirstCate[0]['id']
                    #查询二级分类是否存在
                    sql = "SELECT * FROM zs_category WHERE c_name='%s'" % twoCategory
                    findTwoCate = db.query(sql)
                    if findTwoCate:
                        twoId = findTwoCate[0]['id']
                    else:
                        #不存在二级分类则插入
                        two = {
                            'c_name': twoCategory,
                            'c_sex': 1,
                            'p_id': firstId,
                            'path': '0,%s,' % firstId
                        }
                        twoId = db.insert('zs_category', two)
                        if twoId == False:
                            db.close()
                            return item

                else:
                    #不存在则插入一级分类
                    ins = {
                        'c_name': firstCategory,
                        'c_sex': 1,
                        'p_id': 0,
                        'path': '0,'
                    }
                    firstId = db.insert('zs_category', ins)
                    if firstId == False:
                        db.close()
                        return item

                    #查询二级分类是否存在
                    sql = "SELECT * FROM zs_category WHERE c_name='%s'" % twoCategory
                    findTwoCate = db.query(sql)
                    if findTwoCate:
                        twoId = findTwoCate[0]['id']
                    else:
                        #不存在则插入
                        two = {
                            'c_name': twoCategory,
                            'c_sex': 1,
                            'p_id': firstId,
                            'path': '0,%s,' % firstId
                        }
                        twoId = db.insert('zs_category', two)
                        if twoId == False:
                            db.close()
                            return item
                #查询作者是否存在
                authorSql = "SELECT * FROM zs_author WHERE author_name='%s'" % item['bookAuthor']
                findAuthor = db.query(authorSql)
                if findAuthor:
                    authorId = findAuthor[0]['id']
                else:
                    #不存在则插入
                    ins = {'author_name': item['bookAuthor']}
                    authorId = db.insert('zs_author', ins)
                    if authorId == False:
                        db.close()
                        return item
                #插入书籍
                insertBook = {
                    'b_name': item['bookName'],
                    'b_fid': str(firstId),
                    'b_tid': str(twoId),
                    'b_img': item['bookAvator'],
                    'b_aid': str(authorId),
                    'b_intro': item['bookIntro'],
                    'b_state': item['bookStatus'],
                    'b_word_num': str(item['wordNumber'])
                }
                db.insert('zs_book', insertBook)
                db.close()
                return item
        except Exception as e:
            db.close()
            return item


