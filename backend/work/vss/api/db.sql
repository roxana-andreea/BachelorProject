-- phpMyAdmin SQL Dump
-- version 4.4.13.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 13, 2016 at 10:43 AM
-- Server version: 5.6.30-0ubuntu0.15.10.1
-- PHP Version: 5.6.11-1ubuntu3.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db`
--

-- --------------------------------------------------------

--
-- Table structure for table `Device`
--

CREATE TABLE IF NOT EXISTS `Device` (
  `id` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `serial` varchar(255) NOT NULL,
  `paired` tinyint(1) DEFAULT NULL,
  `description` text,
  `created` datetime DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Device`
--

INSERT INTO `Device` (`id`, `id_user`, `serial`, `paired`, `description`, `created`) VALUES
(1, 1, 'SERIAL_NUMBER', 0, 'Raspberry Pi 2', '2016-05-13 17:42:21');

-- --------------------------------------------------------

--
-- Table structure for table `Location`
--

CREATE TABLE IF NOT EXISTS `Location` (
  `id` int(11) NOT NULL,
  `id_device` int(11) NOT NULL,
  `created` datetime DEFAULT NULL,
  `latitude` varchar(11) NOT NULL,
  `north` tinyint(1) DEFAULT NULL,
  `longitude` varchar(12) NOT NULL,
  `east` tinyint(1) DEFAULT NULL,
  `altitude` int(11) DEFAULT NULL,
  `registered` datetime NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Location`
--

INSERT INTO `Location` (`id`, `id_device`, `created`, `latitude`, `north`, `longitude`, `east`, `altitude`, `registered`) VALUES
(1, 1, '2016-05-13 17:42:21', '4426.788279', 1, '02603.527478', 1, 13, '2016-03-21 19:10:16');

-- --------------------------------------------------------

--
-- Table structure for table `Sensor`
--

CREATE TABLE IF NOT EXISTS `Sensor` (
  `id` int(11) NOT NULL,
  `id_device` int(11) NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Sensor`
--

INSERT INTO `Sensor` (`id`, `id_device`, `type`, `created`, `value`) VALUES
(1, 1, 'temperature', '2016-05-13 17:42:21', '33');

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE IF NOT EXISTS `User` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `token` varchar(255) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`id`, `name`, `email`, `password`, `token`, `created`, `updated`) VALUES
(1, 'Cristian Lupu', 'cristianlupu@gmail.com', 'secret', 'token', '2016-05-13 17:42:21', '2016-05-13 17:42:21');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Device`
--
ALTER TABLE `Device`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `serial` (`serial`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `Location`
--
ALTER TABLE `Location`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_device` (`id_device`);

--
-- Indexes for table `Sensor`
--
ALTER TABLE `Sensor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_device` (`id_device`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Device`
--
ALTER TABLE `Device`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `Location`
--
ALTER TABLE `Location`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `Sensor`
--
ALTER TABLE `Sensor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `User`
--
ALTER TABLE `User`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `Device`
--
ALTER TABLE `Device`
  ADD CONSTRAINT `Device_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `User` (`id`);

--
-- Constraints for table `Location`
--
ALTER TABLE `Location`
  ADD CONSTRAINT `Location_ibfk_1` FOREIGN KEY (`id_device`) REFERENCES `Device` (`id`);

--
-- Constraints for table `Sensor`
--
ALTER TABLE `Sensor`
  ADD CONSTRAINT `Sensor_ibfk_1` FOREIGN KEY (`id_device`) REFERENCES `Device` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
