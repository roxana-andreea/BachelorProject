-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 11, 2016 at 09:49 PM
-- Server version: 5.5.47-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `android_api`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unique_id` varchar(23) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(80) NOT NULL,
  `encrypted_password` varchar(80) NOT NULL,
  `salt` varchar(10) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_id` (`unique_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=13 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `unique_id`, `name`, `email`, `encrypted_password`, `salt`, `created_at`, `updated_at`) VALUES
(1, '570961cb218975.85876992', 'Hfhhfu', 'fjfhi', 'ze3Fq5NWHUvG4syW8eGY2ZndNfE5ZDg1ZTFkMzVl', '9d85e1d35e', '2016-04-09 23:10:51', NULL),
(2, '', 'ana', 'ana', '', '', NULL, NULL),
(3, '57096ada671926.24180951', 'Rox', 'roxana.cazacu93@gmail.com', 'GBal+lHxda9zyrBC90tph+ZZOcU5YzZlOWRiODI5', '9c6e9db829', '2016-04-09 23:49:30', NULL),
(4, '57096b0db27307.39899546', 'Dana', 'barosana', 'bO1K1F3olxKujwaEotLZsIIPu+Y2ZTk4MzcxNTEz', '6e98371513', '2016-04-09 23:50:21', NULL),
(5, '57096d36c5ccb6.58675600', 'Bau', 'bau', 'eeThcS9FSfEWJALsuOaFbYvoqTllZGY3NmZjYTFh', 'edf76fca1a', '2016-04-09 23:59:34', NULL),
(6, '57096df8be2c40.70374153', 'R', 'roxana@barosana', 'EuNhK8aVFcgTJCDGU+4Dx+oG9LI2NjlhOTg4OGQ3', '669a9888d7', '2016-04-10 00:02:48', NULL),
(7, '570a86c83ee7e9.33097804', 'Dan', 'dan', 'SLRGwSFGVNlRawOz3/Ky2LTINrc5ZTk1MzllZTZj', '9e9539ee6c', '2016-04-10 20:00:56', NULL),
(8, '570a8897867cb1.50714363', 'Ada', 'ada@ada', 'sE+JLOxriMBaM8yuw1XgU41CY9kxOGY2Y2E3ZWFk', '18f6ca7ead', '2016-04-10 20:08:39', NULL),
(9, '570a88bd0ae171.79347851', 'Shhddh', 'hdhdjdh', 'boTpbU5A2Hk4ZuVu2ZsY6uWvTVc2ODI0NDllNjUz', '682449e653', '2016-04-10 20:09:17', NULL),
(10, '570aa356187056.47513725', 'Roc', 'roc', 'fudnl7C92GEoFRPx6Uo04QFbk6tiNjM3NmRmMDc0', 'b6376df074', '2016-04-10 22:02:46', NULL),
(12, '570aa3aaa3dde0.23234640', 'Buna', 'buna', '0dzb3BLq1ROQdEh1B0FBjqmaXX8xYzEyNDU0OTlk', '1c1245499d', '2016-04-10 22:04:10', NULL);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
