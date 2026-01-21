# Model Documentation

## Overview

MedPredict uses two main machine learning models:
1. **Admission Predictor**: XGBoost-based model for hospital admission prediction
2. **Disease Risk Assessor**: Multi-output LightGBM model for disease risk assessment

## Admission Predictor

### Algorithm
XGBoost Classifier

### Features
- Demographics: age, gender
- Vital Signs: systolic_bp, diastolic_bp, heart_rate, temperature
- Lab Values: glucose, cholesterol, bmi
- Medical History: has_diabetes, has_hypertension, smoking_status, previous_admissions

### Hyperparameters
```yaml
n_estimators: 100
max_depth: 6
learning_rate: 0.1
objective: binary:logistic
```

### Output
- Binary prediction (0/1)
- Probability score (0.0-1.0)
- Risk category (Low/Medium/High)

## Disease Risk Assessor

### Algorithm
Multi-output LightGBM Classifier

### Disease Categories
1. Cardiovascular Risk
2. Respiratory Risk
3. Metabolic Risk

### Output
For each disease:
- Risk level (High/Low)
- Probability score (0.0-1.0)

## MLOps Practices

- MLflow experiment tracking
- Model versioning
- Automated training pipelines
- Comprehensive logging
- Data validation
