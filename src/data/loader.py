"""Data generation utilities for MedPredict (for demonstration)."""
import pandas as pd
import numpy as np
from typing import Tuple


def generate_synthetic_patient_data(n_samples: int = 1000, random_state: int = 42) -> pd.DataFrame:
    """
    Generate synthetic patient data for demonstration.
    In production, this would be replaced with real patient data.
    """
    np.random.seed(random_state)
    
    # Patient demographics
    age = np.random.normal(55, 15, n_samples).clip(18, 95).astype(int)
    gender = np.random.choice(['Male', 'Female'], n_samples)
    
    # Vital signs
    systolic_bp = np.random.normal(130, 20, n_samples).clip(90, 200)
    diastolic_bp = np.random.normal(85, 15, n_samples).clip(60, 130)
    heart_rate = np.random.normal(75, 12, n_samples).clip(50, 120)
    temperature = np.random.normal(37.0, 0.8, n_samples).clip(35, 40)
    
    # Lab values
    glucose = np.random.normal(110, 30, n_samples).clip(70, 300)
    cholesterol = np.random.normal(200, 40, n_samples).clip(120, 350)
    bmi = np.random.normal(27, 5, n_samples).clip(15, 50)
    
    # Medical history
    has_diabetes = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    has_hypertension = np.random.choice([0, 1], n_samples, p=[0.6, 0.4])
    smoking_status = np.random.choice(['Never', 'Former', 'Current'], n_samples, p=[0.5, 0.3, 0.2])
    
    # Previous admissions
    previous_admissions = np.random.poisson(1.5, n_samples).clip(0, 10)
    
    # Create DataFrame
    df = pd.DataFrame({
        'age': age,
        'gender': gender,
        'systolic_bp': systolic_bp,
        'diastolic_bp': diastolic_bp,
        'heart_rate': heart_rate,
        'temperature': temperature,
        'glucose': glucose,
        'cholesterol': cholesterol,
        'bmi': bmi,
        'has_diabetes': has_diabetes,
        'has_hypertension': has_hypertension,
        'smoking_status': smoking_status,
        'previous_admissions': previous_admissions
    })
    
    # Generate target: admission probability (based on risk factors)
    risk_score = (
        (age > 65) * 0.3 +
        (systolic_bp > 140) * 0.2 +
        (glucose > 140) * 0.2 +
        (bmi > 30) * 0.15 +
        has_diabetes * 0.15 +
        has_hypertension * 0.1 +
        (previous_admissions > 2) * 0.2 +
        np.random.normal(0, 0.1, n_samples)
    )
    df['admission_required'] = (risk_score > 0.5).astype(int)
    
    # Generate multi-disease risk (cardiovascular, respiratory, metabolic)
    df['cardiovascular_risk'] = (
        ((systolic_bp > 140) | (cholesterol > 240) | has_hypertension) * 1.0
    ).astype(int)
    
    df['respiratory_risk'] = (
        ((smoking_status == 'Current') | (age > 60)) * np.random.uniform(0, 1, n_samples) > 0.5
    ).astype(int)
    
    df['metabolic_risk'] = (
        ((glucose > 126) | (bmi > 30) | has_diabetes) * 1.0
    ).astype(int)
    
    return df


def load_patient_data(filepath: str = None) -> pd.DataFrame:
    """
    Load patient data from file or generate synthetic data.
    
    Args:
        filepath: Path to CSV file with patient data. If None, generates synthetic data.
    
    Returns:
        DataFrame with patient data
    """
    if filepath and pd.io.common.file_exists(filepath):
        return pd.read_csv(filepath)
    else:
        # Generate synthetic data for demonstration
        return generate_synthetic_patient_data()
