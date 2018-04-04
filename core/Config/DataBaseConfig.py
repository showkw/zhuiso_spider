# -*- coding: utf-8 -*-
#MYSQL
#数据库配置
MYSQL_CONFIG = {}
MYSQL_CONFIG['default'] = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'pass': '',
    'charset': 'utf8',
    'db': 'bookSpider'
}

#Redis
#redis配置
REDIS_CONFIG = {}
#远程redis  存放待爬取的真实采集网址
REDIS_CONFIG['default']= {
    'host' :'0.0.0.0',
    'port' : '6379',
    'pass' :''
}
#本地redis  存放hash网址 网址去重
REDIS_CONFIG['local']= {
    'host' :'127.0.0.1',
    'port' : '6379',
    'pass': ''
}