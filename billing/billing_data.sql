-- MySQL dump 10.16  Distrib 10.1.12-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: billing
-- ------------------------------------------------------
-- Server version	10.1.12-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `account_id` varchar(64) NOT NULL,
  `username` varchar(64) DEFAULT NULL,
  `cash_balance` decimal(10,4) DEFAULT NULL,
  `gift_balance` decimal(10,4) DEFAULT NULL,
  `type` varchar(32) NOT NULL,
  `credit_line` decimal(10,4) DEFAULT NULL,
  `status` varchar(32) NOT NULL DEFAULT 'normal',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `user_id` varchar(64) DEFAULT NULL,
  `project_id` varchar(64) DEFAULT NULL,
  `frozen_status` varchar(64) DEFAULT NULL,
  `frozon_at` timestamp NULL DEFAULT NULL,
  `current_month_amount` decimal(10,4) DEFAULT '0.0000',
  `current_month_standard_amount` decimal(10,4) DEFAULT '0.0000',
  `parent_account` varchar(64) DEFAULT NULL,
  `salesman_id` int(11) DEFAULT NULL,
  `company_property` varchar(64) DEFAULT NULL,
  `customer_level` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='账户';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES ('1870069a-682d-11e6-a2e2-005056b994a6','ceilometer',0.0000,0.0000,'normal',0.0000,'normal','2016-08-21 21:55:57',NULL,'26d6e9ee2a8b42b48781029c5fae05ac','62d450c4856e4bb6825dc913347a8694',NULL,NULL,0.0000,0.0000,NULL,NULL,NULL,NULL);
