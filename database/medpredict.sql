-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 21, 2026 at 06:30 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `healthcare_admission`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_sessions`
--

CREATE TABLE `admin_sessions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `session_token` varchar(64) NOT NULL,
  `expires_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `admin_users`
--

CREATE TABLE `admin_users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('doctor','clinician','admin') DEFAULT 'clinician',
  `is_active` tinyint(1) DEFAULT 1,
  `last_login` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_users`
--

INSERT INTO `admin_users` (`id`, `username`, `password_hash`, `full_name`, `email`, `role`, `is_active`, `last_login`, `created_at`) VALUES
(4, 'admin', '$2y$10$vZLZPxrtSJzKvY8YOwg4ne5R1PGoFZTHSc6VWrzsjEDYNs2Oew5Ve', 'System Administrator', 'admin@hospital.com', 'admin', 1, '2026-01-21 04:46:54', '2026-01-19 02:17:33'),
(5, 'dr.smith', '$2y$10$g9SroLid6.5.JZRSc6hvPeaNJq7tgFtWxCP34v7DT9MqOw9WLEZEq', 'Dr. John Smith', 'dr.smith@hospital.com', 'doctor', 1, NULL, '2026-01-19 02:17:33'),
(6, 'clinician1', '$2y$10$70Qbdaqtd90f0mZlR6j9NeBTtaPsJaJzwV0Ggtshho1RyosKqQWVq', 'Sarah Johnson', 'sarah.j@hospital.com', 'clinician', 1, '2026-01-19 04:30:45', '2026-01-19 02:17:33');

-- --------------------------------------------------------

--
-- Stand-in structure for view `dashboard_stats`
-- (See below for the actual view)
--
CREATE TABLE `dashboard_stats` (
`total_predictions` bigint(21)
,`active_days` bigint(21)
,`avg_prediction_score` double
,`high_risk_count` decimal(22,0)
,`medium_risk_count` decimal(22,0)
,`low_risk_count` decimal(22,0)
,`male_count` decimal(22,0)
,`female_count` decimal(22,0)
,`avg_patient_age` decimal(14,4)
,`last_prediction_date` timestamp
);

-- --------------------------------------------------------

--
-- Table structure for table `disease_risk_assessments`
--

CREATE TABLE `disease_risk_assessments` (
  `id` int(11) NOT NULL,
  `assessed_by` varchar(100) NOT NULL,
  `age` int(11) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `bmi` float NOT NULL,
  `smoking` varchar(20) NOT NULL,
  `alcohol` varchar(20) NOT NULL,
  `exercise` varchar(20) NOT NULL,
  `family_diabetes` tinyint(1) NOT NULL,
  `family_heart_disease` tinyint(1) NOT NULL,
  `family_hypertension` tinyint(1) NOT NULL,
  `systolic_bp` float NOT NULL,
  `diastolic_bp` float NOT NULL,
  `heart_rate` float NOT NULL,
  `glucose` float NOT NULL,
  `cholesterol` float NOT NULL,
  `hdl` float NOT NULL,
  `ldl` float NOT NULL,
  `triglycerides` float NOT NULL,
  `diabetes_risk` float NOT NULL,
  `diabetes_level` varchar(20) NOT NULL,
  `heart_disease_risk` float NOT NULL,
  `heart_disease_level` varchar(20) NOT NULL,
  `hypertension_risk` float NOT NULL,
  `hypertension_level` varchar(20) NOT NULL,
  `overall_risk` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `disease_risk_assessments`
--

INSERT INTO `disease_risk_assessments` (`id`, `assessed_by`, `age`, `gender`, `bmi`, `smoking`, `alcohol`, `exercise`, `family_diabetes`, `family_heart_disease`, `family_hypertension`, `systolic_bp`, `diastolic_bp`, `heart_rate`, `glucose`, `cholesterol`, `hdl`, `ldl`, `triglycerides`, `diabetes_risk`, `diabetes_level`, `heart_disease_risk`, `heart_disease_level`, `hypertension_risk`, `hypertension_level`, `overall_risk`, `created_at`) VALUES
(1, '1', 75, 'Female', 25.4, 'Former', 'None', 'Sedentary', 1, 1, 1, 114, 74, 78, 85, 177, 70, 129, 108, 0.661, 'High', 0.8835, 'High', 0.7566, 'High', '0.767', '2026-01-05 09:27:50'),
(2, '1', 69, 'Male', 19.7, 'Former', 'None', 'Sedentary', 0, 0, 0, 133, 74, 74, 90, 187, 50, 117, 107, 0.4664, 'Medium', 0.5973, 'Medium', 0.6769, 'High', '0.5802', '2026-01-10 09:27:50'),
(3, '1', 82, 'Female', 23, 'Current', 'Heavy', 'Active', 0, 0, 0, 111, 85, 70, 99, 160, 50, 113, 119, 0.6658, 'High', 0.6168, 'High', 0.6578, 'High', '0.6468', '2026-01-06 09:27:50'),
(4, '1', 74, 'Female', 37.7, 'Never', 'None', 'Active', 1, 1, 1, 162, 106, 85, 202, 229, 32, 185, 190, 0.8991, 'High', 0.7719, 'High', 0.95, 'High', '0.8736', '2026-01-04 09:27:50'),
(5, '1', 54, 'Female', 25.5, 'Former', 'Moderate', 'Active', 0, 1, 0, 110, 71, 75, 118, 172, 75, 92, 145, 0.5374, 'Medium', 0.5452, 'Medium', 0.7015, 'High', '0.5947', '2025-12-22 09:27:50'),
(6, '1', 31, 'Male', 22, 'Current', 'Heavy', 'Light', 1, 0, 1, 116, 75, 66, 96, 206, 60, 89, 118, 0.1651, 'Low', 0.2411, 'Low', 0.2128, 'Low', '0.2063', '2026-01-14 09:27:50'),
(7, '1', 63, 'Male', 37.4, 'Former', 'None', 'Light', 0, 0, 0, 158, 104, 83, 238, 226, 32, 177, 193, 0.4869, 'Medium', 0.5536, 'Medium', 0.6156, 'High', '0.552', '2026-01-08 09:27:50'),
(8, '1', 52, 'Female', 29.8, 'Never', 'Moderate', 'Sedentary', 0, 1, 1, 145, 91, 87, 181, 236, 41, 162, 250, 0.6686, 'High', 0.4063, 'Medium', 0.6459, 'High', '0.5736', '2026-01-13 09:27:50'),
(9, '1', 60, 'Male', 22, 'Current', 'Moderate', 'Moderate', 1, 0, 0, 133, 83, 73, 108, 181, 68, 123, 85, 0.6134, 'High', 0.7118, 'High', 0.6735, 'High', '0.6662', '2025-12-24 09:27:50'),
(10, '1', 29, 'Male', 21, 'Current', 'Moderate', 'Sedentary', 0, 0, 0, 130, 84, 57, 101, 163, 56, 92, 80, 0.0477, 'Low', 0.2126, 'Low', 0.2365, 'Low', '0.1656', '2026-01-05 09:27:50'),
(11, '1', 51, 'Female', 24.3, 'Former', 'Heavy', 'Light', 0, 0, 0, 133, 77, 75, 117, 205, 61, 96, 80, 0.3264, 'Medium', 0.3804, 'Medium', 0.4206, 'Medium', '0.3758', '2026-01-02 09:27:50'),
(12, '1', 21, 'Female', 24.7, 'Current', 'Moderate', 'Moderate', 0, 0, 0, 110, 78, 73, 94, 172, 64, 84, 90, 0.1046, 'Low', 0.0029, 'Low', 0.1623, 'Low', '0.09', '2026-01-04 09:27:50'),
(13, '1', 36, 'Female', 22.1, 'Current', 'Heavy', 'Light', 0, 0, 0, 110, 83, 69, 88, 205, 72, 92, 113, 0.2532, 'Low', 0.261, 'Low', 0.1998, 'Low', '0.238', '2025-12-25 09:27:50'),
(14, '1', 58, 'Male', 21.4, 'Never', 'Moderate', 'Light', 0, 0, 0, 133, 76, 74, 94, 197, 51, 127, 90, 0.3472, 'Medium', 0.3972, 'Medium', 0.5672, 'Medium', '0.4372', '2025-12-27 09:27:50'),
(15, '1', 65, 'Female', 34.3, 'Current', 'Heavy', 'Active', 0, 1, 0, 158, 94, 81, 213, 254, 35, 143, 218, 0.6746, 'High', 0.6058, 'High', 0.95, 'High', '0.7435', '2026-01-05 09:27:50'),
(16, '1', 28, 'Female', 26.6, 'Current', 'Moderate', 'Active', 0, 0, 0, 120, 80, 71, 96, 186, 62, 83, 132, 0.0573, 'Low', 0.1421, 'Low', 0.2519, 'Low', '0.1504', '2026-01-13 09:27:50'),
(17, '1', 40, 'Male', 28, 'Never', 'None', 'Active', 0, 1, 1, 174, 94, 94, 229, 250, 34, 160, 248, 0.4129, 'Medium', 0.4242, 'Medium', 0.5622, 'Medium', '0.4664', '2025-12-28 09:27:50'),
(18, '1', 28, 'Male', 22.8, 'Former', 'Moderate', 'Active', 0, 0, 0, 130, 72, 59, 88, 189, 59, 110, 98, 0.0606, 'Low', 0.2011, 'Low', 0.1833, 'Low', '0.1483', '2026-01-09 09:27:50'),
(19, '1', 79, 'Male', 37.4, 'Former', 'None', 'Moderate', 0, 0, 0, 143, 107, 88, 223, 263, 42, 176, 247, 0.8344, 'High', 0.6707, 'High', 0.8057, 'High', '0.7703', '2025-12-24 09:27:50'),
(20, '1', 36, 'Female', 19.6, 'Never', 'None', 'Sedentary', 1, 0, 1, 122, 70, 78, 80, 209, 51, 83, 100, 0.2394, 'Low', 0.2294, 'Low', 0.2592, 'Low', '0.2427', '2026-01-01 09:27:50'),
(21, '1', 49, 'Female', 18.7, 'Current', 'Moderate', 'Active', 1, 0, 1, 111, 70, 70, 101, 167, 51, 95, 97, 0.4181, 'Medium', 0.3637, 'Medium', 0.4257, 'Medium', '0.4025', '2026-01-10 09:27:50'),
(22, '1', 40, 'Male', 18.5, 'Never', 'None', 'Sedentary', 0, 0, 0, 115, 71, 62, 81, 209, 52, 96, 140, 0.2579, 'Low', 0.2986, 'Low', 0.3483, 'Medium', '0.3016', '2026-01-03 09:27:50'),
(23, '1', 26, 'Male', 31.5, 'Never', 'Moderate', 'Moderate', 0, 0, 0, 152, 95, 85, 232, 222, 30, 140, 231, 0.1843, 'Low', 0.0874, 'Low', 0.3173, 'Medium', '0.1963', '2026-01-13 09:27:50'),
(24, '1', 37, 'Male', 35, 'Current', 'None', 'Sedentary', 0, 0, 0, 148, 90, 94, 155, 238, 43, 182, 243, 0.2422, 'Low', 0.2845, 'Low', 0.454, 'Medium', '0.3269', '2026-01-18 09:27:50'),
(25, '1', 43, 'Male', 34.7, 'Never', 'Moderate', 'Sedentary', 1, 0, 1, 166, 97, 83, 193, 244, 37, 187, 214, 0.5175, 'Medium', 0.3158, 'Medium', 0.5431, 'Medium', '0.4588', '2026-01-09 09:27:50'),
(26, '1', 21, 'Male', 25.5, 'Former', 'Heavy', 'Light', 0, 0, 0, 117, 72, 56, 88, 173, 51, 89, 133, 0.0476, 'Low', 0.0172, 'Low', 0.1998, 'Low', '0.0882', '2025-12-24 09:27:50'),
(27, '1', 67, 'Female', 32.4, 'Current', 'Heavy', 'Active', 0, 1, 0, 161, 97, 84, 205, 259, 35, 178, 208, 0.865, 'High', 0.7621, 'High', 0.95, 'High', '0.859', '2026-01-18 09:27:50'),
(28, '1', 25, 'Male', 25.9, 'Former', 'None', 'Moderate', 1, 1, 1, 132, 84, 59, 110, 195, 51, 84, 150, 0.0792, 'Low', 0.0703, 'Low', 0.2593, 'Low', '0.1363', '2025-12-25 09:27:50'),
(29, '1', 21, 'Male', 25, 'Current', 'None', 'Moderate', 0, 1, 1, 123, 77, 59, 111, 185, 58, 108, 105, -0.0138, 'Low', 0.1905, 'Low', 0.2491, 'Low', '0.1419', '2026-01-09 09:27:50'),
(30, '1', 33, 'Male', 33.6, 'Never', 'Moderate', 'Active', 0, 0, 0, 149, 96, 76, 226, 221, 41, 155, 233, 0.2993, 'Low', 0.2342, 'Low', 0.4969, 'Medium', '0.3434', '2026-01-02 09:27:50'),
(31, '1', 45, 'Male', 33.7, 'Current', 'Heavy', 'Active', 0, 1, 1, 180, 93, 86, 205, 253, 36, 175, 190, 0.4338, 'Medium', 0.4006, 'Medium', 0.7106, 'High', '0.515', '2026-01-18 09:27:50'),
(32, '1', 35, 'Male', 19.6, 'Current', 'Heavy', 'Moderate', 1, 0, 0, 121, 82, 73, 80, 150, 58, 97, 128, 0.3116, 'Medium', 0.2122, 'Low', 0.1963, 'Low', '0.24', '2025-12-30 09:27:50'),
(33, '1', 43, 'Female', 23.5, 'Former', 'None', 'Active', 0, 1, 1, 125, 77, 67, 101, 201, 65, 112, 116, 0.3847, 'Medium', 0.3242, 'Medium', 0.3448, 'Medium', '0.3513', '2025-12-25 09:27:50'),
(34, '1', 62, 'Female', 20.5, 'Never', 'Moderate', 'Sedentary', 0, 0, 0, 119, 70, 81, 107, 166, 74, 126, 105, 0.4494, 'Medium', 0.4717, 'Medium', 0.5551, 'Medium', '0.4921', '2025-12-29 09:27:50'),
(35, '1', 83, 'Female', 20.4, 'Current', 'Moderate', 'Sedentary', 0, 0, 0, 125, 81, 69, 103, 189, 62, 105, 99, 0.7021, 'High', 0.6679, 'High', 0.7595, 'High', '0.7098', '2025-12-21 09:27:50'),
(36, '1', 20, 'Female', 33.9, 'Current', 'Moderate', 'Sedentary', 1, 0, 0, 145, 92, 83, 154, 257, 43, 186, 237, 0.1257, 'Low', 0.0077, 'Low', 0.2472, 'Low', '0.1269', '2025-12-25 09:27:50'),
(37, '1', 83, 'Female', 28.2, 'Former', 'Moderate', 'Sedentary', 0, 0, 1, 159, 110, 90, 213, 273, 43, 157, 211, 0.95, 'High', 0.9051, 'High', 0.95, 'High', '0.935', '2026-01-12 09:27:50'),
(38, '1', 39, 'Female', 21.4, 'Current', 'Heavy', 'Sedentary', 0, 0, 1, 123, 80, 78, 95, 188, 55, 103, 90, 0.2299, 'Low', 0.2423, 'Low', 0.3674, 'Medium', '0.2799', '2026-01-06 09:27:50'),
(39, '1', 23, 'Female', 24.7, 'Former', 'Moderate', 'Sedentary', 0, 0, 0, 129, 81, 59, 103, 183, 55, 98, 97, 0.1168, 'Low', 0.0488, 'Low', 0.0778, 'Low', '0.0812', '2026-01-19 09:27:50'),
(40, '1', 35, 'Female', 25.1, 'Current', 'Moderate', 'Light', 0, 0, 0, 133, 77, 61, 112, 171, 53, 91, 110, 0.2171, 'Low', 0.1448, 'Low', 0.1799, 'Low', '0.1806', '2026-01-16 09:27:50'),
(41, '1', 51, 'Female', 27.2, 'Former', 'Heavy', 'Active', 0, 0, 0, 157, 100, 79, 184, 269, 44, 164, 237, 0.5304, 'Medium', 0.3284, 'Medium', 0.4919, 'Medium', '0.4503', '2026-01-05 09:27:50'),
(42, '1', 43, 'Male', 33, 'Former', 'Heavy', 'Sedentary', 0, 0, 0, 145, 95, 95, 241, 225, 37, 141, 211, 0.3569, 'Medium', 0.5282, 'Medium', 0.4251, 'Medium', '0.4367', '2025-12-27 09:27:50'),
(43, '1', 68, 'Female', 23.9, 'Former', 'None', 'Moderate', 0, 0, 0, 131, 75, 84, 117, 165, 50, 106, 150, 0.4976, 'Medium', 0.5319, 'Medium', 0.6366, 'High', '0.5554', '2026-01-01 09:27:50'),
(44, '1', 73, 'Male', 31.4, 'Current', 'Heavy', 'Light', 0, 0, 0, 157, 94, 85, 153, 279, 34, 169, 247, 0.697, 'High', 0.6554, 'High', 0.757, 'High', '0.7032', '2025-12-29 09:27:50'),
(45, '1', 31, 'Male', 37.1, 'Former', 'Moderate', 'Moderate', 0, 0, 0, 177, 100, 89, 141, 250, 39, 175, 211, 0.185, 'Low', 0.0999, 'Low', 0.3736, 'Medium', '0.2195', '2026-01-08 09:27:50'),
(46, '1', 37, 'Male', 21.9, 'Current', 'Heavy', 'Active', 0, 0, 0, 134, 73, 63, 119, 163, 66, 90, 84, 0.1998, 'Low', 0.2843, 'Low', 0.1826, 'Low', '0.2222', '2026-01-10 09:27:50'),
(47, '1', 56, 'Male', 19.6, 'Never', 'None', 'Moderate', 0, 0, 0, 110, 71, 64, 106, 175, 74, 90, 101, 0.3585, 'Medium', 0.5076, 'Medium', 0.543, 'Medium', '0.4697', '2026-01-03 09:27:50'),
(48, '1', 60, 'Female', 20, 'Current', 'Heavy', 'Light', 0, 0, 0, 127, 83, 84, 93, 176, 65, 94, 104, 0.3824, 'Medium', 0.3849, 'Medium', 0.4046, 'Medium', '0.3906', '2025-12-26 09:27:50'),
(49, '1', 36, 'Male', 24.2, 'Never', 'None', 'Light', 0, 0, 0, 118, 83, 70, 116, 195, 62, 109, 105, 0.2259, 'Low', 0.2183, 'Low', 0.2689, 'Low', '0.2377', '2026-01-05 09:27:50'),
(50, '1', 18, 'Female', 21.4, 'Former', 'None', 'Sedentary', 0, 0, 0, 135, 71, 70, 114, 179, 53, 82, 145, -0.0682, 'Low', 0.0244, 'Low', 0.0724, 'Low', '0.0095', '2026-01-10 09:27:50'),
(51, '1', 49, 'Female', 25.2, 'Never', 'Heavy', 'Sedentary', 0, 0, 0, 125, 83, 61, 89, 198, 65, 130, 107, 0.3572, 'Medium', 0.283, 'Low', 0.4326, 'Medium', '0.3576', '2026-01-02 09:27:50'),
(52, '1', 71, 'Male', 19.6, 'Never', 'None', 'Light', 1, 0, 0, 112, 74, 79, 120, 165, 50, 128, 109, 0.619, 'High', 0.7597, 'High', 0.9076, 'High', '0.7621', '2026-01-09 09:27:50'),
(53, '1', 66, 'Female', 36.3, 'Never', 'None', 'Moderate', 0, 1, 1, 160, 104, 88, 144, 274, 38, 186, 237, 0.8551, 'High', 0.7681, 'High', 0.95, 'High', '0.8577', '2026-01-07 09:27:50'),
(54, '1', 67, 'Female', 32.6, 'Never', 'Moderate', 'Active', 0, 0, 0, 174, 96, 80, 211, 248, 36, 143, 199, 0.7195, 'High', 0.5858, 'Medium', 0.8003, 'High', '0.7019', '2026-01-06 09:27:50'),
(55, '1', 63, 'Male', 19.6, 'Former', 'Moderate', 'Active', 0, 0, 1, 119, 82, 72, 108, 158, 71, 84, 80, 0.6876, 'High', 0.6195, 'High', 0.6239, 'High', '0.6437', '2026-01-09 09:27:50'),
(56, '1', 62, 'Female', 18.5, 'Current', 'Moderate', 'Sedentary', 0, 0, 0, 119, 81, 80, 111, 197, 70, 109, 80, 0.6218, 'High', 0.5454, 'Medium', 0.6969, 'High', '0.6213', '2026-01-01 09:27:50'),
(57, '1', 55, 'Female', 20.3, 'Never', 'Heavy', 'Light', 0, 0, 0, 132, 73, 80, 100, 208, 59, 119, 97, 0.3762, 'Medium', 0.3869, 'Medium', 0.5427, 'Medium', '0.4353', '2026-01-03 09:27:50'),
(58, '1', 53, 'Male', 38, 'Current', 'Heavy', 'Active', 0, 0, 0, 176, 101, 80, 170, 230, 32, 141, 210, 0.4971, 'Medium', 0.3969, 'Medium', 0.4888, 'Medium', '0.461', '2025-12-31 09:27:50'),
(59, '1', 84, 'Male', 19.7, 'Former', 'None', 'Light', 0, 0, 0, 120, 82, 70, 104, 207, 52, 80, 148, 0.6101, 'High', 0.7796, 'High', 0.8203, 'High', '0.7367', '2026-01-15 09:27:50'),
(60, '1', 78, 'Male', 37.9, 'Never', 'Heavy', 'Sedentary', 0, 0, 0, 160, 108, 91, 179, 234, 33, 141, 228, 0.734, 'High', 0.8957, 'High', 0.8489, 'High', '0.8262', '2025-12-24 09:27:50'),
(61, '1', 67, 'Male', 25.3, 'Never', 'Moderate', 'Active', 0, 0, 0, 111, 78, 85, 103, 172, 58, 95, 139, 0.4752, 'Medium', 0.5086, 'Medium', 0.4862, 'Medium', '0.49', '2026-01-15 09:27:50'),
(62, '1', 49, 'Female', 37.6, 'Current', 'Moderate', 'Active', 1, 0, 0, 176, 99, 80, 180, 236, 34, 187, 197, 0.4582, 'Medium', 0.3654, 'Medium', 0.8216, 'High', '0.5484', '2026-01-13 09:27:50'),
(63, '1', 29, 'Female', 24.5, 'Current', 'Moderate', 'Sedentary', 0, 0, 0, 128, 82, 69, 119, 159, 66, 108, 143, 0.1696, 'Low', 0.0923, 'Low', 0.2277, 'Low', '0.1632', '2026-01-14 09:27:50'),
(64, '1', 33, 'Female', 35.3, 'Former', 'None', 'Active', 0, 0, 0, 180, 104, 92, 234, 237, 31, 152, 218, 0.2852, 'Low', 0.3048, 'Medium', 0.2974, 'Low', '0.2958', '2025-12-20 09:27:50'),
(65, '1', 60, 'Male', 21.5, 'Current', 'Heavy', 'Light', 1, 1, 0, 125, 83, 70, 97, 153, 64, 100, 123, 0.6147, 'High', 0.6207, 'High', 0.5932, 'Medium', '0.6095', '2026-01-03 09:27:50'),
(66, '1', 62, 'Male', 23.2, 'Former', 'None', 'Sedentary', 0, 0, 0, 114, 71, 79, 107, 157, 70, 93, 94, 0.4991, 'Medium', 0.5409, 'Medium', 0.4721, 'Medium', '0.5041', '2025-12-28 09:27:50'),
(67, '1', 65, 'Male', 24.9, 'Never', 'Moderate', 'Moderate', 0, 0, 0, 133, 72, 78, 94, 163, 53, 97, 144, 0.51, 'Medium', 0.5236, 'Medium', 0.5669, 'Medium', '0.5335', '2025-12-20 09:27:50'),
(68, '1', 58, 'Female', 19.6, 'Former', 'None', 'Light', 0, 0, 0, 111, 80, 65, 113, 171, 66, 96, 104, 0.4752, 'Medium', 0.4095, 'Medium', 0.513, 'Medium', '0.4659', '2025-12-25 09:27:50'),
(69, '1', 75, 'Male', 24.1, 'Former', 'Heavy', 'Light', 1, 1, 1, 133, 78, 84, 94, 159, 66, 112, 89, 0.6833, 'High', 0.8474, 'High', 0.922, 'High', '0.8176', '2026-01-08 09:27:50'),
(70, '1', 77, 'Male', 20.5, 'Former', 'Moderate', 'Active', 0, 0, 0, 134, 75, 72, 91, 164, 60, 124, 148, 0.6279, 'High', 0.5843, 'Medium', 0.7022, 'High', '0.6381', '2025-12-21 09:27:50'),
(71, '1', 26, 'Male', 25.3, 'Current', 'None', 'Active', 0, 1, 0, 123, 82, 73, 105, 184, 53, 93, 84, 0.1683, 'Low', 0.2167, 'Low', 0.1089, 'Low', '0.1646', '2026-01-19 09:27:50'),
(72, '1', 42, 'Male', 31.4, 'Former', 'None', 'Moderate', 0, 0, 0, 160, 95, 83, 237, 246, 33, 190, 201, 0.4297, 'Medium', 0.2628, 'Low', 0.5767, 'Medium', '0.4231', '2025-12-22 09:27:50'),
(73, '1', 78, 'Male', 20, 'Current', 'Heavy', 'Light', 0, 0, 0, 116, 80, 74, 104, 158, 56, 129, 148, 0.5684, 'Medium', 0.6663, 'High', 0.7624, 'High', '0.6657', '2025-12-31 09:27:50'),
(74, '1', 63, 'Female', 31.6, 'Former', 'None', 'Light', 0, 0, 0, 170, 92, 96, 242, 230, 41, 190, 215, 0.6604, 'High', 0.5617, 'Medium', 0.7974, 'High', '0.6732', '2026-01-09 09:27:50'),
(75, '1', 18, 'Male', 20.3, 'Former', 'Heavy', 'Light', 0, 0, 0, 133, 72, 75, 101, 206, 73, 124, 112, 0.0479, 'Low', 0.0455, 'Low', 0.0488, 'Low', '0.0474', '2026-01-03 09:27:50'),
(76, '1', 47, 'Male', 22.8, 'Former', 'Heavy', 'Moderate', 0, 0, 0, 131, 77, 62, 120, 180, 69, 111, 145, 0.2572, 'Low', 0.3274, 'Medium', 0.4578, 'Medium', '0.3475', '2026-01-19 09:27:50'),
(77, '1', 47, 'Female', 34, 'Current', 'Heavy', 'Sedentary', 0, 0, 0, 164, 104, 93, 234, 276, 43, 182, 217, 0.4743, 'Medium', 0.5601, 'Medium', 0.6019, 'High', '0.5454', '2025-12-24 09:27:50'),
(78, '1', 55, 'Male', 21.3, 'Never', 'Moderate', 'Moderate', 0, 0, 0, 132, 72, 74, 94, 200, 64, 103, 128, 0.406, 'Medium', 0.422, 'Medium', 0.3944, 'Medium', '0.4074', '2026-01-14 09:27:50'),
(79, '1', 29, 'Female', 29.6, 'Current', 'None', 'Sedentary', 0, 0, 0, 157, 94, 76, 151, 267, 43, 170, 235, 0.2605, 'Low', 0.1923, 'Low', 0.396, 'Medium', '0.2829', '2026-01-05 09:27:50'),
(80, '1', 72, 'Female', 25.9, 'Never', 'Heavy', 'Moderate', 0, 0, 0, 122, 80, 70, 85, 184, 64, 103, 123, 0.564, 'Medium', 0.6486, 'High', 0.5922, 'Medium', '0.6016', '2025-12-26 09:27:50'),
(81, '1', 50, 'Male', 25.9, 'Current', 'Heavy', 'Sedentary', 0, 0, 0, 119, 73, 64, 84, 200, 53, 107, 90, 0.315, 'Medium', 0.3489, 'Medium', 0.4282, 'Medium', '0.364', '2025-12-28 09:27:50'),
(82, '1', 65, 'Female', 37.9, 'Never', 'Heavy', 'Sedentary', 0, 0, 0, 174, 105, 82, 228, 221, 33, 168, 207, 0.6469, 'High', 0.5561, 'Medium', 0.7917, 'High', '0.6649', '2026-01-14 09:27:50'),
(83, '1', 32, 'Female', 32, 'Never', 'Moderate', 'Active', 0, 0, 0, 161, 105, 86, 140, 272, 45, 161, 217, 0.3017, 'Medium', 0.2255, 'Low', 0.4952, 'Medium', '0.3408', '2025-12-28 09:27:50'),
(84, '1', 71, 'Female', 24.6, 'Current', 'Moderate', 'Moderate', 1, 0, 0, 133, 81, 75, 99, 168, 75, 100, 137, 0.6775, 'High', 0.7403, 'High', 0.7813, 'High', '0.7331', '2026-01-02 09:27:50'),
(85, '1', 38, 'Male', 29.5, 'Former', 'None', 'Moderate', 0, 0, 0, 172, 91, 90, 241, 224, 32, 152, 197, 0.3859, 'Medium', 0.186, 'Low', 0.5158, 'Medium', '0.3626', '2025-12-28 09:27:50'),
(86, '1', 53, 'Male', 29.5, 'Current', 'None', 'Sedentary', 1, 0, 1, 175, 94, 77, 245, 230, 34, 175, 218, 0.533, 'Medium', 0.588, 'Medium', 0.9351, 'High', '0.6854', '2026-01-13 09:27:50'),
(87, '1', 22, 'Female', 19, 'Never', 'Moderate', 'Moderate', 0, 0, 0, 110, 82, 58, 92, 169, 66, 99, 128, -0.0153, 'Low', 0.0447, 'Low', 0.0795, 'Low', '0.0363', '2026-01-02 09:27:50'),
(88, '1', 65, 'Female', 32.8, 'Current', 'Heavy', 'Light', 0, 0, 1, 178, 90, 95, 213, 224, 34, 143, 200, 0.745, 'High', 0.8492, 'High', 0.95, 'High', '0.8481', '2026-01-13 09:27:50'),
(89, '1', 31, 'Male', 30.2, 'Former', 'Heavy', 'Light', 0, 0, 0, 180, 97, 85, 226, 274, 30, 153, 236, 0.3058, 'Medium', 0.1742, 'Low', 0.4552, 'Medium', '0.3118', '2025-12-26 09:27:50'),
(90, '1', 28, 'Female', 33.5, 'Former', 'Heavy', 'Moderate', 0, 0, 0, 146, 95, 88, 172, 236, 39, 171, 214, 0.1677, 'Low', 0.1406, 'Low', 0.2553, 'Low', '0.1878', '2026-01-14 09:27:50'),
(91, '1', 50, 'Female', 29.6, 'Former', 'Moderate', 'Moderate', 0, 0, 0, 167, 97, 92, 212, 261, 34, 180, 229, 0.439, 'Medium', 0.6073, 'High', 0.5522, 'Medium', '0.5328', '2026-01-04 09:27:50'),
(92, '1', 67, 'Male', 30.6, 'Former', 'Moderate', 'Active', 0, 1, 0, 153, 104, 92, 183, 239, 38, 189, 181, 0.9304, 'High', 0.7915, 'High', 0.8338, 'High', '0.8519', '2026-01-09 09:27:50'),
(93, '1', 46, 'Male', 36.9, 'Former', 'Moderate', 'Moderate', 0, 0, 0, 140, 90, 85, 181, 240, 43, 142, 184, 0.5054, 'Medium', 0.4015, 'Medium', 0.4132, 'Medium', '0.44', '2026-01-08 09:27:50'),
(94, '1', 22, 'Male', 19.2, 'Never', 'Moderate', 'Moderate', 0, 0, 1, 123, 77, 62, 81, 159, 66, 82, 109, 0.1266, 'Low', 0.0941, 'Low', 0.2465, 'Low', '0.1557', '2026-01-04 09:27:50'),
(95, '1', 85, 'Male', 24.3, 'Current', 'Moderate', 'Active', 0, 0, 0, 118, 77, 79, 97, 169, 55, 80, 92, 0.6617, 'High', 0.6438, 'High', 0.8357, 'High', '0.7137', '2025-12-23 09:27:50'),
(96, '1', 77, 'Male', 30.1, 'Former', 'Heavy', 'Light', 0, 0, 0, 179, 90, 100, 170, 244, 34, 174, 213, 0.6776, 'High', 0.6979, 'High', 0.7621, 'High', '0.7125', '2026-01-11 09:27:50'),
(97, '1', 34, 'Male', 29.7, 'Never', 'None', 'Moderate', 0, 0, 0, 146, 90, 86, 189, 275, 40, 143, 182, 0.341, 'Medium', 0.2511, 'Low', 0.493, 'Medium', '0.3617', '2026-01-06 09:27:50'),
(98, '1', 64, 'Female', 27.8, 'Never', 'Moderate', 'Moderate', 0, 0, 0, 164, 93, 97, 141, 246, 38, 176, 244, 0.5356, 'Medium', 0.5576, 'Medium', 0.7726, 'High', '0.6219', '2025-12-25 09:27:50'),
(99, '1', 64, 'Male', 26.3, 'Current', 'Moderate', 'Active', 0, 0, 0, 129, 78, 79, 117, 164, 68, 94, 86, 0.4974, 'Medium', 0.4223, 'Medium', 0.5005, 'Medium', '0.4734', '2026-01-05 09:27:50'),
(100, '1', 82, 'Female', 34.3, 'Never', 'None', 'Moderate', 0, 0, 0, 144, 103, 102, 187, 241, 36, 149, 221, 0.7452, 'High', 0.8427, 'High', 0.8772, 'High', '0.8217', '2025-12-26 09:27:50'),
(101, 'admin', 25, 'Male', 50, 'Never', 'Heavy', 'Sedentary', 1, 0, 0, 120, 120, 120, 120, 120, 120, 120, 120, 0.914, 'High', 0.0075, 'Low', 0.9922, 'High', 'Critical', '2026-01-21 03:58:05'),
(102, 'admin', 25, 'Female', 35, 'Never', 'None', 'Light', 1, 1, 1, 120, 120, 120, 120, 120, 120, 120, 129, 0.135, 'Low', 0.0058, 'Low', 0.9981, 'High', 'Elevated', '2026-01-21 05:18:26');

-- --------------------------------------------------------

--
-- Stand-in structure for view `disease_risk_statistics`
-- (See below for the actual view)
--
CREATE TABLE `disease_risk_statistics` (
`total_assessments` bigint(21)
,`avg_diabetes_risk` double
,`diabetes_high_count` decimal(22,0)
,`diabetes_medium_count` decimal(22,0)
,`diabetes_low_count` decimal(22,0)
,`avg_heart_disease_risk` double
,`heart_disease_high_count` decimal(22,0)
,`heart_disease_medium_count` decimal(22,0)
,`heart_disease_low_count` decimal(22,0)
,`avg_hypertension_risk` double
,`hypertension_high_count` decimal(22,0)
,`hypertension_medium_count` decimal(22,0)
,`hypertension_low_count` decimal(22,0)
,`overall_high_count` decimal(22,0)
,`overall_medium_count` decimal(22,0)
,`overall_low_count` decimal(22,0)
,`avg_age` decimal(14,4)
,`avg_bmi` double
);

-- --------------------------------------------------------

--
-- Table structure for table `patient_requests`
--

CREATE TABLE `patient_requests` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `age` int(11) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `heart_rate` int(11) DEFAULT NULL,
  `glucose` float DEFAULT NULL,
  `prior_admission` int(11) DEFAULT NULL,
  `prediction` float DEFAULT NULL,
  `risk_level` varchar(10) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient_requests`
