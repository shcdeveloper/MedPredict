# 🏥 Healthcare Admission Prediction System - Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [What This Project Does](#what-this-project-does)
3. [Technology Stack](#technology-stack)
4. [Project Architecture](#project-architecture)
5. [Code Structure & File Purposes](#code-structure--file-purposes)
6. [Pages & Their Contributions](#pages--their-contributions)
7. [Key Components](#key-components)
8. [Data Flow](#data-flow)

---

## 🎯 Project Overview

**Healthcare Admission Prediction System** is an intelligent, production-ready machine learning application designed for healthcare professionals to:

- **Predict patient admission probability** using machine learning (93.78% accuracy)
- **Assess multi-disease risk** for diabetes, heart disease, and hypertension (98%+ accuracy)
- **Analyze patient data** with visual analytics and charts
- **Track patient history** and medical predictions
- **Generate ML insights** with SHAP explainability analysis

### 🎓 Purpose
This system helps hospitals and clinics:
- Make data-driven admission decisions
- Identify high-risk patients early
- Prevent unnecessary hospitalizations
- Improve patient outcomes through predictive medicine

### 👥 Target Users
- Hospital administrators
- Clinicians and nurses
- Doctors and medical specialists
- Healthcare data analysts

---

## 🔍 What This Project Does

### Core Functionalities

#### 1. **Admission Prediction** 
- Predicts whether a patient needs hospital admission
- Uses patient vital signs (heart rate, glucose, age, gender, etc.)
- Returns probability score (0-100%)
- Risk level classification: Low, Medium, High

#### 2. **Multi-Disease Risk Assessment**
- **Diabetes Risk**: Predicts likelihood of diabetes based on BMI, glucose, family history
- **Heart Disease Risk**: Analyzes cardiovascular factors (blood pressure, cholesterol)
- **Hypertension Risk**: Evaluates blood pressure and health indicators

#### 3. **Patient Management**
- View all patient records
- Track admission predictions history
- Delete patient records
- Search and filter patients

#### 4. **Analytics & Insights**
- Dashboard with key statistics
- Patient risk distribution charts
- Disease risk statistics
- Model explainability (feature importance)
- Recent predictions timeline

---

## 🛠️ Technology Stack

### **Backend Technologies**

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.11+ | Programming language for ML and API |
| **FastAPI** | Latest | Modern web framework for REST API |
| **Uvicorn** | Latest | ASGI server for running FastAPI |
| **scikit-learn** | Latest | Machine learning models (Random Forest) |
| **Pandas** | Latest | Data manipulation and analysis |
| **NumPy** | Latest | Numerical computing |
| **Joblib** | Latest | Model serialization/deserialization |
| **Pydantic** | Latest | Data validation using Python type hints |

### **ML/AI Technologies**

| Technology | Purpose |
|-----------|---------|
| **Random Forest** | Classification model for admission prediction |
| **Label Encoder** | Categorical variable encoding |
| **StandardScaler** | Feature normalization |
| **SHAP** | Model explainability (feature importance) |
| **LIME** | Local interpretability for predictions |
| **PDP/ICE** | Partial Dependence & Individual Conditional Expectation plots |

### **Frontend Technologies**

| Technology | Version | Purpose |
|-----------|---------|---------|
| **PHP** | 7.4+ | Server-side rendering |
| **JavaScript (Vanilla)** | ES6+ | Client-side interactivity |
| **HTML5** | Latest | Semantic markup |
| **CSS3** | Latest | Styling and responsive design |
| **Font Awesome** | 6.0 | Icon library |
| **Chart.js** | Latest | Data visualization (optional) |

### **Database Technologies**

| Technology | Version | Purpose |
|-----------|---------|---------|
| **MySQL** | 5.7+ | Relational database |
| **MariaDB** | 10.4+ | MySQL-compatible alternative |

### **DevOps & Infrastructure**

| Technology | Purpose |
|-----------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Multi-container orchestration |
| **Git/GitHub** | Version control |
| **XAMPP** | Local development (Apache + MySQL + PHP) |

### **Hosting Platforms**

| Service | Purpose |
|---------|---------|
| **Render.com** | FastAPI backend hosting |
| **InfinityFree** | PHP frontend + MySQL hosting |
| **GitHub** | Source code repository |

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Layer (Frontend)                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Web Browser (HTML/CSS/JavaScript)                   │  │
│  │  - Dashboard                  - Predict              │  │
│  │  - Patient History            - Disease Risk        │  │
│  │  - Analytics                  - ML Insights         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ (AJAX/HTTP)
┌─────────────────────────────────────────────────────────────┐
│                  Application Layer (PHP + API)               │
│  ┌──────────────────────┐      ┌─────────────────────────┐  │
│  │  PHP Web App         │      │  FastAPI Backend        │  │
│  │  - Controllers       │      │  - /predict endpoint    │  │
│  │  - Views             │      │  - /predict-disease     │  │
│  │  - Authentication    │      │  - Health checks        │  │
│  └──────────────────────┘      └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ (SQL Queries)
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer (Database)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  MySQL Database (if0_39888624_healthcare_admission)  │  │
│  │  ┌──────────┐ ┌────────────┐ ┌─────────────────┐    │  │
│  │  │ Tables   │ │ Views      │ │ Relationships   │    │  │
│  │  │ - Users  │ │ - Stats    │ │ - Foreign Keys  │    │  │
│  │  │ - Patients
│  │  │ - Results│ │ - Recent   │ │ - Constraints   │    │  │
│  │  └──────────┘ └────────────┘ └─────────────────┘    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ (joblib)
┌─────────────────────────────────────────────────────────────┐
│              ML Model Layer (Python Artifacts)               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Trained Models                                        │ │
│  │  - admission_model.pkl (Random Forest)                │ │
│  │  - diabetes_model.pkl                                 │ │
│  │  - heart_disease_model.pkl                            │ │
│  │  - hypertension_model.pkl                             │ │
│  │  - Encoders, Scalers, SHAP Explainer                  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Code Structure & File Purposes

### **Backend API Files** (`api/`)

#### `main.py` (424 lines)
**Purpose**: Core FastAPI application with all endpoints
**Key Responsibilities**:
- Initialize FastAPI app with CORS support
- Load all ML models on startup (4 models + artifacts)
- Expose `/predict` endpoint for admission prediction
- Expose `/predict-disease` endpoint for multi-disease risk
- Expose `/health` endpoint for health checks
- Data validation and error handling
- Model inference logic

**Key Functions**:
```python
load_model_artifacts()      # Load all models from disk
predict_admission()         # Make admission prediction
predict_disease_risk()      # Make disease risk prediction
health_check()              # API health status
```

#### `schemas.py` (Pydantic Models)
**Purpose**: Define data validation schemas
**Models**:
- `PatientInput`: Admission prediction input validation
- `PredictionOutput`: Prediction response format
- `DiseasePredictionInput`: Disease risk assessment input
- `DiseasePredictionOutput`: Disease risk assessment output
- `HealthResponse`: API health status response
- `ModelInfo`: Model metadata information

#### `train_model.py`
**Purpose**: Train admission prediction model
**Features**:
- Load and preprocess raw data
- Train Random Forest classifier
- Optimize hyperparameters
- Save trained model and artifacts
- Generate model metadata

#### `train_disease_models.py`
**Purpose**: Train three disease prediction models
**Models Trained**:
1. Diabetes prediction model
2. Heart disease prediction model
3. Hypertension prediction model
**Features**:
- Individual training pipelines
- Separate encoders and scalers per model
- Model evaluation and validation

#### `train_with_explainability.py`
**Purpose**: Add explainability to trained models
**Features**:
- SHAP explainer training
- Feature importance calculation
- LIME setup for local interpretability
- PDP/ICE plot generation

#### Other Training Files
- `bias_fairness_audit.py`: Demographic bias analysis
- `dimensionality_reduction.py`: Feature reduction analysis
- `feature_selection.py`: Important feature identification
- `pdp_ice_analysis.py`: Partial dependence plots
- `populate_sample_data.py`: Generate sample data for testing

---

### **Frontend Files** (`webapp/`)

#### **Authentication & Configuration**

**`config/auth.php`**
- User authentication and session management
- `login()` function: Validate credentials
- `requireLogin()`: Protect pages
- `getCurrentUser()`: Get current logged-in user
- `logout()`: Clear session

**`config/db.php`**
- Database connection management
- `getDBConnection()`: Create MySQL connection
- `closeDBConnection()`: Properly close connections

**`config/db_infinityfree.php`**
- Production InfinityFree database config template

**`login.php`**
- User login page
- Authentication form
- Error handling and validation
- Session creation

**`logout.php`**
- Clear user session
- Redirect to login

#### **Main Application Pages**

**`index.php`** (Public Landing Page)
- **Purpose**: Public entry point
- **Contribution**: 
  - System overview and introduction
  - Call-to-action to login
  - Feature highlights
  - No authentication required

**`dashboard.php`** (Admin Dashboard)
- **Purpose**: System overview and statistics
- **Features**:
  - Total predictions count
  - Active days/weeks statistics
  - Risk distribution (High/Medium/Low)
  - Gender distribution (Male/Female)
  - Average patient age
  - Recent prediction timeline
  - Quick action buttons
- **Contribution**: 
  - Executive summary of system activity
  - KPI monitoring
  - Navigation hub to other features
- **Database Tables Used**:
  - `dashboard_stats` (aggregated statistics)
  - `patient_requests` (predictions data)

**`predict.php`** (Admission Prediction Form)
- **Purpose**: Collect patient data and make admission predictions
- **Features**:
  - Patient information form (name, age, gender)
  - Vital signs input (heart rate, glucose, blood pressure)
  - Medical history (prior admission count)
  - Form validation
  - Real-time prediction via API
  - Visual risk indicator
- **Contribution**: 
  - Main prediction interface
  - API integration point
  - Real-time inference
- **API Integration**: `POST http://localhost:8000/predict`
- **Database Operation**: INSERT into `patient_requests`

**`disease_risk.php`** (Multi-Disease Risk Assessment)
- **Purpose**: Comprehensive disease risk evaluation
- **Features**:
  - Detailed patient health information
  - Lifestyle factors (smoking, alcohol, exercise)
  - Family history questions
  - Medical measurements (blood pressure, cholesterol, glucose)
  - BMI calculation
  - Risk assessment for 3 diseases
  - Visual risk indicators (Low/Medium/High)
- **Contribution**: 
  - Preventive health assessment
  - Multiple disease predictions
  - Health risk stratification
- **API Integration**: `POST http://localhost:8000/predict-disease`
- **Database Operation**: INSERT into `disease_risk_assessments`

**`disease_risk_table.php`** (Disease Risk History)
- **Purpose**: Display all disease risk assessments
- **Features**:
  - Sortable table of all assessments
  - Filter by risk level, disease, date
  - Patient demographics
  - Risk scores and levels for each disease
  - Overall risk classification
  - Search functionality
- **Contribution**: 
  - Historical disease risk tracking
  - Risk trend analysis
  - Data retrieval and display
- **Database Table Used**: `disease_risk_assessments`

**`analytics.php`** (Analytics Dashboard)
- **Purpose**: Advanced data visualization and analytics
- **Features**:
  - Risk distribution charts (pie/bar)
  - Age group analysis
  - Gender-based statistics
  - Risk trends over time
  - Top risk factors
  - Exportable reports
- **Contribution**: 
  - Data insights and trends
  - Visual representation of patterns
  - Reporting capabilities

**`ml_insights.php`** (Model Explainability)
- **Purpose**: Display ML model insights and feature importance
- **Features**:
  - Feature importance rankings (SHAP values)
  - Model accuracy metrics
  - Model comparison (admission vs disease models)
  - Explainability visualizations
  - PDP/ICE plots
  - LIME explanations
- **Contribution**: 
  - Model transparency
  - Trust building for users
  - Feature impact understanding
  - Decision justification

**`patients.php`** (Patient History & Management)
- **Purpose**: Manage and track all patient records
- **Features**:
  - Complete patient list with pagination
  - Patient demographics (age, gender)
  - Prediction scores
  - Risk levels
  - Associated clinician name
  - View patient details
  - **Delete patient records**
  - Search and filter functionality
- **Contribution**: 
  - Patient data management
  - Record retention/deletion
  - Historical tracking
  - Data governance
- **Database Table Used**: `patient_requests`

---

### **Data Processing Files** (`api/`)

#### `populate_sample_data.py`
**Purpose**: Generate sample patient data for testing
**Output**: Creates 400+ patient records with realistic medical data
**Used for**: 
- Development and testing
- Database population
- Performance benchmarking
- Demo purposes

---

### **Database Files** (`database/`)

#### `medpredict_INFINITYFREE_CLEAN.sql` (13.6 KB)
**Purpose**: Complete production-ready database schema
**Contains**:
- 8 tables (4 original + 4 converted from VIEWs)
- 403+ patient records
- 100+ disease assessments
- User accounts and credentials
- Session management tables
- Statistics and aggregation tables

**Tables**:
1. `admin_users` - System users and clinicians
2. `patient_requests` - Admission predictions
3. `disease_risk_assessments` - Disease risk evaluations
4. `admin_sessions` - Session management
5. `dashboard_stats` - Pre-calculated statistics (was VIEW)
6. `disease_risk_statistics` - Disease statistics (was VIEW)
7. `recent_disease_assessments` - Latest assessments (was VIEW)
8. `recent_predictions` - Recent predictions (was VIEW)

---

## 📄 Pages & Their Contributions

### **User Flow & Page Interactions**

```
┌─ index.php (Public Entry Point)
│   ↓
├─ login.php (Authentication)
│   ↓
├─ dashboard.php (Main Hub)
│   ├─ predict.php (Create Admission Predictions)
│   │   ├─ API Call: /predict
│   │   └─ DB: Save to patient_requests
│   │
│   ├─ disease_risk.php (Create Disease Assessments)
│   │   ├─ API Call: /predict-disease
│   │   └─ DB: Save to disease_risk_assessments
│   │
│   ├─ disease_risk_table.php (View Disease History)
│   │   └─ DB: Query disease_risk_assessments
│   │
│   ├─ patients.php (Patient Management)
│   │   ├─ DB: Query patient_requests
│   │   ├─ View: Show all patients
│   │   └─ Delete: Remove patient record
│   │
│   ├─ analytics.php (Data Visualization)
│   │   ├─ DB: Query all tables
│   │   └─ Display: Charts & trends
│   │
│   ├─ ml_insights.php (Model Explainability)
│   │   ├─ DB: Query model metadata
│   │   └─ Display: Feature importance
│   │
│   └─ logout.php (Exit Session)
```

### **Page Contribution Matrix**

| Page | Purpose | Data Source | Output | User Role |
|------|---------|-------------|--------|-----------|
| **dashboard.php** | System overview | `dashboard_stats` | KPI metrics | Admin/Clinician |
| **predict.php** | Create predictions | Form input | Admission probability | Clinician |
| **disease_risk.php** | Disease assessment | Form input | 3 disease risks | Clinician/Doctor |
| **disease_risk_table.php** | View history | `disease_risk_assessments` | Assessment list | Admin/Clinician |
| **patients.php** | Patient management | `patient_requests` | Patient data | Admin |
| **analytics.php** | Data insights | All tables | Charts/graphs | Admin/Analyst |
| **ml_insights.php** | Model explainability | Model files | Feature importance | Admin/Analyst |
| **login.php** | Authentication | `admin_users` | Session token | Public |
| **index.php** | Public information | Static content | Introduction | Public |

---

## 🔑 Key Components

### **1. Machine Learning Models**

#### **Admission Prediction Model**
- **Type**: Random Forest Classifier
- **Accuracy**: 93.78% ROC-AUC
- **Input Features**: 6 features (age, gender, heart_rate, glucose, prior_admission, etc.)
- **Output**: Probability score (0-1), Risk Level (Low/Medium/High)
- **File**: `models/admission_model.pkl`

#### **Disease Prediction Models** (3 models)
1. **Diabetes Model**
   - Input: BMI, glucose, family_history, smoking, alcohol, exercise
   - Output: Diabetes risk probability

2. **Heart Disease Model**
   - Input: Age, blood pressure, cholesterol, smoking, family_history
   - Output: Heart disease risk probability

3. **Hypertension Model**
   - Input: Blood pressure, age, family_history, exercise, stress
   - Output: Hypertension risk probability

### **2. API Endpoints**

#### **POST /predict**
```json
Request:
{
  "age": 65,
  "gender": "M",
  "heart_rate": 95,
  "glucose": 140,
  "prior_admission": 2
}

Response:
{
  "prediction": 0.73,
  "risk_level": "High",
  "probability_percentage": 73.2
}
```

#### **POST /predict-disease**
```json
Request:
{
  "age": 50,
  "gender": "F",
  "bmi": 28.5,
  "smoking": "Never",
  "alcohol": "Moderate",
  "exercise": "Light",
  "family_diabetes": true,
  "systolic_bp": 130,
  "diastolic_bp": 85,
  "glucose": 115
}

Response:
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

### **3. Database Schema**

#### **Core Tables**
- `admin_users`: User accounts and authentication
- `patient_requests`: Admission prediction records
- `disease_risk_assessments`: Disease risk evaluation records
- `admin_sessions`: Session management

#### **Analytics Tables** (Pre-calculated)
- `dashboard_stats`: Aggregated dashboard metrics
- `disease_risk_statistics`: Disease statistics summary
- `recent_disease_assessments`: Latest assessments
- `recent_predictions`: Latest predictions

---

## 📊 Data Flow

### **Admission Prediction Flow**

```
1. User submits form (predict.php)
   ↓
2. Patient data captured (age, heart_rate, glucose, etc.)
   ↓
3. JavaScript AJAX sends POST to /predict endpoint
   ↓
4. FastAPI receives data
   ↓
5. Data validated (Pydantic schemas)
   ↓
6. Load trained model + scalers + encoders
   ↓
7. Preprocess data (normalization, encoding)
   ↓
8. Run model.predict()
   ↓
9. Return probability score + risk level
   ↓
10. JavaScript receives response
   ↓
11. Display prediction result to user
   ↓
12. Save to database (patient_requests table)
```

### **Disease Risk Assessment Flow**

```
1. User fills disease risk form (disease_risk.php)
   ↓
2. Comprehensive health data collected
   ↓
3. JavaScript AJAX sends to /predict-disease
   ↓
4. FastAPI receives data
   ↓
5. For each disease (diabetes, heart disease, hypertension):
   ├─ Load specific disease model
   ├─ Load specific encoder & scaler
   ├─ Preprocess data
   ├─ Run model.predict()
   └─ Get probability + risk level
   ↓
6. Calculate overall risk level
   ↓
7. Return all three disease risks
   ↓
8. Display results (color-coded by severity)
   ↓
9. Save assessment to database (disease_risk_assessments)
```

---

## 🔄 Deployment Architecture

### **Local Development**
```
XAMPP (Port 80, 3306)
├── PHP Web App: http://localhost/webapp/
└── MySQL Database: localhost:3306
```

### **Production**
```
Render.com (Port 8000)
├── FastAPI Backend: https://medpredict-gkaa.onrender.com
└── Python Models: In container

InfinityFree
├── PHP Web App: patty-portfolio.infinityfree.me
├── MySQL Database: sql300.infinityfree.com
└── Config: Production credentials
```

---

## 📚 Summary

This project is a **comprehensive healthcare intelligence system** combining:

- **Advanced ML Models** (93-98% accuracy) for predictive medicine
- **RESTful API** (FastAPI) for scalable predictions
- **Professional Web Interface** (PHP) for user interaction
- **Production-Ready Infrastructure** (Docker, MySQL, Git)
- **Complete Documentation** for deployment and maintenance

**Key Innovation**: Bridges gap between ML models and clinical practice by providing explainable, accessible predictions for healthcare professionals.

---

*Last Updated: January 22, 2026*
*Project Status: 94% Complete - Production Ready*
