# MedPredict API Documentation

## Overview

MedPredict provides a REST API for patient admission prediction and multi-disease risk assessment.

## Base URL

```
http://localhost:8000
```

## Endpoints

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": true,
  "version": "1.0.0"
}
```

### POST /predict

Make predictions for patient admission and disease risks.

**Request Body:**
```json
{
  "age": 65,
  "gender": "Male",
  "systolic_bp": 145,
  "diastolic_bp": 90,
  "heart_rate": 78,
  "temperature": 37.2,
  "glucose": 135,
  "cholesterol": 220,
  "bmi": 28.5,
  "has_diabetes": 1,
  "has_hypertension": 1,
  "smoking_status": "Former",
  "previous_admissions": 2
}
```

**Response:**
```json
{
  "admission_prediction": {
    "admission_required": true,
    "admission_probability": 0.78,
    "risk_category": "High"
  },
  "disease_risk_assessment": {
    "cardiovascular_risk": {
      "risk_level": "High",
      "probability": 0.85
    },
    "respiratory_risk": {
      "risk_level": "Low",
      "probability": 0.32
    },
    "metabolic_risk": {
      "risk_level": "High",
      "probability": 0.71
    }
  },
  "recommendations": [
    "Immediate hospital admission recommended"
  ]
}
```

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
