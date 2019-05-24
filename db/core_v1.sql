/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50721
 Source Host           : localhost:3306
 Source Schema         : mall_spider_test

 Target Server Type    : MySQL
 Target Server Version : 50721
 File Encoding         : 65001

 Date: 19/01/2019 15:05:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cmm_sys_commodity
-- ----------------------------
DROP TABLE IF EXISTS `cmm_sys_commodity`;
CREATE TABLE `cmm_sys_commodity` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `version` int(11) NOT NULL DEFAULT '1',
  `content` varchar(3000) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;

-- ----------------------------
-- Table structure for cmm_sys_stream_good_data
-- ----------------------------
DROP TABLE IF EXISTS `cmm_sys_stream_good_data`;
CREATE TABLE `cmm_sys_stream_good_data` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_by` bigint(20) NOT NULL DEFAULT '0',
  `update_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_by` bigint(20) NOT NULL DEFAULT '0',
  `version` int(11) NOT NULL DEFAULT '0',
  `raw_data` longtext NOT NULL,
  `flag` int(11) NOT NULL DEFAULT '10',
  `category_name` varchar(50) NOT NULL DEFAULT '',
  `brand_name` varchar(50) NOT NULL DEFAULT '',
  `category_id` varchar(20) NOT NULL DEFAULT '',
  `date` varchar(10) NOT NULL DEFAULT '',
  `model_name` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=143216 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for cmm_sys_stream_handle_task
-- ----------------------------
DROP TABLE IF EXISTS `cmm_sys_stream_handle_task`;
CREATE TABLE `cmm_sys_stream_handle_task` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL DEFAULT '0',
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_by` bigint(20) NOT NULL DEFAULT '0',
  `update_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_by` bigint(20) NOT NULL DEFAULT '0',
  `version` int(11) NOT NULL DEFAULT '0',
  `raw_data` longtext NOT NULL,
  `origin_id` bigint(20) NOT NULL DEFAULT '0',
  `date` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13806 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for cmm_sys_stream_opt_data
-- ----------------------------
DROP TABLE IF EXISTS `cmm_sys_stream_opt_data`;
CREATE TABLE `cmm_sys_stream_opt_data` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL DEFAULT '0',
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_by` bigint(20) NOT NULL DEFAULT '0',
  `update_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_by` bigint(20) NOT NULL DEFAULT '0',
  `version` int(11) NOT NULL DEFAULT '0',
  `raw_data` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8929 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for cmm_sys_stream_risk
-- ----------------------------
DROP TABLE IF EXISTS `cmm_sys_stream_risk`;
CREATE TABLE `cmm_sys_stream_risk` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL DEFAULT '0',
  `raw_data` varchar(50) NOT NULL DEFAULT '',
  `version` int(11) NOT NULL DEFAULT '0',
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_type_raw_data` (`type`,`raw_data`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=156 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for cmm_sys_stream_unhandle_task
-- ----------------------------
DROP TABLE IF EXISTS `cmm_sys_stream_unhandle_task`;
CREATE TABLE `cmm_sys_stream_unhandle_task` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL DEFAULT '0',
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_by` bigint(20) NOT NULL DEFAULT '0',
  `update_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_by` bigint(20) NOT NULL DEFAULT '0',
  `version` int(11) NOT NULL DEFAULT '0',
  `raw_data` longtext NOT NULL,
  `origin_id` bigint(20) NOT NULL DEFAULT '0',
  `date` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=167050 DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
