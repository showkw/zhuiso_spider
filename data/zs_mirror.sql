/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : bookspider

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2018-04-02 00:08:26
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for zs_mirror
-- ----------------------------
DROP TABLE IF EXISTS `zs_mirror`;
CREATE TABLE `zs_mirror` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `m_name` varchar(100) NOT NULL DEFAULT '' COMMENT '源站名称',
  `m_domain` varchar(255) NOT NULL DEFAULT '' COMMENT '源站域名',
  `m_sex` enum('1','2') NOT NULL COMMENT '源站所属性别 1男 2女',
  `charset` varchar(20) NOT NULL DEFAULT 'utf-8' COMMENT '源站编码',
  `b_info_url_tags` varchar(255) NOT NULL DEFAULT '' COMMENT '标识信息页的标签',
  `m_cp_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '源站目录页面章节采集规则标签',
  `m_cp_url_rule` tinyint(2) NOT NULL DEFAULT '0' COMMENT '目录章节列表页链接前缀规则 0使用本身链接 1需拼接域名 2表示使用自定前缀 3使用拼接域名+书籍标识path',
  `m_cp_url` varchar(255) NOT NULL DEFAULT '' COMMENT '自定义章节链接前缀',
  `m_cp_last_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '最新章节a标签匹配规则',
  `m_so_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '源站搜索采集url',
  `m_ct_tags` varchar(255) NOT NULL DEFAULT '' COMMENT '用作识别 标识章节内容页的标签规则',
  `m_ct_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '章节内容页 小说内容采集规则标签',
  `m_ct_i_url_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '章节内容页 获取书籍目录列表页的链接a标签 规则',
  `m_ct_i_rule` tinyint(2) unsigned NOT NULL DEFAULT '0' COMMENT '章节内容页 采集目录章节页链接前缀规则 0使用本身链接 1使用拼接域名 2表示使用自定前缀 3使用拼接域名书籍标识path',
  `m_cp_title_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '章节列表页 获取小说标题规则',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` tinyint(2) NOT NULL DEFAULT '1' COMMENT '是否启用源站采集规则',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_domian` (`m_domain`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of zs_mirror
-- ----------------------------
INSERT INTO `zs_mirror` VALUES ('1', '笔趣阁', 'www.biquge.vip', '1', 'utf-8', '//div[@id=\"maininfo\"]', '//*[@id=\'list\']/dl//dd//a', '1', '', '//*[@id=\'list\']/dl//dd[last()]//a', '', '//*[@id=\'content\']', '//*[@id=\'content\']', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '1', '//div[@id=\'info\']/h1', '2018-03-31 13:59:14', '2018-03-31 20:17:05', '1');
INSERT INTO `zs_mirror` VALUES ('2', '梦想文学', 'www.mxguan.com', '1', 'gbk', '//div[@class=\"book\"]/div[@class=\"path\"]', '//*[@class=\'listmain\']/dl//dd[position()>9]/a', '1', '', '//*[@class=\'listmain\']/dl/dd[1]/a', 'http://www.mxguan.com/s.php?ie=gbk&s=3938690446586478210&q=', '//*[@id=\'content\']', '//*[@id=\'content\']', '//div[@class=\'path\']/div[@class=\'p\']/a[last()]', '1', '//div[@class=\'path\']/div[@class=\'p\']/a[last()]', '2018-03-31 17:09:50', '2018-04-01 00:47:26', '1');
INSERT INTO `zs_mirror` VALUES ('3', '幻月书院', 'www.huanyue123.com', '1', 'gbk', '//div[@class=\"book_info\"]/div[@class=\"pic\"]', '//div[@class=\'book_list\']/ul//li/a', '0', '', '//div[@id=\"info\"]//h3[@class=bookinfo_intro]/div[@class=\"options\"]/a', 'http://www.huanyue123.com/modules/article/search.php?searchkey=', '//*[@id=\"htmlContent\"]', '//*[@id=\"htmlContent\"]', '//div[@id=\'main\']//div[@class=\'title\']//a[last()]', '0', '//div[@id=\'info\']/h1', '2018-03-31 17:17:00', '2018-03-31 21:59:29', '1');
INSERT INTO `zs_mirror` VALUES ('4', '22中文', 'www.22zw.com', '1', 'gbk', '//div[@id=\"maininfo\"]', '//*[@id=\'list\']/dl//dd//a', '1', '', '//*[@id=\'list\']/dl//dd[last()]//a', 'http://zhannei.baidu.com/cse/search?s=16810437655506969639&ie=gbk&q=', '//*[@id=\'content\']', '//*[@id=\'content\']', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '1', '//div[@id=\'info\']/h1', '2018-03-31 17:24:52', '2018-03-31 21:58:13', '1');
INSERT INTO `zs_mirror` VALUES ('5', '棉花糖', 'www.mht.la', '1', 'utf-8', '//div[@class=\"quanwen\"]/div[@class=\"book_info\"]', '//*[@class=\"novel_list\"]/dl//dd/a', '3', '', '//div[@class=\'new9chapter\']/dl/dd[1]/a', '', '//*[@class=\'content\']/div[@class=\'con_r\']', '//*[@class=\'content\']', '//div[@class=\'nav\']/a[last()]', '1', '//div[@class=\'nowplace\']/a[last()]', '2018-03-31 17:32:53', '2018-03-31 20:17:13', '1');
INSERT INTO `zs_mirror` VALUES ('6', '八八读书', 'www.88dus.com', '1', 'gbk', '//div[@class=\"jieshao\"]/div[@class=\'lf\']', '//div[@class=\"mulu\"]/ul//li/a', '3', '', '//div[@class=\"mulu\"]/ul//li[last()]/a', '', '//div[@class=\'novel\']/div[@class=\'yd_text2\']', '//div[@class=\'novel\']/div[@class=\'yd_text2\']', '//div[@class=\'read_t\']//a[last()]', '0', '//div[@class=\'jieshao\']/div[@class=\'rt\']/h1', '2018-04-01 00:53:22', '2018-04-01 00:57:28', '1');
INSERT INTO `zs_mirror` VALUES ('7', '妙笔阁', 'www.miaobige.com', '1', 'gbk', '//div[@id=\'readerlists\']', '//div[@id=\'readerlists\']/ul//li/a', '1', '', '[@id=\'readerlists\']/ul//li[last()]/a', '', '//*[@id=\'content\']', '//*[@id=\'content\']', '//div[@id=\'center\']/div[@class=\'jumptop\']//a[3]', '1', '//div[@id=smallcons]/h1', '2018-04-01 01:02:23', '2018-04-01 21:24:44', '1');
INSERT INTO `zs_mirror` VALUES ('8', '2k小说', 'www.2kxs.com', '1', 'gbk', '//div[@id=\'bookinfo\']/div[@id=\'title\']', '//dl[@class=\'book\']//dd[position()>4]/a', '3', '', '//dl[@class=\'book\']//dd[1]/a', '', '//*[@id=\'content\']', '//*[@id=\'content\']/p[@class=\'Text\']', '//div[@id=\'content\']/p[@class=\'summary\']/strong/a', '1', '//div[@id=\'content\']/p[@class=\'summary\']/strong/a', '2018-04-01 01:13:01', '2018-04-01 01:21:50', '1');
INSERT INTO `zs_mirror` VALUES ('9', '顶点小说', 'www.booktxt.net', '1', 'gbk', '//div[@id=\"maininfo\"]', '//*[@id=\'list\']/dl//dd[position()>9]/a', '1', '', '[@id=\'list\']/dl//dd[1]/a', '', '//*[@id=\'content\']', '//*[@id=\'content\']', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '0', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '2018-04-01 01:21:05', '2018-04-01 01:24:11', '1');
INSERT INTO `zs_mirror` VALUES ('10', '笔趣阁', 'www.biquge.info', '1', 'utf-8', '//div[@id=\"maininfo\"]', '//div[@id=\'list\']/dl//dd//a', '3', '', '//div[@id=\'list\']/dl//dd[last()]//a', '', '//*[@id=\'content\']', '//*[@id=\'content\']', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '0', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '2018-04-01 01:26:15', '2018-04-01 02:15:54', '1');
