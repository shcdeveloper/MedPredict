"""Tests for ML models."""
import pytest
import pandas as pd
from src.data.loader import generate_synthetic_patient_data
from src.data.preprocessing import DataPreprocessor, split_data
from src.models.admission_predictor import AdmissionPredictor
from src.models.disease_risk_assessor import DiseaseRiskAssessor


@pytest.fixture
def sample_data():
    """Generate sample data for testing."""
    df = generate_synthetic_patient_data(n_samples=200)
    
    feature_cols = [
        'age', 'gender', 'systolic_bp', 'diastolic_bp', 'heart_rate',
        'temperature', 'glucose', 'cholesterol', 'bmi', 'has_diabetes',
        'has_hypertension', 'smoking_status', 'previous_admissions'
    ]
    
    X = df[feature_cols]
    y_admission = df['admission_required']
    y_diseases = df[['cardiovascular_risk', 'respiratory_risk', 'metabolic_risk']]
    
    # Preprocess
    preprocessor = DataPreprocessor()
    X_processed = preprocessor.fit_transform(X)
    
    # Split
    X_train, X_val, X_test, y_adm_train, y_adm_val, y_adm_test = split_data(
        X_processed, y_admission, test_size=0.2, val_size=0.1
    )
    
    y_dis_train = y_diseases.loc[y_adm_train.index]
    y_dis_test = y_diseases.loc[y_adm_test.index]
    
    return X_train, X_test, y_adm_train, y_adm_test, y_dis_train, y_dis_test


def test_admission_predictor(sample_data):
    """Test admission predictor model."""
    X_train, X_test, y_train, y_test, _, _ = sample_data
    
    # Train model
    model = AdmissionPredictor()
    model.train(X_train, y_train)
    
    assert model.is_trained
    
    # Make predictions
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)
    
    assert len(predictions) == len(X_test)
    assert len(probabilities) == len(X_test)
    assert all(p >= 0 and p <= 1 for p in probabilities)
    
    # Evaluate
    metrics = model.evaluate(X_test, y_test)
    assert 'accuracy' in metrics
    assert 'roc_auc' in metrics
    assert metrics['accuracy'] >= 0 and metrics['accuracy'] <= 1


def test_disease_risk_assessor(sample_data):
    """Test disease risk assessor model."""
    X_train, X_test, _, _, y_train, y_test = sample_data
    
    # Train model
    model = DiseaseRiskAssessor()
    model.train(X_train, y_train)
    
    assert model.is_trained
    
    # Make predictions
    predictions = model.predict(X_test)
    risk_dicts = model.predict_dict(X_test)
    
    assert predictions.shape[0] == len(X_test)
    assert predictions.shape[1] == 3  # 3 disease categories
    assert len(risk_dicts) == len(X_test)
    
    # Check risk dictionary format
    first_risk = risk_dicts[0]
    assert 'cardiovascular_risk' in first_risk
    assert 'respiratory_risk' in first_risk
    assert 'metabolic_risk' in first_risk
    
    # Evaluate
    metrics = model.evaluate(X_test, y_test)
    assert 'hamming_loss' in metrics
    assert 'accuracy' in metrics
