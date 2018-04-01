/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : bookspider

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2018-04-02 00:07:52
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for zs_author
-- ----------------------------
DROP TABLE IF EXISTS `zs_author`;
CREATE TABLE `zs_author` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `author_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `author_unique` (`author_name`)
) ENGINE=InnoDB AUTO_INCREMENT=439511 DEFAULT CHARSET=utf8;
