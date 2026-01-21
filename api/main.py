"""
FastAPI Backend for Healthcare Admission Prediction
Provides REST API endpoints for patient admission predictions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import os
from pathlib import Path
import sqlite3
import json

from api.schemas import PatientInput, PredictionOutput, HealthResponse, ModelInfo, DiseasePredictionInput, DiseasePredictionOutput

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Admission Prediction API",
    description="ML-powered API for predicting patient admission probability",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model artifacts
model = None
scaler = None
label_encoder = None
feature_names = None
model_metadata = None

# Disease prediction models
disease_models = {}
disease_scalers = {}
disease_encoders = {}
disease_features = None
disease_metadata = None


def load_model_artifacts():
    """Load trained model and preprocessing objects"""
    global model, scaler, label_encoder, feature_names, model_metadata
    global disease_models, disease_scalers, disease_encoders, disease_features, disease_metadata
    
    model_dir = Path(__file__).parent.parent / 'models'
    
    try:
        print("Loading admission model artifacts...")
        model = joblib.load(model_dir / 'admission_model.pkl')
        scaler = joblib.load(model_dir / 'scaler.pkl')
        label_encoder = joblib.load(model_dir / 'label_encoder.pkl')
        feature_names = joblib.load(model_dir / 'feature_names.pkl')
        model_metadata = joblib.load(model_dir / 'model_metadata.pkl')
        print("✓ Admission model loaded successfully")
    except FileNotFoundError as e:
        print(f"⚠️  Admission model files not found.")
        print(f"   Run: python -m api.train_model")
    
    # Load disease prediction models
    disease_model_dir = model_dir / 'disease_models'
    if disease_model_dir.exists():
        try:
            print("\nLoading disease prediction models...")
            for disease in ['diabetes', 'heart_disease', 'hypertension']:
                disease_models[disease] = joblib.load(disease_model_dir / f'{disease}_model.pkl')
                disease_scalers[disease] = joblib.load(disease_model_dir / f'{disease}_scaler.pkl')
                disease_encoders[disease] = joblib.load(disease_model_dir / f'{disease}_encoders.pkl')
                print(f"✓ {disease.replace('_', ' ').title()} model loaded")
            
            disease_features = joblib.load(disease_model_dir / 'feature_names.pkl')
            disease_metadata = joblib.load(disease_model_dir / 'metadata.pkl')
            print("✓ All disease models loaded successfully")
        except FileNotFoundError as e:
            print(f"⚠️  Disease model files not found.")
            print(f"   Run: python data/generate_disease_data.py")
            print(f"   Then: python api/train_disease_models.py")
    else:
        print("⚠️  Disease models directory not found.")


@app.on_event("startup")
async def startup_event():
    """Load model on application startup"""
    load_model_artifacts()


@app.get("/", tags=["General"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Healthcare Admission Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "model-info": "/model-info",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        message="API is running and model is loaded" if model else "Model not loaded",
        timestamp=datetime.now().isoformat()
    )


@app.get("/model-info", response_model=ModelInfo, tags=["Model"])
async def get_model_info():
    """Get information about the loaded model"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return ModelInfo(
        model_type=type(model).__name__,
        features=feature_names,
        trained_at=model_metadata.get('trained_at', 'Unknown'),
        metrics=model_metadata.get('metrics', {})
    )


