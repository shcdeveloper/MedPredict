"""
Data schemas for API request/response validation
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal, Optional, Dict


class PatientInput(BaseModel):
    """Input schema for patient data"""
    age: int = Field(..., ge=18, le=100, description="Patient age in years")
    gender: Literal['M', 'F'] = Field(..., description="Patient gender (M/F)")
    heart_rate: int = Field(..., ge=40, le=200, description="Heart rate in bpm")
    glucose: float = Field(..., ge=50, le=400, description="Blood glucose level (mg/dL)")
    prior_admission: int = Field(..., ge=0, le=20, description="Number of prior admissions")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 65,
                "gender": "M",
                "heart_rate": 95,
                "glucose": 140.5,
                "prior_admission": 2
            }
        }
    )


class DiseasePredictionInput(BaseModel):
    """Input schema for comprehensive disease risk prediction"""
    age: int = Field(..., ge=18, le=100, description="Patient age")
    gender: Literal['Male', 'Female'] = Field(..., description="Patient gender")
    bmi: float = Field(..., ge=15.0, le=50.0, description="Body Mass Index")
    smoking: Literal['Never', 'Former', 'Current'] = Field(..., description="Smoking status")
    alcohol: Literal['None', 'Moderate', 'Heavy'] = Field(..., description="Alcohol consumption")
    exercise: Literal['Sedentary', 'Light', 'Moderate', 'Active'] = Field(..., description="Exercise level")
    
    family_diabetes: int = Field(..., ge=0, le=1, description="Family history of diabetes (0 or 1)")
    family_heart_disease: int = Field(..., ge=0, le=1, description="Family history of heart disease (0 or 1)")
    family_hypertension: int = Field(..., ge=0, le=1, description="Family history of hypertension (0 or 1)")
    
    systolic_bp: float = Field(..., ge=80, le=220, description="Systolic blood pressure")
    diastolic_bp: float = Field(..., ge=50, le=140, description="Diastolic blood pressure")
    heart_rate: float = Field(..., ge=40, le=150, description="Heart rate (bpm)")
    
    glucose: float = Field(..., ge=50, le=400, description="Fasting glucose (mg/dL)")
    cholesterol: float = Field(..., ge=100, le=400, description="Total cholesterol (mg/dL)")
    hdl: float = Field(..., ge=20, le=120, description="HDL cholesterol (mg/dL)")
    ldl: float = Field(..., ge=40, le=300, description="LDL cholesterol (mg/dL)")
    triglycerides: float = Field(..., ge=30, le=500, description="Triglycerides (mg/dL)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 55,
                "gender": "Male",
                "bmi": 28.5,
                "smoking": "Former",
                "alcohol": "Moderate",
                "exercise": "Light",
                "family_diabetes": 1,
                "family_heart_disease": 0,
                "family_hypertension": 1,
                "systolic_bp": 135,
                "diastolic_bp": 85,
                "heart_rate": 78,
                "glucose": 110,
                "cholesterol": 220,
                "hdl": 45,
                "ldl": 145,
                "triglycerides": 180
            }
        }
    )


class DiseasePredictionOutput(BaseModel):
    """Output schema for disease risk predictions"""
    diabetes_risk: float = Field(..., description="Diabetes risk probability (0-1)")
    diabetes_level: str = Field(..., description="Risk level: Low, Medium, or High")
    
    heart_disease_risk: float = Field(..., description="Heart disease risk probability (0-1)")
    heart_disease_level: str = Field(..., description="Risk level: Low, Medium, or High")
    
    hypertension_risk: float = Field(..., description="Hypertension risk probability (0-1)")
    hypertension_level: str = Field(..., description="Risk level: Low, Medium, or High")
    
    overall_risk: str = Field(..., description="Overall health risk assessment")
    recommendations: list = Field(..., description="Personalized health recommendations")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "diabetes_risk": 0.65,
                "diabetes_level": "High",
                "heart_disease_risk": 0.42,
                "heart_disease_level": "Medium",
                "hypertension_risk": 0.58,
                "hypertension_level": "Medium",
                "overall_risk": "Elevated",
                "recommendations": [
                    "Consult with an endocrinologist for diabetes screening",
                    "Monitor blood pressure regularly",
                    "Increase physical activity to at least 150 minutes per week"
                ]
            }
        }
    )


class PredictionOutput(BaseModel):
    """Output schema for prediction results"""
    admission_probability: float = Field(..., description="Probability of admission (0-1)")
    risk_level: str = Field(..., description="Risk level: Low, Medium, or High")
    message: str = Field(..., description="Interpretation message")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "admission_probability": 0.78,
                "risk_level": "High",
                "message": "High risk of admission. Immediate medical attention recommended."
            }
        }
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    timestamp: str


class ModelInfo(BaseModel):
    """Model information response"""
    model_type: str
    features: list
    trained_at: str
    metrics: dict