--

INSERT INTO `patient_requests` (`id`, `user_id`, `patient_name`, `age`, `gender`, `heart_rate`, `glucose`, `prior_admission`, `prediction`, `risk_level`, `created_at`) VALUES
(1, NULL, NULL, 25, 'M', 95, 140, 0, 0.21, 'Low', '2026-01-19 01:38:37'),
(2, 4, 'Juan Dela Cruz', 55, 'M', 86, 130, 3, 0.22, 'Low', '2026-01-19 02:18:58'),
(3, NULL, NULL, 83, 'Female', 82, 113, 1, 0.6256, 'medium', '2026-01-02 09:23:21'),
(4, NULL, NULL, 75, 'Male', 102, 142, 1, 0.95, 'high', '2025-12-21 09:23:21'),
(5, NULL, NULL, 55, 'Female', 66, 80, 0, 0.2744, 'low', '2026-01-14 09:23:21'),
(6, NULL, NULL, 60, 'Female', 68, 100, 0, 0.2929, 'low', '2025-12-30 09:23:21'),
(7, NULL, NULL, 20, 'Male', 61, 80, 0, 0.046, 'low', '2026-01-08 09:23:21'),
(8, NULL, NULL, 80, 'Male', 70, 87, 0, 0.4632, 'medium', '2025-12-27 09:23:21'),
(9, NULL, NULL, 45, 'Female', 74, 101, 0, 0.1894, 'low', '2026-01-05 09:23:21'),
(10, NULL, NULL, 34, 'Male', 59, 117, 1, 0.1496, 'low', '2026-01-17 09:23:21'),
(11, NULL, NULL, 76, 'Female', 76, 114, 0, 0.4627, 'medium', '2025-12-27 09:23:21'),
(12, NULL, NULL, 81, 'Female', 94, 154, 0, 0.7749, 'high', '2026-01-08 09:23:21'),
(13, NULL, NULL, 26, 'Female', 83, 233, 0, 0.4571, 'medium', '2026-01-16 09:23:21'),
(14, NULL, NULL, 59, 'Female', 63, 107, 0, 0.2511, 'low', '2026-01-11 09:23:21'),
(15, NULL, NULL, 52, 'Male', 80, 175, 1, 0.5257, 'medium', '2025-12-25 09:23:21'),
(16, NULL, NULL, 83, 'Female', 84, 91, 0, 0.493, 'medium', '2025-12-31 09:23:21'),
(17, NULL, NULL, 23, 'Female', 71, 96, 1, 0.0668, 'low', '2026-01-02 09:23:21'),
(18, NULL, NULL, 52, 'Male', 92, 231, 0, 0.546, 'medium', '2025-12-24 09:23:21'),
(19, NULL, NULL, 56, 'Female', 93, 230, 1, 0.7687, 'high', '2026-01-11 09:23:21'),
(20, NULL, NULL, 36, 'Female', 81, 246, 0, 0.5204, 'medium', '2026-01-01 09:23:21'),
(21, NULL, NULL, 54, 'Male', 83, 219, 0, 0.6255, 'medium', '2025-12-30 09:23:21'),
(22, NULL, NULL, 29, 'Male', 59, 86, 0, 0.0831, 'low', '2026-01-08 09:23:21'),
(23, NULL, NULL, 51, 'Male', 75, 105, 0, 0.2038, 'low', '2026-01-12 09:23:21'),
(24, NULL, NULL, 30, 'Male', 74, 81, 0, 0.0938, 'low', '2025-12-22 09:23:21'),
(25, NULL, NULL, 40, 'Male', 71, 120, 0, 0.1347, 'low', '2026-01-15 09:23:21'),
(26, NULL, NULL, 75, 'Female', 77, 116, 0, 0.4437, 'medium', '2026-01-05 09:23:21'),
(27, NULL, NULL, 36, 'Female', 64, 117, 1, 0.1918, 'low', '2026-01-15 09:23:21'),
(28, NULL, NULL, 28, 'Female', 81, 176, 0, 0.1562, 'low', '2026-01-01 09:23:21'),
(29, NULL, NULL, 33, 'Female', 68, 110, 0, 0.093, 'low', '2026-01-12 09:23:21'),
(30, NULL, NULL, 32, 'Female', 78, 177, 0, 0.1598, 'low', '2025-12-25 09:23:21'),
(31, NULL, NULL, 26, 'Male', 73, 113, 1, 0.0887, 'low', '2026-01-18 09:23:21'),
(32, NULL, NULL, 25, 'Male', 92, 229, 0, 0.607, 'medium', '2025-12-28 09:23:21'),
(33, NULL, NULL, 51, 'Female', 67, 91, 1, 0.3042, 'low', '2025-12-21 09:23:21'),
(34, NULL, NULL, 69, 'Male', 96, 143, 0, 0.4644, 'medium', '2025-12-24 09:23:21'),
(35, NULL, NULL, 37, 'Male', 70, 114, 0, 0.1246, 'low', '2025-12-21 09:23:21'),
(36, NULL, NULL, 84, 'Male', 93, 244, 1, 0.77, 'high', '2026-01-17 09:23:21'),
(37, NULL, NULL, 18, 'Female', 75, 87, 0, -0.0056, 'low', '2026-01-01 09:23:21'),
(38, NULL, NULL, 37, 'Male', 70, 90, 1, 0.2272, 'low', '2026-01-08 09:23:21'),
(39, NULL, NULL, 81, 'Female', 78, 118, 0, 0.5054, 'medium', '2026-01-07 09:23:21'),
(40, NULL, NULL, 35, 'Female', 78, 80, 1, 0.1214, 'low', '2025-12-22 09:23:21'),
(41, NULL, NULL, 38, 'Female', 74, 87, 0, 0.1908, 'low', '2026-01-11 09:23:21'),
(42, NULL, NULL, 24, 'Male', 81, 168, 1, 0.0703, 'low', '2026-01-07 09:23:21'),
(43, NULL, NULL, 75, 'Male', 76, 80, 0, 0.4632, 'medium', '2026-01-18 09:23:21'),
(44, NULL, NULL, 69, 'Male', 82, 96, 1, 0.5163, 'medium', '2025-12-23 09:23:21'),
(45, NULL, NULL, 68, 'Male', 71, 81, 0, 0.388, 'low', '2025-12-31 09:23:21'),
(46, NULL, NULL, 56, 'Male', 75, 94, 1, 0.3306, 'low', '2026-01-02 09:23:21'),
(47, NULL, NULL, 40, 'Male', 69, 103, 1, 0.2033, 'low', '2025-12-22 09:23:21'),
(48, NULL, NULL, 85, 'Male', 97, 249, 0, 0.7347, 'high', '2025-12-21 09:23:21'),
(49, NULL, NULL, 25, 'Male', 63, 112, 0, 0.1009, 'low', '2026-01-09 09:23:21'),
(50, NULL, NULL, 31, 'Male', 73, 159, 1, 0.435, 'medium', '2026-01-11 09:23:21'),
(51, NULL, NULL, 18, 'Male', 65, 85, 1, 0.0855, 'low', '2025-12-30 09:23:21'),
(52, NULL, NULL, 84, 'Female', 91, 142, 0, 0.7571, 'high', '2026-01-11 09:23:21'),
(53, NULL, NULL, 49, 'Male', 61, 89, 0, 0.2156, 'low', '2026-01-01 09:23:21'),
(54, NULL, NULL, 37, 'Female', 69, 119, 0, 0.1347, 'low', '2025-12-22 09:23:21'),
(55, NULL, NULL, 67, 'Male', 68, 84, 1, 0.5027, 'medium', '2026-01-19 09:23:21'),
(56, NULL, NULL, 61, 'Female', 82, 88, 1, 0.3807, 'low', '2025-12-27 09:23:21'),
(57, NULL, NULL, 28, 'Female', 74, 105, 0, 0.0839, 'low', '2025-12-30 09:23:21'),
(58, NULL, NULL, 58, 'Male', 74, 83, 0, 0.2927, 'low', '2025-12-21 09:23:21'),
(59, NULL, NULL, 37, 'Male', 93, 236, 0, 0.5504, 'medium', '2026-01-09 09:23:21'),
(60, NULL, NULL, 79, 'Male', 81, 92, 0, 0.4925, 'medium', '2026-01-11 09:23:21'),
(61, NULL, NULL, 65, 'Male', 100, 200, 1, 0.6122, 'medium', '2026-01-02 09:23:21'),
(62, NULL, NULL, 85, 'Male', 94, 188, 0, 0.95, 'high', '2025-12-25 09:23:21'),
(63, NULL, NULL, 82, 'Female', 93, 250, 0, 0.6907, 'medium', '2026-01-18 09:23:21'),
(64, NULL, NULL, 35, 'Female', 77, 197, 1, 0.3563, 'low', '2026-01-04 09:23:21'),
(65, NULL, NULL, 23, 'Male', 75, 100, 1, 0.0521, 'low', '2025-12-30 09:23:21'),
(66, NULL, NULL, 73, 'Female', 72, 90, 1, 0.5374, 'medium', '2026-01-11 09:23:21'),
(67, NULL, NULL, 25, 'Female', 68, 102, 0, 0.0747, 'low', '2025-12-30 09:23:21'),
(68, NULL, NULL, 28, 'Female', 62, 96, 1, 0.1491, 'low', '2026-01-02 09:23:21'),
(69, NULL, NULL, 48, 'Female', 78, 213, 1, 0.4465, 'medium', '2026-01-01 09:23:21'),
(70, NULL, NULL, 85, 'Male', 83, 84, 0, 0.5042, 'medium', '2025-12-24 09:23:21'),
(71, NULL, NULL, 37, 'Female', 71, 118, 0, 0.1407, 'low', '2026-01-07 09:23:21'),
(72, NULL, NULL, 41, 'Female', 63, 110, 0, 0.1695, 'low', '2025-12-29 09:23:21'),
(73, NULL, NULL, 24, 'Female', 59, 96, 0, 0.0498, 'low', '2025-12-21 09:23:21'),
(74, NULL, NULL, 34, 'Female', 67, 114, 0, 0.1294, 'low', '2026-01-03 09:23:21'),
(75, NULL, NULL, 27, 'Female', 64, 115, 0, 0.0496, 'low', '2026-01-01 09:23:21'),
(76, NULL, NULL, 28, 'Female', 85, 240, 0, 0.4605, 'medium', '2025-12-27 09:23:21'),
(77, NULL, NULL, 22, 'Male', 70, 108, 0, 0.0513, 'low', '2026-01-13 09:23:21'),
(78, NULL, NULL, 34, 'Male', 65, 107, 1, 0.1981, 'low', '2026-01-07 09:23:21'),
(79, NULL, NULL, 27, 'Female', 72, 85, 1, 0.0863, 'low', '2025-12-31 09:23:21'),
(80, NULL, NULL, 79, 'Female', 94, 227, 1, 0.77, 'high', '2026-01-07 09:23:21'),
(81, NULL, NULL, 54, 'Male', 80, 146, 1, 0.6997, 'medium', '2026-01-08 09:23:21'),
(82, NULL, NULL, 74, 'Female', 85, 99, 0, 0.4337, 'medium', '2026-01-09 09:23:21'),
(83, NULL, NULL, 24, 'Female', 75, 93, 1, 0.1261, 'low', '2025-12-25 09:23:21'),
(84, NULL, NULL, 31, 'Female', 68, 112, 0, 0.127, 'low', '2026-01-03 09:23:21'),
(85, NULL, NULL, 52, 'Male', 94, 230, 1, 0.4937, 'medium', '2026-01-10 09:23:21'),
(86, NULL, NULL, 71, 'Male', 71, 119, 1, 0.5096, 'medium', '2026-01-10 09:23:21'),
(87, NULL, NULL, 34, 'Male', 81, 150, 1, 0.3817, 'low', '2025-12-23 09:23:21'),
(88, NULL, NULL, 46, 'Male', 76, 109, 1, 0.2569, 'low', '2025-12-30 09:23:21'),
(89, NULL, NULL, 79, 'Female', 77, 109, 0, 0.4407, 'medium', '2026-01-15 09:23:21'),
(90, NULL, NULL, 57, 'Male', 69, 84, 0, 0.2577, 'low', '2026-01-09 09:23:21'),
(91, NULL, NULL, 57, 'Female', 93, 160, 0, 0.3383, 'low', '2025-12-26 09:23:21'),
(92, NULL, NULL, 41, 'Male', 63, 116, 0, 0.1629, 'low', '2025-12-29 09:23:21'),
(93, NULL, NULL, 54, 'Female', 64, 114, 1, 0.3211, 'low', '2026-01-14 09:23:21'),
(94, NULL, NULL, 33, 'Male', 62, 82, 1, 0.1819, 'low', '2026-01-14 09:23:21'),
(95, NULL, NULL, 54, 'Male', 77, 85, 1, 0.3138, 'low', '2025-12-21 09:23:21'),
(96, NULL, NULL, 45, 'Female', 63, 111, 1, 0.2285, 'low', '2025-12-23 09:23:21'),
(97, NULL, NULL, 43, 'Male', 73, 113, 1, 0.2493, 'low', '2025-12-31 09:23:21'),
(98, NULL, NULL, 43, 'Female', 70, 91, 0, 0.1982, 'low', '2026-01-07 09:23:21'),
(99, NULL, NULL, 23, 'Male', 71, 95, 0, 0.0291, 'low', '2026-01-02 09:23:21'),
(100, NULL, NULL, 54, 'Male', 80, 100, 0, 0.2374, 'low', '2026-01-11 09:23:21'),
(101, NULL, NULL, 57, 'Female', 92, 182, 0, 0.4792, 'medium', '2025-12-21 09:23:21'),
(102, NULL, NULL, 80, 'Female', 103, 211, 0, 0.95, 'high', '2026-01-06 09:23:21'),
(103, NULL, NULL, 65, 'Female', 70, 102, 0, 0.2837, 'low', '2025-12-25 09:23:38'),
(104, NULL, NULL, 63, 'Male', 92, 247, 1, 0.7534, 'high', '2025-12-24 09:23:38'),
(105, NULL, NULL, 49, 'Female', 81, 102, 0, 0.2121, 'low', '2025-12-30 09:23:38'),
(106, NULL, NULL, 49, 'Female', 72, 101, 0, 0.2165, 'low', '2026-01-18 09:23:38'),
(107, NULL, NULL, 68, 'Female', 69, 107, 0, 0.4092, 'medium', '2026-01-19 09:23:38'),
(108, NULL, NULL, 30, 'Female', 66, 118, 0, 0.1037, 'low', '2026-01-12 09:23:38'),
(109, NULL, NULL, 72, 'Female', 66, 91, 0, 0.4555, 'medium', '2025-12-28 09:23:38'),
(110, NULL, NULL, 72, 'Male', 86, 113, 0, 0.403, 'medium', '2025-12-31 09:23:38'),
(111, NULL, NULL, 59, 'Female', 96, 235, 1, 0.9387, 'high', '2026-01-04 09:23:38'),
(112, NULL, NULL, 40, 'Male', 63, 112, 1, 0.1901, 'low', '2026-01-07 09:23:38'),
(113, NULL, NULL, 23, 'Male', 66, 97, 0, 0.0751, 'low', '2026-01-02 09:23:38'),
(114, NULL, NULL, 75, 'Female', 81, 98, 0, 0.4271, 'medium', '2026-01-12 09:23:38'),
(115, NULL, NULL, 22, 'Female', 64, 84, 0, 0.0446, 'low', '2025-12-27 09:23:38'),
(116, NULL, NULL, 73, 'Female', 80, 85, 0, 0.4016, 'medium', '2025-12-22 09:23:38'),
(117, NULL, NULL, 31, 'Male', 92, 207, 0, 0.447, 'medium', '2026-01-14 09:23:38'),
(118, NULL, NULL, 54, 'Female', 63, 100, 0, 0.2479, 'low', '2025-12-30 09:23:38'),
(119, NULL, NULL, 48, 'Female', 90, 145, 1, 0.713, 'high', '2026-01-10 09:23:38'),
(120, NULL, NULL, 81, 'Male', 74, 94, 0, 0.4879, 'medium', '2026-01-05 09:23:38'),
(121, NULL, NULL, 25, 'Male', 87, 159, 0, 0.2501, 'low', '2026-01-04 09:23:38'),
(122, NULL, NULL, 23, 'Male', 59, 83, 0, 0.0666, 'low', '2025-12-28 09:23:38'),
(123, NULL, NULL, 44, 'Female', 88, 166, 1, 0.4638, 'medium', '2026-01-18 09:23:38'),
(124, NULL, NULL, 42, 'Female', 61, 95, 0, 0.1615, 'low', '2025-12-27 09:23:38'),
(125, NULL, NULL, 34, 'Male', 72, 95, 0, 0.1162, 'low', '2025-12-25 09:23:38'),
(126, NULL, NULL, 59, 'Male', 65, 84, 1, 0.3181, 'low', '2025-12-21 09:23:38'),
(127, NULL, NULL, 48, 'Female', 96, 177, 1, 0.7406, 'high', '2025-12-21 09:23:38'),
(128, NULL, NULL, 57, 'Male', 78, 80, 0, 0.2434, 'low', '2026-01-12 09:23:38'),
(129, NULL, NULL, 20, 'Male', 69, 82, 1, 0.0546, 'low', '2026-01-07 09:23:38'),
(130, NULL, NULL, 57, 'Female', 96, 147, 0, 0.546, 'medium', '2026-01-03 09:23:38'),
(131, NULL, NULL, 84, 'Female', 71, 114, 0, 0.5286, 'medium', '2025-12-20 09:23:38'),
(132, NULL, NULL, 54, 'Female', 75, 90, 0, 0.2418, 'low', '2026-01-13 09:23:38'),
(133, NULL, NULL, 40, 'Female', 62, 115, 1, 0.2416, 'low', '2025-12-23 09:23:38'),
(134, NULL, NULL, 65, 'Male', 88, 243, 1, 0.5729, 'medium', '2026-01-01 09:23:38'),
(135, NULL, NULL, 85, 'Male', 75, 117, 0, 0.5259, 'medium', '2025-12-23 09:23:38'),
(136, NULL, NULL, 68, 'Male', 73, 116, 1, 0.4781, 'medium', '2025-12-31 09:23:38'),
(137, NULL, NULL, 42, 'Male', 79, 105, 0, 0.1489, 'low', '2026-01-03 09:23:38'),
(138, NULL, NULL, 71, 'Male', 81, 120, 0, 0.4213, 'medium', '2026-01-19 09:23:38'),
(139, NULL, NULL, 72, 'Female', 68, 87, 1, 0.5124, 'medium', '2026-01-11 09:23:38'),
(140, NULL, NULL, 80, 'Male', 73, 85, 1, 0.5854, 'medium', '2026-01-08 09:23:38'),
(141, NULL, NULL, 79, 'Female', 100, 242, 1, 0.7639, 'high', '2025-12-26 09:23:38'),
(142, NULL, NULL, 75, 'Male', 76, 101, 1, 0.5525, 'medium', '2026-01-09 09:23:38'),
(143, NULL, NULL, 40, 'Male', 80, 145, 0, 0.5854, 'medium', '2025-12-20 09:23:38'),
(144, NULL, NULL, 21, 'Male', 80, 164, 1, 0.2947, 'low', '2025-12-31 09:23:38'),
(145, NULL, NULL, 67, 'Female', 74, 90, 0, 0.4139, 'medium', '2026-01-18 09:23:38'),
(146, NULL, NULL, 50, 'Male', 65, 105, 0, 0.2251, 'low', '2026-01-04 09:23:38'),
(147, NULL, NULL, 40, 'Female', 85, 231, 0, 0.3345, 'low', '2026-01-01 09:23:38'),
(148, NULL, NULL, 75, 'Female', 82, 198, 1, 0.7521, 'high', '2026-01-11 09:23:38'),
(149, NULL, NULL, 77, 'Female', 82, 151, 1, 0.6036, 'medium', '2025-12-23 09:23:38'),
(150, NULL, NULL, 82, 'Male', 85, 174, 1, 0.95, 'high', '2026-01-13 09:23:38'),
(151, NULL, NULL, 23, 'Male', 66, 119, 0, 0.0597, 'low', '2026-01-10 09:23:38'),
(152, NULL, NULL, 25, 'Male', 74, 116, 1, 0.0788, 'low', '2025-12-25 09:23:38'),
(153, NULL, NULL, 46, 'Male', 62, 118, 0, 0.1968, 'low', '2026-01-08 09:23:38'),
(154, NULL, NULL, 85, 'Male', 82, 112, 0, 0.5005, 'medium', '2025-12-22 09:23:38'),
(155, NULL, NULL, 37, 'Female', 73, 86, 0, 0.1068, 'low', '2026-01-06 09:23:38'),
(156, NULL, NULL, 54, 'Female', 76, 88, 0, 0.256, 'low', '2026-01-13 09:23:38'),
(157, NULL, NULL, 53, 'Male', 69, 120, 0, 0.2344, 'low', '2026-01-09 09:23:38'),
(158, NULL, NULL, 64, 'Male', 80, 238, 0, 0.4502, 'medium', '2026-01-06 09:23:38'),
(159, NULL, NULL, 67, 'Male', 97, 248, 1, 0.9224, 'high', '2025-12-26 09:23:38'),
(160, NULL, NULL, 39, 'Female', 86, 238, 0, 0.5025, 'medium', '2025-12-25 09:23:38'),
(161, NULL, NULL, 46, 'Female', 81, 186, 1, 0.6403, 'medium', '2026-01-07 09:23:38'),
(162, NULL, NULL, 30, 'Female', 89, 234, 0, 0.6184, 'medium', '2025-12-29 09:23:38'),
(163, NULL, NULL, 50, 'Female', 72, 118, 0, 0.1887, 'low', '2026-01-09 09:23:38'),
(164, NULL, NULL, 54, 'Male', 73, 80, 1, 0.2982, 'low', '2026-01-06 09:23:38'),
(165, NULL, NULL, 71, 'Male', 101, 248, 1, 0.86, 'high', '2025-12-25 09:23:38'),
(166, NULL, NULL, 67, 'Male', 94, 169, 0, 0.6712, 'medium', '2026-01-01 09:23:38'),
(167, NULL, NULL, 82, 'Male', 79, 81, 1, 0.6343, 'medium', '2026-01-19 09:23:38'),
(168, NULL, NULL, 27, 'Male', 73, 86, 0, 0.088, 'low', '2026-01-13 09:23:38'),
(169, NULL, NULL, 27, 'Female', 64, 111, 0, 0.076, 'low', '2026-01-09 09:23:38'),
(170, NULL, NULL, 53, 'Male', 62, 115, 0, 0.2334, 'low', '2026-01-10 09:23:38'),
(171, NULL, NULL, 20, 'Male', 91, 162, 1, 0.5149, 'medium', '2025-12-26 09:23:38'),
(172, NULL, NULL, 52, 'Male', 73, 80, 0, 0.2191, 'low', '2025-12-30 09:23:38'),
(173, NULL, NULL, 68, 'Male', 84, 95, 0, 0.3953, 'low', '2026-01-09 09:23:38'),
(174, NULL, NULL, 47, 'Male', 72, 113, 1, 0.221, 'low', '2025-12-31 09:23:38'),
(175, NULL, NULL, 25, 'Female', 76, 98, 0, 0.1066, 'low', '2026-01-13 09:23:38'),
(176, NULL, NULL, 22, 'Female', 75, 93, 0, 0.0082, 'low', '2025-12-22 09:23:38'),
(177, NULL, NULL, 53, 'Male', 82, 164, 0, 0.6547, 'medium', '2026-01-14 09:23:38'),
(178, NULL, NULL, 54, 'Female', 82, 89, 0, 0.2425, 'low', '2026-01-09 09:23:38'),
(179, NULL, NULL, 30, 'Female', 60, 115, 0, 0.1211, 'low', '2026-01-16 09:23:38'),
(180, NULL, NULL, 78, 'Male', 101, 193, 0, 0.95, 'high', '2026-01-06 09:23:38'),
(181, NULL, NULL, 47, 'Female', 79, 102, 0, 0.2279, 'low', '2025-12-29 09:23:38'),
(182, NULL, NULL, 28, 'Male', 90, 240, 0, 0.6455, 'medium', '2025-12-29 09:23:38'),
(183, NULL, NULL, 74, 'Female', 85, 147, 0, 0.6834, 'medium', '2026-01-14 09:23:38'),
(184, NULL, NULL, 76, 'Male', 87, 140, 1, 0.7585, 'high', '2026-01-12 09:23:38'),
(185, NULL, NULL, 35, 'Male', 74, 197, 0, 0.4538, 'medium', '2026-01-01 09:23:38'),
(186, NULL, NULL, 26, 'Male', 70, 102, 0, 0.061, 'low', '2025-12-24 09:23:38'),
(187, NULL, NULL, 50, 'Male', 64, 97, 1, 0.3172, 'low', '2026-01-07 09:23:38'),
(188, NULL, NULL, 38, 'Male', 85, 177, 1, 0.3624, 'low', '2025-12-24 09:23:38'),
(189, NULL, NULL, 58, 'Female', 79, 156, 0, 0.3573, 'low', '2025-12-27 09:23:38'),
(190, NULL, NULL, 34, 'Male', 72, 80, 1, 0.1306, 'low', '2026-01-18 09:23:38'),
(191, NULL, NULL, 39, 'Male', 59, 93, 0, 0.1494, 'low', '2026-01-05 09:23:38'),
(192, NULL, NULL, 38, 'Female', 74, 159, 1, 0.2653, 'low', '2026-01-16 09:23:38'),
(193, NULL, NULL, 56, 'Female', 78, 80, 0, 0.2521, 'low', '2025-12-24 09:23:38'),
(194, NULL, NULL, 72, 'Male', 73, 96, 1, 0.5477, 'medium', '2025-12-20 09:23:38'),
(195, NULL, NULL, 61, 'Male', 89, 173, 0, 0.501, 'medium', '2026-01-06 09:23:38'),
(196, NULL, NULL, 64, 'Male', 65, 97, 0, 0.3006, 'low', '2026-01-01 09:23:38'),
(197, NULL, NULL, 72, 'Female', 94, 232, 1, 0.9031, 'high', '2026-01-09 09:23:38'),
(198, NULL, NULL, 62, 'Female', 66, 96, 0, 0.3203, 'low', '2025-12-31 09:23:38'),
(199, NULL, NULL, 18, 'Male', 90, 193, 0, 0.2416, 'low', '2025-12-20 09:23:38'),
(200, NULL, NULL, 22, 'Male', 65, 90, 0, 0.0567, 'low', '2025-12-29 09:23:38'),
(201, NULL, NULL, 77, 'Male', 93, 192, 1, 0.95, 'high', '2026-01-06 09:23:38'),
(202, NULL, NULL, 83, 'Female', 78, 95, 1, 0.6008, 'medium', '2026-01-17 09:23:38'),
(203, NULL, 'Charles Baker', 55, 'Male', 79, 239, 1, 0.6438, 'medium', '2026-01-13 09:24:23'),
(204, NULL, 'Dorothy King', 46, 'Male', 66, 81, 1, 0.2832, 'low', '2025-12-21 09:24:23'),
(205, NULL, 'Timothy Anderson', 42, 'Male', 77, 113, 0, 0.1641, 'low', '2026-01-02 09:24:23'),
(206, NULL, 'Jennifer Anderson', 27, 'Female', 77, 196, 0, 0.4754, 'medium', '2026-01-05 09:24:23'),
(207, NULL, 'Jack Allen', 19, 'Male', 61, 98, 0, 0.0184, 'low', '2026-01-15 09:24:23'),
(208, NULL, 'Catherine Phillips', 62, 'Female', 79, 172, 0, 0.3666, 'low', '2026-01-09 09:24:23'),
(209, NULL, 'Melissa Gutierrez', 65, 'Female', 91, 203, 0, 0.6396, 'medium', '2026-01-01 09:24:23'),
(210, NULL, 'Jack Green', 20, 'Male', 69, 98, 1, 0.104, 'low', '2025-12-29 09:24:23'),
(211, NULL, 'Emma Phillips', 55, 'Male', 92, 210, 1, 0.8807, 'high', '2025-12-21 09:24:23'),
(212, NULL, 'Ryan Ward', 43, 'Female', 61, 82, 0, 0.1744, 'low', '2026-01-03 09:24:23'),
(213, NULL, 'Daniel Campbell', 84, 'Female', 84, 109, 1, 0.5862, 'medium', '2026-01-07 09:24:23'),
(214, NULL, 'Betty Harris', 45, 'Male', 77, 148, 1, 0.4794, 'medium', '2026-01-08 09:24:23'),
(215, NULL, 'Cynthia Sanchez', 42, 'Male', 80, 250, 1, 0.6216, 'medium', '2025-12-28 09:24:23'),
(216, NULL, 'Janet Nelson', 30, 'Male', 65, 86, 0, 0.0819, 'low', '2026-01-11 09:24:23'),
(217, NULL, 'Elizabeth Martinez', 49, 'Male', 77, 111, 0, 0.1983, 'low', '2025-12-22 09:24:23'),
(218, NULL, 'Paul Cooper', 47, 'Male', 89, 199, 1, 0.6184, 'medium', '2026-01-15 09:24:23'),
(219, NULL, 'James Howard', 84, 'Male', 75, 97, 0, 0.4933, 'medium', '2026-01-12 09:24:23'),
(220, NULL, 'Brian Cruz', 82, 'Female', 75, 82, 1, 0.5967, 'medium', '2026-01-08 09:24:23'),
(221, NULL, 'Mark Baker', 33, 'Male', 75, 115, 1, 0.1696, 'low', '2025-12-31 09:24:23'),
(222, NULL, 'Jennifer Smith', 61, 'Female', 79, 109, 1, 0.3867, 'low', '2025-12-29 09:24:23'),
(223, NULL, 'Scott Morales', 45, 'Female', 75, 83, 1, 0.2346, 'low', '2025-12-29 09:24:23'),
(224, NULL, 'Eric Phillips', 73, 'Female', 85, 103, 0, 0.462, 'medium', '2026-01-16 09:24:23'),
(225, NULL, 'Jennifer Morales', 67, 'Female', 92, 232, 0, 0.6445, 'medium', '2025-12-29 09:24:23'),
(226, NULL, 'Rebecca Davis', 53, 'Female', 77, 92, 0, 0.2357, 'low', '2026-01-01 09:24:23'),
(227, NULL, 'Kimberly Wright', 82, 'Male', 103, 178, 0, 0.6815, 'medium', '2026-01-02 09:24:23'),
(228, NULL, 'Shirley White', 48, 'Female', 72, 102, 0, 0.2436, 'low', '2025-12-24 09:24:23'),
(229, NULL, 'Amy Rivera', 18, 'Male', 55, 87, 1, 0.0502, 'low', '2026-01-19 09:24:23'),
(230, NULL, 'Pamela Martin', 59, 'Female', 65, 119, 0, 0.288, 'low', '2025-12-27 09:24:23'),
(231, NULL, 'Karen Jones', 77, 'Female', 99, 240, 0, 0.95, 'high', '2025-12-27 09:24:23'),
(232, NULL, 'Jack Hill', 76, 'Female', 87, 106, 0, 0.4324, 'medium', '2026-01-11 09:24:23'),
(233, NULL, 'Mary Gonzalez', 33, 'Female', 58, 91, 1, 0.1076, 'low', '2025-12-25 09:24:23'),
(234, NULL, 'Carol Cox', 38, 'Female', 72, 89, 0, 0.1458, 'low', '2025-12-25 09:24:23'),
(235, NULL, 'Kenneth Martinez', 27, 'Male', 77, 85, 1, 0.1482, 'low', '2026-01-19 09:24:23'),
(236, NULL, 'Kimberly Collins', 79, 'Female', 82, 80, 0, 0.4948, 'medium', '2026-01-08 09:24:23'),
(237, NULL, 'Frank Lewis', 56, 'Male', 92, 187, 0, 0.4994, 'medium', '2025-12-30 09:24:23'),
(238, NULL, 'Stephen Garcia', 66, 'Female', 87, 143, 0, 0.773, 'high', '2026-01-15 09:24:23'),
(239, NULL, 'Nicole Cruz', 43, 'Male', 64, 99, 1, 0.2445, 'low', '2025-12-21 09:24:23'),
(240, NULL, 'Patricia Phillips', 24, 'Male', 82, 158, 0, 0.3159, 'low', '2025-12-28 09:24:23'),
(241, NULL, 'Joseph Howard', 74, 'Female', 80, 82, 1, 0.5287, 'medium', '2026-01-14 09:24:23'),
(242, NULL, 'Christopher Jackson', 42, 'Female', 60, 97, 0, 0.169, 'low', '2026-01-16 09:24:23'),
(243, NULL, 'Sarah Williams', 49, 'Female', 69, 84, 1, 0.2897, 'low', '2025-12-22 09:24:23'),
(244, NULL, 'Robert Kim', 56, 'Female', 76, 114, 0, 0.2479, 'low', '2026-01-12 09:24:23'),
(245, NULL, 'Samantha Green', 35, 'Male', 59, 88, 1, 0.1164, 'low', '2025-12-31 09:24:23'),
(246, NULL, 'Joseph Rivera', 25, 'Male', 65, 104, 1, 0.0464, 'low', '2026-01-12 09:24:23'),
(247, NULL, 'Catherine Edwards', 66, 'Male', 65, 93, 0, 0.3788, 'low', '2026-01-04 09:24:23'),
(248, NULL, 'Charles Wilson', 78, 'Female', 92, 207, 0, 0.95, 'high', '2026-01-13 09:24:23'),
(249, NULL, 'Sharon Reed', 24, 'Female', 66, 88, 0, 0.0665, 'low', '2025-12-28 09:24:23'),
(250, NULL, 'Larry White', 83, 'Male', 85, 161, 0, 0.5261, 'medium', '2026-01-05 09:24:23'),
(251, NULL, 'Emily Scott', 84, 'Male', 78, 113, 0, 0.5078, 'medium', '2026-01-17 09:24:23'),
(252, NULL, 'Margaret Hill', 74, 'Male', 81, 145, 1, 0.6002, 'medium', '2025-12-27 09:24:23'),
(253, NULL, 'Daniel Kelly', 50, 'Male', 67, 99, 0, 0.2042, 'low', '2026-01-15 09:24:23'),
(254, NULL, 'Elizabeth Flores', 24, 'Female', 58, 85, 0, 0.0828, 'low', '2026-01-02 09:24:23'),
(255, NULL, 'Larry Edwards', 29, 'Male', 78, 250, 0, 0.5747, 'medium', '2025-12-30 09:24:23'),
(256, NULL, 'Melissa Thomas', 80, 'Female', 97, 150, 0, 0.7601, 'high', '2026-01-01 09:24:23'),
(257, NULL, 'Mary Howard', 62, 'Female', 64, 93, 1, 0.3566, 'low', '2025-12-24 09:24:23'),
(258, NULL, 'Margaret Edwards', 53, 'Female', 82, 88, 0, 0.2439, 'low', '2026-01-01 09:24:23'),
(259, NULL, 'Frank Sanchez', 18, 'Male', 56, 120, 1, 0.0097, 'low', '2026-01-02 09:24:23'),
(260, NULL, 'Steven Thompson', 44, 'Female', 75, 101, 0, 0.1713, 'low', '2025-12-20 09:24:23'),
(261, NULL, 'Scott Walker', 60, 'Male', 99, 215, 1, 0.932, 'high', '2025-12-27 09:24:23'),
(262, NULL, 'Daniel Lewis', 58, 'Male', 86, 164, 1, 0.6411, 'medium', '2026-01-12 09:24:23'),
(263, NULL, 'Sarah Roberts', 74, 'Female', 70, 85, 0, 0.422, 'medium', '2026-01-10 09:24:23'),
(264, NULL, 'Margaret Nelson', 23, 'Male', 71, 111, 0, 0.0381, 'low', '2026-01-18 09:24:23'),
(265, NULL, 'Nicholas Evans', 21, 'Male', 72, 211, 1, 0.4602, 'medium', '2026-01-08 09:24:23'),
(266, NULL, 'Thomas Adams', 48, 'Male', 71, 89, 0, 0.1802, 'low', '2026-01-04 09:24:23'),
(267, NULL, 'Linda Kelly', 61, 'Male', 79, 111, 0, 0.3076, 'low', '2026-01-18 09:24:23'),
(268, NULL, 'George Roberts', 85, 'Female', 69, 85, 0, 0.535, 'medium', '2026-01-01 09:24:23'),
(269, NULL, 'Barbara Gomez', 22, 'Male', 82, 173, 0, 0.2637, 'low', '2026-01-10 09:24:23'),
(270, NULL, 'Dorothy Hill', 67, 'Female', 68, 104, 0, 0.3758, 'low', '2025-12-22 09:24:23'),
(271, NULL, 'Sarah Reyes', 32, 'Female', 74, 148, 0, 0.3848, 'low', '2025-12-21 09:24:23'),
(272, NULL, 'Edward Lee', 63, 'Male', 72, 87, 1, 0.3741, 'low', '2025-12-23 09:24:23'),
(273, NULL, 'John Nguyen', 33, 'Female', 61, 99, 0, 0.1005, 'low', '2026-01-12 09:24:23'),
(274, NULL, 'Mark Morris', 79, 'Female', 75, 87, 0, 0.4753, 'medium', '2026-01-02 09:24:23'),
(275, NULL, 'Gary Williams', 74, 'Male', 82, 212, 0, 0.95, 'high', '2025-12-20 09:24:23'),
(276, NULL, 'Charles Smith', 82, 'Female', 83, 110, 0, 0.5163, 'medium', '2026-01-03 09:24:23'),
(277, NULL, 'Catherine Hernandez', 83, 'Female', 84, 89, 0, 0.5123, 'medium', '2026-01-13 09:24:23'),
(278, NULL, 'Frank Robinson', 62, 'Male', 99, 241, 1, 0.6327, 'medium', '2026-01-01 09:24:23'),
(279, NULL, 'Amanda Wright', 82, 'Male', 81, 81, 0, 0.4855, 'medium', '2025-12-22 09:24:23'),
(280, NULL, 'David Stewart', 23, 'Female', 60, 88, 0, 0.0399, 'low', '2025-12-30 09:24:23'),
(281, NULL, 'Amy Kelly', 53, 'Female', 82, 173, 0, 0.2962, 'low', '2026-01-13 09:24:23'),
(282, NULL, 'Frank Hall', 79, 'Male', 96, 149, 0, 0.9357, 'high', '2026-01-12 09:24:23'),
(283, NULL, 'Rebecca Adams', 39, 'Female', 63, 107, 0, 0.1615, 'low', '2025-12-24 09:24:23'),
(284, NULL, 'Charles Diaz', 69, 'Male', 76, 84, 0, 0.395, 'low', '2026-01-13 09:24:23'),
(285, NULL, 'Christine Brown', 52, 'Female', 69, 111, 1, 0.2786, 'low', '2026-01-04 09:24:23'),
(286, NULL, 'Frank Hernandez', 64, 'Male', 71, 102, 1, 0.4013, 'medium', '2026-01-18 09:24:23'),
(287, NULL, 'Raymond Parker', 50, 'Female', 65, 101, 0, 0.2168, 'low', '2025-12-20 09:24:23'),
(288, NULL, 'Emma Clark', 49, 'Male', 91, 197, 0, 0.6248, 'medium', '2025-12-20 09:24:23'),
(289, NULL, 'James Thompson', 78, 'Female', 67, 87, 1, 0.5562, 'medium', '2026-01-06 09:24:23'),
(290, NULL, 'Scott Nelson', 47, 'Female', 93, 225, 0, 0.5762, 'medium', '2026-01-17 09:24:23'),
(291, NULL, 'Christopher Martin', 66, 'Female', 87, 157, 0, 0.6325, 'medium', '2025-12-28 09:24:23'),
(292, NULL, 'Jennifer White', 81, 'Male', 88, 118, 0, 0.4827, 'medium', '2026-01-04 09:24:23'),
(293, NULL, 'Brandon Torres', 80, 'Male', 71, 86, 1, 0.5634, 'medium', '2025-12-20 09:24:23'),
(294, NULL, 'Kathleen Cook', 78, 'Male', 98, 184, 0, 0.95, 'high', '2026-01-04 09:24:23'),
(295, NULL, 'Deborah Martinez', 52, 'Male', 67, 81, 0, 0.2181, 'low', '2026-01-07 09:24:23'),
(296, NULL, 'Eric Morales', 28, 'Male', 77, 107, 1, 0.1041, 'low', '2025-12-21 09:24:23'),
(297, NULL, 'Donna Hernandez', 33, 'Female', 75, 113, 1, 0.1465, 'low', '2026-01-10 09:24:23'),
(298, NULL, 'Charles Martinez', 59, 'Male', 67, 101, 0, 0.282, 'low', '2025-12-20 09:24:23'),
(299, NULL, 'Christine Gomez', 80, 'Male', 84, 220, 1, 0.746, 'high', '2025-12-22 09:24:23'),
(300, NULL, 'Thomas Nelson', 49, 'Female', 70, 112, 0, 0.1873, 'low', '2025-12-21 09:24:23'),
(301, NULL, 'Richard Lee', 69, 'Male', 84, 115, 1, 0.5159, 'medium', '2025-12-24 09:24:23'),
(302, NULL, 'Stephen Sanchez', 55, 'Male', 79, 151, 0, 0.6379, 'medium', '2026-01-14 09:24:23'),
(303, NULL, 'Nancy Taylor', 75, 'Female', 78, 85, 1, 0.5402, 'medium', '2026-01-05 09:27:50'),
(304, NULL, 'Lisa Moore', 69, 'Male', 74, 90, 0, 0.4281, 'medium', '2026-01-10 09:27:50'),
(305, NULL, 'Jessica Wilson', 82, 'Female', 70, 99, 0, 0.4681, 'medium', '2026-01-06 09:27:50'),
(306, NULL, 'Kevin Roberts', 74, 'Female', 85, 202, 1, 0.95, 'high', '2026-01-04 09:27:50'),
(307, NULL, 'Rebecca Parker', 54, 'Female', 75, 118, 1, 0.3568, 'low', '2025-12-22 09:27:50'),
(308, NULL, 'Richard Roberts', 31, 'Male', 66, 96, 1, 0.1238, 'low', '2026-01-14 09:27:50'),
(309, NULL, 'Jacob Wilson', 63, 'Male', 83, 238, 0, 0.4512, 'medium', '2026-01-08 09:27:50'),
(310, NULL, 'Nancy Hernandez', 52, 'Female', 87, 181, 1, 0.6642, 'medium', '2026-01-13 09:27:50'),
(311, NULL, 'John Davis', 60, 'Male', 73, 108, 1, 0.3997, 'low', '2025-12-24 09:27:50'),
(312, NULL, 'Stephanie Anderson', 29, 'Male', 57, 101, 0, 0.0994, 'low', '2026-01-05 09:27:50'),
(313, NULL, 'Brian Brown', 51, 'Female', 75, 117, 0, 0.2255, 'low', '2026-01-02 09:27:50'),
(314, NULL, 'Deborah Nelson', 21, 'Female', 73, 94, 0, 0.054, 'low', '2026-01-04 09:27:50'),
(315, NULL, 'Patricia Miller', 36, 'Female', 69, 88, 0, 0.1428, 'low', '2025-12-25 09:27:50'),
(316, NULL, 'Matthew Young', 58, 'Male', 74, 94, 0, 0.2623, 'low', '2025-12-27 09:27:50'),
(317, NULL, 'Jacob Ortiz', 65, 'Female', 81, 213, 1, 0.7661, 'high', '2026-01-05 09:27:50'),
(318, NULL, 'Scott Davis', 28, 'Female', 71, 96, 0, 0.0902, 'low', '2026-01-13 09:27:50'),
(319, NULL, 'Amy Carter', 40, 'Male', 94, 229, 1, 0.5498, 'medium', '2025-12-28 09:27:50'),
(320, NULL, 'Melissa Howard', 28, 'Male', 59, 88, 0, 0.089, 'low', '2026-01-09 09:27:50'),
(321, NULL, 'Rebecca Kim', 79, 'Male', 88, 223, 0, 0.8622, 'high', '2025-12-24 09:27:50'),
(322, NULL, 'Frank Morgan', 36, 'Female', 78, 80, 1, 0.1456, 'low', '2026-01-01 09:27:50'),
(323, NULL, 'Paul Bailey', 49, 'Female', 70, 101, 1, 0.2415, 'low', '2026-01-10 09:27:50'),
(324, NULL, 'Gregory Anderson', 40, 'Male', 62, 81, 0, 0.181, 'low', '2026-01-03 09:27:50'),
(325, NULL, 'Alexander Turner', 26, 'Male', 85, 232, 0, 0.4378, 'medium', '2026-01-13 09:27:50'),
(326, NULL, 'Samuel Bailey', 37, 'Male', 94, 155, 0, 0.1961, 'low', '2026-01-18 09:27:50'),
(327, NULL, 'Elizabeth Howard', 43, 'Male', 83, 193, 1, 0.5453, 'medium', '2026-01-09 09:27:50'),
(328, NULL, 'Amy Mitchell', 21, 'Male', 56, 88, 0, 0.0529, 'low', '2025-12-24 09:27:50'),
(329, NULL, 'Stephanie Young', 67, 'Female', 84, 205, 1, 0.8654, 'high', '2026-01-18 09:27:50'),
(330, NULL, 'Nancy Kim', 25, 'Male', 59, 110, 1, 0.0818, 'low', '2025-12-25 09:27:50'),
(331, NULL, 'Richard Cooper', 21, 'Male', 59, 111, 1, 0.0851, 'low', '2026-01-09 09:27:50'),
(332, NULL, 'Helen Harris', 33, 'Male', 76, 226, 0, 0.326, 'low', '2026-01-02 09:27:50'),
(333, NULL, 'Angela Gomez', 45, 'Male', 86, 205, 1, 0.779, 'high', '2026-01-18 09:27:50'),
(334, NULL, 'Kevin Walker', 35, 'Male', 73, 80, 1, 0.144, 'low', '2025-12-30 09:27:50'),
(335, NULL, 'Margaret Cruz', 43, 'Female', 67, 101, 1, 0.2108, 'low', '2025-12-25 09:27:50'),
(336, NULL, 'Patrick White', 62, 'Female', 81, 107, 0, 0.2953, 'low', '2025-12-29 09:27:50'),
(337, NULL, 'Brenda Gutierrez', 83, 'Female', 69, 103, 0, 0.5059, 'medium', '2025-12-21 09:27:50'),
(338, NULL, 'Timothy Nguyen', 20, 'Female', 83, 154, 1, 0.2761, 'low', '2025-12-25 09:27:50'),
(339, NULL, 'Christine Hill', 83, 'Female', 90, 213, 1, 0.95, 'high', '2026-01-12 09:27:50'),
(340, NULL, 'Benjamin Roberts', 39, 'Female', 78, 95, 1, 0.1679, 'low', '2026-01-06 09:27:50'),
(341, NULL, 'Kevin Gutierrez', 23, 'Female', 59, 103, 0, 0.0487, 'low', '2026-01-19 09:27:50'),
(342, NULL, 'Frank Richardson', 35, 'Female', 61, 112, 0, 0.1084, 'low', '2026-01-16 09:27:50'),
(343, NULL, 'Amy Ortiz', 51, 'Female', 79, 184, 0, 0.5902, 'medium', '2026-01-05 09:27:50'),
(344, NULL, 'Rachel Thomas', 43, 'Male', 95, 241, 0, 0.582, 'medium', '2025-12-27 09:27:50'),
(345, NULL, 'Helen Wright', 68, 'Female', 84, 117, 0, 0.4132, 'medium', '2026-01-01 09:27:50'),
(346, NULL, 'Brenda Reyes', 73, 'Male', 85, 153, 0, 0.7019, 'high', '2025-12-29 09:27:50'),
(347, NULL, 'Ryan Lee', 31, 'Male', 89, 141, 0, 0.2817, 'low', '2026-01-08 09:27:50'),
(348, NULL, 'Brenda King', 37, 'Male', 63, 119, 0, 0.1333, 'low', '2026-01-10 09:27:50'),
(349, NULL, 'Donald Carter', 56, 'Male', 64, 106, 0, 0.2818, 'low', '2026-01-03 09:27:50'),
(350, NULL, 'Betty Perez', 60, 'Female', 84, 93, 0, 0.2344, 'low', '2025-12-26 09:27:50'),
(351, NULL, 'Ashley Wright', 36, 'Male', 70, 116, 0, 0.1426, 'low', '2026-01-05 09:27:50'),
(352, NULL, 'Ashley Peterson', 18, 'Female', 70, 114, 0, 0.0057, 'low', '2026-01-10 09:27:50'),
(353, NULL, 'Mark Ward', 49, 'Female', 61, 89, 0, 0.2146, 'low', '2026-01-02 09:27:50'),
(354, NULL, 'Debra Adams', 71, 'Male', 79, 120, 1, 0.5373, 'medium', '2026-01-09 09:27:50'),
(355, NULL, 'David Hill', 66, 'Female', 88, 144, 1, 0.5946, 'medium', '2026-01-07 09:27:50'),
(356, NULL, 'Nicholas Morales', 67, 'Female', 80, 211, 0, 0.95, 'high', '2026-01-06 09:27:50'),
(357, NULL, 'Jacob Hall', 63, 'Male', 72, 108, 1, 0.3862, 'low', '2026-01-09 09:27:50'),
(358, NULL, 'Margaret Reed', 62, 'Female', 80, 111, 1, 0.3728, 'low', '2026-01-01 09:27:50'),
(359, NULL, 'Jessica Richardson', 55, 'Female', 80, 100, 0, 0.2612, 'low', '2026-01-03 09:27:50'),
(360, NULL, 'Dorothy Baker', 53, 'Male', 80, 170, 0, 0.4266, 'medium', '2025-12-31 09:27:50'),
(361, NULL, 'Jack Parker', 84, 'Male', 70, 104, 0, 0.522, 'medium', '2026-01-15 09:27:50'),
(362, NULL, 'Stephen Reyes', 78, 'Male', 91, 179, 0, 0.7757, 'high', '2025-12-24 09:27:50'),
(363, NULL, 'Jacob Wilson', 67, 'Male', 85, 103, 0, 0.374, 'low', '2026-01-15 09:27:50'),
(364, NULL, 'Deborah Miller', 49, 'Female', 80, 180, 1, 0.679, 'medium', '2026-01-13 09:27:50'),
(365, NULL, 'Brenda Williams', 29, 'Female', 69, 119, 1, 0.0979, 'low', '2026-01-14 09:27:50'),
(366, NULL, 'Emma Morales', 33, 'Female', 92, 234, 0, 0.4475, 'medium', '2025-12-20 09:27:50'),
(367, NULL, 'Jacob Clark', 60, 'Male', 70, 97, 1, 0.3657, 'low', '2026-01-03 09:27:50'),
(368, NULL, 'Ashley Morris', 62, 'Male', 79, 107, 0, 0.3025, 'low', '2025-12-28 09:27:50'),
(369, NULL, 'Kenneth Torres', 65, 'Male', 78, 94, 0, 0.3201, 'low', '2025-12-20 09:27:50'),
(370, NULL, 'Shirley Collins', 58, 'Female', 65, 113, 0, 0.2795, 'low', '2025-12-25 09:27:50'),
(371, NULL, 'Helen Anderson', 75, 'Male', 84, 94, 1, 0.5706, 'medium', '2026-01-08 09:27:50'),
(372, NULL, 'Lisa Campbell', 77, 'Male', 72, 91, 0, 0.4629, 'medium', '2025-12-21 09:27:50'),
(373, NULL, 'Katherine Murphy', 26, 'Male', 73, 105, 1, 0.0988, 'low', '2026-01-19 09:27:50'),
(374, NULL, 'John Hernandez', 42, 'Male', 83, 237, 0, 0.3739, 'low', '2025-12-22 09:27:50'),
(375, NULL, 'John Campbell', 78, 'Male', 74, 104, 0, 0.4794, 'medium', '2025-12-31 09:27:50'),
(376, NULL, 'Rebecca Sanchez', 63, 'Female', 96, 242, 0, 0.8739, 'high', '2026-01-09 09:27:50'),
(377, NULL, 'Cynthia Lopez', 18, 'Male', 75, 101, 0, 0.0284, 'low', '2026-01-03 09:27:50'),
(378, NULL, 'James Morris', 47, 'Male', 62, 120, 0, 0.2085, 'low', '2026-01-19 09:27:50'),
(379, NULL, 'Samuel Cook', 47, 'Female', 93, 234, 0, 0.7972, 'high', '2025-12-24 09:27:50'),
(380, NULL, 'Jason Hall', 55, 'Male', 74, 94, 0, 0.2444, 'low', '2026-01-14 09:27:50'),
(381, NULL, 'Mark Clark', 29, 'Female', 76, 151, 0, 0.1697, 'low', '2026-01-05 09:27:50'),
(382, NULL, 'Charles Bailey', 72, 'Female', 70, 85, 0, 0.441, 'medium', '2025-12-26 09:27:50'),
(383, NULL, 'Jonathan Sanchez', 50, 'Male', 64, 84, 0, 0.2184, 'low', '2025-12-28 09:27:50'),
(384, NULL, 'Joseph Allen', 65, 'Female', 82, 228, 0, 0.8689, 'high', '2026-01-14 09:27:50'),
(385, NULL, 'Barbara Cooper', 32, 'Female', 86, 140, 0, 0.5545, 'medium', '2025-12-28 09:27:50'),
(386, NULL, 'Amy Williams', 71, 'Female', 75, 99, 1, 0.5199, 'medium', '2026-01-02 09:27:50'),
(387, NULL, 'Thomas Murphy', 38, 'Male', 90, 241, 0, 0.4876, 'medium', '2025-12-28 09:27:50'),
(388, NULL, 'Jack Peterson', 53, 'Male', 77, 245, 1, 0.6812, 'medium', '2026-01-13 09:27:50'),
(389, NULL, 'James Kelly', 22, 'Female', 58, 92, 0, 0.0218, 'low', '2026-01-02 09:27:50'),
(390, NULL, 'Paul Scott', 65, 'Female', 95, 213, 1, 0.95, 'high', '2026-01-13 09:27:50'),
(391, NULL, 'Christopher Walker', 31, 'Male', 85, 226, 0, 0.6571, 'medium', '2025-12-26 09:27:50'),
(392, NULL, 'Betty Gonzalez', 28, 'Female', 88, 172, 0, 0.3127, 'low', '2026-01-14 09:27:50'),
(393, NULL, 'Michelle Lee', 50, 'Female', 92, 212, 0, 0.5897, 'medium', '2026-01-04 09:27:50'),
(394, NULL, 'Larry Lewis', 67, 'Male', 92, 183, 1, 0.7111, 'high', '2026-01-09 09:27:50'),
(395, NULL, 'Frank Gutierrez', 46, 'Male', 85, 181, 0, 0.584, 'medium', '2026-01-08 09:27:50'),
(396, NULL, 'Betty Cooper', 22, 'Male', 62, 81, 1, 0.0934, 'low', '2026-01-04 09:27:50'),
(397, NULL, 'Betty Campbell', 85, 'Male', 79, 97, 0, 0.5082, 'medium', '2025-12-23 09:27:50'),
(398, NULL, 'Cynthia Lee', 77, 'Male', 100, 170, 0, 0.8575, 'high', '2026-01-11 09:27:50'),
(399, NULL, 'Stephen Allen', 34, 'Male', 86, 189, 0, 0.337, 'low', '2026-01-06 09:27:50'),
(400, NULL, 'Steven Collins', 64, 'Female', 97, 141, 0, 0.5231, 'medium', '2025-12-25 09:27:50'),
(401, NULL, 'Mark Perez', 64, 'Male', 79, 117, 0, 0.284, 'low', '2026-01-05 09:27:50'),
(402, NULL, 'Margaret Cooper', 82, 'Female', 102, 187, 0, 0.95, 'high', '2025-12-26 09:27:50'),
(403, 4, 'Juan Dela Cruz', 65, 'F', 95, 140, 2, 0.27, 'Low', '2026-01-20 00:19:05'),
(404, 4, 'Juan Dela Cruz', 65, 'M', 95, 140.5, 2, 0.37, 'Medium', '2026-01-21 02:08:53'),
(405, 4, 'Juan Dela Cruz', 50, 'F', 95, 140.5, 1, 0.1, 'Low', '2026-01-21 04:48:47');

