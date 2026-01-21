# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Root Endpoint
```http
GET /
```

**Response:**
```json
{
  "message": "Healthcare Admission Prediction API",
  "version": "1.0.0",
  "endpoints": {
    "predict": "/predict",
    "health": "/health",
    "model-info": "/model-info",
    "docs": "/docs"
  }
}
```

### 2. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running and model is loaded",
  "timestamp": "2026-01-19T10:30:00"
}
```

### 3. Model Information
```http
GET /model-info
```

**Response:**
```json
{
  "model_type": "RandomForestClassifier",
  "features": ["age", "heart_rate", "glucose", "prior_admission", "gender_encoded"],
  "trained_at": "2026-01-19T10:00:00",
  "metrics": {
    "Random Forest": {
      "accuracy": 0.85,
      "precision": 0.82,
      "recall": 0.88,
      "f1": 0.85,
      "roc_auc": 0.91
    }
  }
}
```

### 4. Predict Admission (Single)
```http
POST /predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "age": 65,
  "gender": "M",
  "heart_rate": 95,
  "glucose": 140.5,
  "prior_admission": 2
}
```

**Field Validation:**
- `age`: 18-100
- `gender`: "M" or "F"
- `heart_rate`: 40-200 bpm
- `glucose`: 50-400 mg/dL
- `prior_admission`: 0-20

**Response:**
```json
{
  "admission_probability": 0.7845,
  "risk_level": "High",
  "message": "High risk of admission. Immediate medical attention recommended."
}
```

**Risk Levels:**
- **Low**: probability < 0.3
- **Medium**: 0.3 ≤ probability < 0.7
- **High**: probability ≥ 0.7

### 5. Predict Admission (Batch)
```http
POST /predict-batch
Content-Type: application/json
```

**Request Body:**
```json
[
  {
    "age": 65,
    "gender": "M",
    "heart_rate": 95,
    "glucose": 140.5,
    "prior_admission": 2
  },
  {
    "age": 45,
    "gender": "F",
    "heart_rate": 72,
    "glucose": 95.0,
    "prior_admission": 0
  }
]
```

**Response:**
```json
{
  "predictions": [
    {
      "input": { "age": 65, ... },
      "prediction": {
        "admission_probability": 0.7845,
        "risk_level": "High",
        "message": "..."
      }
    },
    {
      "input": { "age": 45, ... },
      "prediction": {
        "admission_probability": 0.2341,
        "risk_level": "Low",
        "message": "..."
      }
    }
  ],
  "count": 2
}
```

## Error Responses

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "ensure this value is less than or equal to 100",
      "type": "value_error.number.not_le"
    }
  ]
}
```

### 503 Service Unavailable
```json
{
  "detail": "Model not loaded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Prediction error: ..."
}
```

## Examples

### Python
```python
import requests

url = "http://localhost:8000/predict"
data = {
    "age": 65,
    "gender": "M",
    "heart_rate": 95,
    "glucose": 140.5,
    "prior_admission": 2
}

response = requests.post(url, json=data)
print(response.json())
```

### cURL
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age":65,"gender":"M","heart_rate":95,"glucose":140.5,"prior_admission":2}'
```

### PowerShell
```powershell
$body = @{
    age = 65
    gender = "M"
    heart_rate = 95
    glucose = 140.5
    prior_admission = 2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $body -ContentType "application/json"
```

## Interactive Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
