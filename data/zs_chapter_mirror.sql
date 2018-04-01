/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : bookspider

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2018-04-02 00:08:16
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for zs_chapter_mirror
-- ----------------------------
DROP TABLE IF EXISTS `zs_chapter_mirror`;
CREATE TABLE `zs_chapter_mirror` (
  `b_id` int(11) NOT NULL COMMENT '书籍id',
  `m_id` int(11) NOT NULL COMMENT '源id',
  `m_name` varchar(255) NOT NULL DEFAULT '' COMMENT '源站名称',
  `last_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  `last_title` varchar(255) NOT NULL COMMENT '最后更新章节',
  `b_no` varchar(100) NOT NULL DEFAULT '' COMMENT '书籍链接标识',
  `last_url` varchar(255) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`b_id`,`m_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
