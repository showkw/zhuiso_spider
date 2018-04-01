/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : bookspider

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2018-04-02 00:08:00
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for zs_book
-- ----------------------------
DROP TABLE IF EXISTS `zs_book`;
CREATE TABLE `zs_book` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `b_name` varchar(100) NOT NULL DEFAULT '' COMMENT '书籍名称',
  `b_fid` int(11) NOT NULL DEFAULT '0' COMMENT '所属一级分类id',
  `b_img` varchar(255) DEFAULT '' COMMENT '书籍封面图片地址',
  `b_aid` varchar(255) DEFAULT '' COMMENT '书籍作者',
  `b_intro` varchar(1500) NOT NULL DEFAULT '' COMMENT '书籍简介',
  `b_tid` int(11) NOT NULL DEFAULT '0' COMMENT '所属二级分类id',
  `b_state` tinyint(2) NOT NULL DEFAULT '0' COMMENT '连载状态 0未知 1连载 2完本',
  `b_word_num` int(11) NOT NULL DEFAULT '0' COMMENT '字数 万字为单位',
  `b_sex` tinyint(2) unsigned NOT NULL DEFAULT '1' COMMENT '性别 默认1男生 2女生',
  `b_follow` float unsigned NOT NULL DEFAULT '0' COMMENT '追书人数',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `b_click` float unsigned NOT NULL DEFAULT '0' COMMENT '点击量',
  PRIMARY KEY (`id`),
  UNIQUE KEY `book_name_unique` (`b_name`)
) ENGINE=InnoDB AUTO_INCREMENT=492968 DEFAULT CHARSET=utf8;
