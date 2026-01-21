# Database Setup Instructions for Disease Risk Assessment

## Overview
You need to add a new table to your database to store disease risk assessment results.

## Required Changes

### 1. New Table: `disease_risk_assessments`
This table will store:
- Patient demographics (age, gender, BMI)
- Lifestyle factors (smoking, alcohol, exercise)
- Family history (diabetes, heart disease, hypertension)
- Vital signs (blood pressure, heart rate)
- Lab results (glucose, cholesterol, HDL, LDL, triglycerides)
- Prediction results for all three diseases
- Overall risk assessment

### 2. New Database Views
- `disease_risk_statistics` - Aggregate statistics for all assessments
- `recent_disease_assessments` - Quick view of the last 50 assessments

## Installation Steps

### Option 1: Using MySQL Command Line
```bash
mysql -u root -p < C:\Users\SHC\Desktop\careApp\database\add_disease_risk_table.sql
```

### Option 2: Using phpMyAdmin
1. Open phpMyAdmin (http://localhost/phpmyadmin)
2. Select the `healthcare_admission` database
3. Click on "SQL" tab
4. Copy and paste the contents of `add_disease_risk_table.sql`
5. Click "Go" to execute

### Option 3: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your local MySQL server
3. File → Open SQL Script → Select `add_disease_risk_table.sql`
4. Execute the script (⚡ icon or Ctrl+Shift+Enter)

## What Gets Created

### Table Structure
```sql
disease_risk_assessments (
    - id (auto increment)
    - assessed_by (username who ran the assessment)
    - Demographics: age, gender, bmi
    - Lifestyle: smoking, alcohol, exercise
    - Family History: family_diabetes, family_heart_disease, family_hypertension
    - Vitals: systolic_bp, diastolic_bp, heart_rate
    - Labs: glucose, cholesterol, hdl, ldl, triglycerides
    - Results: diabetes_risk, diabetes_level, heart_disease_risk, heart_disease_level,
               hypertension_risk, hypertension_level, overall_risk
    - created_at (timestamp)
)
```

### Indexes for Performance
- `assessed_by` - Find assessments by user
- `created_at` - Sort by date
- `overall_risk` - Filter by risk level
- `diabetes_level`, `heart_disease_level`, `hypertension_level` - Filter by disease risk

## What Happens After Setup

Once you run the SQL script:

1. ✅ The `disease_risk_assessments` table will be created
2. ✅ Views for statistics will be available
3. ✅ The disease risk page will automatically save results to the database
4. ✅ You can track assessment history
5. ✅ You can create reports and analytics

## Verify Installation

After running the script, verify with:

```sql
USE healthcare_admission;
SHOW TABLES;  -- Should show disease_risk_assessments
DESCRIBE disease_risk_assessments;  -- Should show table structure
SELECT * FROM disease_risk_statistics;  -- Should show stats (initially 0)
```

## Features Now Available

With the database table:
- **History Tracking**: All disease risk assessments are saved
- **User Attribution**: Know who performed each assessment
- **Trend Analysis**: Track changes over time
- **Statistics**: Aggregate data across all assessments
- **Reporting**: Generate reports by risk level, disease type, etc.

## Future Enhancements (Optional)

You can add:
1. A "History" page to view past assessments
2. Patient profile tracking (multiple assessments per patient)
3. Export functionality (PDF reports, CSV downloads)
4. Email notifications for high-risk assessments
5. Dashboard widgets showing recent assessments

## Troubleshooting

**Error: Table already exists**
- The script uses `CREATE TABLE IF NOT EXISTS`, so it's safe to run multiple times

**Error: Access denied**
- Make sure you're logged in as root or a user with CREATE privileges

**Error: Database not found**
- Make sure `healthcare_admission` database exists
- Run the main `setup.sql` first if needed

## Notes

- The current implementation automatically saves assessments when predictions are made
- Failed database saves won't prevent the prediction from being displayed to the user
- Errors are logged to PHP error log for debugging
- The `assessed_by` field tracks which admin user performed the assessment
