/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : bookspider

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2018-04-02 00:08:07
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for zs_category
-- ----------------------------
DROP TABLE IF EXISTS `zs_category`;
CREATE TABLE `zs_category` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `c_name` varchar(100) DEFAULT NULL,
  `c_sex` enum('1','2') NOT NULL,
  `p_id` int(11) NOT NULL,
  `path` varchar(50) NOT NULL DEFAULT '0,',
  `sort` float NOT NULL DEFAULT '100',
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_unique` (`c_name`)
) ENGINE=MyISAM AUTO_INCREMENT=111 DEFAULT CHARSET=utf8;
