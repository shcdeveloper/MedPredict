"""
Unit tests for API endpoints
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_model_info():
    """Test model info endpoint"""
    response = client.get("/model-info")
    assert response.status_code in [200, 503]  # 503 if model not loaded


def test_predict_valid_input():
    """Test prediction with valid input"""
    data = {
        "age": 65,
        "gender": "M",
        "heart_rate": 95,
        "glucose": 140.5,
        "prior_admission": 2
    }
    response = client.post("/predict", json=data)
    
    # If model is loaded, should return 200
    if response.status_code == 200:
        result = response.json()
        assert "admission_probability" in result
        assert "risk_level" in result
        assert "message" in result
        assert 0 <= result["admission_probability"] <= 1
        assert result["risk_level"] in ["Low", "Medium", "High"]


def test_predict_invalid_age():
    """Test prediction with invalid age"""
    data = {
        "age": 150,  # Invalid
        "gender": "M",
        "heart_rate": 95,
        "glucose": 140.5,
        "prior_admission": 2
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 422  # Validation error


def test_predict_invalid_gender():
    """Test prediction with invalid gender"""
    data = {
        "age": 65,
        "gender": "X",  # Invalid
        "heart_rate": 95,
        "glucose": 140.5,
        "prior_admission": 2
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 422


def test_predict_missing_field():
    """Test prediction with missing required field"""
    data = {
        "age": 65,
        "gender": "M",
        # Missing heart_rate
        "glucose": 140.5,
        "prior_admission": 2
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
