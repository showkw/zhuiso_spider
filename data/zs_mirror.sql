/*
Navicat MySQL Data Transfer

Source Server         : 123.207.9.120_3306
Source Server Version : 50721
Source Host           : 123.207.9.120:3306
Source Database       : zhuiso

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-04-04 01:54:35
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
  `m_scheme` varchar(10) NOT NULL DEFAULT 'http' COMMENT '协议规则',
  `m_sex` enum('1','2') NOT NULL DEFAULT '1' COMMENT '源站所属性别',
  `charset` varchar(20) NOT NULL DEFAULT 'utf-8' COMMENT '源站编码',
  `b_info_url_tags` varchar(255) NOT NULL DEFAULT '' COMMENT '标识信息页的标签',
  `m_cp_url_regx` varchar(255) NOT NULL DEFAULT '' COMMENT '章节链接正则匹配规则',
  `m_cp_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '源站目录页面章节采集规则标签',
  `m_cp_url_rule` tinyint(2) NOT NULL DEFAULT '0' COMMENT '目录章节链接前缀规则 0使用页面章节本身链接 1使用拼接域名 2表示使用自定前缀 3使用拼接域名+书籍标识path',
  `m_cp_url` varchar(255) NOT NULL DEFAULT '' COMMENT '自定义章节链接前缀',
  `m_cp_last_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '最新章节匹配标签',
  `m_so_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '源站搜索采集url',
  `m_ct_tags` varchar(255) NOT NULL DEFAULT '' COMMENT '识别标识章节内容页规则',
  `m_ct_url_regx` varchar(255) NOT NULL DEFAULT '' COMMENT '章节内容链接正则匹配规则',
  `m_ct_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '源站章节内容页面采集规则标签',
  `m_ct_i_url_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '章节内容页 获取书籍主页链接的标签规则',
  `m_ct_i_rule` tinyint(2) unsigned NOT NULL DEFAULT '0' COMMENT '目录章节链接前缀规则 0使用页面章节本身链接 1使用拼接域名 2表示使用自定前缀 3使用拼接域名书籍标识path',
  `m_cp_title_rule` varchar(255) NOT NULL DEFAULT '' COMMENT '书籍主页获取标题规则',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` tinyint(2) NOT NULL DEFAULT '1' COMMENT '是否启用',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_domian` (`m_domain`) USING BTREE,
  KEY `idx_status` (`status`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of zs_mirror
-- ----------------------------
INSERT INTO `zs_mirror` VALUES ('8', '笔趣阁', 'www.biquge.vip', 'https', '1', 'utf-8', '//div[@id=\"maininfo\"]', '/\\d+_\\d+/', '//*[@id=\'list\']/dl//dd//a', '1', '', '//*[@id=\'list\']/dl//dd[last()]//a', '', '//*[@id=\'content\']', '', '//*[@id=\'content\']', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '1', '//div[@id=\'info\']/h1', '2018-03-31 13:59:14', '2018-04-03 23:29:44', '1');
INSERT INTO `zs_mirror` VALUES ('5', '梦想文学', 'www.mxguan.com', 'http', '1', 'gbk', '//div[@class=\"book\"]/div[@class=\"path\"]', '/book/\\d+/', '//*[@class=\'listmain\']/dl//dd[position()>9]/a', '1', '', '//*[@class=\'listmain\']/dl/dd[1]/a', 'http://www.mxguan.com/s.php?ie=gbk&s=3938690446586478210&q=', '//*[@id=\'content\']', '', '//*[@id=\'content\']', '//div[@class=\'path\']/div[@class=\'p\']/a[last()]', '1', '//div[@class=\'path\']/div[@class=\'p\']/a[last()]', '2018-03-31 17:09:50', '2018-04-03 23:29:49', '1');
INSERT INTO `zs_mirror` VALUES ('10', '幻月书院', 'www.huanyue123.com', 'http', '1', 'gbk', '//div[@class=\"book_info\"]/div[@class=\"pic\"]', '/book/\\d+/', '//div[@class=\'book_list\']/ul//li/a', '0', '', '//div[@id=\"info\"]//h3[@class=bookinfo_intro]/div[@class=\"options\"]/a', 'http://www.huanyue123.com/modules/article/search.php?searchkey=', '//*[@id=\"htmlContent\"]', '', '//*[@id=\"htmlContent\"]', '//div[@id=\'main\']//div[@class=\'title\']//a[last()]', '0', '//div[@id=\'info\']/h1', '2018-03-31 17:17:00', '2018-04-03 23:29:46', '1');
INSERT INTO `zs_mirror` VALUES ('3', '22中文', 'www.22zw.com', 'http', '1', 'gbk', '//div[@id=\"maininfo\"]', '/files/article/html/\\d+/\\d+/', '//*[@id=\'list\']/dl//dd//a', '1', '', '//*[@id=\'list\']/dl//dd[last()]//a', 'http://zhannei.baidu.com/cse/search?s=16810437655506969639&ie=gbk&q=', '//*[@id=\'content\']', '', '//*[@id=\'content\']', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '1', '//div[@id=\'info\']/h1', '2018-03-31 17:24:52', '2018-04-03 23:29:51', '1');
INSERT INTO `zs_mirror` VALUES ('4', '棉花糖', 'www.mht.la', 'http', '1', 'utf-8', '//div[@class=\"quanwen\"]/div[@class=\"book_info\"]', '/\\d+/\\d+/', '//*[@class=\"novel_list\"]/dl//dd/a', '3', '', '//div[@class=\'new9chapter\']/dl/dd[1]/a', '', '//*[@class=\'content\']/div[@class=\'con_r\']', '', '//*[@class=\'content\']', '//div[@class=\'nav\']/a[last()]', '1', '//div[@class=\'nowplace\']/a[last()]', '2018-03-31 17:32:53', '2018-04-03 23:29:50', '1');
INSERT INTO `zs_mirror` VALUES ('6', '八八读书', 'www.88dus.com', 'https', '1', 'gbk', '//div[@class=\"jieshao\"]/div[@class=\'lf\']', '/xiaoshuo/\\d+/\\d+/', '//div[@class=\"mulu\"]/ul//li/a', '3', '', '//div[@class=\"mulu\"]/ul//li[last()]/a', '', '//div[@class=\'novel\']/div[@class=\'yd_text2\']', '', '//div[@class=\'novel\']/div[@class=\'yd_text2\']', '//div[@class=\'read_t\']//a[last()]', '0', '//div[@class=\'jieshao\']/div[@class=\'rt\']/h1', '2018-04-01 00:53:22', '2018-04-03 23:29:48', '1');
INSERT INTO `zs_mirror` VALUES ('7', '妙笔阁', 'www.miaobige.com', 'https', '1', 'gbk', '//div[@id=\'readerlists\']', '/read/\\d+/', '//div[@id=\'readerlists\']/ul//li/a', '1', '', '[@id=\'readerlists\']/ul//li[last()]/a', '', '//*[@id=\'content\']', '', '//*[@id=\'content\']', '//div[@id=\'center\']/div[@class=\'jumptop\']//a[3]', '1', '//div[@id=smallcons]/h1', '2018-04-01 01:02:23', '2018-04-03 23:29:45', '1');
INSERT INTO `zs_mirror` VALUES ('1', '2k小说', 'www.2kxs.com', 'https', '1', 'gbk', '//div[@id=\'bookinfo\']/div[@id=\'title\']', '/xiaoshuo/\\d+/\\d+/', '//dl[@class=\'book\']//dd[position()>4]/a', '3', '', '//dl[@class=\'book\']//dd[1]/a', '', '//*[@id=\'content\']', '', '//*[@id=\'content\']/p[@class=\'Text\']', '//div[@id=\'content\']/p[@class=\'summary\']/strong/a', '1', '//div[@id=\'content\']/p[@class=\'summary\']/strong/a', '2018-04-01 01:13:01', '2018-04-03 23:29:54', '1');
INSERT INTO `zs_mirror` VALUES ('2', '顶点小说', 'www.booktxt.net', 'http', '1', 'gbk', '//div[@id=\"maininfo\"]', '/\\d+_\\d+/', '//*[@id=\'list\']/dl//dd[position()>9]/a', '1', '', '[@id=\'list\']/dl//dd[1]/a', '', '//*[@id=\'content\']', '', '//*[@id=\'content\']', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '0', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '2018-04-01 01:21:05', '2018-04-03 23:29:52', '1');
INSERT INTO `zs_mirror` VALUES ('9', '笔趣阁', 'www.biquge.info', 'http', '1', 'utf-8', '//div[@id=\"maininfo\"]', '/\\d+_\\d+/', '//div[@id=\'list\']/dl//dd//a', '3', '', '//div[@id=\'list\']/dl//dd[last()]//a', '', '//*[@id=\'content\']', '', '//*[@id=\'content\']', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '0', '//div[@class=\'box_con\']/div[@class=\'con_top\']/a[last()]', '2018-04-01 01:26:15', '2018-04-03 23:29:42', '1');
