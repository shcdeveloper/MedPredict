"""
Train healthcare admission prediction models
Includes preprocessing, model training, evaluation, and persistence
"""

import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb

import warnings
warnings.filterwarnings('ignore')


class HealthcareAdmissionModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = None
        self.model_metrics = {}
        
    def load_data(self, filepath='data/processed/patient_data_processed.csv'):
        """Load and prepare the dataset"""
        print(f"Loading data from {filepath}...")
        
        # Check if data exists
        if not os.path.exists(filepath):
            print(f"❌ Data file not found at {filepath}")
            print(f"   Please run: python data/generate_data.py")
            raise FileNotFoundError(f"Data file not found: {filepath}")
            
        df = pd.read_csv(filepath)
        print(f"✓ Loaded {len(df)} records")
        return df
    
    def preprocess_data(self, df):
        """Preprocess features and target"""
        print("\nPreprocessing data...")
        
        # Separate features and target
        X = df.drop('admission', axis=1)
        y = df['admission']
        
        # Encode gender
        self.label_encoder = LabelEncoder()
        X['gender_encoded'] = self.label_encoder.fit_transform(X['gender'])
        X = X.drop('gender', axis=1)
        
        self.feature_names = X.columns.tolist()
        print(f"✓ Features: {self.feature_names}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"✓ Training set: {len(X_train)} samples")
        print(f"✓ Test set: {len(X_test)} samples")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def train_models(self, X_train, X_test, y_train, y_test):
        """Train and compare multiple models"""
        print("\n" + "="*60)
        print("Training and Comparing Models")
        print("="*60)
        
        models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
            ),
            'Logistic Regression': LogisticRegression(
                max_iter=1000, random_state=42
            ),
            'Decision Tree': DecisionTreeClassifier(
                max_depth=10, random_state=42
            ),
            'XGBoost': xgb.XGBClassifier(
                n_estimators=100, max_depth=5, learning_rate=0.1,
                random_state=42, eval_metric='logloss'
            )
        }
        
        # Store predictions for ROC curve
        self.model_predictions = {}
        
        best_model_name = None
        best_score = 0
        
        for name, model in models.items():
            print(f"\n🔄 Training {name}...")
            
            # Train
            model.fit(X_train, y_train)
            
            # Predict
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Evaluate
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred),
                'recall': recall_score(y_test, y_pred),
                'f1': f1_score(y_test, y_pred),
                'roc_auc': roc_auc_score(y_test, y_pred_proba)
            }
            
            self.model_metrics[name] = metrics
            
            # Store predictions for ROC curve visualization
            self.model_predictions[name] = {
                'y_true': y_test,
                'y_pred_proba': y_pred_proba
            }
            
            print(f"  Accuracy:  {metrics['accuracy']:.4f}")
            print(f"  Precision: {metrics['precision']:.4f}")
            print(f"  Recall:    {metrics['recall']:.4f}")
            print(f"  F1 Score:  {metrics['f1']:.4f}")
            print(f"  ROC AUC:   {metrics['roc_auc']:.4f}")
            
            # Track best model
            if metrics['roc_auc'] > best_score:
                best_score = metrics['roc_auc']
                best_model_name = name
                self.model = model
        
        print("\n" + "="*60)
        print(f"🏆 Best Model: {best_model_name} (ROC AUC: {best_score:.4f})")
        print("="*60)
        
        # Generate comparison visualizations
        self.generate_comparison_visualizations()
        
        return best_model_name
    
    def generate_comparison_visualizations(self, output_dir='models/model_comparison'):
        """Generate comparison visualizations for all trained models"""
        print("\n" + "="*60)
        print("Generating Model Comparison Visualizations")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Save metrics to CSV
        print("\n📊 Saving metrics comparison...")
        metrics_df = pd.DataFrame(self.model_metrics).T
        metrics_df.index.name = 'Model'
        metrics_df = metrics_df.round(4)
        metrics_df.to_csv(f'{output_dir}/comparison_metrics.csv')
        print(f"✓ Saved: {output_dir}/comparison_metrics.csv")
        
        # 2. Metrics Comparison Bar Chart
        print("📊 Creating metrics comparison chart...")
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
        
        metrics_to_plot = ['accuracy', 'precision', 'recall', 'roc_auc']
        metric_labels = ['Accuracy', 'Precision', 'Recall', 'ROC-AUC']
        colors = ['#FF6D1F', '#4CAF50', '#2196F3', '#FFC107']
        
        for idx, (metric, label) in enumerate(zip(metrics_to_plot, metric_labels)):
            ax = axes[idx // 2, idx % 2]
            values = [self.model_metrics[model][metric] for model in self.model_metrics.keys()]
            bars = ax.bar(self.model_metrics.keys(), values, color=colors[idx], alpha=0.8)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=10)
            
            ax.set_ylabel(label, fontsize=12)
            ax.set_ylim([0, 1.1])
            ax.set_title(f'{label} Comparison', fontsize=12, fontweight='bold')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/metrics_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {output_dir}/metrics_comparison.png")
        
        # 3. ROC Curves Comparison
        print("📊 Creating ROC curves comparison...")
        plt.figure(figsize=(10, 8))
        
        colors_roc = ['#FF6D1F', '#4CAF50', '#2196F3', '#9C27B0']
        
        for idx, (model_name, preds) in enumerate(self.model_predictions.items()):
            fpr, tpr, _ = roc_curve(preds['y_true'], preds['y_pred_proba'])
            auc_score = self.model_metrics[model_name]['roc_auc']
            plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc_score:.3f})', 
                    linewidth=2.5, color=colors_roc[idx % len(colors_roc)])
        
        plt.plot([0, 1], [0, 1], 'k--', linewidth=1.5, label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontsize=12)
        plt.ylabel('True Positive Rate', fontsize=12)
        plt.title('ROC Curves Comparison', fontsize=14, fontweight='bold')
        plt.legend(loc="lower right", fontsize=11)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/roc_curves_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {output_dir}/roc_curves_comparison.png")
        
        # 4. Overall Ranking Table Visualization
        print("📊 Creating ranking table...")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.axis('tight')
        ax.axis('off')
        
        # Prepare data
        ranking_data = []
        for rank, (model_name, metrics) in enumerate(
            sorted(self.model_metrics.items(), key=lambda x: x[1]['roc_auc'], reverse=True), 1
        ):
            ranking_data.append([
                rank,
                model_name,
                f"{metrics['accuracy']:.4f}",
                f"{metrics['precision']:.4f}",
                f"{metrics['recall']:.4f}",
                f"{metrics['f1']:.4f}",
                f"{metrics['roc_auc']:.4f}"
            ])
        
        columns = ['Rank', 'Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
        
        table = ax.table(cellText=ranking_data, colLabels=columns, 
                        cellLoc='center', loc='center',
                        colColours=['#FF6D1F']*len(columns))
        
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2.5)
        
        # Style header
        for i in range(len(columns)):
            table[(0, i)].set_facecolor('#FF6D1F')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Highlight best model (rank 1)
        for i in range(len(columns)):
            table[(1, i)].set_facecolor('#FFF3E0')
            table[(1, i)].set_text_props(weight='bold')
        
        plt.title('Model Performance Ranking', fontsize=16, fontweight='bold', pad=20)
        plt.savefig(f'{output_dir}/ranking_table.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {output_dir}/ranking_table.png")
        
        print("\n✅ All comparison visualizations generated!")
        print(f"\nGenerated files in {output_dir}/:")
        print("  - comparison_metrics.csv")
        print("  - metrics_comparison.png")
        print("  - roc_curves_comparison.png")
        print("  - ranking_table.png")
    
    def save_model(self, model_dir='models'):
        """Save trained model and preprocessing objects"""
        print(f"\nSaving model artifacts to {model_dir}/...")
        
        os.makedirs(model_dir, exist_ok=True)
        
        # Save model
        model_path = os.path.join(model_dir, 'admission_model.pkl')
        joblib.dump(self.model, model_path)
        print(f"✓ Model saved: {model_path}")
        
        # Save scaler
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        print(f"✓ Scaler saved: {scaler_path}")
        
        # Save label encoder
        encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
        joblib.dump(self.label_encoder, encoder_path)
        print(f"✓ Label encoder saved: {encoder_path}")
        
        # Save feature names
        features_path = os.path.join(model_dir, 'feature_names.pkl')
        joblib.dump(self.feature_names, features_path)
        print(f"✓ Feature names saved: {features_path}")
        
        # Save metadata
        metadata = {
            'trained_at': datetime.now().isoformat(),
            'feature_names': self.feature_names,
            'metrics': self.model_metrics
        }
        metadata_path = os.path.join(model_dir, 'model_metadata.pkl')
        joblib.dump(metadata, metadata_path)
        print(f"✓ Metadata saved: {metadata_path}")
        
        print("\n✅ Model training and saving completed successfully!")


def main():
    """Main training pipeline"""
    print("="*60)
    print("Healthcare Admission Prediction - Model Training")
    print("="*60)
    
    # Initialize
    trainer = HealthcareAdmissionModel()
    
    # Load data
    df = trainer.load_data()
    
    # Preprocess
    X_train, X_test, y_train, y_test = trainer.preprocess_data(df)
    
    # Train models
    best_model = trainer.train_models(X_train, X_test, y_train, y_test)
    
    # Save
    trainer.save_model()
    
    print("\n" + "="*60)
    print("🎉 Training pipeline completed!")
    print("="*60)


if __name__ == '__main__':
    main()
