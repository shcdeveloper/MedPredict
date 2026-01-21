"""
Generate synthetic patient data for disease likelihood prediction
Includes features for: Diabetes, Heart Disease, Hypertension
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

def generate_disease_prediction_data(n_samples=2000):
    """Generate comprehensive patient data for disease prediction"""
    
    print(f"Generating {n_samples} patient records with disease risk data...")
    
    data = []
    
    for i in range(n_samples):
        # Demographics
        age = np.random.randint(25, 85)
        gender = np.random.choice(['Male', 'Female'])
        
        # Lifestyle factors
        bmi = np.random.normal(27, 6)  # BMI with realistic distribution
        bmi = max(15, min(50, bmi))  # Clamp to realistic range
        
        smoking = np.random.choice(['Never', 'Former', 'Current'], p=[0.5, 0.3, 0.2])
        alcohol = np.random.choice(['None', 'Moderate', 'Heavy'], p=[0.4, 0.5, 0.1])
        exercise = np.random.choice(['Sedentary', 'Light', 'Moderate', 'Active'], 
                                    p=[0.3, 0.3, 0.25, 0.15])
        
        # Family history (binary)
        family_diabetes = np.random.choice([0, 1], p=[0.7, 0.3])
        family_heart_disease = np.random.choice([0, 1], p=[0.65, 0.35])
        family_hypertension = np.random.choice([0, 1], p=[0.6, 0.4])
        
        # Vital signs
        systolic_bp = np.random.normal(125, 18)
        systolic_bp = max(90, min(200, systolic_bp))
        
        diastolic_bp = np.random.normal(80, 12)
        diastolic_bp = max(60, min(120, diastolic_bp))
        
        heart_rate = np.random.normal(75, 12)
        heart_rate = max(50, min(120, heart_rate))
        
        # Lab results
        glucose = np.random.normal(100, 25)  # mg/dL
        glucose = max(70, min(300, glucose))
        
        cholesterol = np.random.normal(200, 40)  # mg/dL
        cholesterol = max(120, min(350, cholesterol))
        
        hdl = np.random.normal(50, 15)  # Good cholesterol
        hdl = max(20, min(100, hdl))
        
        ldl = np.random.normal(130, 35)  # Bad cholesterol
        ldl = max(50, min(250, ldl))
        
        triglycerides = np.random.normal(150, 60)
        triglycerides = max(50, min(400, triglycerides))
        
        # Calculate risk scores using medical guidelines
        
        # DIABETES RISK (based on ADA criteria)
        diabetes_risk = 0
        if age > 45: diabetes_risk += 15
        if bmi > 25: diabetes_risk += 10
        if bmi > 30: diabetes_risk += 20
        if family_diabetes: diabetes_risk += 25
        if glucose > 100: diabetes_risk += 15
        if glucose > 125: diabetes_risk += 30
        if exercise == 'Sedentary': diabetes_risk += 10
        if systolic_bp > 140: diabetes_risk += 10
        
        diabetes_likelihood = min(100, diabetes_risk) / 100
        has_diabetes = 1 if diabetes_likelihood > 0.6 else 0
        
        # HEART DISEASE RISK (based on Framingham criteria)
        heart_risk = 0
        if age > 55: heart_risk += 20
        if gender == 'Male': heart_risk += 10
        if smoking == 'Current': heart_risk += 25
        if smoking == 'Former': heart_risk += 10
        if family_heart_disease: heart_risk += 20
        if systolic_bp > 140: heart_risk += 15
        if cholesterol > 240: heart_risk += 20
        if hdl < 40: heart_risk += 15
        if ldl > 160: heart_risk += 15
        if bmi > 30: heart_risk += 10
        if exercise == 'Sedentary': heart_risk += 10
        
        heart_likelihood = min(100, heart_risk) / 100
        has_heart_disease = 1 if heart_likelihood > 0.65 else 0
        
        # HYPERTENSION RISK
        hypertension_risk = 0
        if age > 50: hypertension_risk += 20
        if family_hypertension: hypertension_risk += 25
        if bmi > 25: hypertension_risk += 15
        if bmi > 30: hypertension_risk += 25
        if alcohol == 'Heavy': hypertension_risk += 15
        if exercise == 'Sedentary': hypertension_risk += 10
        if systolic_bp > 130: hypertension_risk += 20
        if diastolic_bp > 85: hypertension_risk += 15
        
        hypertension_likelihood = min(100, hypertension_risk) / 100
        has_hypertension = 1 if hypertension_likelihood > 0.6 else 0
        
        # Original admission prediction (based on overall health)
        admission_score = 0
        if has_diabetes: admission_score += 30
        if has_heart_disease: admission_score += 35
        if has_hypertension: admission_score += 25
        if age > 65: admission_score += 15
        if bmi > 35: admission_score += 10
        
        admission = 1 if (admission_score > 50 or np.random.random() < 0.3) else 0
        
        # Create record
        record = {
            'age': int(age),
            'gender': gender,
            'bmi': round(bmi, 1),
            'smoking': smoking,
            'alcohol': alcohol,
            'exercise': exercise,
            'family_diabetes': family_diabetes,
            'family_heart_disease': family_heart_disease,
            'family_hypertension': family_hypertension,
            'systolic_bp': round(systolic_bp, 1),
            'diastolic_bp': round(diastolic_bp, 1),
            'heart_rate': round(heart_rate, 1),
            'glucose': round(glucose, 1),
            'cholesterol': round(cholesterol, 1),
            'hdl': round(hdl, 1),
            'ldl': round(ldl, 1),
            'triglycerides': round(triglycerides, 1),
            'diabetes_risk': round(diabetes_likelihood, 3),
            'heart_disease_risk': round(heart_likelihood, 3),
            'hypertension_risk': round(hypertension_likelihood, 3),
            'has_diabetes': has_diabetes,
            'has_heart_disease': has_heart_disease,
            'has_hypertension': has_hypertension,
            'admission': admission
        }
        
        data.append(record)
    
    df = pd.DataFrame(data)
    
    # Save dataset
    os.makedirs('data/processed', exist_ok=True)
    output_path = 'data/processed/disease_prediction_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Dataset saved to: {output_path}")
    print(f"\nDataset Summary:")
    print(f"  Total records: {len(df)}")
    print(f"  Diabetes cases: {df['has_diabetes'].sum()} ({df['has_diabetes'].mean()*100:.1f}%)")
    print(f"  Heart disease cases: {df['has_heart_disease'].sum()} ({df['has_heart_disease'].mean()*100:.1f}%)")
    print(f"  Hypertension cases: {df['has_hypertension'].sum()} ({df['has_hypertension'].mean()*100:.1f}%)")
    print(f"  Admissions: {df['admission'].sum()} ({df['admission'].mean()*100:.1f}%)")
    
    return df

if __name__ == '__main__':
    generate_disease_prediction_data(2000)
