"# zhuiso_spider"

暂时还没整理写说明文档

开发环境为windows python3 redis Mysql

linux下不知是否会有问题  还没来得及测试

总共分开 三个爬虫项目

data目录 ---mysql数据库结构文件

qidian目录 采集起点小说基本信息数据,如小说名称 作者 所属分类,二级分类 简介,封面图片等信息

baidu目录 根据数据库配置的不同源站采集规则 从百度搜索结果中提取对应小说源站的数据采集链接 并存储到redis队列

FirstChapter目录 从redis队列中获取链接进行采集,从数据库查询对应源站采集规则,采集获取小说的最新章节信息(主要用作首次采集)

baiduSpider 与 FirstChapter 是分布式爬虫,(都可直接复制多个项目,部署到不同的主机运行)

运行之前:
安装pyhton
安装pip
安装requirements.txt依赖
pip install -r requirements.txt

爬虫运行顺序 qidan > baidu > FirstChapter

cd 进入爬虫项目

1. 临时一次运行  scrpay crawl 爬虫名称( QiDianSpider/bdSpider/fcSpider )

2. 自动重启运行  python main.py
