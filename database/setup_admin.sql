-- Add admin users table and enhance database
USE healthcare_admission;

-- Create admin users table
CREATE TABLE IF NOT EXISTS admin_users (
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

-- Create sessions table for login management
CREATE TABLE IF NOT EXISTS admin_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_token VARCHAR(64) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE CASCADE,
    INDEX idx_session_token (session_token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Add user_id to patient_requests to track who made the prediction
ALTER TABLE patient_requests 
ADD COLUMN user_id INT NULL AFTER id,
ADD COLUMN patient_name VARCHAR(100) NULL AFTER user_id,
ADD FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE SET NULL;

-- Insert default admin accounts
-- Password: admin123 (hashed with password_hash)
INSERT INTO admin_users (username, password_hash, full_name, email, role) VALUES
('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'System Administrator', 'admin@hospital.com', 'admin'),
('dr.smith', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Dr. John Smith', 'dr.smith@hospital.com', 'doctor'),
('clinician1', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Sarah Johnson', 'sarah.j@hospital.com', 'clinician');

-- Create view for dashboard statistics
CREATE OR REPLACE VIEW dashboard_stats AS
SELECT 
    COUNT(*) as total_predictions,
    COUNT(DISTINCT DATE(created_at)) as active_days,
    AVG(prediction) as avg_prediction_score,
    SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) as high_risk_count,
    SUM(CASE WHEN risk_level = 'Medium' THEN 1 ELSE 0 END) as medium_risk_count,
    SUM(CASE WHEN risk_level = 'Low' THEN 1 ELSE 0 END) as low_risk_count,
    SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END) as male_count,
    SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) as female_count,
    AVG(age) as avg_patient_age,
    MAX(created_at) as last_prediction_date
FROM patient_requests;

-- Create view for recent predictions
CREATE OR REPLACE VIEW recent_predictions AS
SELECT 
    pr.id,
    pr.patient_name,
    pr.age,
    pr.gender,
    pr.prediction,
    pr.risk_level,
    pr.created_at,
    au.full_name as clinician_name
FROM patient_requests pr
LEFT JOIN admin_users au ON pr.user_id = au.id
ORDER BY pr.created_at DESC
LIMIT 100;

SELECT 'Admin database setup completed successfully!' as message;
SELECT 'Default credentials - Username: admin, Password: admin123' as credentials;
