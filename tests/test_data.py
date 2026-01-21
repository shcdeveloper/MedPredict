"""Tests for data preprocessing."""
import pytest
import pandas as pd
import numpy as np
from src.data.preprocessing import DataPreprocessor, split_data
from src.data.loader import generate_synthetic_patient_data


def test_data_preprocessor():
    """Test data preprocessor."""
    # Generate sample data
    df = generate_synthetic_patient_data(n_samples=100)
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Test fit_transform
    X = df.drop(['admission_required', 'cardiovascular_risk', 'respiratory_risk', 'metabolic_risk'], axis=1)
    X_transformed = preprocessor.fit_transform(X)
    
    assert preprocessor.is_fitted
    assert X_transformed.shape[0] == 100
    assert len(preprocessor.feature_names) > 0


def test_split_data():
    """Test data splitting."""
    # Generate sample data
    df = generate_synthetic_patient_data(n_samples=100)
    
    X = df.drop(['admission_required', 'cardiovascular_risk', 'respiratory_risk', 'metabolic_risk'], axis=1)
    y = df['admission_required']
    
    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y, test_size=0.2, val_size=0.1)
    
    # Check sizes
    assert len(X_train) + len(X_val) + len(X_test) == 100
    assert len(X_train) > len(X_val)
    assert len(X_test) == 20


def test_generate_synthetic_data():
    """Test synthetic data generation."""
    df = generate_synthetic_patient_data(n_samples=50)
    
    assert len(df) == 50
    assert 'age' in df.columns
    assert 'admission_required' in df.columns
    assert 'cardiovascular_risk' in df.columns
