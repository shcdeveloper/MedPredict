"""
Train disease likelihood prediction models
Separate models for: Diabetes, Heart Disease, Hypertension
"""

import pandas as pd
import numpy as np
import joblib
import os
import sys
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report
)
import xgboost as xgb

import warnings
warnings.filterwarnings('ignore')


class DiseaseRiskModels:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.feature_names = None
        self.metrics = {}
        
    def load_data(self, filepath='data/processed/disease_prediction_data.csv'):
        """Load disease prediction dataset"""
        print(f"Loading data from {filepath}...")
        
        if not os.path.exists(filepath):
            print(f"❌ Data file not found!")
            print(f"   Run: python data/generate_disease_data.py")
            raise FileNotFoundError(f"Data file not found: {filepath}")
            
        df = pd.read_csv(filepath)
        print(f"✓ Loaded {len(df)} records")
        return df
    
    def preprocess_data(self, df, target_column):
        """Preprocess features for a specific disease target"""
        
        # Define features to use
        exclude_cols = ['has_diabetes', 'has_heart_disease', 'has_hypertension', 
                       'admission', 'diabetes_risk', 'heart_disease_risk', 'hypertension_risk']
        
        X = df.drop(columns=exclude_cols)
        y = df[target_column]
        
        # Encode categorical features
        categorical_cols = ['gender', 'smoking', 'alcohol', 'exercise']
        
        X_encoded = X.copy()
        label_encoders = {}
        
        for col in categorical_cols:
            le = LabelEncoder()
            X_encoded[col] = le.fit_transform(X[col])
            label_encoders[col] = le
        
        self.feature_names = X_encoded.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, scaler, label_encoders
    
    def train_disease_model(self, X_train, X_test, y_train, y_test, disease_name):
        """Train models for specific disease"""
        print(f"\n{'='*60}")
        print(f"Training {disease_name} Prediction Models")
        print(f"{'='*60}")
        
        models_to_train = {
            'Random Forest': RandomForestClassifier(
                n_estimators=150, max_depth=12, random_state=42, n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100, max_depth=5, random_state=42
            ),
            'XGBoost': xgb.XGBClassifier(
                n_estimators=100, max_depth=6, learning_rate=0.1,
                random_state=42, eval_metric='logloss'
            ),
            'Logistic Regression': LogisticRegression(
                max_iter=1000, random_state=42
            )
        }
        
        best_model = None
        best_score = 0
        best_name = None
        
        for name, model in models_to_train.items():
            print(f"\n🔄 Training {name}...")
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall': recall_score(y_test, y_pred, zero_division=0),
                'f1': f1_score(y_test, y_pred, zero_division=0),
                'roc_auc': roc_auc_score(y_test, y_pred_proba)
            }
            
            print(f"  Accuracy:  {metrics['accuracy']:.4f}")
            print(f"  Precision: {metrics['precision']:.4f}")
            print(f"  Recall:    {metrics['recall']:.4f}")
            print(f"  F1 Score:  {metrics['f1']:.4f}")
            print(f"  ROC AUC:   {metrics['roc_auc']:.4f}")
            
            if metrics['roc_auc'] > best_score:
                best_score = metrics['roc_auc']
                best_model = model
                best_name = name
        
        print(f"\n🏆 Best Model: {best_name} (ROC AUC: {best_score:.4f})")
        
        return best_model, best_score, best_name
    
    def train_all_models(self, df):
        """Train models for all diseases"""
        
        diseases = {
            'diabetes': 'has_diabetes',
            'heart_disease': 'has_heart_disease',
            'hypertension': 'has_hypertension'
        }
        
        for disease_name, target_col in diseases.items():
            print(f"\n\n{'#'*60}")
            print(f"# Processing: {disease_name.upper()}")
            print(f"{'#'*60}")
            
            # Preprocess
            X_train, X_test, y_train, y_test, scaler, label_encoders = \
                self.preprocess_data(df, target_col)
            
            # Train
            model, score, model_name = self.train_disease_model(
                X_train, X_test, y_train, y_test, disease_name.replace('_', ' ').title()
            )
            
            # Store
            self.models[disease_name] = model
            self.scalers[disease_name] = scaler
            self.label_encoders[disease_name] = label_encoders
            self.metrics[disease_name] = {
                'best_model': model_name,
                'roc_auc': score
            }
    
    def save_models(self, model_dir='models/disease_models'):
        """Save all trained models"""
        print(f"\n{'='*60}")
        print(f"Saving Disease Prediction Models")
        print(f"{'='*60}")
        
        os.makedirs(model_dir, exist_ok=True)
        
        for disease_name in self.models.keys():
            # Save model
            model_path = os.path.join(model_dir, f'{disease_name}_model.pkl')
            joblib.dump(self.models[disease_name], model_path)
            print(f"✓ {disease_name} model saved")
            
            # Save scaler
            scaler_path = os.path.join(model_dir, f'{disease_name}_scaler.pkl')
            joblib.dump(self.scalers[disease_name], scaler_path)
            
            # Save label encoders
            encoders_path = os.path.join(model_dir, f'{disease_name}_encoders.pkl')
            joblib.dump(self.label_encoders[disease_name], encoders_path)
        
        # Save feature names
        features_path = os.path.join(model_dir, 'feature_names.pkl')
        joblib.dump(self.feature_names, features_path)
        
        # Save metadata
        metadata = {
            'trained_at': datetime.now().isoformat(),
            'feature_names': self.feature_names,
            'metrics': self.metrics
        }
        metadata_path = os.path.join(model_dir, 'metadata.pkl')
        joblib.dump(metadata, metadata_path)
        
        print(f"\n✅ All models saved to {model_dir}/")


def main():
    print("="*60)
    print("Disease Likelihood Prediction - Model Training")
    print("="*60)
    
    trainer = DiseaseRiskModels()
    df = trainer.load_data()
    trainer.train_all_models(df)
    trainer.save_models()
    
    print(f"\n{'='*60}")
    print("🎉 Disease prediction models training completed!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
