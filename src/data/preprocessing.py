"""Data preprocessing utilities for MedPredict."""
import pandas as pd
import numpy as np
from typing import Tuple, List, Optional
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from loguru import logger


class DataPreprocessor:
    """Preprocessor for patient data."""
    
    def __init__(self):
        """Initialize preprocessor."""
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.is_fitted = False
    
    def fit(self, df: pd.DataFrame, target_col: Optional[str] = None) -> 'DataPreprocessor':
        """Fit preprocessor on training data."""
        logger.info("Fitting preprocessor on data")
        
        # Store feature names (excluding target)
        if target_col:
            self.feature_names = [col for col in df.columns if col != target_col]
        else:
            self.feature_names = df.columns.tolist()
        
        # Identify categorical and numerical columns
        categorical_cols = df[self.feature_names].select_dtypes(include=['object']).columns
        numerical_cols = df[self.feature_names].select_dtypes(include=[np.number]).columns
        
        # Fit label encoders for categorical columns
        for col in categorical_cols:
            self.label_encoders[col] = LabelEncoder()
            self.label_encoders[col].fit(df[col].fillna('missing'))
        
        # Fit scaler on numerical columns
        if len(numerical_cols) > 0:
            numerical_data = df[numerical_cols].fillna(df[numerical_cols].median())
            self.scaler.fit(numerical_data)
        
        self.is_fitted = True
        logger.info(f"Preprocessor fitted with {len(self.feature_names)} features")
        
        return self
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform data using fitted preprocessor."""
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        df_transformed = df.copy()
        
        # Handle missing values
        categorical_cols = df_transformed.select_dtypes(include=['object']).columns
        numerical_cols = df_transformed.select_dtypes(include=[np.number]).columns
        
        # Fill missing values
        for col in categorical_cols:
            df_transformed[col] = df_transformed[col].fillna('missing')
        
        for col in numerical_cols:
            if col in df_transformed.columns:
                df_transformed[col] = df_transformed[col].fillna(df_transformed[col].median())
        
        # Encode categorical variables
        for col, encoder in self.label_encoders.items():
            if col in df_transformed.columns:
                df_transformed[col] = encoder.transform(df_transformed[col])
        
        # Scale numerical features
        if len(numerical_cols) > 0:
            scaled_cols = [col for col in numerical_cols if col in self.feature_names]
            if scaled_cols:
                df_transformed[scaled_cols] = self.scaler.transform(df_transformed[scaled_cols])
        
        return df_transformed[self.feature_names]
    
    def fit_transform(self, df: pd.DataFrame, target_col: Optional[str] = None) -> pd.DataFrame:
        """Fit and transform data."""
        self.fit(df, target_col)
        return self.transform(df)


def split_data(
    X: pd.DataFrame,
    y: pd.DataFrame,
    test_size: float = 0.2,
    val_size: float = 0.1,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    """Split data into train, validation, and test sets."""
    # First split: train+val vs test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y if len(y.shape) == 1 else None
    )
    
    # Second split: train vs val
    val_ratio = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_ratio, random_state=random_state, stratify=y_temp if len(y_temp.shape) == 1 else None
    )
    
    logger.info(f"Data split - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    return X_train, X_val, X_test, y_train, y_val, y_test
