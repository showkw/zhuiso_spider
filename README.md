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

linux环境安装依赖:


    若已安装python 报错:ImportError: No module named _sqlite3
    
    直接按照1,2步骤重新编译安装即可
    
    1. 安装 sqlite(否则后边会报错)
    
        wget http://www.sqlite.org/sqlite-amalgamation-3.6.20.tar.gz

        tar zxvf  sqlite-amalgamation-3.6.20.tar.gz

        cd  sqlite-3.6.20

        ./configure –prefix=/usr/local/lib/sqlite3

        make && make install

    2. 安装 python (2.7/3.5都行) 注意点:
    
         py2.7 执行
         
         wget https://www.python.org/ftp/python/2.7.14/Python-2.7.14.tgz
         
         tar zxvf  Python-2.7.14.tgz

         py3 执行
         
         wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
         
         tar zxvf  Python-3.6.5.tgz

         重点来了:
         
         cd python解压后的目录
         
         vi setup.py
         
         在下面这段的下一行添加’/usr/local/lib/sqlite3/include’,
         
         sqlite_inc_paths = [ ‘/usr/include’,

                                     ‘/usr/include/sqlite’,

                                     ‘/usr/include/sqlite3′,

                                     ‘/usr/local/include’,

                                     ‘/usr/local/include/sqlite’,

                                     ‘/usr/local/include/sqlite3′,

                                     ‘/usr/local/lib/sqlite3/include’,

         ./configure --prefix=/usr/local/python

         make && make install  至此python安装完成
         

    3. 安装pip(安装pip前需要前置安装setuptools)
    
        wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools19.6.tar.gz#md5=c607dd118eae682c44ed146367a17e26
        
        tar -zxvf setuptools-19.6.tar.gz

        cd setuptools-19.6

        python setup.py build

        python setup.py install
        
        安装pip
        
        wget --no-check-certificate  https://pypi.python.org/packages/source/p/pip/pip-8.0.2.tar.gz#md5=3a73c4188f8dbad6a1e6f6d44d117eeb

        tar -zxvf pip-8.0.2.tar.gz

        cd pip-8.0.2

        python setup.py build

        python setup.py install
    
    4. 安装redis
    
    5. 安装requirements.txt依赖(在爬虫项目目录)
    
        pip install -r requirements.txt

windows注意 需安装pywin32依赖

然后测试运行 缺少什么包就 pip install 包名

最后:先配置数据库配置文件信息


爬虫运行顺序 qidan > baidu > FirstChapter

cd 进入爬虫项目

1. 临时一次运行  scrapy crawl 爬虫名称( QiDianSpider/bdSpider/fcSpider )

2. 自动重启运行  python main.py (已更新)

更新记录:

2018-04-04 

  1.百度(bdSpider)停止更新(完全是之前思路想歪了,哈哈 别打我)
  
  2.新增coreSpider  还是分布式爬虫(原百度爬虫的替代品),coreSpider将从zs_mirror源表取出所有可用域名,然后进行全站爬取所需数据的链接,将链接压入redis    队列,还是搭配fcSpider 协同工作,coreSpider负责采集链接,fcSpider爬取具体数据
  
  3.新增扩展文件extension.py
  
    扩展类:RedisSpiderSmartIdleClosedExensions
    主要解决分布式爬虫空跑问题，redis_key链接跑完后，自动关闭爬虫的问题
    
  4.配置文件setting.py 新增扩展类的配置项
  
  5.优化爬虫 mysql db链接长时间占用未关闭问题
  
  6.data目录 zs_mirror表 新增两个字段 m_scheme(源站协议类型) 和 m_cp_rule_regx( 章节链接匹配正则 )
 
 
