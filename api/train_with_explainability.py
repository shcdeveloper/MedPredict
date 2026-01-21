"""
Enhanced model training with SHAP explainability
"""
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import shap
try:
    from lime import lime_tabular
    LIME_AVAILABLE = True
except ImportError:
    print("Warning: LIME not available. Install with: pip install lime")
    LIME_AVAILABLE = False
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
import warnings
warnings.filterwarnings('ignore')


class ExplainableHealthcareModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.explainer_shap = None
        self.explainer_lime = None
        self.feature_names = None
        self.X_train = None
        self.X_test = None
        
    def load_and_preprocess_data(self):
        """Load and preprocess data"""
        print("Loading data...")
        df = pd.read_csv('data/processed/patient_data_processed.csv')
        
        X = df.drop('admission', axis=1)
        y = df['admission']
        
        # Encode gender
        self.label_encoder = LabelEncoder()
        X['gender_encoded'] = self.label_encoder.fit_transform(X['gender'])
        X = X.drop('gender', axis=1)
        
        self.feature_names = X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.X_train = pd.DataFrame(X_train_scaled, columns=self.feature_names)
        self.X_test = pd.DataFrame(X_test_scaled, columns=self.feature_names)
        
        print(f"✓ Data loaded: {len(X_train)} training samples, {len(X_test)} test samples")
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def train_model(self, X_train, y_train):
        """Train Random Forest model"""
        print("\nTraining model...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        print("✓ Model trained")
        
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        print("\nEvaluating model...")
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]
        
        accuracy = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)
        
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  ROC-AUC: {auc:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['No Admission', 'Admission']))
        
        return accuracy, auc
        
    def create_shap_explainer(self):
        """Create SHAP explainer"""
        print("\nCreating SHAP explainer...")
        self.explainer_shap = shap.TreeExplainer(self.model)
        print("✓ SHAP explainer created")
        
    def create_lime_explainer(self, X_train):
        """Create LIME explainer"""
        if not LIME_AVAILABLE:
            print("⚠️ LIME not available, skipping LIME explainer")
            return
            
        print("Creating LIME explainer...")
        self.explainer_lime = lime_tabular.LimeTabularExplainer(
            X_train,
            feature_names=self.feature_names,
            class_names=['No Admission', 'Admission'],
            mode='classification'
        )
        print("✓ LIME explainer created")
    
    def generate_shap_visualizations(self, output_dir='models/explainability'):
        """Generate SHAP visualizations"""
        print("\n" + "="*60)
        print("Generating SHAP Visualizations")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Calculate SHAP values (using smaller subset for speed)
        n_samples = min(100, len(self.X_test))
        print(f"Calculating SHAP values for {n_samples} samples...")
        shap_values = self.explainer_shap.shap_values(self.X_test[:n_samples])
        
        # Handle different SHAP value formats (list vs array)
        if isinstance(shap_values, list):
            # Multi-class output - use class 1 (admission)
            shap_values_plot = shap_values[1]
        else:
            # Single output
            shap_values_plot = shap_values
        
        # 1. Summary Plot (Feature Importance)
        print("Creating summary plot...")
        plt.figure(figsize=(10, 6))
        shap.summary_plot(
            shap_values_plot, 
            self.X_test[:n_samples], 
            feature_names=self.feature_names,
            show=False
        )
        plt.tight_layout()
        plt.savefig(f'{output_dir}/shap_summary_plot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {output_dir}/shap_summary_plot.png")
        
        # 2. Bar Plot (Mean Absolute SHAP Values)
        print("Creating importance bar plot...")
        plt.figure(figsize=(10, 6))
        shap.summary_plot(
            shap_values_plot, 
            self.X_test[:n_samples], 
            feature_names=self.feature_names,
            plot_type='bar',
            show=False
        )
        plt.tight_layout()
        plt.savefig(f'{output_dir}/shap_importance_bar.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {output_dir}/shap_importance_bar.png")
        
        # 3. Force Plot (Single Prediction)
        print("Creating force plot...")
        try:
            X_test_sample = self.X_test.iloc[0]
            shap_values_single = self.explainer_shap.shap_values(X_test_sample.values.reshape(1, -1))
            
            # Handle expected value format
            if isinstance(self.explainer_shap.expected_value, (list, np.ndarray)):
                expected_val = self.explainer_shap.expected_value[1]
            else:
                expected_val = self.explainer_shap.expected_value
                
            # Handle shap values format for single prediction
            if isinstance(shap_values_single, list):
                shap_val_single = shap_values_single[1].flatten()
            else:
                shap_val_single = shap_values_single.flatten()
            
            shap.force_plot(
                expected_val,
                shap_val_single,
                X_test_sample,
                feature_names=self.feature_names,
                matplotlib=True,
                show=False
            )
            plt.savefig(f'{output_dir}/shap_force_plot.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✓ Saved: {output_dir}/shap_force_plot.png")
        except Exception as e:
            print(f"⚠️  Force plot skipped due to: {str(e)}")
        
        # 4. Dependence Plot (Top Feature)
        print("Creating dependence plot...")
        try:
            # Get feature with highest importance
            mean_abs_shap = np.abs(shap_values_plot).mean(axis=0)
            top_feature_idx = np.argmax(mean_abs_shap)
            top_feature = self.feature_names[top_feature_idx]
            
            plt.figure(figsize=(10, 6))
            shap.dependence_plot(
                top_feature_idx,  # Use index instead of name for better compatibility
                shap_values_plot,
                self.X_test[:n_samples],
                feature_names=self.feature_names,
                show=False
            )
            plt.tight_layout()
            plt.savefig(f'{output_dir}/shap_dependence_plot.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✓ Saved: {output_dir}/shap_dependence_plot.png")
        except Exception as e:
            print(f"⚠️  Dependence plot skipped due to: {str(e)}")
            # Use mean absolute SHAP from earlier for feature importance
            mean_abs_shap = np.abs(shap_values_plot).mean(axis=0)
        
        # Save SHAP values
        try:
            # Ensure 2D shape for DataFrame
            if len(shap_values_plot.shape) == 3:
                # Multi-dimensional SHAP values - flatten or select single output
                shap_values_to_save = shap_values_plot[:n_samples, :, 1] if shap_values_plot.shape[2] > 1 else shap_values_plot[:n_samples, :, 0]
            else:
                shap_values_to_save = shap_values_plot[:n_samples]
                
            shap_df = pd.DataFrame(
                shap_values_to_save,
                columns=self.feature_names
            )
            shap_df.to_csv(f'{output_dir}/shap_values.csv', index=False)
            print(f"✓ Saved: {output_dir}/shap_values.csv")
        except Exception as e:
            print(f"⚠️  Could not save SHAP values CSV: {str(e)}")
        
        # Feature importance summary
        try:
            # Ensure mean_abs_shap is 1D
            if hasattr(mean_abs_shap, 'shape') and len(mean_abs_shap.shape) > 1:
                mean_abs_shap = mean_abs_shap.flatten()[:len(self.feature_names)]
                
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': mean_abs_shap
            }).sort_values('importance', ascending=False)
            
            feature_importance.to_csv(f'{output_dir}/feature_importance.csv', index=False)
            print(f"✓ Saved: {output_dir}/feature_importance.csv")
            print("\nTop 3 Most Important Features:")
            for idx, row in feature_importance.head(3).iterrows():
                print(f"  {row['feature']}: {row['importance']:.4f}")
        except Exception as e:
            print(f"⚠️  Could not save feature importance: {str(e)}")
        
    def generate_lime_explanation(self, instance_idx=0, output_dir='models/explainability'):
        """Generate LIME explanation for a single prediction"""
        if not LIME_AVAILABLE or self.explainer_lime is None:
            print("\n⚠️ LIME not available, skipping LIME explanation")
            return
            
        print("\n" + "="*60)
        print("Generating LIME Explanation")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Get instance
        instance = self.X_test.iloc[instance_idx].values
        
        print(f"Explaining prediction for test instance {instance_idx}...")
        # Generate explanation
        explanation = self.explainer_lime.explain_instance(
            instance,
            self.model.predict_proba,
            num_features=len(self.feature_names)
        )
        
        # Save as HTML
        explanation.save_to_file(f'{output_dir}/lime_explanation.html')
        print(f"✓ Saved: {output_dir}/lime_explanation.html")
        
        # Create matplotlib figure
        fig = explanation.as_pyplot_figure()
        plt.tight_layout()
        plt.savefig(f'{output_dir}/lime_explanation.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {output_dir}/lime_explanation.png")
        
        # Save explanation data
        lime_values = dict(explanation.as_list())
        lime_df = pd.DataFrame(list(lime_values.items()), columns=['Feature', 'Impact'])
        lime_df.to_csv(f'{output_dir}/lime_values.csv', index=False)
        print(f"✓ Saved: {output_dir}/lime_values.csv")
        
        # Show prediction
        prediction = self.model.predict(instance.reshape(1, -1))[0]
        probability = self.model.predict_proba(instance.reshape(1, -1))[0]
        print(f"\nPrediction: {'Admission' if prediction == 1 else 'No Admission'}")
        print(f"Probability: {probability[1]:.4f}")
        
    def save_explainers(self, model_dir='models'):
        """Save explainer objects"""
        print("\n" + "="*60)
        print("Saving Model Artifacts")
        print("="*60)
        
        # Save model
        joblib.dump(self.model, f'{model_dir}/admission_model.pkl')
        print(f"✓ Saved: {model_dir}/admission_model.pkl")
        
        joblib.dump(self.scaler, f'{model_dir}/scaler.pkl')
        print(f"✓ Saved: {model_dir}/scaler.pkl")
        
        joblib.dump(self.label_encoder, f'{model_dir}/label_encoder.pkl')
        print(f"✓ Saved: {model_dir}/label_encoder.pkl")
        
        joblib.dump(self.feature_names, f'{model_dir}/feature_names.pkl')
        print(f"✓ Saved: {model_dir}/feature_names.pkl")
        
        # Save model metadata
        metadata = {
            'model_type': 'RandomForestClassifier',
            'n_estimators': 100,
            'max_depth': 10,
            'features': self.feature_names,
            'n_features': len(self.feature_names)
        }
        joblib.dump(metadata, f'{model_dir}/model_metadata.pkl')
        print(f"✓ Saved: {model_dir}/model_metadata.pkl")
        
        # Save explainers
        joblib.dump(self.explainer_shap, f'{model_dir}/shap_explainer.pkl')
        print(f"✓ Saved: {model_dir}/shap_explainer.pkl")
        
        print("✓ All artifacts saved")


def main():
    print("="*60)
    print("Healthcare Model Training with Explainability")
    print("="*60)
    print()
    
    trainer = ExplainableHealthcareModel()
    
    # Load and preprocess
    X_train, X_test, y_train, y_test = trainer.load_and_preprocess_data()
    
    # Train model
    trainer.train_model(X_train, y_train)
    
    # Evaluate
    trainer.evaluate_model(X_test, y_test)
    
    # Create explainers
    trainer.create_shap_explainer()
    trainer.create_lime_explainer(X_train)
    
    # Generate visualizations
    trainer.generate_shap_visualizations()
    trainer.generate_lime_explanation(instance_idx=0)
    
    # Save everything
    trainer.save_explainers()
    
    print("\n" + "="*60)
    print("✅ Training and Explainability Generation Complete!")
    print("="*60)
    print("\nGenerated files in models/explainability/:")
    print("  - shap_summary_plot.png")
    print("  - shap_importance_bar.png")
    print("  - shap_force_plot.png")
    print("  - shap_dependence_plot.png")
    print("  - shap_values.csv")
    print("  - feature_importance.csv")
    print("  - lime_explanation.html")
    print("  - lime_explanation.png")
    print("  - lime_values.csv")
    print("\nTo view LIME explanation, open:")
    print("  models/explainability/lime_explanation.html")


if __name__ == '__main__':
    main()