-- --------------------------------------------------------

--
-- Stand-in structure for view `recent_disease_assessments`
-- (See below for the actual view)
--
CREATE TABLE `recent_disease_assessments` (
`id` int(11)
,`assessed_by` varchar(100)
,`age` int(11)
,`gender` varchar(10)
,`diabetes_level` varchar(20)
,`heart_disease_level` varchar(20)
,`hypertension_level` varchar(20)
,`overall_risk` varchar(20)
,`created_at` timestamp
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `recent_predictions`
-- (See below for the actual view)
--
CREATE TABLE `recent_predictions` (
`id` int(11)
,`patient_name` varchar(100)
,`age` int(11)
,`gender` varchar(10)
,`prediction` float
,`risk_level` varchar(10)
,`created_at` timestamp
,`clinician_name` varchar(100)
);

-- --------------------------------------------------------

--
-- Structure for view `dashboard_stats`
--
DROP TABLE IF EXISTS `dashboard_stats`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `dashboard_stats`  AS SELECT count(0) AS `total_predictions`, count(distinct cast(`patient_requests`.`created_at` as date)) AS `active_days`, avg(`patient_requests`.`prediction`) AS `avg_prediction_score`, sum(case when `patient_requests`.`risk_level` = 'High' then 1 else 0 end) AS `high_risk_count`, sum(case when `patient_requests`.`risk_level` = 'Medium' then 1 else 0 end) AS `medium_risk_count`, sum(case when `patient_requests`.`risk_level` = 'Low' then 1 else 0 end) AS `low_risk_count`, sum(case when `patient_requests`.`gender` = 'M' then 1 else 0 end) AS `male_count`, sum(case when `patient_requests`.`gender` = 'F' then 1 else 0 end) AS `female_count`, avg(`patient_requests`.`age`) AS `avg_patient_age`, max(`patient_requests`.`created_at`) AS `last_prediction_date` FROM `patient_requests` ;

-- --------------------------------------------------------

--
-- Structure for view `disease_risk_statistics`
--
DROP TABLE IF EXISTS `disease_risk_statistics`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `disease_risk_statistics`  AS SELECT count(0) AS `total_assessments`, avg(`disease_risk_assessments`.`diabetes_risk`) AS `avg_diabetes_risk`, sum(case when `disease_risk_assessments`.`diabetes_level` = 'High' then 1 else 0 end) AS `diabetes_high_count`, sum(case when `disease_risk_assessments`.`diabetes_level` = 'Medium' then 1 else 0 end) AS `diabetes_medium_count`, sum(case when `disease_risk_assessments`.`diabetes_level` = 'Low' then 1 else 0 end) AS `diabetes_low_count`, avg(`disease_risk_assessments`.`heart_disease_risk`) AS `avg_heart_disease_risk`, sum(case when `disease_risk_assessments`.`heart_disease_level` = 'High' then 1 else 0 end) AS `heart_disease_high_count`, sum(case when `disease_risk_assessments`.`heart_disease_level` = 'Medium' then 1 else 0 end) AS `heart_disease_medium_count`, sum(case when `disease_risk_assessments`.`heart_disease_level` = 'Low' then 1 else 0 end) AS `heart_disease_low_count`, avg(`disease_risk_assessments`.`hypertension_risk`) AS `avg_hypertension_risk`, sum(case when `disease_risk_assessments`.`hypertension_level` = 'High' then 1 else 0 end) AS `hypertension_high_count`, sum(case when `disease_risk_assessments`.`hypertension_level` = 'Medium' then 1 else 0 end) AS `hypertension_medium_count`, sum(case when `disease_risk_assessments`.`hypertension_level` = 'Low' then 1 else 0 end) AS `hypertension_low_count`, sum(case when `disease_risk_assessments`.`overall_risk` = 'High' then 1 else 0 end) AS `overall_high_count`, sum(case when `disease_risk_assessments`.`overall_risk` = 'Medium' then 1 else 0 end) AS `overall_medium_count`, sum(case when `disease_risk_assessments`.`overall_risk` = 'Low' then 1 else 0 end) AS `overall_low_count`, avg(`disease_risk_assessments`.`age`) AS `avg_age`, avg(`disease_risk_assessments`.`bmi`) AS `avg_bmi` FROM `disease_risk_assessments` ;

-- --------------------------------------------------------

--
-- Structure for view `recent_disease_assessments`
--
DROP TABLE IF EXISTS `recent_disease_assessments`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `recent_disease_assessments`  AS SELECT `disease_risk_assessments`.`id` AS `id`, `disease_risk_assessments`.`assessed_by` AS `assessed_by`, `disease_risk_assessments`.`age` AS `age`, `disease_risk_assessments`.`gender` AS `gender`, `disease_risk_assessments`.`diabetes_level` AS `diabetes_level`, `disease_risk_assessments`.`heart_disease_level` AS `heart_disease_level`, `disease_risk_assessments`.`hypertension_level` AS `hypertension_level`, `disease_risk_assessments`.`overall_risk` AS `overall_risk`, `disease_risk_assessments`.`created_at` AS `created_at` FROM `disease_risk_assessments` ORDER BY `disease_risk_assessments`.`created_at` DESC LIMIT 0, 50 ;

-- --------------------------------------------------------

--
-- Structure for view `recent_predictions`
--
DROP TABLE IF EXISTS `recent_predictions`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `recent_predictions`  AS SELECT `pr`.`id` AS `id`, `pr`.`patient_name` AS `patient_name`, `pr`.`age` AS `age`, `pr`.`gender` AS `gender`, `pr`.`prediction` AS `prediction`, `pr`.`risk_level` AS `risk_level`, `pr`.`created_at` AS `created_at`, `au`.`full_name` AS `clinician_name` FROM (`patient_requests` `pr` left join `admin_users` `au` on(`pr`.`user_id` = `au`.`id`)) ORDER BY `pr`.`created_at` DESC LIMIT 0, 100 ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_sessions`
--
ALTER TABLE `admin_sessions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `session_token` (`session_token`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_session_token` (`session_token`);

--
-- Indexes for table `admin_users`
--
ALTER TABLE `admin_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_username` (`username`),
  ADD KEY `idx_email` (`email`);

--
-- Indexes for table `disease_risk_assessments`
--
ALTER TABLE `disease_risk_assessments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_assessed_by` (`assessed_by`),
  ADD KEY `idx_created_at` (`created_at`),
  ADD KEY `idx_overall_risk` (`overall_risk`),
  ADD KEY `idx_diabetes_level` (`diabetes_level`),
  ADD KEY `idx_heart_disease_level` (`heart_disease_level`),
  ADD KEY `idx_hypertension_level` (`hypertension_level`);

--
-- Indexes for table `patient_requests`
--
ALTER TABLE `patient_requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_sessions`
--
ALTER TABLE `admin_sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `admin_users`
--
ALTER TABLE `admin_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `disease_risk_assessments`
--
ALTER TABLE `disease_risk_assessments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `patient_requests`
--
ALTER TABLE `patient_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=406;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin_sessions`
--
ALTER TABLE `admin_sessions`
  ADD CONSTRAINT `admin_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `admin_users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `patient_requests`
--
ALTER TABLE `patient_requests`
  ADD CONSTRAINT `patient_requests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `admin_users` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
