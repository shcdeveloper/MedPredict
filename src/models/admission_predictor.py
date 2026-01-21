"""Admission prediction model for MedPredict."""
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, classification_report
)
import joblib
from pathlib import Path
from loguru import logger


class AdmissionPredictor:
    """Model for predicting patient admission probability."""
    
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        """Initialize admission predictor."""
        self.params = params or {
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'objective': 'binary:logistic',
            'random_state': 42
        }
        self.model = xgb.XGBClassifier(**self.params)
        self.is_trained = False
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series, 
              X_val: Optional[pd.DataFrame] = None, 
              y_val: Optional[pd.Series] = None) -> Dict[str, float]:
        """Train the admission prediction model."""
        logger.info("Training admission prediction model")
        
        # Prepare validation data for early stopping
        eval_set = [(X_train, y_train)]
        if X_val is not None and y_val is not None:
            eval_set.append((X_val, y_val))
        
        # Train model
        self.model.fit(
            X_train, y_train,
            eval_set=eval_set,
            verbose=False
        )
        
        self.is_trained = True
        logger.info("Admission prediction model trained successfully")
        
        # Evaluate on training data
        metrics = self.evaluate(X_train, y_train)
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict admission requirement (0 or 1)."""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        return self.model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict admission probability."""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        return self.model.predict_proba(X)[:, 1]
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Evaluate model performance."""
        y_pred = self.predict(X)
        y_proba = self.predict_proba(X)
        
        metrics = {
            'accuracy': accuracy_score(y, y_pred),
            'precision': precision_score(y, y_pred, zero_division=0),
            'recall': recall_score(y, y_pred, zero_division=0),
            'f1_score': f1_score(y, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y, y_proba)
        }
        
        logger.info(f"Model evaluation metrics: {metrics}")
        return metrics
    
    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance."""
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")
        
        importance = pd.DataFrame({
            'feature': self.model.feature_names_in_,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance
    
    def save(self, filepath: str):
        """Save model to file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, filepath)
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'AdmissionPredictor':
        """Load model from file."""
        model = joblib.load(filepath)
        logger.info(f"Model loaded from {filepath}")
        return model
