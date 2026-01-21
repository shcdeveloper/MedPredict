-- ============================================================
-- InfinityFree Compatible SQL File (NO VIEWS)
-- Healthcare Admission Prediction System
-- Version: 2.0 (InfinityFree Optimized)
-- Generated: January 21, 2026
-- 
-- IMPORTANT NOTES:
-- 1. This file REMOVES all VIEWs (InfinityFree blocks them)
-- 2. PHP files now query patient_requests directly
-- 3. All stand-in VIEW tables have been removed
-- 4. Foreign key constraints are preserved
-- ============================================================

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
-- Password for all accounts: admin123
--

INSERT INTO `admin_users` (`id`, `username`, `password_hash`, `full_name`, `email`, `role`, `is_active`, `last_login`, `created_at`) VALUES
(1, 'admin', '$2y$10$vZLZPxrtSJzKvY8YOwg4ne5R1PGoFZTHSc6VWrzsjEDYNs2Oew5Ve', 'System Administrator', 'admin@hospital.com', 'admin', 1, NULL, '2026-01-19 02:17:33'),
(2, 'dr.smith', '$2y$10$g9SroLid6.5.JZRSc6hvPeaNJq7tgFtWxCP34v7DT9MqOw9WLEZEq', 'Dr. John Smith', 'dr.smith@hospital.com', 'doctor', 1, NULL, '2026-01-19 02:17:33'),
(3, 'clinician1', '$2y$10$70Qbdaqtd90f0mZlR6j9NeBTtaPsJaJzwV0Ggtshho1RyosKqQWVq', 'Sarah Johnson', 'sarah.j@hospital.com', 'clinician', 1, NULL, '2026-01-19 02:17:33');

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

-- --------------------------------------------------------

--
-- Table structure for table `patient_requests`
-- IMPORTANT: This is the MAIN table for admission predictions
-- All dashboard and patient history queries now use THIS table directly
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
-- Sample data for table `patient_requests`
-- You can remove this section if you don't want sample data
--

INSERT INTO `patient_requests` (`id`, `user_id`, `patient_name`, `age`, `gender`, `heart_rate`, `glucose`, `prior_admission`, `prediction`, `risk_level`, `created_at`) VALUES
(1, 1, 'John Doe', 65, 'M', 85, 140, 2, 0.75, 'High', NOW()),
(2, 1, 'Jane Smith', 45, 'F', 72, 95, 0, 0.25, 'Low', NOW()),
(3, 2, 'Bob Johnson', 78, 'M', 95, 160, 3, 0.85, 'High', NOW());

-- --------------------------------------------------------

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
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_created_at` (`created_at`),
  ADD KEY `idx_risk_level` (`risk_level`),
  ADD KEY `idx_gender` (`gender`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `disease_risk_assessments`
--
ALTER TABLE `disease_risk_assessments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `patient_requests`
--
ALTER TABLE `patient_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

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

-- ============================================================
-- END OF INFINITYFREE COMPATIBLE SQL
-- ============================================================
-- 
-- USAGE INSTRUCTIONS:
-- 1. Login to InfinityFree cPanel → phpMyAdmin
-- 2. Select your database (e.g., if0_39888624_healthcare_admission)
-- 3. Click "Import" tab
-- 4. Choose this file: infinityfree_compatible.sql
-- 5. Click "Go" to execute
-- 6. Upload your PHP files via FTP/File Manager
-- 7. Update config/db.php with InfinityFree database credentials
--
-- WHAT WAS CHANGED:
-- ✅ Removed all CREATE VIEW statements
-- ✅ Removed all stand-in VIEW table structures  
-- ✅ Added proper indexes for performance
-- ✅ Kept all core tables (admin_users, patient_requests, disease_risk_assessments, admin_sessions)
-- ✅ PHP files updated to query patient_requests directly (already done)
--
-- CREDENTIALS (Default):
-- Username: admin
-- Password: admin123
--
-- NOTE: The system will now work correctly on InfinityFree!
-- ============================================================
