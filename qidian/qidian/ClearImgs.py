# -*- coding: utf-8 -*-
import os
import urllib.parse
from yuedu.settings import IMAGES_STORE
from yuedu.Db import Db

#清理磁盘中与数据库中不匹配/不存在的图片
def clearImgsFile():
    file_dir = IMAGES_STORE +'full\\'
    db = Db()
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            fileName = 'full/%s' % file
            sql = "SELECT id FROM zs_book WHERE b_img='%s'" % fileName
            res = db.query(sql)
            if res:
                continue
            else:
                os.remove(file_dir+file)
                print('删除了%s'%file)
    return True

#清理数据库中 没有对应小说的作者
def clearReptAuthor():
    sql ="DELETE FROM zs_author WHERE id NOT IN(SELECT b_aid FROM zs_book)"
    db = Db()
    res = db.query(sql)
    print('清理成功')
    return True

#从数据库清理不存在的图片
def clearSqlImgs():
    file_dir = IMAGES_STORE +'full\\'
    db = Db()
    sql = "SELECT count(*) as num from zs_book"
    res = db.query(sql)
    k=1
    size = 10
    count = int(res[0]['num'])
    while k <= count:
        start = (k-1)*size
        sql = "SELECT id,b_img from zs_book where b_img!='' limit %d,%d" % (start,size)
        res = db.query(sql)
        for i in res:
            img = i['b_img'].strip('full/')
            if os.path.exists(file_dir + img):
                continue
            else:
                print( i )
                id = i['id']
                sql = "UPDATE zs_book set b_img='' where id=%d" % id
                db.dml(sql)
        k+=1
    return True


#clearSqlImgs()
#clearImgsFile()
#clearReptAuthor()