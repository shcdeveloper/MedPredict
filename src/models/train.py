"""Training pipeline for MedPredict models with MLOps practices."""
import pandas as pd
import mlflow
import mlflow.sklearn
import joblib
from pathlib import Path
from typing import Dict, Any, Tuple

from src.data.loader import load_patient_data
from src.data.preprocessing import DataPreprocessor, split_data
from src.models.admission_predictor import AdmissionPredictor
from src.models.disease_risk_assessor import DiseaseRiskAssessor
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger()


class MedPredictTrainer:
    """Training pipeline for MedPredict models."""
    
    def __init__(self, config_path: str = "configs/config.yaml"):
        """Initialize trainer with configuration."""
        self.config = Config(config_path)
        self.preprocessor = DataPreprocessor()
        
        # Setup MLflow
        mlflow.set_tracking_uri(self.config.mlflow_config['tracking_uri'])
        mlflow.set_experiment(self.config.mlflow_config['experiment_name'])
    
    def load_and_prepare_data(self, data_path: str = None) -> Tuple:
        """Load and prepare data for training."""
        logger.info("Loading patient data")
        df = load_patient_data(data_path)
        
        logger.info(f"Loaded {len(df)} patient records")
        
        # Separate features and targets
        feature_cols = [
            'age', 'gender', 'systolic_bp', 'diastolic_bp', 'heart_rate',
            'temperature', 'glucose', 'cholesterol', 'bmi', 'has_diabetes',
            'has_hypertension', 'smoking_status', 'previous_admissions'
        ]
        
        admission_target = 'admission_required'
        disease_targets = ['cardiovascular_risk', 'respiratory_risk', 'metabolic_risk']
        
        X = df[feature_cols]
        y_admission = df[admission_target]
        y_diseases = df[disease_targets]
        
        # Preprocess features
        logger.info("Preprocessing features")
        X_processed = self.preprocessor.fit_transform(X)
        
        # Split data
        data_config = self.config.data_config
        X_train, X_val, X_test, y_adm_train, y_adm_val, y_adm_test = split_data(
            X_processed, y_admission,
            test_size=data_config['test_size'],
            val_size=data_config['validation_size'],
            random_state=data_config['random_state']
        )
        
        # Split disease targets
        y_dis_train = y_diseases.loc[y_adm_train.index]
        y_dis_val = y_diseases.loc[y_adm_val.index]
        y_dis_test = y_diseases.loc[y_adm_test.index]
        
        return (X_train, X_val, X_test, 
                y_adm_train, y_adm_val, y_adm_test,
                y_dis_train, y_dis_val, y_dis_test)
    
    def train_admission_predictor(self, X_train, X_val, y_train, y_val) -> AdmissionPredictor:
        """Train admission prediction model with MLflow tracking."""
        logger.info("Training admission predictor")
        
        with mlflow.start_run(run_name="admission_predictor"):
            # Initialize model
            model_config = self.config.model_config['admission_predictor']
            model = AdmissionPredictor(params=model_config['params'])
            
            # Log parameters
            mlflow.log_params(model_config['params'])
            
            # Train model
            train_metrics = model.train(X_train, y_train, X_val, y_val)
            
            # Evaluate on validation set
            val_metrics = model.evaluate(X_val, y_val)
            
            # Log metrics
            mlflow.log_metrics({f"train_{k}": v for k, v in train_metrics.items()})
            mlflow.log_metrics({f"val_{k}": v for k, v in val_metrics.items()})
            
            # Log model
            mlflow.sklearn.log_model(model.model, "model")
            
            # Save feature importance
            feature_importance = model.get_feature_importance()
            logger.info(f"Top 5 important features:\n{feature_importance.head()}")
            
            logger.info("Admission predictor training completed")
            
        return model
    
    def train_disease_risk_assessor(self, X_train, X_val, y_train, y_val) -> DiseaseRiskAssessor:
        """Train disease risk assessment model with MLflow tracking."""
        logger.info("Training disease risk assessor")
        
        with mlflow.start_run(run_name="disease_risk_assessor"):
            # Initialize model
            model_config = self.config.model_config['disease_risk_assessor']
            model = DiseaseRiskAssessor(
                params=model_config['params'],
                disease_names=['cardiovascular_risk', 'respiratory_risk', 'metabolic_risk']
            )
            
            # Log parameters
            mlflow.log_params(model_config['params'])
            
            # Train model
            train_metrics = model.train(X_train, y_train)
            
            # Evaluate on validation set
            val_metrics = model.evaluate(X_val, y_val)
            
            # Log metrics
            mlflow.log_metric("train_hamming_loss", train_metrics['hamming_loss'])
            mlflow.log_metric("val_hamming_loss", val_metrics['hamming_loss'])
            mlflow.log_metric("train_accuracy", train_metrics['accuracy'])
            mlflow.log_metric("val_accuracy", val_metrics['accuracy'])
            
            # Log per-disease metrics
            for disease, metrics in val_metrics['per_disease'].items():
                for metric_name, value in metrics.items():
                    mlflow.log_metric(f"val_{disease}_{metric_name}", value)
            
            logger.info("Disease risk assessor training completed")
            
        return model
    
    def train(self, data_path: str = None, 
              save_models: bool = True,
              models_dir: str = "models/trained") -> Dict[str, Any]:
        """Train all models."""
        logger.info("Starting MedPredict training pipeline")
        
        # Load and prepare data
        data = self.load_and_prepare_data(data_path)
        X_train, X_val, X_test, y_adm_train, y_adm_val, y_adm_test, y_dis_train, y_dis_val, y_dis_test = data
        
        # Train admission predictor
        admission_model = self.train_admission_predictor(X_train, X_val, y_adm_train, y_adm_val)
        
        # Train disease risk assessor
        disease_model = self.train_disease_risk_assessor(X_train, X_val, y_dis_train, y_dis_val)
        
        # Evaluate on test set
        logger.info("Evaluating models on test set")
        test_metrics_admission = admission_model.evaluate(X_test, y_adm_test)
        test_metrics_disease = disease_model.evaluate(X_test, y_dis_test)
        
        logger.info(f"Test metrics - Admission Predictor: {test_metrics_admission}")
        logger.info(f"Test metrics - Disease Risk Assessor: Hamming Loss={test_metrics_disease['hamming_loss']:.4f}")
        
        # Save models
        if save_models:
            models_path = Path(models_dir)
            models_path.mkdir(parents=True, exist_ok=True)
            
            admission_model.save(f"{models_dir}/admission_predictor.pkl")
            disease_model.save(f"{models_dir}/disease_risk_assessor.pkl")
            
            # Save preprocessor
            joblib.dump(self.preprocessor, f"{models_dir}/preprocessor.pkl")
            logger.info("Preprocessor saved")
        
        logger.info("Training pipeline completed successfully")
        
        return {
            'admission_model': admission_model,
            'disease_model': disease_model,
            'preprocessor': self.preprocessor,
            'test_metrics': {
                'admission': test_metrics_admission,
                'disease': test_metrics_disease
            }
        }


if __name__ == "__main__":
    trainer = MedPredictTrainer()
    results = trainer.train()
