-- Add Disease Risk Assessment Table
-- Date: 2026-01-19
-- This script adds a new table to store disease risk assessment results

USE healthcare_admission;

-- Create disease_risk_assessments table
CREATE TABLE IF NOT EXISTS disease_risk_assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- User Information
    assessed_by VARCHAR(100) NOT NULL,
    
    -- Demographics
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    bmi FLOAT NOT NULL,
    
    -- Lifestyle Factors
    smoking VARCHAR(20) NOT NULL,
    alcohol VARCHAR(20) NOT NULL,
    exercise VARCHAR(20) NOT NULL,
    
    -- Family History
    family_diabetes TINYINT(1) NOT NULL,
    family_heart_disease TINYINT(1) NOT NULL,
    family_hypertension TINYINT(1) NOT NULL,
    
    -- Vital Signs
    systolic_bp FLOAT NOT NULL,
    diastolic_bp FLOAT NOT NULL,
    heart_rate FLOAT NOT NULL,
    
    -- Lab Results
    glucose FLOAT NOT NULL,
    cholesterol FLOAT NOT NULL,
    hdl FLOAT NOT NULL,
    ldl FLOAT NOT NULL,
    triglycerides FLOAT NOT NULL,
    
    -- Prediction Results
    diabetes_risk FLOAT NOT NULL,
    diabetes_level VARCHAR(20) NOT NULL,
    heart_disease_risk FLOAT NOT NULL,
    heart_disease_level VARCHAR(20) NOT NULL,
    hypertension_risk FLOAT NOT NULL,
    hypertension_level VARCHAR(20) NOT NULL,
    overall_risk VARCHAR(20) NOT NULL,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for better query performance
    INDEX idx_assessed_by (assessed_by),
    INDEX idx_created_at (created_at),
    INDEX idx_overall_risk (overall_risk),
    INDEX idx_diabetes_level (diabetes_level),
    INDEX idx_heart_disease_level (heart_disease_level),
    INDEX idx_hypertension_level (hypertension_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create view for disease statistics
CREATE OR REPLACE VIEW disease_risk_statistics AS
SELECT 
    COUNT(*) as total_assessments,
    -- Diabetes Statistics
    AVG(diabetes_risk) as avg_diabetes_risk,
    SUM(CASE WHEN diabetes_level = 'High' THEN 1 ELSE 0 END) as diabetes_high_count,
    SUM(CASE WHEN diabetes_level = 'Medium' THEN 1 ELSE 0 END) as diabetes_medium_count,
    SUM(CASE WHEN diabetes_level = 'Low' THEN 1 ELSE 0 END) as diabetes_low_count,
    -- Heart Disease Statistics
    AVG(heart_disease_risk) as avg_heart_disease_risk,
    SUM(CASE WHEN heart_disease_level = 'High' THEN 1 ELSE 0 END) as heart_disease_high_count,
    SUM(CASE WHEN heart_disease_level = 'Medium' THEN 1 ELSE 0 END) as heart_disease_medium_count,
    SUM(CASE WHEN heart_disease_level = 'Low' THEN 1 ELSE 0 END) as heart_disease_low_count,
    -- Hypertension Statistics
    AVG(hypertension_risk) as avg_hypertension_risk,
    SUM(CASE WHEN hypertension_level = 'High' THEN 1 ELSE 0 END) as hypertension_high_count,
    SUM(CASE WHEN hypertension_level = 'Medium' THEN 1 ELSE 0 END) as hypertension_medium_count,
    SUM(CASE WHEN hypertension_level = 'Low' THEN 1 ELSE 0 END) as hypertension_low_count,
    -- Overall Risk
    SUM(CASE WHEN overall_risk = 'High' THEN 1 ELSE 0 END) as overall_high_count,
    SUM(CASE WHEN overall_risk = 'Medium' THEN 1 ELSE 0 END) as overall_medium_count,
    SUM(CASE WHEN overall_risk = 'Low' THEN 1 ELSE 0 END) as overall_low_count,
    -- Demographics
    AVG(age) as avg_age,
    AVG(bmi) as avg_bmi
FROM disease_risk_assessments;

-- Create view for recent assessments
CREATE OR REPLACE VIEW recent_disease_assessments AS
SELECT 
    id,
    assessed_by,
    age,
    gender,
    diabetes_level,
    heart_disease_level,
    hypertension_level,
    overall_risk,
    created_at
FROM disease_risk_assessments
ORDER BY created_at DESC
LIMIT 50;

-- Show table structure
DESCRIBE disease_risk_assessments;

-- Success message
SELECT 'Disease risk assessment table created successfully!' as message;
SELECT 'You can now store disease risk predictions in the database.' as info;