@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
async def predict_admission(patient: PatientInput):
    """
    Predict patient admission probability
    
    Takes patient data and returns admission probability and risk level
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Prepare input data
        gender_encoded = label_encoder.transform([patient.gender])[0]
        
        input_data = pd.DataFrame({
            'age': [patient.age],
            'heart_rate': [patient.heart_rate],
            'glucose': [patient.glucose],
            'prior_admission': [patient.prior_admission],
            'gender_encoded': [gender_encoded]
        })
        
        # Reorder columns to match training
        input_data = input_data[feature_names]
        
        # Scale features
        input_scaled = scaler.transform(input_data)
        
        # Predict
        probability = float(model.predict_proba(input_scaled)[0][1])
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
            message = "Low risk of admission. Regular monitoring recommended."
        elif probability < 0.7:
            risk_level = "Medium"
            message = "Medium risk of admission. Close monitoring advised."
        else:
            risk_level = "High"
            message = "High risk of admission. Immediate medical attention recommended."
        
        return PredictionOutput(
            admission_probability=round(probability, 4),
            risk_level=risk_level,
            message=message
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict-batch", tags=["Prediction"])
async def predict_batch(patients: list[PatientInput]):
    """
    Batch prediction for multiple patients
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    for patient in patients:
        try:
            prediction = await predict_admission(patient)
            results.append({
                "input": patient.dict(),
                "prediction": prediction.dict()
            })
        except Exception as e:
            results.append({
                "input": patient.dict(),
                "error": str(e)
            })
    
    return {"predictions": results, "count": len(results)}


