"""Multi-disease risk assessment model for MedPredict."""
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
import lightgbm as lgb
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, classification_report, hamming_loss
)
import joblib
from pathlib import Path
from loguru import logger


class DiseaseRiskAssessor:
    """Model for multi-disease risk assessment."""
    
    def __init__(self, params: Optional[Dict[str, Any]] = None, 
                 disease_names: Optional[List[str]] = None):
        """Initialize disease risk assessor."""
        self.params = params or {
            'n_estimators': 100,
            'max_depth': 5,
            'learning_rate': 0.05,
            'random_state': 42,
            'verbose': -1
        }
        
        # Disease categories
        self.disease_names = disease_names or [
            'cardiovascular_risk',
            'respiratory_risk',
            'metabolic_risk'
        ]
        
        # Multi-output classifier with LightGBM
        base_estimator = lgb.LGBMClassifier(**self.params)
        self.model = MultiOutputClassifier(base_estimator)
        self.is_trained = False
    
    def train(self, X_train: pd.DataFrame, y_train: pd.DataFrame) -> Dict[str, float]:
        """Train the multi-disease risk assessment model."""
        logger.info("Training multi-disease risk assessment model")
        
        # Train model
        self.model.fit(X_train, y_train)
        
        self.is_trained = True
        logger.info("Multi-disease risk assessment model trained successfully")
        
        # Evaluate on training data
        metrics = self.evaluate(X_train, y_train)
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict disease risks (0 or 1 for each disease)."""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        return self.model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> List[np.ndarray]:
        """Predict disease risk probabilities."""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Get probabilities for each disease
        probas = []
        for estimator in self.model.estimators_:
            proba = estimator.predict_proba(X)[:, 1]
            probas.append(proba)
        
        return probas
    
    def predict_dict(self, X: pd.DataFrame) -> List[Dict[str, float]]:
        """Predict disease risks as dictionary with probabilities."""
        predictions = self.predict(X)
        probabilities = self.predict_proba(X)
        
        results = []
        for i in range(len(X)):
            patient_risks = {}
            for j, disease_name in enumerate(self.disease_names):
                patient_risks[disease_name] = {
                    'risk_level': 'High' if predictions[i, j] == 1 else 'Low',
                    'probability': float(probabilities[j][i])
                }
            results.append(patient_risks)
        
        return results
    
    def evaluate(self, X: pd.DataFrame, y: pd.DataFrame) -> Dict[str, Any]:
        """Evaluate model performance."""
        y_pred = self.predict(X)
        
        # Overall metrics
        metrics = {
            'hamming_loss': hamming_loss(y, y_pred),
            'accuracy': accuracy_score(y, y_pred),
        }
        
        # Per-disease metrics
        disease_metrics = {}
        for i, disease_name in enumerate(self.disease_names):
            disease_metrics[disease_name] = {
                'accuracy': accuracy_score(y.iloc[:, i], y_pred[:, i]),
                'precision': precision_score(y.iloc[:, i], y_pred[:, i], zero_division=0),
                'recall': recall_score(y.iloc[:, i], y_pred[:, i], zero_division=0),
                'f1_score': f1_score(y.iloc[:, i], y_pred[:, i], zero_division=0)
            }
        
        metrics['per_disease'] = disease_metrics
        
        logger.info(f"Model evaluation - Hamming Loss: {metrics['hamming_loss']:.4f}, "
                   f"Overall Accuracy: {metrics['accuracy']:.4f}")
        
        return metrics
    
    def save(self, filepath: str):
        """Save model to file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, filepath)
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'DiseaseRiskAssessor':
        """Load model from file."""
        model = joblib.load(filepath)
        logger.info(f"Model loaded from {filepath}")
        return model