INSERT INTO `account` VALUES ('1870089f-682d-11e6-a2e2-005056b994a6','demo',0.0000,0.0000,'normal',0.0000,'normal','2016-08-21 21:55:57',NULL,'b9cd6e486a0d4ca59d7241803014046c','84bc7367dd51496d93c57d9acb9f7d1c',NULL,NULL,0.0000,0.0000,NULL,NULL,NULL,NULL);
INSERT INTO `account` VALUES ('18700976-682d-11e6-a2e2-005056b994a6','admin',0.0000,0.0000,'normal',0.0000,'normal','2016-08-21 21:55:57',NULL,'6944c1de6f96421b8d182d05702a37e7','b8de93e20148470dbc45e802240c3d10',NULL,NULL,0.0000,0.0000,NULL,NULL,NULL,NULL);
INSERT INTO `account` VALUES ('21400308-cecb-48dd-b65e-26f9caee6716','test00',0.0000,0.0000,'normal',0.0000,'normal','2016-10-08 02:11:53',NULL,'69dd85f51fed475da82ce6b4e45a22c8','069e0d4570594fa29473c6857263f469',NULL,NULL,0.0000,0.0000,NULL,NULL,NULL,NULL);
INSERT INTO `account` VALUES ('52c1c6f8-1c4e-4c8d-b99f-a541c784bba1','test00',0.0000,0.0000,'normal',0.0000,'normal','2016-10-08 02:13:04',NULL,'75b7aeca836b497ea02afe6cc714b23c','63cba4605ea948cd9a09e5707a88ef1b',NULL,NULL,0.0000,0.0000,NULL,NULL,NULL,NULL);
INSERT INTO `account` VALUES ('5a1ef93f-2ba3-4901-8e94-d8b4505d5111','test00',0.0000,0.0000,'normal',0.0000,'normal','2016-10-08 01:48:38',NULL,'450cd912c4b7497daf6201b60187e4e9','11d1994470eb4d71850a7ecb70d03cbb',NULL,NULL,0.0000,0.0000,NULL,NULL,NULL,NULL);
INSERT INTO `account` VALUES ('7895d132-abf4-4384-b0bd-9b0e354cc185','test00',0.0000,0.0000,'normal',0.0000,'deleted','2016-10-09 00:34:08','2016-10-09 00:34:41','a0106c7fe37d412a8c208f584d2afcd1','5090dfca667e46468ac93484598df738',NULL,NULL,0.0000,0.0000,NULL,NULL,NULL,NULL);
INSERT INTO `account` VALUES ('8f60f5ff-4c9d-4c32-8573-bd1a315b21f5','test00',0.0000,0.0000,'normal',0.0000,'deleted','2016-10-08 02:16:22','2016-10-08 02:16:39','c223f3deed1e4a029e46de2e5637a434','1adc9895709c4b8ab653de40a7a431b0',NULL,NULL,0.0000,0.0000,NULL,NULL,NULL,NULL);
INSERT INTO `account` VALUES ('ae1f975e-e656-47d5-b02c-e958c751a848','test00',0.0000,0.0000,'normal',0.0000,'normal','2016-10-08 02:09:24',NULL,'c49453403cf44268a3f317ac6987388d','1664e37573e249cbb545bce35f59e70d',NULL,NULL,0.0000,0.0000,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `action_log`
--

DROP TABLE IF EXISTS `action_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `action_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `user_name` varchar(128) DEFAULT NULL,
  `resource_name` varchar(128) DEFAULT NULL,
  `resource_type` varchar(64) DEFAULT NULL,
  `action_id` varchar(64) DEFAULT NULL,
  `action_name` varchar(128) DEFAULT NULL,
  `detail` varchar(4000) DEFAULT NULL,
  `action_at` timestamp NULL DEFAULT NULL,
  `status` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `action_log`
--

LOCK TABLES `action_log` WRITE;
/*!40000 ALTER TABLE `action_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `action_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address` (
  `address_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` varchar(64) NOT NULL,
  `name` varchar(32) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `post_code` varchar(32) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `mobile` varchar(32) DEFAULT NULL,
  `status` varchar(32) DEFAULT 'using',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`address_id`),
  KEY `FK_fk_address_account_id` (`account_id`),
  CONSTRAINT `FK_fk_address_account_id` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='地址';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advert`
--

DROP TABLE IF EXISTS `advert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advert` (
  `advert_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) DEFAULT NULL,
  `url` varchar(256) DEFAULT NULL,
  `started_at` timestamp NULL DEFAULT NULL,
  `ended_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`advert_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advert`
--

LOCK TABLES `advert` WRITE;
/*!40000 ALTER TABLE `advert` DISABLE KEYS */;
/*!40000 ALTER TABLE `advert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alipay_info`
--

DROP TABLE IF EXISTS `alipay_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alipay_info` (
  `alipay_info_id` int(11) NOT NULL AUTO_INCREMENT,
  `recharge_id` int(11) DEFAULT NULL,
  `order_no` varchar(20) DEFAULT NULL,
  `payer` varchar(32) DEFAULT NULL,
  `pay_account` varchar(64) DEFAULT NULL,
  `trade_no` varchar(64) DEFAULT NULL,
  `status` varchar(32) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `remark` varchar(256) DEFAULT NULL,
  `pay_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `amount` decimal(8,2) DEFAULT NULL,
  `bank_no` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`alipay_info_id`),
  KEY `FK_fk_alipay_info_recharge` (`recharge_id`),
  CONSTRAINT `FK_fk_alipay_info_recharge` FOREIGN KEY (`recharge_id`) REFERENCES `recharge` (`recharge_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='支付宝信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alipay_info`
--

LOCK TABLES `alipay_info` WRITE;
/*!40000 ALTER TABLE `alipay_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `alipay_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bill`
--

DROP TABLE IF EXISTS `bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bill` (
  `bill_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` varchar(64) NOT NULL,
  `no` varchar(32) NOT NULL,
  `started_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ended_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `amount` decimal(8,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `standard_amount` decimal(8,2) DEFAULT NULL,
  `gift_amount` decimal(8,2) DEFAULT NULL,
  `type` varchar(32) DEFAULT 'cloud',
  PRIMARY KEY (`bill_id`),
  KEY `FK_fk_bill_account_id` (`account_id`),
  CONSTRAINT `FK_fk_bill_account_id` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='账单';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill`
--

LOCK TABLES `bill` WRITE;
/*!40000 ALTER TABLE `bill` DISABLE KEYS */;
/*!40000 ALTER TABLE `bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bill_item`
--

DROP TABLE IF EXISTS `bill_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bill_item` (
  `bill_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `resource_id` varchar(64) NOT NULL,
  `region_id` varchar(64) NOT NULL,
  `resource_type` varchar(32) DEFAULT NULL,
  `started_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ended_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `amount` decimal(8,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `resource_name` varchar(64) DEFAULT NULL,
  `standard_amount` decimal(8,2) DEFAULT NULL,
  `gift_amount` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`bill_item_id`),
  KEY `FK_fk_bill_detail_bill_id` (`bill_id`),
  CONSTRAINT `FK_fk_bill_detail_bill_id` FOREIGN KEY (`bill_id`) REFERENCES `bill` (`bill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='账单项';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill_item`
--

LOCK TABLES `bill_item` WRITE;
/*!40000 ALTER TABLE `bill_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `bill_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_item`
--

DROP TABLE IF EXISTS `billing_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `billing_item` (
  `billing_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `region_id` varchar(64) DEFAULT NULL,
  `billing_item` varchar(64) NOT NULL,
  `unit` varchar(64) DEFAULT NULL,
  `price` decimal(10,4) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`billing_item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8 COMMENT='计费项';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_item`
--

LOCK TABLES `billing_item` WRITE;
/*!40000 ALTER TABLE `billing_item` DISABLE KEYS */;
INSERT INTO `billing_item` VALUES (1,'RegionCdn','cdnflow_1_G','yuan/G.month',0.3000,NULL,NULL);
INSERT INTO `billing_item` VALUES (2,'RegionCdn','cdnbandwidth_1_M','yuan/M.day',1.2500,NULL,NULL);
INSERT INTO `billing_item` VALUES (3,'RegionOne','instance_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (4,'RegionOne','cpu_1_core','yuan/core.hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (5,'RegionOne','memory_1024_M','yuan/1024M.hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (6,'RegionOne','disk_1_G','yuan/G.hour',0.0004,NULL,NULL);
INSERT INTO `billing_item` VALUES (7,'RegionOne','snapshot_1_G','yuan/G.hour',0.0002,NULL,NULL);
INSERT INTO `billing_item` VALUES (8,'RegionOne','router_1','yuan/hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (9,'RegionOne','ip_1','yuan/hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (10,'RegionOne','bandwidth_1_M','yuan/M.hour',0.0960,NULL,NULL);
INSERT INTO `billing_item` VALUES (11,'RegionOne','image_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (12,'RegionOne','vpn_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (13,'RegionTwo','instance_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (14,'RegionTwo','cpu_1_core','yuan/core.hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (15,'RegionTwo','memory_1024_M','yuan/1024M.hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (16,'RegionTwo','disk_1_G','yuan/G.hour',0.0004,NULL,NULL);
INSERT INTO `billing_item` VALUES (17,'RegionTwo','snapshot_1_G','yuan/G.hour',0.0002,NULL,NULL);
INSERT INTO `billing_item` VALUES (18,'RegionTwo','router_1','yuan/hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (19,'RegionTwo','ip_1','yuan/hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (20,'RegionTwo','bandwidth_1_M','yuan/M.hour',0.0960,NULL,NULL);
INSERT INTO `billing_item` VALUES (21,'RegionTwo','image_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (22,'RegionTwo','vpn_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (23,'RegionThree','instance_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (24,'RegionThree','cpu_1_core','yuan/core.hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (25,'RegionThree','memory_1024_M','yuan/1024M.hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (26,'RegionThree','disk_1_G','yuan/G.hour',0.0004,NULL,NULL);
INSERT INTO `billing_item` VALUES (27,'RegionThree','snapshot_1_G','yuan/G.hour',0.0002,NULL,NULL);
INSERT INTO `billing_item` VALUES (28,'RegionThree','router_1','yuan/hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (29,'RegionThree','ip_1','yuan/hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (30,'RegionThree','bandwidth_1_M','yuan/M.hour',0.0960,NULL,NULL);
INSERT INTO `billing_item` VALUES (31,'RegionThree','image_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (32,'RegionThree','vpn_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (33,'RegionFour','instance_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (34,'RegionFour','cpu_1_core','yuan/core.hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (35,'RegionFour','memory_1024_M','yuan/1024M.hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (36,'RegionFour','disk_1_G','yuan/G.hour',0.0004,NULL,NULL);
INSERT INTO `billing_item` VALUES (37,'RegionFour','snapshot_1_G','yuan/G.hour',0.0002,NULL,NULL);
INSERT INTO `billing_item` VALUES (38,'RegionFour','router_1','yuan/hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (39,'RegionFour','ip_1','yuan/hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (40,'RegionFour','bandwidth_1_M','yuan/M.hour',0.0960,NULL,NULL);
INSERT INTO `billing_item` VALUES (41,'RegionFour','image_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (42,'RegionFour','vpn_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (43,'RegionFive','instance_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (44,'RegionFive','cpu_1_core','yuan/core.hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (45,'RegionFive','memory_1024_M','yuan/1024M.hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (46,'RegionFive','disk_1_G','yuan/G.hour',0.0004,NULL,NULL);
INSERT INTO `billing_item` VALUES (47,'RegionFive','snapshot_1_G','yuan/G.hour',0.0002,NULL,NULL);
INSERT INTO `billing_item` VALUES (48,'RegionFive','router_1','yuan/hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (49,'RegionFive','ip_1','yuan/hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (50,'RegionFive','bandwidth_1_M','yuan/M.hour',0.0960,NULL,NULL);
INSERT INTO `billing_item` VALUES (51,'RegionFive','image_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (52,'RegionFive','vpn_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (53,'Regionsix','instance_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (54,'Regionsix','cpu_1_core','yuan/core.hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (55,'Regionsix','memory_1024_M','yuan/1024M.hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (56,'Regionsix','disk_1_G','yuan/G.hour',0.0004,NULL,NULL);
INSERT INTO `billing_item` VALUES (57,'Regionsix','snapshot_1_G','yuan/G.hour',0.0002,NULL,NULL);
INSERT INTO `billing_item` VALUES (58,'Regionsix','router_1','yuan/hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (59,'Regionsix','ip_1','yuan/hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (60,'Regionsix','bandwidth_1_M','yuan/M.hour',0.0960,NULL,NULL);
INSERT INTO `billing_item` VALUES (61,'Regionsix','image_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (62,'Regionsix','vpn_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (63,'RegionSeven','instance_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (64,'RegionSeven','cpu_1_core','yuan/core.hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (65,'RegionSeven','memory_1024_M','yuan/1024M.hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (66,'RegionSeven','disk_1_G','yuan/G.hour',0.0004,NULL,NULL);
INSERT INTO `billing_item` VALUES (67,'RegionSeven','snapshot_1_G','yuan/G.hour',0.0002,NULL,NULL);
INSERT INTO `billing_item` VALUES (68,'RegionSeven','router_1','yuan/hour',0.0420,NULL,NULL);
INSERT INTO `billing_item` VALUES (69,'RegionSeven','ip_1','yuan/hour',0.0690,NULL,NULL);
INSERT INTO `billing_item` VALUES (70,'RegionSeven','bandwidth_1_M','yuan/M.hour',0.0960,NULL,NULL);
INSERT INTO `billing_item` VALUES (71,'RegionSeven','image_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (72,'RegionSeven','vpn_1','yuan/hour',0.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (73,'naas','normal_0-200_0-200','yuan/M.day',28.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (74,'naas','normal_201-500_0-200','yuan/M.day',29.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (75,'naas','normal_501-1000_0-200','yuan/M.day',30.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (76,'naas','normal_1001-9999_0-200','yuan/M.day',31.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (77,'naas','normal_0-200_201-500','yuan/M.day',32.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (78,'naas','normal_201-500_201-500','yuan/M.day',33.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (79,'naas','normal_501-1000_201-500','yuan/M.day',34.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (80,'naas','normal_1001-9999_201-500','yuan/M.day',35.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (81,'naas','normal_0-200_501-1000','yuan/M.day',36.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (82,'naas','normal_201-500_501-1000','yuan/M.day',37.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (83,'naas','normal_501-1000_501-1000','yuan/M.day',38.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (84,'naas','normal_1001-9999_501-1000','yuan/M.day',39.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (85,'naas','normal_0-200_1001-99999','yuan/M.day',40.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (86,'naas','normal_201-500_1001-99999','yuan/M.day',41.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (87,'naas','normal_501-1000_1001-99999','yuan/M.day',42.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (88,'naas','normal_1001-9999_1001-99999','yuan/M.day',43.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (89,'naas','ha_0-200_0-200','yuan/M.day',44.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (90,'naas','ha_201-500_0-200','yuan/M.day',45.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (91,'naas','ha_501-1000_0-200','yuan/M.day',46.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (92,'naas','ha_1001-9999_0-200','yuan/M.day',47.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (93,'naas','ha_0-200_201-500','yuan/M.day',48.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (94,'naas','ha_201-500_201-500','yuan/M.day',49.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (95,'naas','ha_501-1000_201-500','yuan/M.day',50.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (96,'naas','ha_1001-9999_201-500','yuan/M.day',51.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (97,'naas','ha_0-200_501-1000','yuan/M.day',52.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (98,'naas','ha_201-500_501-1000','yuan/M.day',53.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (99,'naas','ha_501-1000_501-1000','yuan/M.day',54.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (100,'naas','ha_1001-9999_501-1000','yuan/M.day',55.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (101,'naas','ha_0-200_1001-99999','yuan/M.day',56.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (102,'naas','ha_201-500_1001-99999','yuan/M.day',57.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (103,'naas','ha_501-1000_1001-99999','yuan/M.day',58.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (104,'naas','ha_1001-9999_1001-99999','yuan/M.day',59.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (105,'naas','trust_0-200_0-200','yuan/M.day',60.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (106,'naas','trust_201-500_0-200','yuan/M.day',61.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (107,'naas','trust_501-1000_0-200','yuan/M.day',62.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (108,'naas','trust_1001-9999_0-200','yuan/M.day',63.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (109,'naas','trust_0-200_201-500','yuan/M.day',64.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (110,'naas','trust_201-500_201-500','yuan/M.day',65.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (111,'naas','trust_501-1000_201-500','yuan/M.day',66.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (112,'naas','trust_1001-9999_201-500','yuan/M.day',67.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (113,'naas','trust_0-200_501-1000','yuan/M.day',68.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (114,'naas','trust_201-500_501-1000','yuan/M.day',69.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (115,'naas','trust_501-1000_501-1000','yuan/M.day',70.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (116,'naas','trust_1001-9999_501-1000','yuan/M.day',71.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (117,'naas','trust_0-200_1001-99999','yuan/M.day',72.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (118,'naas','trust_201-500_1001-99999','yuan/M.day',73.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (119,'naas','trust_501-1000_1001-99999','yuan/M.day',74.0000,NULL,NULL);
INSERT INTO `billing_item` VALUES (120,'naas','trust_1001-9999_1001-99999','yuan/M.day',75.0000,NULL,NULL);
/*!40000 ALTER TABLE `billing_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consumption`
--

DROP TABLE IF EXISTS `consumption`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consumption` (
  `consumption_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` varchar(64) NOT NULL,
  `amount` decimal(10,4) NOT NULL,
  `billing_item` varchar(64) DEFAULT NULL,
  `sum` decimal(10,2) DEFAULT NULL,
  `price` decimal(10,4) DEFAULT NULL,
  `unit` varchar(64) DEFAULT NULL,
  `discount_ratio` decimal(3,2) DEFAULT NULL,
  `resource_id` varchar(64) NOT NULL,
  `resource_name` varchar(64) DEFAULT NULL,
  `parent_id` varchar(64) DEFAULT NULL,
  `region_id` varchar(64) NOT NULL,
  `discounted_at` timestamp NULL DEFAULT NULL,
  `discount_by` varchar(32) DEFAULT NULL,
  `resource_type` varchar(32) NOT NULL,
  `started_at` timestamp NULL DEFAULT NULL,
  `ended_at` timestamp NULL DEFAULT NULL,
  `standard_amount` decimal(10,4) DEFAULT NULL,
  `parent_discount_ratio` decimal(3,2) DEFAULT NULL,
  `rebate_amount` decimal(10,4) DEFAULT '0.0000',
  PRIMARY KEY (`consumption_id`),
  UNIQUE KEY `consumption_resource_date` (`resource_id`,`started_at`,`ended_at`),
  KEY `FK_fk_consumption_account_id` (`account_id`),
  KEY `index_resource_id` (`resource_id`),
  CONSTRAINT `FK_fk_consumption_account_id` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='消费记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consumption`
--

LOCK TABLES `consumption` WRITE;
/*!40000 ALTER TABLE `consumption` DISABLE KEYS */;
/*!40000 ALTER TABLE `consumption` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact` (
  `contact_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `position` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `telephone` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `account_id` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `remark` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discount`
--

DROP TABLE IF EXISTS `discount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discount` (
  `discount_id` int(11) NOT NULL AUTO_INCREMENT,
  `billing_item_id` int(11) DEFAULT NULL,
  `account_id` varchar(64) DEFAULT NULL,
  `discount_ratio` decimal(3,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`discount_id`),
  KEY `FK_fk_discount_account_id` (`account_id`),
  KEY `FK_fk_discount_billing_item_id` (`billing_item_id`),
  CONSTRAINT `FK_fk_discount_account_id` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`),
  CONSTRAINT `FK_fk_discount_billing_item_id` FOREIGN KEY (`billing_item_id`) REFERENCES `billing_item` (`billing_item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='折扣';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discount`
--

LOCK TABLES `discount` WRITE;
/*!40000 ALTER TABLE `discount` DISABLE KEYS */;
/*!40000 ALTER TABLE `discount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gift`
--

DROP TABLE IF EXISTS `gift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gift` (
  `gift_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(20) DEFAULT NULL,
  `gift_by` varchar(64) DEFAULT NULL,
  `status` varchar(32) DEFAULT NULL,
  `remark` varchar(256) DEFAULT NULL,
  `gift_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `amount` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`gift_id`),
  KEY `FK_fk_gift_order` (`order_no`),
  CONSTRAINT `FK_fk_gift_order` FOREIGN KEY (`order_no`) REFERENCES `order` (`order_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='赠送';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gift`
--

LOCK TABLES `gift` WRITE;
/*!40000 ALTER TABLE `gift` DISABLE KEYS */;
/*!40000 ALTER TABLE `gift` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instead_recharge`
--

DROP TABLE IF EXISTS `instead_recharge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `instead_recharge` (
  `instead_recharge_id` int(11) NOT NULL AUTO_INCREMENT,
  `recharge_id` int(11) DEFAULT NULL,
  `instead_recharge_by` varchar(32) DEFAULT NULL,
  `instead_recharge_account` varchar(64) DEFAULT NULL,
  `remark` varchar(256) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`instead_recharge_id`),
  KEY `FK_fk_instead_recharge_recharge` (`recharge_id`),
  CONSTRAINT `FK_fk_instead_recharge_recharge` FOREIGN KEY (`recharge_id`) REFERENCES `recharge` (`recharge_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='代充值';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instead_recharge`
--

LOCK TABLES `instead_recharge` WRITE;
/*!40000 ALTER TABLE `instead_recharge` DISABLE KEYS */;
/*!40000 ALTER TABLE `instead_recharge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `invoice` (
  `invoice_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` varchar(64) NOT NULL,
  `address_id` int(11) DEFAULT NULL,
  `type` varchar(32) DEFAULT NULL,
  `title` varchar(64) DEFAULT NULL,
  `amount` decimal(8,2) DEFAULT NULL,
  `prove` varchar(256) DEFAULT NULL,
  `apply_at` timestamp NULL DEFAULT NULL,
  `status` varchar(32) DEFAULT NULL,
  `post_by` varchar(64) DEFAULT NULL,
  `process_by` varchar(64) DEFAULT NULL,
  `reason` varchar(64) DEFAULT NULL,
  `express_no` varchar(64) DEFAULT NULL,
  `invoice_no` varchar(64) DEFAULT NULL,
  `process_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`invoice_id`),
  KEY `FK_fk_invoice_account_id` (`account_id`),
  KEY `FK_fk_invoice_address_id` (`address_id`),
  CONSTRAINT `FK_fk_invoice_account_id` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`),
  CONSTRAINT `FK_fk_invoice_address_id` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='发票';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice`
--

LOCK TABLES `invoice` WRITE;
/*!40000 ALTER TABLE `invoice` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order` (
  `order_no` varchar(20) NOT NULL,
  `account_id` varchar(64) DEFAULT NULL,
  `payment_type` varchar(32) DEFAULT NULL,
  `amount` decimal(8,2) DEFAULT NULL,
  `status` varchar(32) DEFAULT NULL,
  `remark` varchar(256) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`order_no`),
  KEY `FK_fk_order_account` (`account_id`),
  CONSTRAINT `FK_fk_order_account` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `codename` (`codename`)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES (1,'客户管理','menu_customer');
INSERT INTO `permission` VALUES (2,'客户列表','submenu_customer_list');
INSERT INTO `permission` VALUES (3,'查看客户列表','customer_ViewList');
INSERT INTO `permission` VALUES (4,'查看客户详情','customer_ViewDetail');
INSERT INTO `permission` VALUES (5,'修改客户基本信息','customer_basic_modify');
INSERT INTO `permission` VALUES (6,'修改客户账户类型','account_type_modify');
INSERT INTO `permission` VALUES (7,'管理区域','region_manage');
INSERT INTO `permission` VALUES (8,'折扣管理','discount_manage');
INSERT INTO `permission` VALUES (9,'管理联系人','contact_manage');
INSERT INTO `permission` VALUES (10,'查看联系人','contact_view');
INSERT INTO `permission` VALUES (11,'赠送金钱','money_gift');
INSERT INTO `permission` VALUES (12,'分配业务员','sales_assign');
INSERT INTO `permission` VALUES (13,'升级客户为分销商','project_admin_upgrade');
INSERT INTO `permission` VALUES (14,'查看子账户','subaccount_view');
INSERT INTO `permission` VALUES (15,'资源列表','submenu_resource_list');
INSERT INTO `permission` VALUES (16,'任务','menu_task');
INSERT INTO `permission` VALUES (17,'工单列表','submenu_workorder_list');
INSERT INTO `permission` VALUES (18,'创建工单','workorder_create');
INSERT INTO `permission` VALUES (19,'操作工单','workorder_operate');
INSERT INTO `permission` VALUES (20,'IP查询','submenu_IP_search');
INSERT INTO `permission` VALUES (21,'财务','menu_finance');
INSERT INTO `permission` VALUES (22,'账单','submenu_bill');
INSERT INTO `permission` VALUES (24,'充值','submenu_recharge');
INSERT INTO `permission` VALUES (25,'发票','submenu_invoice');
INSERT INTO `permission` VALUES (26,'系统设置','menu_system_settings');
INSERT INTO `permission` VALUES (27,'操作日志','submenu_operation_log');
INSERT INTO `permission` VALUES (28,'用户','submenu_user');
INSERT INTO `permission` VALUES (29,'角色','submenu_role');
INSERT INTO `permission` VALUES (30,'权限','submenu_permission');
INSERT INTO `permission` VALUES (59,'添加用户','add_user');
INSERT INTO `permission` VALUES (71,'账单列表查看','bill_list');
INSERT INTO `permission` VALUES (72,'账单记录详情查看','bill_list_detail');
INSERT INTO `permission` VALUES (73,'充值列表查看','recharge_list');
INSERT INTO `permission` VALUES (74,'充值记录详情查看','recharge_list_detail');
INSERT INTO `permission` VALUES (75,'代充值','recharge_instead_recharge');
INSERT INTO `permission` VALUES (76,'发票列表查看','invoice_list');
INSERT INTO `permission` VALUES (77,'未处理发票处理','invoice_list_handle');
INSERT INTO `permission` VALUES (79,'已处理发票详情查看','invoice_list_detail');
INSERT INTO `permission` VALUES (80,'查看用户详情','view_user_profile');
INSERT INTO `permission` VALUES (81,'编辑用户信息','edit_user_profile');
INSERT INTO `permission` VALUES (82,'重置用户密码','reset_password');
INSERT INTO `permission` VALUES (83,'删除用户','delete_user');
INSERT INTO `permission` VALUES (86,'添加角色','add_role');
INSERT INTO `permission` VALUES (87,'编辑角色','edit_role');
INSERT INTO `permission` VALUES (88,'管理角色的权限','manage_role_permission');
INSERT INTO `permission` VALUES (89,'删除角色','delete_role');
INSERT INTO `permission` VALUES (90,'添加权限','add_permission');
INSERT INTO `permission` VALUES (92,'编辑权限','edit_permission');
INSERT INTO `permission` VALUES (94,'创建客户','customer_create');
INSERT INTO `permission` VALUES (96,'删除权限','delete_permission');
INSERT INTO `permission` VALUES (104,'个人信息','submenu_user_profile');
INSERT INTO `permission` VALUES (105,'公告列表获取','advert_list');
INSERT INTO `permission` VALUES (106,'公告编辑','advert_list_edit');
INSERT INTO `permission` VALUES (107,'公告创建','advert_create');
INSERT INTO `permission` VALUES (108,'公告删除','advert_delete');
INSERT INTO `permission` VALUES (110,'个人信息密码修改','change_password');
INSERT INTO `permission` VALUES (112,'用户角色分配','manage_user_role');
INSERT INTO `permission` VALUES (113,'个人信息修改','user_profile_edit');
INSERT INTO `permission` VALUES (114,'公告菜单','submenu_advert');
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_type`
--

DROP TABLE IF EXISTS `product_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_type` (
  `product_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `billing_item_id` int(11) DEFAULT NULL,
  `network_type` varchar(128) DEFAULT NULL,
  `billing_item` varchar(32) DEFAULT NULL,
  `distance_start` int(11) DEFAULT NULL,
  `distance_end` int(11) DEFAULT NULL,
  `bandwidth_start` int(11) DEFAULT NULL,
  `bandwidth_end` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`product_type_id`),
  KEY `Reference_product_type_billing_item_FK` (`billing_item_id`),
  CONSTRAINT `Reference_product_type_billing_item_FK` FOREIGN KEY (`billing_item_id`) REFERENCES `billing_item` (`billing_item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_type`
--

LOCK TABLES `product_type` WRITE;
/*!40000 ALTER TABLE `product_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rebate_bill`
--

DROP TABLE IF EXISTS `rebate_bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rebate_bill` (
  `rebate_bill_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` varchar(64) NOT NULL,
  `no` varchar(32) NOT NULL,
  `started_at` timestamp NULL DEFAULT NULL,
  `ended_at` timestamp NULL DEFAULT NULL,
  `rebate_amount` decimal(8,2) DEFAULT '0.00',
  `subaccount_amount` decimal(8,2) DEFAULT '0.00',
  `subaccount_gift_amount` decimal(8,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`rebate_bill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rebate_bill`
--

LOCK TABLES `rebate_bill` WRITE;
/*!40000 ALTER TABLE `rebate_bill` DISABLE KEYS */;
/*!40000 ALTER TABLE `rebate_bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rebate_bill_item`
--

DROP TABLE IF EXISTS `rebate_bill_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rebate_bill_item` (
  `rebate_bill_item` int(11) NOT NULL AUTO_INCREMENT,
  `rebate_subbill_id` int(11) DEFAULT NULL,
  `resource_id` varchar(64) DEFAULT NULL,
  `resource_name` varchar(64) DEFAULT NULL,
  `resource_type` varchar(32) DEFAULT NULL,
  `region_id` varchar(64) DEFAULT NULL,
  `amount` decimal(8,2) DEFAULT NULL,
  `gift_amount` decimal(8,2) DEFAULT NULL,
  `rebate_amount` decimal(8,2) DEFAULT NULL,
  `started_at` timestamp NULL DEFAULT NULL,
  `ended_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`rebate_bill_item`),
  KEY `FK_rebate_bill_item_rebate_subill_id` (`rebate_subbill_id`),
  CONSTRAINT `FK_rebate_bill_item_rebate_subill_id` FOREIGN KEY (`rebate_subbill_id`) REFERENCES `rebate_subbill` (`rebate_subbill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rebate_bill_item`
--

LOCK TABLES `rebate_bill_item` WRITE;
/*!40000 ALTER TABLE `rebate_bill_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `rebate_bill_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rebate_subbill`
--

DROP TABLE IF EXISTS `rebate_subbill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rebate_subbill` (
  `rebate_subbill_id` int(11) NOT NULL AUTO_INCREMENT,
  `rebate_bill_id` int(11) NOT NULL,
  `account_id` varchar(64) NOT NULL,
  `rebate_amount` decimal(8,2) DEFAULT '0.00',
  `amount` decimal(8,2) DEFAULT '0.00',
  `gift_amount` decimal(8,2) DEFAULT '0.00',
  `started_at` timestamp NULL DEFAULT NULL,
  `ended_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`rebate_subbill_id`),
  KEY `FK_rebate_subbill_rebate_bill_id` (`rebate_bill_id`),
  CONSTRAINT `FK_rebate_subbill_rebate_bill_id` FOREIGN KEY (`rebate_bill_id`) REFERENCES `rebate_bill` (`rebate_bill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rebate_subbill`
--

LOCK TABLES `rebate_subbill` WRITE;
/*!40000 ALTER TABLE `rebate_subbill` DISABLE KEYS */;
/*!40000 ALTER TABLE `rebate_subbill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recharge`
--

DROP TABLE IF EXISTS `recharge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recharge` (
  `recharge_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(20) DEFAULT NULL,
  `payment_way` varchar(32) DEFAULT NULL,
  `receive_account` varchar(64) DEFAULT NULL,
  `status` varchar(32) DEFAULT NULL,
  `is_instead_recharge` tinyint(1) DEFAULT NULL,
  `remark` varchar(256) DEFAULT NULL,
  `pay_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `amount` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`recharge_id`),
  KEY `FK_fk_recharge_order` (`order_no`),
  CONSTRAINT `FK_fk_recharge_order` FOREIGN KEY (`order_no`) REFERENCES `order` (`order_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='充值';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recharge`
--

LOCK TABLES `recharge` WRITE;
/*!40000 ALTER TABLE `recharge` DISABLE KEYS */;
/*!40000 ALTER TABLE `recharge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `codename` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'管理员','admin');
INSERT INTO `role` VALUES (2,'销售','salesman');
INSERT INTO `role` VALUES (3,'财务','finance');
INSERT INTO `role` VALUES (4,'运维','dev_ops');
INSERT INTO `role` VALUES (5,'客服','support');
INSERT INTO `role` VALUES (6,'公告员','advert');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permission_relation`
--

DROP TABLE IF EXISTS `role_permission_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_permission_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_id` int(11) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `role_permission__permission_id_43b94f258a694004_fk_permission_id` (`permission_id`),
  KEY `role_permission_relation_role_id_8fb68e39119e615_fk_role_id` (`role_id`),
  CONSTRAINT `role_permission__permission_id_43b94f258a694004_fk_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`),
  CONSTRAINT `role_permission_relation_role_id_8fb68e39119e615_fk_role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2106 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permission_relation`
--

LOCK TABLES `role_permission_relation` WRITE;
/*!40000 ALTER TABLE `role_permission_relation` DISABLE KEYS */;
INSERT INTO `role_permission_relation` VALUES (10,1,5);
INSERT INTO `role_permission_relation` VALUES (11,2,5);
INSERT INTO `role_permission_relation` VALUES (12,15,5);
INSERT INTO `role_permission_relation` VALUES (13,16,5);
INSERT INTO `role_permission_relation` VALUES (14,17,5);
INSERT INTO `role_permission_relation` VALUES (15,20,5);
INSERT INTO `role_permission_relation` VALUES (16,26,5);
INSERT INTO `role_permission_relation` VALUES (17,27,5);
INSERT INTO `role_permission_relation` VALUES (18,3,5);
INSERT INTO `role_permission_relation` VALUES (19,4,5);
INSERT INTO `role_permission_relation` VALUES (20,14,5);
INSERT INTO `role_permission_relation` VALUES (21,21,5);
INSERT INTO `role_permission_relation` VALUES (22,22,5);
INSERT INTO `role_permission_relation` VALUES (23,24,5);
INSERT INTO `role_permission_relation` VALUES (24,25,5);
INSERT INTO `role_permission_relation` VALUES (25,10,5);
INSERT INTO `role_permission_relation` VALUES (26,71,5);
INSERT INTO `role_permission_relation` VALUES (27,72,5);
INSERT INTO `role_permission_relation` VALUES (28,73,5);
INSERT INTO `role_permission_relation` VALUES (29,74,5);
INSERT INTO `role_permission_relation` VALUES (30,76,5);
INSERT INTO `role_permission_relation` VALUES (31,79,5);
INSERT INTO `role_permission_relation` VALUES (32,18,5);
INSERT INTO `role_permission_relation` VALUES (33,19,5);
INSERT INTO `role_permission_relation` VALUES (34,104,5);
INSERT INTO `role_permission_relation` VALUES (35,110,5);
INSERT INTO `role_permission_relation` VALUES (36,113,5);
INSERT INTO `role_permission_relation` VALUES (37,1,3);
INSERT INTO `role_permission_relation` VALUES (38,2,3);
INSERT INTO `role_permission_relation` VALUES (39,16,3);
INSERT INTO `role_permission_relation` VALUES (40,17,3);
INSERT INTO `role_permission_relation` VALUES (41,21,3);
INSERT INTO `role_permission_relation` VALUES (42,22,3);
INSERT INTO `role_permission_relation` VALUES (43,24,3);
INSERT INTO `role_permission_relation` VALUES (44,25,3);
INSERT INTO `role_permission_relation` VALUES (45,26,3);
INSERT INTO `role_permission_relation` VALUES (46,27,3);
INSERT INTO `role_permission_relation` VALUES (47,3,3);
INSERT INTO `role_permission_relation` VALUES (48,4,3);
INSERT INTO `role_permission_relation` VALUES (49,14,3);
INSERT INTO `role_permission_relation` VALUES (50,71,3);
INSERT INTO `role_permission_relation` VALUES (51,72,3);
INSERT INTO `role_permission_relation` VALUES (52,73,3);
INSERT INTO `role_permission_relation` VALUES (53,74,3);
INSERT INTO `role_permission_relation` VALUES (54,75,3);
INSERT INTO `role_permission_relation` VALUES (55,76,3);
INSERT INTO `role_permission_relation` VALUES (56,77,3);
INSERT INTO `role_permission_relation` VALUES (57,79,3);
INSERT INTO `role_permission_relation` VALUES (58,15,3);
INSERT INTO `role_permission_relation` VALUES (59,20,3);
INSERT INTO `role_permission_relation` VALUES (60,10,3);
INSERT INTO `role_permission_relation` VALUES (61,18,3);
INSERT INTO `role_permission_relation` VALUES (62,19,3);
INSERT INTO `role_permission_relation` VALUES (63,104,3);
INSERT INTO `role_permission_relation` VALUES (64,110,3);
INSERT INTO `role_permission_relation` VALUES (65,113,3);
INSERT INTO `role_permission_relation` VALUES (66,1,2);
INSERT INTO `role_permission_relation` VALUES (67,2,2);
INSERT INTO `role_permission_relation` VALUES (68,15,2);
INSERT INTO `role_permission_relation` VALUES (69,16,2);
INSERT INTO `role_permission_relation` VALUES (70,17,2);
INSERT INTO `role_permission_relation` VALUES (71,26,2);
INSERT INTO `role_permission_relation` VALUES (72,27,2);
INSERT INTO `role_permission_relation` VALUES (73,20,2);
INSERT INTO `role_permission_relation` VALUES (74,21,2);
INSERT INTO `role_permission_relation` VALUES (75,22,2);
INSERT INTO `role_permission_relation` VALUES (76,24,2);
INSERT INTO `role_permission_relation` VALUES (77,25,2);
INSERT INTO `role_permission_relation` VALUES (78,3,2);
INSERT INTO `role_permission_relation` VALUES (79,4,2);
INSERT INTO `role_permission_relation` VALUES (80,5,2);
INSERT INTO `role_permission_relation` VALUES (81,6,2);
INSERT INTO `role_permission_relation` VALUES (82,13,2);
INSERT INTO `role_permission_relation` VALUES (83,11,2);
INSERT INTO `role_permission_relation` VALUES (84,10,2);
INSERT INTO `role_permission_relation` VALUES (85,9,2);
INSERT INTO `role_permission_relation` VALUES (86,8,2);
INSERT INTO `role_permission_relation` VALUES (87,12,2);
INSERT INTO `role_permission_relation` VALUES (88,14,2);
INSERT INTO `role_permission_relation` VALUES (89,71,2);
INSERT INTO `role_permission_relation` VALUES (90,72,2);
INSERT INTO `role_permission_relation` VALUES (91,73,2);
INSERT INTO `role_permission_relation` VALUES (92,74,2);
INSERT INTO `role_permission_relation` VALUES (93,76,2);
INSERT INTO `role_permission_relation` VALUES (94,7,2);
INSERT INTO `role_permission_relation` VALUES (95,79,2);
INSERT INTO `role_permission_relation` VALUES (96,18,2);
INSERT INTO `role_permission_relation` VALUES (97,19,2);
INSERT INTO `role_permission_relation` VALUES (98,94,2);
INSERT INTO `role_permission_relation` VALUES (99,104,2);
INSERT INTO `role_permission_relation` VALUES (100,110,2);
INSERT INTO `role_permission_relation` VALUES (101,113,2);
INSERT INTO `role_permission_relation` VALUES (102,1,4);
INSERT INTO `role_permission_relation` VALUES (103,2,4);
INSERT INTO `role_permission_relation` VALUES (104,15,4);
INSERT INTO `role_permission_relation` VALUES (105,16,4);
INSERT INTO `role_permission_relation` VALUES (106,17,4);
INSERT INTO `role_permission_relation` VALUES (107,20,4);
INSERT INTO `role_permission_relation` VALUES (108,21,4);
INSERT INTO `role_permission_relation` VALUES (109,22,4);
INSERT INTO `role_permission_relation` VALUES (110,25,4);
INSERT INTO `role_permission_relation` VALUES (111,27,4);
INSERT INTO `role_permission_relation` VALUES (112,26,4);
INSERT INTO `role_permission_relation` VALUES (113,3,4);
INSERT INTO `role_permission_relation` VALUES (114,4,4);
INSERT INTO `role_permission_relation` VALUES (115,5,4);
INSERT INTO `role_permission_relation` VALUES (116,6,4);
INSERT INTO `role_permission_relation` VALUES (117,13,4);
INSERT INTO `role_permission_relation` VALUES (118,10,4);
INSERT INTO `role_permission_relation` VALUES (119,8,4);
INSERT INTO `role_permission_relation` VALUES (120,14,4);
INSERT INTO `role_permission_relation` VALUES (121,7,4);
INSERT INTO `role_permission_relation` VALUES (122,71,4);
INSERT INTO `role_permission_relation` VALUES (123,72,4);
INSERT INTO `role_permission_relation` VALUES (124,76,4);
INSERT INTO `role_permission_relation` VALUES (125,73,4);
INSERT INTO `role_permission_relation` VALUES (126,74,4);
INSERT INTO `role_permission_relation` VALUES (127,79,4);
INSERT INTO `role_permission_relation` VALUES (128,18,4);
INSERT INTO `role_permission_relation` VALUES (129,19,4);
INSERT INTO `role_permission_relation` VALUES (130,24,4);
INSERT INTO `role_permission_relation` VALUES (131,110,4);
INSERT INTO `role_permission_relation` VALUES (132,113,4);
INSERT INTO `role_permission_relation` VALUES (2075,26,1);
INSERT INTO `role_permission_relation` VALUES (2076,27,1);
INSERT INTO `role_permission_relation` VALUES (2077,28,1);
INSERT INTO `role_permission_relation` VALUES (2078,29,1);
INSERT INTO `role_permission_relation` VALUES (2079,30,1);
INSERT INTO `role_permission_relation` VALUES (2080,59,1);
INSERT INTO `role_permission_relation` VALUES (2081,80,1);
INSERT INTO `role_permission_relation` VALUES (2082,81,1);
INSERT INTO `role_permission_relation` VALUES (2083,82,1);
INSERT INTO `role_permission_relation` VALUES (2084,83,1);
INSERT INTO `role_permission_relation` VALUES (2085,86,1);
INSERT INTO `role_permission_relation` VALUES (2086,87,1);
INSERT INTO `role_permission_relation` VALUES (2087,88,1);
INSERT INTO `role_permission_relation` VALUES (2088,89,1);
INSERT INTO `role_permission_relation` VALUES (2089,90,1);
INSERT INTO `role_permission_relation` VALUES (2090,92,1);
INSERT INTO `role_permission_relation` VALUES (2091,96,1);
INSERT INTO `role_permission_relation` VALUES (2092,104,1);
INSERT INTO `role_permission_relation` VALUES (2093,110,1);
INSERT INTO `role_permission_relation` VALUES (2094,112,1);
INSERT INTO `role_permission_relation` VALUES (2095,113,1);
INSERT INTO `role_permission_relation` VALUES (2096,26,6);
INSERT INTO `role_permission_relation` VALUES (2097,27,6);
INSERT INTO `role_permission_relation` VALUES (2098,104,6);
INSERT INTO `role_permission_relation` VALUES (2099,105,6);
INSERT INTO `role_permission_relation` VALUES (2100,106,6);
INSERT INTO `role_permission_relation` VALUES (2101,107,6);
INSERT INTO `role_permission_relation` VALUES (2102,108,6);
INSERT INTO `role_permission_relation` VALUES (2103,110,6);
INSERT INTO `role_permission_relation` VALUES (2104,113,6);
INSERT INTO `role_permission_relation` VALUES (2105,114,6);
/*!40000 ALTER TABLE `role_permission_relation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transfer_info`
--

DROP TABLE IF EXISTS `transfer_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transfer_info` (
  `transfer_info_id` int(11) NOT NULL AUTO_INCREMENT,
  `recharge_id` int(11) DEFAULT NULL,
  `trade_no` varchar(64) DEFAULT NULL,
  `remittance_account` varchar(128) DEFAULT NULL,
  `remittance_bank` varchar(256) DEFAULT NULL,
  `remittance_way` varchar(64) DEFAULT NULL,
  `remittance_at` timestamp NULL DEFAULT NULL,
  `remittance_remark` varchar(256) DEFAULT NULL,
  `remittance_corporation` varchar(128) DEFAULT NULL,
  `inward_account` varchar(128) DEFAULT NULL,
  `inward_bank` varchar(256) DEFAULT NULL,
  `inward_at` timestamp NULL DEFAULT NULL,
  `inward_corporation` varchar(128) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `amount` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`transfer_info_id`),
  KEY `FK_Reference_27` (`recharge_id`),
  CONSTRAINT `FK_transfer_recharge` FOREIGN KEY (`recharge_id`) REFERENCES `recharge` (`recharge_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transfer_info`
--

LOCK TABLES `transfer_info` WRITE;
/*!40000 ALTER TABLE `transfer_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `transfer_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  `user_id` varchar(128) DEFAULT NULL,
  `real_name` varchar(128) DEFAULT NULL,
  `position` varchar(128) DEFAULT NULL,
  `gender` varchar(16) DEFAULT NULL,
  `phone` varchar(64) DEFAULT NULL,
  `mobile` varchar(64) DEFAULT NULL,
  `status` varchar(64) DEFAULT NULL,
  `leader_id` varchar(64) DEFAULT NULL,
  `dept_id` varchar(64) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'pbkdf2_sha256$20000$5ut9sbTfakxX$egZz9NSoiM5pzACmblyrGtlM4GFehfaLau0rhezmCtE=','2016-01-19 03:13:48',0,'admin','','','',1,1,'0000-00-00 00:00:00','','','','secrecy','','','normal',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_role_relation`
--

DROP TABLE IF EXISTS `user_role_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_role_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_role_relation_role_id_4c10861a690880bb_fk_role_id` (`role_id`),
  KEY `user_role_relation_user_id_79bfe90fa8d5786_fk_user_id` (`user_id`),
  CONSTRAINT `user_role_relation_role_id_4c10861a690880bb_fk_role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `user_role_relation_user_id_79bfe90fa8d5786_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=331 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_role_relation`
--

LOCK TABLES `user_role_relation` WRITE;
/*!40000 ALTER TABLE `user_role_relation` DISABLE KEYS */;
INSERT INTO `user_role_relation` VALUES (330,1,1);
/*!40000 ALTER TABLE `user_role_relation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workorder`
--

DROP TABLE IF EXISTS `workorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workorder` (
  `workoder_id` int(11) NOT NULL AUTO_INCREMENT,
  `workorder_no` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `workorder_type_id` int(11) DEFAULT NULL,
  `apply_by` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `apply_source` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `theme` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `content` varchar(4000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `status` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `apply_at` timestamp NULL DEFAULT NULL,
  `lasthandled_at` timestamp NULL DEFAULT NULL,
  `lasthandled_by` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`workoder_id`),
  KEY `FK_workorder` (`workorder_type_id`),
  KEY `FK_lasthandled_by_user_id` (`lasthandled_by`),
  CONSTRAINT `FK_workorder_type_id_workorder_type_id` FOREIGN KEY (`workorder_type_id`) REFERENCES `workorder_type` (`workorder_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workorder`
--

LOCK TABLES `workorder` WRITE;
/*!40000 ALTER TABLE `workorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `workorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workorder_record`
--

DROP TABLE IF EXISTS `workorder_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workorder_record` (
  `workorder_record_id` int(11) NOT NULL AUTO_INCREMENT,
  `workorder_id` int(11) DEFAULT NULL,
  `record_by` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `content` varchar(4000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `status` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `record_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`workorder_record_id`),
  KEY `FK_workorder_record` (`workorder_id`),
  CONSTRAINT `FK_workorder` FOREIGN KEY (`workorder_id`) REFERENCES `workorder` (`workoder_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workorder_record`
--

LOCK TABLES `workorder_record` WRITE;
/*!40000 ALTER TABLE `workorder_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `workorder_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workorder_type`
--

DROP TABLE IF EXISTS `workorder_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workorder_type` (
  `workorder_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `remark` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`workorder_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workorder_type`
--

LOCK TABLES `workorder_type` WRITE;
/*!40000 ALTER TABLE `workorder_type` DISABLE KEYS */;
INSERT INTO `workorder_type` VALUES (1,'consult','商务咨询工单',NULL,NULL,NULL);
INSERT INTO `workorder_type` VALUES (2,'function','功能咨询工单',NULL,NULL,NULL);
INSERT INTO `workorder_type` VALUES (3,'error','故障工单',NULL,NULL,NULL);
INSERT INTO `workorder_type` VALUES (4,'finance','财务,发票工单',NULL,NULL,NULL);
INSERT INTO `workorder_type` VALUES (5,'payment','催款工单',NULL,NULL,NULL);
INSERT INTO `workorder_type` VALUES (6,'regionQuota','区域,配额申请工单',NULL,NULL,NULL);
INSERT INTO `workorder_type` VALUES (7,'others','其他',NULL,NULL,NULL);
/*!40000 ALTER TABLE `workorder_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-27 14:50:08
