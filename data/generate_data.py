"""
Generate synthetic patient data for Healthcare Admission Prediction
This creates realistic patient data with correlations between features
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples
n_samples = 1000

print("Generating synthetic patient data...")

# Generate features with realistic distributions
age = np.random.normal(58, 18, n_samples).clip(18, 95).astype(int)
gender = np.random.choice(['M', 'F'], n_samples, p=[0.48, 0.52])

# Heart rate (influenced by age and health status)
base_hr = 70 + (age - 50) * 0.3 + np.random.normal(0, 10, n_samples)
heart_rate = base_hr.clip(50, 120).astype(int)

# Glucose (influenced by age)
base_glucose = 100 + (age - 50) * 0.5 + np.random.normal(0, 20, n_samples)
glucose = base_glucose.clip(70, 300).round(1)

# Prior admissions (influenced by age)
prior_admission_prob = (age - 18) / 77  # Higher age = more likely to have prior admissions
prior_admission = np.array([
    np.random.poisson(prob * 2) for prob in prior_admission_prob
]).clip(0, 10)

# Generate admission outcome (target variable)
# Higher probability with: older age, abnormal heart rate, high glucose, more prior admissions
risk_score = (
    (age - 18) / 77 * 0.3 +  # Age factor
    np.abs(heart_rate - 70) / 50 * 0.2 +  # Heart rate deviation
    (glucose - 100) / 200 * 0.25 +  # Glucose elevation
    prior_admission / 10 * 0.25  # Prior admission history
)

# Add some randomness
risk_score += np.random.normal(0, 0.1, n_samples)
risk_score = risk_score.clip(0, 1)

# Convert to binary outcome (0=no admission, 1=admission)
admission = (risk_score > 0.5).astype(int)

# Create DataFrame
df = pd.DataFrame({
    'age': age,
    'gender': gender,
    'heart_rate': heart_rate,
    'glucose': glucose,
    'prior_admission': prior_admission,
    'admission': admission
})

# Display statistics
print("\n" + "="*50)
print("Dataset Statistics")
print("="*50)
print(f"Total samples: {len(df)}")
print(f"\nAdmission rate: {df['admission'].mean():.2%}")
print(f"\nAge: {df['age'].mean():.1f} ± {df['age'].std():.1f} years")
print(f"Heart rate: {df['heart_rate'].mean():.1f} ± {df['heart_rate'].std():.1f} bpm")
print(f"Glucose: {df['glucose'].mean():.1f} ± {df['glucose'].std():.1f} mg/dL")
print(f"Prior admissions: {df['prior_admission'].mean():.2f} ± {df['prior_admission'].std():.2f}")
print(f"\nGender distribution:")
print(df['gender'].value_counts())
print(f"\nAdmission by gender:")
print(df.groupby('gender')['admission'].mean())

# Save raw data
raw_path = os.path.join('data', 'raw', 'patient_data_raw.csv')
df.to_csv(raw_path, index=False)
print(f"\n✓ Raw data saved to: {raw_path}")

# Save processed data (same for now, preprocessing happens in training)
processed_path = os.path.join('data', 'processed', 'patient_data_processed.csv')
df.to_csv(processed_path, index=False)
print(f"✓ Processed data saved to: {processed_path}")

# Display sample records
print("\n" + "="*50)
print("Sample Records")
print("="*50)
print(df.head(10).to_string(index=False))

print("\n✅ Data generation completed successfully!")
