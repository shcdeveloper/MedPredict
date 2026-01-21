-- Healthcare Admission Prediction System - InfinityFree Compatible
-- All VIEWs converted to TABLES, DEFINER and ALGORITHM statements REMOVED

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- Drop existing tables
DROP TABLE IF EXISTS `admin_sessions`;
DROP TABLE IF EXISTS `disease_risk_assessments`;
DROP TABLE IF EXISTS `patient_requests`;
DROP TABLE IF EXISTS `admin_users`;
DROP TABLE IF EXISTS `recent_predictions`;
DROP TABLE IF EXISTS `recent_disease_assessments`;
DROP TABLE IF EXISTS `disease_risk_statistics`;
DROP TABLE IF EXISTS `dashboard_stats`;

-- =====================================================
-- TABLE: admin_users
-- =====================================================
CREATE TABLE `admin_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('doctor','clinician','admin') DEFAULT 'clinician',
  `is_active` tinyint(1) DEFAULT 1,
  `last_login` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_username` (`username`),
  KEY `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `admin_users` VALUES
(4, 'admin', '$2y$10$vZLZPxrtSJzKvY8YOwg4ne5R1PGoFZTHSc6VWrzsjEDYNs2Oew5Ve', 'System Administrator', 'admin@hospital.com', 'admin', 1, '2026-01-21 04:46:54', '2026-01-19 02:17:33'),
(5, 'dr.smith', '$2y$10$g9SroLid6.5.JZRSc6hvPeaNJq7tgFtWxCP34v7DT9MqOw9WLEZEq', 'Dr. John Smith', 'dr.smith@hospital.com', 'doctor', 1, NULL, '2026-01-19 02:17:33'),
(6, 'clinician1', '$2y$10$70Qbdaqtd90f0mZlR6j9NeBTtaPsJaJzwV0Ggtshho1RyosKqQWVq', 'Sarah Johnson', 'sarah.j@hospital.com', 'clinician', 1, '2026-01-19 04:30:45', '2026-01-19 02:17:33');

-- =====================================================
-- TABLE: patient_requests
-- =====================================================
CREATE TABLE `patient_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `age` int(11) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `heart_rate` int(11) DEFAULT NULL,
  `glucose` float DEFAULT NULL,
  `prior_admission` int(11) DEFAULT NULL,
  `prediction` float DEFAULT NULL,
  `risk_level` varchar(10) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_risk_level` (`risk_level`),
  CONSTRAINT `patient_requests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `admin_users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `patient_requests` VALUES
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
(403, 4, 'Juan Dela Cruz', 65, 'F', 95, 140, 2, 0.27, 'Low', '2026-01-20 00:19:05'),
(404, 4, 'Juan Dela Cruz', 65, 'M', 95, 140.5, 2, 0.37, 'Medium', '2026-01-21 02:08:53'),
(405, 4, 'Juan Dela Cruz', 50, 'F', 95, 140.5, 1, 0.1, 'Low', '2026-01-21 04:48:47');

-- =====================================================
-- TABLE: disease_risk_assessments
-- =====================================================
CREATE TABLE `disease_risk_assessments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
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
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_assessed_by` (`assessed_by`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_overall_risk` (`overall_risk`),
  KEY `idx_diabetes_level` (`diabetes_level`),
  KEY `idx_heart_disease_level` (`heart_disease_level`),
  KEY `idx_hypertension_level` (`hypertension_level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `disease_risk_assessments` VALUES
(1, '1', 75, 'Female', 25.4, 'Former', 'None', 'Sedentary', 1, 1, 1, 114, 74, 78, 85, 177, 70, 129, 108, 0.661, 'High', 0.8835, 'High', 0.7566, 'High', 'Critical', '2026-01-05 09:27:50'),
(2, '1', 69, 'Male', 19.7, 'Former', 'None', 'Sedentary', 0, 0, 0, 133, 74, 74, 90, 187, 50, 117, 107, 0.4664, 'Medium', 0.5973, 'Medium', 0.6769, 'High', 'Elevated', '2026-01-10 09:27:50'),
(101, 'admin', 25, 'Male', 50, 'Never', 'Heavy', 'Sedentary', 1, 0, 0, 120, 120, 120, 120, 120, 120, 120, 120, 0.914, 'High', 0.0075, 'Low', 0.9922, 'High', 'Critical', '2026-01-21 03:58:05'),
(102, 'admin', 25, 'Female', 35, 'Never', 'None', 'Light', 1, 1, 1, 120, 120, 120, 120, 120, 120, 120, 129, 0.135, 'Low', 0.0058, 'Low', 0.9981, 'High', 'Elevated', '2026-01-21 05:18:26');

-- =====================================================
-- TABLE: admin_sessions
-- =====================================================
CREATE TABLE `admin_sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `session_token` varchar(64) NOT NULL,
  `expires_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_token` (`session_token`),
  KEY `user_id` (`user_id`),
  KEY `idx_session_token` (`session_token`),
  CONSTRAINT `admin_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `admin_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =====================================================
-- TABLE: dashboard_stats (CONVERTED FROM VIEW)
-- =====================================================
CREATE TABLE `dashboard_stats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `total_predictions` int(11) DEFAULT 0,
  `active_days` int(11) DEFAULT 0,
  `avg_prediction_score` float DEFAULT 0,
  `high_risk_count` int(11) DEFAULT 0,
  `medium_risk_count` int(11) DEFAULT 0,
  `low_risk_count` int(11) DEFAULT 0,
  `male_count` int(11) DEFAULT 0,
  `female_count` int(11) DEFAULT 0,
  `avg_patient_age` float DEFAULT 0,
  `last_prediction_date` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `dashboard_stats` (`id`, `total_predictions`, `active_days`, `avg_prediction_score`, `high_risk_count`, `medium_risk_count`, `low_risk_count`, `male_count`, `female_count`, `avg_patient_age`, `last_prediction_date`) VALUES
(1, 13, 7, 0.32, 2, 1, 10, 6, 7, 52.5, '2026-01-21 04:48:47');

-- =====================================================
-- TABLE: disease_risk_statistics (CONVERTED FROM VIEW)
-- =====================================================
CREATE TABLE `disease_risk_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `total_assessments` int(11) DEFAULT 0,
  `high_diabetes_risk` int(11) DEFAULT 0,
  `medium_diabetes_risk` int(11) DEFAULT 0,
  `low_diabetes_risk` int(11) DEFAULT 0,
  `high_heart_disease_risk` int(11) DEFAULT 0,
  `medium_heart_disease_risk` int(11) DEFAULT 0,
  `low_heart_disease_risk` int(11) DEFAULT 0,
  `high_hypertension_risk` int(11) DEFAULT 0,
  `medium_hypertension_risk` int(11) DEFAULT 0,
  `low_hypertension_risk` int(11) DEFAULT 0,
  `critical_risk_count` int(11) DEFAULT 0,
  `elevated_risk_count` int(11) DEFAULT 0,
  `moderate_risk_count` int(11) DEFAULT 0,
  `avg_age` float DEFAULT 0,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `disease_risk_statistics` (`id`, `total_assessments`, `high_diabetes_risk`, `medium_diabetes_risk`, `low_diabetes_risk`, `high_heart_disease_risk`, `medium_heart_disease_risk`, `low_heart_disease_risk`, `high_hypertension_risk`, `medium_hypertension_risk`, `low_hypertension_risk`, `critical_risk_count`, `elevated_risk_count`, `moderate_risk_count`, `avg_age`) VALUES
(1, 4, 2, 0, 2, 2, 1, 1, 4, 0, 0, 2, 2, 0, 54);

-- =====================================================
-- TABLE: recent_disease_assessments (CONVERTED FROM VIEW)
-- =====================================================
CREATE TABLE `recent_disease_assessments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `disease_id` int(11) NOT NULL,
  `patient_age` int(11) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `diabetes_risk` float DEFAULT NULL,
  `diabetes_level` varchar(20) DEFAULT NULL,
  `heart_disease_risk` float DEFAULT NULL,
  `heart_disease_level` varchar(20) DEFAULT NULL,
  `hypertension_risk` float DEFAULT NULL,
  `hypertension_level` varchar(20) DEFAULT NULL,
  `overall_risk` varchar(20) DEFAULT NULL,
  `assessed_date` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `disease_id` (`disease_id`),
  KEY `idx_assessed_date` (`assessed_date`),
  CONSTRAINT `recent_disease_ibfk_1` FOREIGN KEY (`disease_id`) REFERENCES `disease_risk_assessments` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `recent_disease_assessments` (`id`, `disease_id`, `patient_age`, `gender`, `diabetes_risk`, `diabetes_level`, `heart_disease_risk`, `heart_disease_level`, `hypertension_risk`, `hypertension_level`, `overall_risk`, `assessed_date`) VALUES
(1, 102, 25, 'Female', 0.135, 'Low', 0.0058, 'Low', 0.9981, 'High', 'Elevated', '2026-01-21 05:18:26'),
(2, 101, 25, 'Male', 0.914, 'High', 0.0075, 'Low', 0.9922, 'High', 'Critical', '2026-01-21 03:58:05');

-- =====================================================
-- TABLE: recent_predictions (CONVERTED FROM VIEW)
-- =====================================================
CREATE TABLE `recent_predictions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) NOT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `age` int(11) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `prediction_score` float NOT NULL,
  `risk_level` varchar(10) NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `idx_created_date` (`created_date`),
  CONSTRAINT `recent_predictions_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient_requests` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `recent_predictions` (`id`, `patient_id`, `patient_name`, `age`, `gender`, `prediction_score`, `risk_level`, `created_date`) VALUES
(1, 405, 'Juan Dela Cruz', 50, 'F', 0.1, 'Low', '2026-01-21 04:48:47'),
(2, 404, 'Juan Dela Cruz', 65, 'M', 0.37, 'Medium', '2026-01-21 02:08:53'),
(3, 403, 'Juan Dela Cruz', 65, 'F', 0.27, 'Low', '2026-01-20 00:19:05');

-- =====================================================
-- Set AUTO_INCREMENT values
-- =====================================================
ALTER TABLE `admin_users` AUTO_INCREMENT=7;
ALTER TABLE `patient_requests` AUTO_INCREMENT=406;
ALTER TABLE `disease_risk_assessments` AUTO_INCREMENT=103;
ALTER TABLE `admin_sessions` AUTO_INCREMENT=1;
ALTER TABLE `dashboard_stats` AUTO_INCREMENT=2;
ALTER TABLE `disease_risk_statistics` AUTO_INCREMENT=2;
ALTER TABLE `recent_disease_assessments` AUTO_INCREMENT=3;
ALTER TABLE `recent_predictions` AUTO_INCREMENT=4;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET CHARACTER_SET_CONNECTION=@OLD_COLLATION_CONNECTION */;
