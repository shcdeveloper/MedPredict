"""Pydantic models for API request/response validation."""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum


class Gender(str, Enum):
    """Gender enum."""
    MALE = "Male"
    FEMALE = "Female"


class SmokingStatus(str, Enum):
    """Smoking status enum."""
    NEVER = "Never"
    FORMER = "Former"
    CURRENT = "Current"


class PatientData(BaseModel):
    """Patient data for prediction."""
    age: int = Field(..., ge=0, le=120, description="Patient age in years")
    gender: Gender = Field(..., description="Patient gender")
    systolic_bp: float = Field(..., ge=70, le=250, description="Systolic blood pressure (mmHg)")
    diastolic_bp: float = Field(..., ge=40, le=150, description="Diastolic blood pressure (mmHg)")
    heart_rate: float = Field(..., ge=40, le=200, description="Heart rate (bpm)")
    temperature: float = Field(..., ge=35, le=42, description="Body temperature (Celsius)")
    glucose: float = Field(..., ge=50, le=400, description="Blood glucose level (mg/dL)")
    cholesterol: float = Field(..., ge=100, le=400, description="Cholesterol level (mg/dL)")
    bmi: float = Field(..., ge=10, le=60, description="Body Mass Index")
    has_diabetes: int = Field(..., ge=0, le=1, description="Has diabetes (0 or 1)")
    has_hypertension: int = Field(..., ge=0, le=1, description="Has hypertension (0 or 1)")
    smoking_status: SmokingStatus = Field(..., description="Smoking status")
    previous_admissions: int = Field(..., ge=0, description="Number of previous hospital admissions")
    
    class Config:
        schema_extra = {
            "example": {
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
        }


class DiseaseRisk(BaseModel):
    """Disease risk assessment."""
    risk_level: str = Field(..., description="Risk level (High or Low)")
    probability: float = Field(..., ge=0, le=1, description="Risk probability")


class AdmissionPrediction(BaseModel):
    """Admission prediction response."""
    admission_required: bool = Field(..., description="Whether admission is required")
    admission_probability: float = Field(..., ge=0, le=1, description="Probability of admission")
    risk_category: str = Field(..., description="Risk category (Low, Medium, High)")


class DiseaseRiskAssessment(BaseModel):
    """Multi-disease risk assessment response."""
    cardiovascular_risk: DiseaseRisk
    respiratory_risk: DiseaseRisk
    metabolic_risk: DiseaseRisk


class PredictionResponse(BaseModel):
    """Complete prediction response."""
    admission_prediction: AdmissionPrediction
    disease_risk_assessment: DiseaseRiskAssessment
    recommendations: List[str] = Field(..., description="Clinical recommendations")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    models_loaded: bool
    version: str