@app.post("/predict-disease", response_model=DiseasePredictionOutput, tags=["Disease Prediction"])
async def predict_disease_risk(patient: DiseasePredictionInput):
    """
    Predict disease likelihood (Diabetes, Heart Disease, Hypertension)
    
    Takes comprehensive patient data and returns risk probabilities for multiple diseases
    """
    if not disease_models:
        raise HTTPException(
            status_code=503, 
            detail="Disease prediction models not loaded. Please train models first."
        )
    
    try:
        # Prepare input data
        input_df = pd.DataFrame([{
            'age': patient.age,
            'gender': patient.gender,
            'bmi': patient.bmi,
            'smoking': patient.smoking,
            'alcohol': patient.alcohol,
            'exercise': patient.exercise,
            'family_diabetes': patient.family_diabetes,
            'family_heart_disease': patient.family_heart_disease,
            'family_hypertension': patient.family_hypertension,
            'systolic_bp': patient.systolic_bp,
            'diastolic_bp': patient.diastolic_bp,
            'heart_rate': patient.heart_rate,
            'glucose': patient.glucose,
            'cholesterol': patient.cholesterol,
            'hdl': patient.hdl,
            'ldl': patient.ldl,
            'triglycerides': patient.triglycerides
        }])
        
        # Validate categorical inputs
        categorical_validation = {
            'gender': ['Male', 'Female'],
            'smoking': ['Never', 'Former', 'Current'],
            'alcohol': ['None', 'Moderate', 'Heavy'],
            'exercise': ['Sedentary', 'Light', 'Moderate', 'Active']
        }
        
        for field, valid_values in categorical_validation.items():
            value = input_df[field].iloc[0]
            if value not in valid_values:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid value for {field}: '{value}'. Must be one of: {', '.join(valid_values)}"
                )
        
        results = {}
        recommendations = []
        
        # Predict for each disease
        for disease_name in ['diabetes', 'heart_disease', 'hypertension']:
            # Encode categorical features
            input_encoded = input_df.copy()
            
            # Convert 'None' string to NaN for fields that were trained with NaN
            # This handles the mismatch between form data and training data
            if input_encoded['alcohol'].iloc[0] == 'None':
                input_encoded['alcohol'] = np.nan
            
            encoders = disease_encoders[disease_name]
            
            try:
                for col, encoder in encoders.items():
                    # Skip NaN values - they're handled separately by the model
                    if pd.isna(input_encoded[col].iloc[0]):
                        # Use a default encoding for NaN (usually 0 or -1)
                        input_encoded[col] = -1
                    else:
                        input_encoded[col] = encoder.transform(input_df[col])
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Encoding error for {disease_name} - {col}: {str(e)}"
                )
            
            # Scale features
            scaler = disease_scalers[disease_name]
            input_scaled = scaler.transform(input_encoded[disease_features])
            
            # Predict
            model = disease_models[disease_name]
            probability = float(model.predict_proba(input_scaled)[0][1])
            
            # Determine risk level
            if probability < 0.4:
                risk_level = "Low"
            elif probability < 0.7:
                risk_level = "Medium"
            else:
                risk_level = "High"
            
            results[disease_name] = {
                'risk': round(probability, 4),
                'level': risk_level
            }
            
            # Generate recommendations
            if risk_level == "High":
                if disease_name == "diabetes":
                    recommendations.append("Consult with an endocrinologist for diabetes screening")
                    recommendations.append("Monitor blood glucose levels regularly")
                    if patient.bmi > 30:
                        recommendations.append("Work on weight reduction to lower diabetes risk")
                elif disease_name == "heart_disease":
                    recommendations.append("Schedule a cardiology consultation")
                    recommendations.append("Consider stress test and cardiac imaging")
                    if patient.smoking == "Current":
                        recommendations.append("Strongly advised to quit smoking immediately")
                elif disease_name == "hypertension":
                    recommendations.append("Monitor blood pressure daily")
                    recommendations.append("Reduce sodium intake to less than 2,300mg per day")
            elif risk_level == "Medium":
                if disease_name == "diabetes":
                    recommendations.append("Schedule HbA1c test within 3 months")
                elif disease_name == "heart_disease":
                    recommendations.append("Regular cardiovascular checkups recommended")
                elif disease_name == "hypertension":
                    recommendations.append("Monitor blood pressure weekly")
        
        # General recommendations
        if patient.exercise == "Sedentary":
            recommendations.append("Increase physical activity to at least 150 minutes per week")
        
        if patient.bmi > 30:
            recommendations.append("Aim for gradual weight loss of 1-2 pounds per week")
        
        if patient.cholesterol > 240:
            recommendations.append("Follow a heart-healthy diet low in saturated fats")
        
        # Determine overall risk
        high_risks = sum(1 for r in results.values() if r['level'] == "High")
        medium_risks = sum(1 for r in results.values() if r['level'] == "Medium")
        
        if high_risks >= 2:
            overall_risk = "Critical"
        elif high_risks == 1 or medium_risks >= 2:
            overall_risk = "Elevated"
        elif medium_risks == 1:
            overall_risk = "Moderate"
        else:
            overall_risk = "Low"
        
        # Remove duplicates from recommendations
        recommendations = list(dict.fromkeys(recommendations))
        
        return DiseasePredictionOutput(
            diabetes_risk=results['diabetes']['risk'],
            diabetes_level=results['diabetes']['level'],
            heart_disease_risk=results['heart_disease']['risk'],
            heart_disease_level=results['heart_disease']['level'],
            hypertension_risk=results['hypertension']['risk'],
            hypertension_level=results['hypertension']['level'],
            overall_risk=overall_risk,
            recommendations=recommendations[:8]  # Limit to 8 recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Disease prediction error: {str(e)}")


@app.get("/dashboard/stats", tags=["Dashboard"])
async def get_dashboard_stats():
    """
    Get dashboard statistics
    Returns aggregated statistics for the dashboard
    """
    # For now, return mock/default stats since we don't have a database connection yet
    # TODO: Connect to actual database when available
    
    return {
        "total_predictions": 0,
        "active_days": 0,
        "avg_prediction_score": 0.0,
        "high_risk_count": 0,
        "medium_risk_count": 0,
        "low_risk_count": 0,
        "male_count": 0,
        "female_count": 0,
        "avg_patient_age": 0.0,
        "last_prediction_date": None,
        "models_loaded": {
            "admission_model": model is not None,
            "disease_models": len(disease_models) > 0
        }
    }


@app.get("/dashboard/recent", tags=["Dashboard"])
async def get_recent_predictions():
    """
    Get recent predictions
    Returns the most recent predictions made
    """
    # For now, return empty array since we don't have a database connection yet
    # TODO: Connect to actual database when available
    
    return {
        "predictions": [],
        "count": 0,
        "message": "No predictions stored yet. Database integration pending."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
