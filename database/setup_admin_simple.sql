-- Simple Admin Setup for Healthcare Admission System
-- Run this in phpMyAdmin after running setup.sql

USE healthcare_admission;

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS admin_sessions;
DROP TABLE IF EXISTS admin_users;

-- Create admin users table
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role ENUM('doctor', 'clinician', 'admin') DEFAULT 'clinician',
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create sessions table
CREATE TABLE admin_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_token VARCHAR(64) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE CASCADE,
    INDEX idx_session_token (session_token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Add user_id column to patient_requests if it doesn't exist
ALTER TABLE patient_requests 
ADD COLUMN IF NOT EXISTS user_id INT NULL AFTER id,
ADD COLUMN IF NOT EXISTS patient_name VARCHAR(100) NULL AFTER user_id;

-- Add foreign key if it doesn't exist
-- Note: This might fail if the constraint already exists, which is OK
SET @sql = 'ALTER TABLE patient_requests ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE SET NULL';
SET @constraintExists = (SELECT COUNT(*) FROM information_schema.TABLE_CONSTRAINTS 
    WHERE CONSTRAINT_SCHEMA = 'healthcare_admission' 
    AND TABLE_NAME = 'patient_requests' 
    AND CONSTRAINT_NAME = 'fk_user_id');
    
SET @sql = IF(@constraintExists = 0, @sql, 'SELECT 1');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Insert default admin accounts
-- All passwords are: admin123
-- These are pre-hashed with PHP password_hash (bcrypt)
INSERT INTO admin_users (username, password_hash, full_name, email, role) VALUES
('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'System Administrator', 'admin@hospital.com', 'admin'),
('dr.smith', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Dr. John Smith', 'dr.smith@hospital.com', 'doctor'),
('clinician1', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Sarah Johnson', 'sarah.j@hospital.com', 'clinician');

-- Verify the insert
SELECT 'Admin users created successfully!' as status;
SELECT id, username, full_name, email, role, is_active FROM admin_users;

-- Show table structures
SELECT 'Database tables ready!' as message;
