"""FastAPI application for MedPredict."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import uvicorn
from pathlib import Path
from typing import List

from src.api.schemas import (
    PatientData, PredictionResponse, AdmissionPrediction,
    DiseaseRiskAssessment, DiseaseRisk, HealthResponse
)
from src.models.admission_predictor import AdmissionPredictor
from src.models.disease_risk_assessor import DiseaseRiskAssessor
from src.utils.logger import setup_logger

logger = setup_logger()

# Initialize FastAPI app
app = FastAPI(
    title="MedPredict API",
    description="Machine learning system for patient admission probability and multi-disease risk assessment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
admission_model = None
disease_model = None
preprocessor = None
models_loaded = False


def load_models(models_dir: str = "models/trained"):
    """Load trained models."""
    global admission_model, disease_model, preprocessor, models_loaded
    
    try:
        models_path = Path(models_dir)
        
        # Load models
        admission_model = AdmissionPredictor.load(f"{models_dir}/admission_predictor.pkl")
        disease_model = DiseaseRiskAssessor.load(f"{models_dir}/disease_risk_assessor.pkl")
        preprocessor = joblib.load(f"{models_dir}/preprocessor.pkl")
        
        models_loaded = True
        logger.info("Models loaded successfully")
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        models_loaded = False


def get_recommendations(admission_prob: float, disease_risks: dict) -> List[str]:
    """Generate clinical recommendations based on predictions."""
    recommendations = []
    
    # Admission recommendations
    if admission_prob > 0.7:
        recommendations.append("Immediate hospital admission recommended")
    elif admission_prob > 0.4:
        recommendations.append("Close monitoring required - consider admission")
    else:
        recommendations.append("Outpatient management appropriate")
    
    # Disease-specific recommendations
    if disease_risks['cardiovascular_risk']['risk_level'] == 'High':
        recommendations.append("Cardiovascular assessment recommended - monitor BP and cholesterol")
    
    if disease_risks['respiratory_risk']['risk_level'] == 'High':
        recommendations.append("Respiratory evaluation needed - consider pulmonary function tests")
    
    if disease_risks['metabolic_risk']['risk_level'] == 'High':
        recommendations.append("Metabolic assessment required - check glucose and lipid panels")
    
    # General recommendations
    high_risks = sum(1 for risk in disease_risks.values() if risk['risk_level'] == 'High')
    if high_risks >= 2:
        recommendations.append("Multi-system evaluation recommended due to multiple high-risk factors")
    
    return recommendations


@app.on_event("startup")
async def startup_event():
    """Load models on startup."""
    logger.info("Starting MedPredict API")
    load_models()


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint."""
    return {
        "status": "healthy",
        "models_loaded": models_loaded,
        "version": "1.0.0"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy" if models_loaded else "unhealthy",
        "models_loaded": models_loaded,
        "version": "1.0.0"
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(patient_data: PatientData):
    """
    Make predictions for patient admission and disease risks.
    
    Args:
        patient_data: Patient clinical data
    
    Returns:
        Prediction response with admission probability and disease risks
    """
    if not models_loaded:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # Convert patient data to DataFrame
        patient_dict = patient_data.dict()
        df = pd.DataFrame([patient_dict])
        
        # Preprocess data
        X = preprocessor.transform(df)
        
        # Get admission prediction
        admission_prob = float(admission_model.predict_proba(X)[0])
        admission_required = bool(admission_model.predict(X)[0])
        
        # Determine risk category
        if admission_prob >= 0.7:
            risk_category = "High"
        elif admission_prob >= 0.4:
            risk_category = "Medium"
        else:
            risk_category = "Low"
        
        # Get disease risk assessment
        disease_predictions = disease_model.predict_dict(X)[0]
        
        # Generate recommendations
        recommendations = get_recommendations(admission_prob, disease_predictions)
        
        # Build response
        response = PredictionResponse(
            admission_prediction=AdmissionPrediction(
                admission_required=admission_required,
                admission_probability=admission_prob,
                risk_category=risk_category
            ),
            disease_risk_assessment=DiseaseRiskAssessment(
                cardiovascular_risk=DiseaseRisk(**disease_predictions['cardiovascular_risk']),
                respiratory_risk=DiseaseRisk(**disease_predictions['respiratory_risk']),
                metabolic_risk=DiseaseRisk(**disease_predictions['metabolic_risk'])
            ),
            recommendations=recommendations
        )
        
        logger.info(f"Prediction made - Admission prob: {admission_prob:.3f}, Risk: {risk_category}")
        
        return response
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/reload-models")
async def reload_models():
    """Reload models from disk."""
    try:
        load_models()
        return {"status": "success", "message": "Models reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reloading models: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
