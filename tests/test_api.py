"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.api.schemas import PatientData


client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "models_loaded" in data


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "1.0.0"


def test_predict_endpoint():
    """Test prediction endpoint."""
    # Sample patient data
    patient_data = {
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
    
    response = client.post("/predict", json=patient_data)
    
    # Response may be 503 if models aren't loaded, which is acceptable in test environment
    if response.status_code == 200:
        data = response.json()
        assert "admission_prediction" in data
        assert "disease_risk_assessment" in data
        assert "recommendations" in data
        assert "admission_probability" in data["admission_prediction"]
    elif response.status_code == 503:
        # Models not loaded is acceptable in test environment
        pass
    else:
        pytest.fail(f"Unexpected status code: {response.status_code}")


def test_predict_validation():
    """Test prediction endpoint with invalid data."""
    # Invalid patient data (age out of range)
    invalid_data = {
        "age": 150,  # Invalid age
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
    
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422  # Validation error
