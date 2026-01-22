# 🏗️ Technical Architecture & Component Documentation

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Component Interactions](#component-interactions)
3. [Technology Stack Deep Dive](#technology-stack-deep-dive)
4. [File Dependencies & Relationships](#file-dependencies--relationships)
5. [Data Models](#data-models)
6. [API Specifications](#api-specifications)
7. [Configuration & Deployment](#configuration--deployment)

---

## System Architecture

### **Layered Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Web Browser (HTML/CSS/JavaScript)             │  │
│  │  Responsive UI with real-time form validation           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                    ↕ HTTP/AJAX (JSON)
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                            │
│  ┌──────────────────────────┐  ┌─────────────────────────────┐ │
│  │  PHP Web Application     │  │  FastAPI Python Backend     │ │
│  │  ├─ Controllers          │  │  ├─ Route Handlers         │ │
│  │  │  - Form Processing    │  │  │  - /predict             │ │
│  │  │  - Session Mgmt       │  │  │  - /predict-disease      │ │
│  │  │  - Authentication     │  │  │  - /health              │ │
│  │  │                       │  │  │                          │ │
│  │  ├─ Views                │  │  ├─ Validation (Pydantic)  │ │
│  │  │  - Dashboard          │  │  │  - Input schemas        │ │
│  │  │  - Patient Pages      │  │  │  - Output schemas       │ │
│  │  │  - Analytics          │  │  │                          │ │
│  │  │                       │  │  ├─ ML Inference           │ │
│  │  ├─ Business Logic       │  │  │  - Model loading        │ │
│  │  │  - Data validation    │  │  │  - Data preprocessing   │ │
│  │  │  - Risk calculation   │  │  │  - Prediction logic     │ │
│  │  │                       │  │  │  - Result post-process  │ │
│  │  ├─ Database Interface   │  │  ├─ Error Handling         │ │
│  │  │  - Query construction │  │  │  - HTTP exceptions      │ │
│  │  │  - Result processing  │  │  │  - Logging              │ │
│  │  └──────────────────────┘  │  └─ CORS Support            │ │
│  │                            │  └─────────────────────────────┘ │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
              ↕ SQL Queries / ↕ joblib Model Loading
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  MySQL Relational Database                              │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │ User Data   │  │ Prediction   │  │ Assessment   │   │  │
│  │  │ Tables:     │  │ Tables:      │  │ Tables:      │   │  │
│  │  │ - admin_    │  │ - patient_   │  │ - disease_   │   │  │
│  │  │   users     │  │   requests   │  │   risk_      │   │  │
│  │  │ - admin_    │  │ - dashboard_ │  │   assessments│   │  │
│  │  │   sessions  │  │   stats      │  │ - disease_   │   │  │
│  │  │             │  │ - recent_    │  │   risk_      │   │  │
│  │  │             │  │   predictions│  │   statistics │   │  │
│  │  └─────────────┘  └──────────────┘  └──────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
              ↕ Load Models / Access Artifacts
┌─────────────────────────────────────────────────────────────────┐
│                      MODEL LAYER                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Trained Machine Learning Models (Python)               │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │  │
│  │  │ Admission   │  │ Disease      │  │ Artifacts      │  │  │
│  │  │ Model:      │  │ Models:      │  │                │  │  │
│  │  │ - RF Model  │  │ - Diabetes   │  │ - Scalers      │  │  │
│  │  │ - 93.78%    │  │ - Heart Dis. │  │ - Encoders     │  │  │
│  │  │   ROC-AUC   │  │ - Hyperten.  │  │ - SHAP         │  │  │
│  │  │             │  │ - 98%+       │  │   Explainers   │  │  │
│  │  │             │  │   Accuracy   │  │ - Feature      │  │  │
│  │  │             │  │              │  │   Names        │  │  │
│  │  └─────────────┘  └──────────────┘  └────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Interactions

### **Data Flow Sequence Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│ ADMISSION PREDICTION FLOW                                        │
└─────────────────────────────────────────────────────────────────┘

User                Browser              PHP App              API              Database
 │                    │                    │                   │                 │
 │─ Fill Form ──────→ │                    │                   │                 │
 │                    │─ AJAX POST ────→  │                   │                 │
 │                    │                   │─ /predict ──────→ │                 │
 │                    │                    │                   │─ Load Model    │
 │                    │                    │                   │ & Artifacts    │
 │                    │                    │ ← Validate Input   │                 │
 │                    │                    │ ← Preprocess Data  │                 │
 │                    │                    │ ← Run Prediction   │                 │
 │                    │ ← JSON Response ── │ ← Get Result ───  │                 │
 │ ← Display Result ─ │                    │                   │                 │
 │                    │                   │─ Save to DB ──────────────────────→  │
 │                    │                   │ ← Confirmation ───────────────────  │
 │                    │                    │                   │                 │

┌─────────────────────────────────────────────────────────────────┐
│ DISEASE RISK ASSESSMENT FLOW                                    │
└─────────────────────────────────────────────────────────────────┘

User              Browser          PHP App              API           Database
 │                  │                 │                │               │
 │─ Fill Form ────→ │                 │                │               │
 │                  │─ AJAX POST ────→│                │               │
 │                  │                │─ /predict-disease│               │
 │                  │                │                ├─ Load Diabetes Model
 │                  │                │                ├─ Load Heart Disease Model
 │                  │                │                ├─ Load Hypertension Model
 │                  │                │ ← 3 Predictions │               │
 │                  │ ← JSON Response─│                │               │
 │ ← Display Result─│                │                │               │
 │                  │                │─ Save Results ──────────────────→
 │                  │                │                │               │
 │                  │                │ ← Success ────────────────────  │
```

### **Component Dependencies**

```
predict.php
├─ config/auth.php (Authentication)
├─ config/db.php (Database connection)
├─ JavaScript AJAX
│  └─ POST to http://127.0.0.1:8000/predict
└─ Database: patient_requests TABLE
   └─ Stores: (age, gender, heart_rate, glucose, prediction, risk_level)

disease_risk.php
├─ config/auth.php
├─ config/db.php
├─ JavaScript AJAX
│  └─ POST to http://127.0.0.1:8000/predict-disease
└─ Database: disease_risk_assessments TABLE
   └─ Stores: (age, gender, bmi, smoking, alcohol, etc., 3 disease risks)

dashboard.php
├─ config/auth.php
├─ config/db.php
└─ Database: dashboard_stats TABLE
   └─ Reads: (total_predictions, active_days, risk_distribution)

patients.php
├─ config/auth.php
├─ config/db.php
└─ Database: patient_requests TABLE
   ├─ Reads: All patient records
   └─ Deletes: Individual records on user request

api/main.py
├─ Load models/ (admission_model.pkl, disease models)
├─ Load artifacts/ (scalers, encoders, SHAP explainers)
├─ Pydantic schemas (validation)
└─ Endpoints:
   ├─ /predict (uses admission_model)
   └─ /predict-disease (uses all 3 disease models)
```

---

## Technology Stack Deep Dive

### **Backend Stack Details**

#### **FastAPI (Web Framework)**
```python
# Why FastAPI?
✓ Automatic API documentation (Swagger UI)
✓ Type hints with Pydantic validation
✓ Fast performance (based on Starlette)
✓ Easy CORS configuration
✓ Built-in error handling

# Key features used:
- @app.post() decorators for endpoints
- FastAPI(title, description, version) for metadata
- HTTPException for error responses
- CORSMiddleware for cross-origin requests
```

#### **scikit-learn (ML Framework)**
```python
# Models used:
- RandomForestClassifier (admission prediction)
- LabelEncoder (categorical features)
- StandardScaler (feature normalization)

# Model pipeline:
1. Load saved model with joblib.load()
2. Encode categorical features (gender, smoking, etc.)
3. Scale numerical features (age, glucose, etc.)
4. model.predict_proba() for probability
5. model.predict() for classification
```

#### **joblib (Model Persistence)**
```python
# Usage:
- joblib.load('path/to/model.pkl')
- model artifacts are binary files
- Preserves object state and structure
- Fast loading compared to pickle
```

### **Frontend Stack Details**

#### **PHP (Server-side)**
```php
// Session-based authentication
$_SESSION['user_id']
$_SESSION['username']

// Database operations
$conn->query()
$result->fetch_assoc()
$conn->prepare() // For security

// Include structure
require_once 'config/auth.php'
require_once 'config/db.php'
```

#### **JavaScript (Client-side)**
```javascript
// AJAX for async API calls
fetch('/api/endpoint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
})

// DOM manipulation
document.getElementById()
document.addEventListener()
element.style.display
```

#### **CSS Framework**
```css
/* Custom design system using CSS variables */
:root {
    --primary: #FF6D1F (Orange)
    --danger: #ef4444 (Red)
    --success: #10b981 (Green)
    --secondary: #64748b (Gray)
}

/* Component library */
.btn, .btn-primary, .btn-outline
.card, .card-header, .card-body
.table-container, .data-table
.sidebar, .sidebar-menu
```

### **Database Stack Details**

#### **MySQL Schema**
```sql
-- Relational design with foreign keys
CREATE TABLE patient_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT FOREIGN KEY REFERENCES admin_users(id),
    patient_name VARCHAR(100),
    prediction FLOAT,
    risk_level ENUM('Low', 'Medium', 'High'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
KEY idx_created_at (created_at)
KEY idx_risk_level (risk_level)
```

---

## File Dependencies & Relationships

### **Dependency Map**

```
webapp/
├── config/
│   ├── auth.php ──────┐
│   └── db.php ────────┤
│                       ↓ (included by all pages)
├── index.php (public, no deps)
├── login.php ──→ auth.php, db.php
├── logout.php ─→ auth.php
├── dashboard.php ──→ auth.php, db.php, patient_requests table
├── predict.php ──→ auth.php, db.php, AJAX→API
├── disease_risk.php ──→ auth.php, db.php, AJAX→API
├── disease_risk_table.php ──→ auth.php, db.php
├── patients.php ──→ auth.php, db.php
├── analytics.php ──→ auth.php, db.php
└── ml_insights.php ──→ auth.php, db.php

api/
├── main.py ──→ 
│   ├── schemas.py (Pydantic validation)
│   ├── models/ (ML artifacts)
│   │   ├── admission_model.pkl
│   │   ├── disease_models/ (3 disease models)
│   │   ├── scaler.pkl
│   │   ├── label_encoder.pkl
│   │   └── shap_explainer.pkl
│   └── External: scikit-learn, joblib, numpy, pandas
│
├── train_model.py ──→
│   ├── data/processed/ (cleaned data)
│   ├── scikit-learn
│   └── Outputs: admission_model.pkl + artifacts
│
├── train_disease_models.py ──→
│   ├── data/processed/
│   ├── scikit-learn
│   └── Outputs: 3 disease models + artifacts
│
└── train_with_explainability.py ──→
    ├── Trained models
    ├── SHAP library
    └── Outputs: SHAP explainers

database/
├── medpredict_INFINITYFREE_CLEAN.sql ──→
│   ├── Creates: 8 tables
│   ├── Inserts: 403+ patient records
│   └── Target: MySQL database
└── medpredict.sql (original with VIEWs)
```

---

## Data Models

### **Core Data Structures**

#### **Admission Prediction Input**
```python
# Pydantic schema (api/schemas.py)
class PatientInput(BaseModel):
    age: int                    # Patient age (18-120)
    gender: str                 # 'M' or 'F'
    heart_rate: int            # BPM (40-200)
    glucose: float             # mg/dL (50-400)
    prior_admission: int       # Count (0-10+)
    
# Example:
{
    "age": 65,
    "gender": "M",
    "heart_rate": 95,
    "glucose": 140,
    "prior_admission": 2
}
```

#### **Disease Risk Assessment Input**
```python
class DiseasePredictionInput(BaseModel):
    age: int
    gender: str
    bmi: float
    smoking: str               # 'Never', 'Former', 'Current'
    alcohol: str               # 'None', 'Light', 'Moderate', 'Heavy'
    exercise: str              # 'Sedentary', 'Light', 'Moderate', 'Heavy'
    family_diabetes: bool
    family_heart_disease: bool
    family_hypertension: bool
    systolic_bp: float
    diastolic_bp: float
    heart_rate: float
    glucose: float
    cholesterol: float
    hdl: float
    ldl: float
    triglycerides: float
```

#### **Prediction Response**
```python
class PredictionOutput(BaseModel):
    prediction: float          # 0.0 to 1.0
    risk_level: str           # 'Low', 'Medium', 'High'
    probability_percentage: float  # 0 to 100
    
# Example:
{
    "prediction": 0.73,
    "risk_level": "High",
    "probability_percentage": 73.2
}
```

#### **Database Record Model**

```sql
-- patient_requests
{
    id: INT PRIMARY KEY,
    user_id: INT FOREIGN KEY,
    patient_name: VARCHAR(100),
    age: INT,
    gender: VARCHAR(10),
    heart_rate: INT,
    glucose: FLOAT,
    prior_admission: INT,
    prediction: FLOAT,
    risk_level: VARCHAR(10),
    created_at: TIMESTAMP
}

-- disease_risk_assessments
{
    id: INT PRIMARY KEY,
    assessed_by: VARCHAR(100),
    age: INT,
    gender: VARCHAR(10),
    bmi: FLOAT,
    smoking: VARCHAR(20),
    alcohol: VARCHAR(20),
    exercise: VARCHAR(20),
    family_diabetes: BOOLEAN,
    family_heart_disease: BOOLEAN,
    family_hypertension: BOOLEAN,
    systolic_bp: FLOAT,
    diastolic_bp: FLOAT,
    heart_rate: FLOAT,
    glucose: FLOAT,
    cholesterol: FLOAT,
    hdl: FLOAT,
    ldl: FLOAT,
    triglycerides: FLOAT,
    diabetes_risk: FLOAT,
    diabetes_level: VARCHAR(20),
    heart_disease_risk: FLOAT,
    heart_disease_level: VARCHAR(20),
    hypertension_risk: FLOAT,
    hypertension_level: VARCHAR(20),
    overall_risk: VARCHAR(20),
    created_at: TIMESTAMP
}
```

---

## API Specifications

### **Endpoint: POST /predict**

**Purpose**: Make admission prediction for a single patient

**Request**:
```json
{
    "age": 65,
    "gender": "M",
    "heart_rate": 95,
    "glucose": 140,
    "prior_admission": 2
}
```

**Response (Success - 200)**:
```json
{
    "prediction": 0.73,
    "risk_level": "High",
    "probability_percentage": 73.2
}
```

**Response (Validation Error - 422)**:
```json
{
    "detail": [
        {
            "loc": ["body", "age"],
            "msg": "ensure this value is greater than 18",
            "type": "value_error"
        }
    ]
}
```

**Response (Server Error - 500)**:
```json
{
    "detail": "Model loading failed"
}
```

### **Endpoint: POST /predict-disease**

**Purpose**: Assess disease risk (3 diseases simultaneously)

**Request**:
```json
{
    "age": 50,
    "gender": "F",
    "bmi": 28.5,
    "smoking": "Never",
    "alcohol": "Moderate",
    "exercise": "Light",
    "family_diabetes": true,
    "family_heart_disease": false,
    "family_hypertension": true,
    "systolic_bp": 130,
    "diastolic_bp": 85,
    "heart_rate": 72,
    "glucose": 115,
    "cholesterol": 220,
    "hdl": 45,
    "ldl": 145,
    "triglycerides": 150
}
```

**Response (Success - 200)**:
```json
{
    "diabetes_risk": 0.45,
    "diabetes_level": "Medium",
    "heart_disease_risk": 0.32,
    "heart_disease_level": "Low",
    "hypertension_risk": 0.68,
    "hypertension_level": "High",
    "overall_risk": "Elevated"
}
```

### **Endpoint: GET /health**

**Purpose**: Health check for monitoring

**Response (Success - 200)**:
```json
{
    "status": "healthy",
    "models_loaded": true,
    "timestamp": "2026-01-22T10:30:00Z"
}
```

### **Endpoint: GET /docs**

**Purpose**: Interactive API documentation (Swagger UI)

**Access**: `http://localhost:8000/docs`

**Features**:
- Try-it-out functionality
- Request/response examples
- Parameter descriptions
- Error code documentation

---

## Configuration & Deployment

### **Development Configuration** (db.php)

```php
<?php
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'healthcare_admission');
?>
```

### **Production Configuration** (db_infinityfree.php)

```php
<?php
define('DB_HOST', 'sql300.infinityfree.com');
define('DB_USER', 'if0_39888624');
define('DB_PASS', 'your_actual_password');
define('DB_NAME', 'if0_39888624_healthcare_admission');
?>
```

### **Environment Setup**

```bash
# Python virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Start API
python -m uvicorn api.main:app --reload --port 8000

# Start PHP app (XAMPP)
# Place files in C:\xampp\htdocs\webapp\
# Visit: http://localhost/webapp/
```

### **Docker Deployment**

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./api:/app/api
    environment:
      - MODEL_PATH=/app/models
      
  database:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=healthcare_admission
    volumes:
      - ./database/medpredict_INFINITYFREE_CLEAN.sql:/docker-entrypoint-initdb.d/init.sql
      
  web:
    image: php:7.4-apache
    ports:
      - "80:80"
    volumes:
      - ./webapp:/var/www/html/webapp
```

---

## Summary

This technical architecture document outlines:

✅ **Multi-layer architecture** separating concerns (presentation, application, data, model)
✅ **Clear component interactions** through APIs and database
✅ **Detailed file dependencies** showing how components relate
✅ **Comprehensive data models** for type safety and validation
✅ **Complete API specifications** for integration
✅ **Configuration management** for different environments

The system is designed for **scalability**, **maintainability**, and **production-readiness**.

---

*Last Updated: January 22, 2026*
*Architecture Version: 1.0*
