-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: details
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `google_forms`
--

DROP TABLE IF EXISTS `google_forms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `google_forms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `form_name` varchar(255) DEFAULT NULL,
  `sheet_id` varchar(255) DEFAULT NULL,
  `form_id` varchar(255) DEFAULT NULL,
  `sheet_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `google_forms`
--

LOCK TABLES `google_forms` WRITE;
/*!40000 ALTER TABLE `google_forms` DISABLE KEYS */;
INSERT INTO `google_forms` VALUES (1,'contact','https://docs.google.com/spreadsheets/d/e/2PACX-1vS6opsDi2VkOpEjd9RrG33Qp8Le1g6irHL1C_0ar9r1fCrpXyD06oMqDoAq28xQ9wAWBDWC-afyE7Rm/pub?output=csv','https://docs.google.com/forms/d/e/1FAIpQLSfDAetHr-LxhNYqEe7NJlJU810coIlY0OuqCUHcwF_8WtQ2aA/viewform?usp=dialog','https://docs.google.com/spreadsheets/d/13CT-CXorrYco7rJICSM04pN8JvIsQ76tzi3QJPUtD5w/edit?usp=sharing'),(7,'Info','https://docs.google.com/spreadsheets/d/e/2PACX-1vQvJOxPBhxkv2g4A6GytuCoqkqTN0_GkYGcrW-ES1ZjQA4BCid2XY--b8z074s1I9ELC2dWMnbIFp8I/pub?output=csv','https://docs.google.com/forms/d/e/1FAIpQLSeIQkxVPI7grmgDmDuC0aj37fGw6gLZIqmRNJV22ssLVrtAIw/viewform?usp=header','https://docs.google.com/spreadsheets/d/1Fi_ts7YdSqxtL-D58ZJbB68eWoTsVwxPhsYvsDAg_ig/edit?usp=sharing'),(8,'workshop feedback','https://docs.google.com/spreadsheets/d/e/2PACX-1vQvkAUt_k3OuaG4osXglz2rI8Ax6r-Znt3PbpqWmwDh6jgo454nfKFp7qEj7Hb0zFSLTu4AAq5MJOKw/pub?output=csv','https://docs.google.com/forms/d/e/1FAIpQLSef7rlMGv3dzEyyHSzrlIx32iKhy4oKtcXtefBFHfg8jUxz8w/viewform?usp=header','https://docs.google.com/spreadsheets/d/1rOeiXKsp3MWh7JIaXPSWymh8My-2EwDoFRcVd9xRhDU/edit?usp=sharing');
/*!40000 ALTER TABLE `google_forms` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-16 19:22:05
