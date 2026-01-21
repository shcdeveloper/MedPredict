-- Healthcare Admission Prediction Database Setup
-- Date: 2026-01-19

-- Create database
CREATE DATABASE IF NOT EXISTS healthcare_admission;
USE healthcare_admission;

-- Drop table if exists (for clean setup)
DROP TABLE IF EXISTS patient_requests;

-- Create patient_requests table
CREATE TABLE patient_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    heart_rate INT NOT NULL,
    glucose FLOAT NOT NULL,
    prior_admission INT NOT NULL,
    prediction FLOAT NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at),
    INDEX idx_risk_level (risk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample test data
INSERT INTO patient_requests (age, gender, heart_rate, glucose, prior_admission, prediction, risk_level) VALUES
(65, 'M', 95, 140.5, 2, 0.78, 'High'),
(45, 'F', 72, 95.3, 0, 0.23, 'Low'),
(72, 'M', 88, 165.2, 3, 0.85, 'High'),
(38, 'F', 68, 88.5, 0, 0.15, 'Low'),
(55, 'M', 82, 120.8, 1, 0.52, 'Medium'),
(60, 'F', 90, 145.0, 2, 0.68, 'Medium'),
(80, 'M', 98, 180.5, 4, 0.92, 'High'),
(42, 'F', 70, 92.0, 0, 0.18, 'Low'),
(68, 'M', 85, 138.5, 2, 0.72, 'High'),
(50, 'F', 75, 105.0, 1, 0.38, 'Low');

-- Create view for statistics
CREATE OR REPLACE VIEW prediction_statistics AS
SELECT 
    COUNT(*) as total_predictions,
    AVG(prediction) as avg_prediction,
    AVG(age) as avg_age,
    SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) as high_risk_count,
    SUM(CASE WHEN risk_level = 'Medium' THEN 1 ELSE 0 END) as medium_risk_count,
    SUM(CASE WHEN risk_level = 'Low' THEN 1 ELSE 0 END) as low_risk_count,
    SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END) as male_count,
    SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) as female_count
FROM patient_requests;

-- Show table structure
DESCRIBE patient_requests;

-- Show sample data
SELECT * FROM patient_requests LIMIT 5;

-- Show statistics
SELECT * FROM prediction_statistics;

-- Success message
SELECT 'Database setup completed successfully!' as message;
