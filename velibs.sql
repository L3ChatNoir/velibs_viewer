-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : sam. 03 juin 2023 à 14:50
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `velibs`
--

-- --------------------------------------------------------

--
-- Structure de la table `history_change`
--

DROP TABLE IF EXISTS `history_change`;
CREATE TABLE IF NOT EXISTS `history_change` (
  `date_time` datetime DEFAULT NULL,
  `table_use` varchar(50) DEFAULT NULL,
  `action` varchar(50) DEFAULT NULL,
  `stationcode` varchar(100) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `station_information`
--

DROP TABLE IF EXISTS `station_information`;
CREATE TABLE IF NOT EXISTS `station_information` (
  `stationcode` varchar(100) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `capacity` int DEFAULT NULL,
  `coordonnees_geo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`stationcode`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déclencheurs `station_information`
--
DROP TRIGGER IF EXISTS `logs_INSERT_information`;
DELIMITER $$
CREATE TRIGGER `logs_INSERT_information` AFTER INSERT ON `station_information` FOR EACH ROW INSERT INTO history_change (date_time, table_use, action, stationcode, user) VALUES (NOW(), 'station_information', 'INSERT', new.stationcode, CURRENT_USER)
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `logs_UPDATE_information`;
DELIMITER $$
CREATE TRIGGER `logs_UPDATE_information` AFTER UPDATE ON `station_information` FOR EACH ROW INSERT INTO history_change (date_time, table_use, action, stationcode, user) VALUES (NOW(), 'station_information', 'UPDATE', new.stationcode, CURRENT_USER)
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `logs_delete_information`;
DELIMITER $$
CREATE TRIGGER `logs_delete_information` AFTER DELETE ON `station_information` FOR EACH ROW INSERT INTO history_change (date_time, table_use, action, stationcode, user) VALUES (NOW(), 'station_information', 'DELETE', old.stationcode, CURRENT_USER)
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `station_status`
--

DROP TABLE IF EXISTS `station_status`;
CREATE TABLE IF NOT EXISTS `station_status` (
  `date` datetime NOT NULL,
  `stationcode` varchar(100) NOT NULL,
  `is_installed` varchar(100) DEFAULT NULL,
  `numdocksavailable` int DEFAULT NULL,
  `numbikesavailable` int DEFAULT NULL,
  `mechanical` int DEFAULT NULL,
  `ebike` int DEFAULT NULL,
  `nom_arrondissement_communes` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`date`,`stationcode`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déclencheurs `station_status`
--
DROP TRIGGER IF EXISTS `logs_INSERT_status`;
DELIMITER $$
CREATE TRIGGER `logs_INSERT_status` AFTER INSERT ON `station_status` FOR EACH ROW INSERT INTO history_change (date_time, table_use, action, stationcode, user) VALUES (NOW(), 'station_status', 'INSERT', new.stationcode, CURRENT_USER)
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `logs_UPDATE_status`;
DELIMITER $$
CREATE TRIGGER `logs_UPDATE_status` AFTER UPDATE ON `station_status` FOR EACH ROW INSERT INTO history_change (date_time, table_use, action, stationcode, user) VALUES (NOW(), 'station_status', 'UPDATE', new.stationcode, CURRENT_USER)
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `logs_delete_status`;
DELIMITER $$
CREATE TRIGGER `logs_delete_status` AFTER DELETE ON `station_status` FOR EACH ROW INSERT INTO history_change (date_time, table_use, action, stationcode, user) VALUES (NOW(), 'station_status', 'DELETE', old.stationcode, CURRENT_USER)
$$
DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
