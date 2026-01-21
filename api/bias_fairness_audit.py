"""
Bias & Fairness Audit for Healthcare Prediction Models
Analyzes model predictions across demographic groups and calculates fairness metrics
"""

import pandas as pd
import numpy as np
import joblib
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score

import warnings
warnings.filterwarnings('ignore')


class BiasAudit:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = None
        self.data = None
        self.predictions = None
        self.fairness_metrics = {}
        
    def load_model_and_data(self):
        """Load trained model and test data"""
        print("Loading model and data...")
        
        # Load model artifacts
        self.model = joblib.load('models/admission_model.pkl')
        self.scaler = joblib.load('models/scaler.pkl')
        self.label_encoder = joblib.load('models/label_encoder.pkl')
        self.feature_names = joblib.load('models/feature_names.pkl')
        print("✓ Model loaded")
        
        # Load data
        df = pd.read_csv('data/processed/patient_data_processed.csv')
        
        # Prepare features
        X = df.drop('admission', axis=1)
        y = df['admission']
        
        # Encode gender
        X['gender_encoded'] = self.label_encoder.transform(X['gender'])
        
        # Store original gender for analysis
        self.data = df.copy()
        self.data['gender_encoded'] = X['gender_encoded']
        
        # Scale features
        X_scaled = self.scaler.transform(X[self.feature_names])
        
        # Make predictions
        self.data['prediction'] = self.model.predict(X_scaled)
        self.data['prediction_proba'] = self.model.predict_proba(X_scaled)[:, 1]
        
        print(f"✓ Loaded {len(self.data)} records with predictions")
        
    def create_age_groups(self):
        """Create age group categories"""
        self.data['age_group'] = pd.cut(
            self.data['age'], 
            bins=[0, 40, 60, 100], 
            labels=['Young (18-40)', 'Middle (41-60)', 'Senior (61+)']
        )
        
    def analyze_class_imbalance(self, output_dir='models/bias_analysis'):
        """Analyze class imbalance in the dataset"""
        print("\n" + "="*60)
        print("Class Imbalance Analysis")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Calculate class distribution
        class_dist = self.data['admission'].value_counts()
        class_pct = self.data['admission'].value_counts(normalize=True) * 100
        
        print(f"\nClass Distribution:")
        print(f"  No Admission (0): {class_dist[0]} ({class_pct[0]:.1f}%)")
        print(f"  Admission (1):    {class_dist[1]} ({class_pct[1]:.1f}%)")
        
        imbalance_ratio = class_dist[0] / class_dist[1] if class_dist[1] > 0 else 0
        print(f"  Imbalance Ratio: {imbalance_ratio:.2f}:1")
        
        # Visualize
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Bar chart
        colors = ['#4CAF50', '#FF6D1F']
        ax1.bar(['No Admission', 'Admission'], class_dist.values, color=colors, alpha=0.8)
        ax1.set_ylabel('Count', fontsize=12)
        ax1.set_title('Class Distribution', fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(class_dist.values):
            ax1.text(i, v + 10, str(v), ha='center', fontsize=11, fontweight='bold')
        
        # Pie chart
        ax2.pie(class_dist.values, labels=['No Admission', 'Admission'], 
                colors=colors, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Class Proportion', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/class_imbalance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/class_imbalance.png")
        
        # Document findings
        findings = {
            'no_admission_count': int(class_dist[0]),
            'admission_count': int(class_dist[1]),
            'no_admission_pct': float(class_pct[0]),
            'admission_pct': float(class_pct[1]),
            'imbalance_ratio': float(imbalance_ratio),
            'severity': 'Moderate' if 1.5 <= imbalance_ratio <= 3 else 'Severe' if imbalance_ratio > 3 else 'Balanced'
        }
        
        return findings
    
    def analyze_gender_bias(self, output_dir='models/bias_analysis'):
        """Analyze prediction bias across gender groups"""
        print("\n" + "="*60)
        print("Gender Bias Analysis")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Calculate metrics by gender
        gender_groups = self.data.groupby('gender')
        
        gender_metrics = {}
        for gender in ['M', 'F']:
            group_data = self.data[self.data['gender'] == gender]
            
            metrics = {
                'count': len(group_data),
                'positive_rate': (group_data['prediction'] == 1).mean(),
                'actual_positive_rate': (group_data['admission'] == 1).mean(),
                'accuracy': accuracy_score(group_data['admission'], group_data['prediction']),
                'precision': precision_score(group_data['admission'], group_data['prediction'], zero_division=0),
                'recall': recall_score(group_data['admission'], group_data['prediction'], zero_division=0),
                'avg_probability': group_data['prediction_proba'].mean()
            }
            
            gender_metrics[gender] = metrics
            
            print(f"\n{gender} (n={metrics['count']}):")
            print(f"  Positive Prediction Rate: {metrics['positive_rate']:.3f}")
            print(f"  Actual Positive Rate:     {metrics['actual_positive_rate']:.3f}")
            print(f"  Accuracy:                 {metrics['accuracy']:.3f}")
            print(f"  Avg Prediction Prob:      {metrics['avg_probability']:.3f}")
        
        # Calculate fairness metrics
        self.fairness_metrics['gender'] = self.calculate_fairness_metrics(
            gender_metrics['M'], gender_metrics['F']
        )
        
        # Visualize
        self.visualize_gender_bias(gender_metrics, output_dir)
        
        return gender_metrics
    
    def analyze_age_bias(self, output_dir='models/bias_analysis'):
        """Analyze prediction bias across age groups"""
        print("\n" + "="*60)
        print("Age Group Bias Analysis")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Calculate metrics by age group
        age_metrics = {}
        for age_group in self.data['age_group'].unique():
            group_data = self.data[self.data['age_group'] == age_group]
            
            metrics = {
                'count': len(group_data),
                'positive_rate': (group_data['prediction'] == 1).mean(),
                'actual_positive_rate': (group_data['admission'] == 1).mean(),
                'accuracy': accuracy_score(group_data['admission'], group_data['prediction']),
                'precision': precision_score(group_data['admission'], group_data['prediction'], zero_division=0),
                'recall': recall_score(group_data['admission'], group_data['prediction'], zero_division=0),
                'avg_probability': group_data['prediction_proba'].mean()
            }
            
            age_metrics[age_group] = metrics
            
            print(f"\n{age_group} (n={metrics['count']}):")
            print(f"  Positive Prediction Rate: {metrics['positive_rate']:.3f}")
            print(f"  Actual Positive Rate:     {metrics['actual_positive_rate']:.3f}")
            print(f"  Accuracy:                 {metrics['accuracy']:.3f}")
            print(f"  Avg Prediction Prob:      {metrics['avg_probability']:.3f}")
        
        # Visualize
        self.visualize_age_bias(age_metrics, output_dir)
        
        return age_metrics
    
    def calculate_fairness_metrics(self, group1_metrics, group2_metrics):
        """Calculate fairness metrics between two groups"""
        
        # Demographic Parity (difference in positive prediction rates)
        demographic_parity = abs(group1_metrics['positive_rate'] - group2_metrics['positive_rate'])
        
        # Disparate Impact Ratio
        disparate_impact = (
            group1_metrics['positive_rate'] / group2_metrics['positive_rate']
            if group2_metrics['positive_rate'] > 0 else 0
        )
        
        # Equal Opportunity (difference in recall/TPR)
        equal_opportunity = abs(group1_metrics['recall'] - group2_metrics['recall'])
        
        # Accuracy difference
        accuracy_diff = abs(group1_metrics['accuracy'] - group2_metrics['accuracy'])
        
        fairness = {
            'demographic_parity': demographic_parity,
            'disparate_impact': disparate_impact,
            'equal_opportunity': equal_opportunity,
            'accuracy_difference': accuracy_diff,
            'is_fair_demographic': demographic_parity < 0.1,  # Within 10%
            'is_fair_disparate': 0.8 <= disparate_impact <= 1.25,  # 80% rule
            'is_fair_opportunity': equal_opportunity < 0.1
        }
        
        print(f"\n📊 Fairness Metrics:")
        print(f"  Demographic Parity Diff:  {fairness['demographic_parity']:.3f} {'✓' if fairness['is_fair_demographic'] else '⚠️'}")
        print(f"  Disparate Impact Ratio:   {fairness['disparate_impact']:.3f} {'✓' if fairness['is_fair_disparate'] else '⚠️'}")
        print(f"  Equal Opportunity Diff:   {fairness['equal_opportunity']:.3f} {'✓' if fairness['is_fair_opportunity'] else '⚠️'}")
        print(f"  Accuracy Difference:      {fairness['accuracy_difference']:.3f}")
        
        return fairness
    
    def visualize_gender_bias(self, gender_metrics, output_dir):
        """Create gender bias visualizations"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Gender Bias Analysis', fontsize=16, fontweight='bold')
        
        genders = list(gender_metrics.keys())
        colors = ['#2196F3', '#FF6D1F']
        
        # 1. Positive Prediction Rate
        ax = axes[0, 0]
        rates = [gender_metrics[g]['positive_rate'] for g in genders]
        bars = ax.bar(genders, rates, color=colors, alpha=0.8)
        ax.set_ylabel('Positive Prediction Rate', fontsize=11)
        ax.set_title('Positive Prediction Rate by Gender', fontweight='bold')
        ax.set_ylim([0, 1])
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom', fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        # 2. Accuracy Comparison
        ax = axes[0, 1]
        accuracies = [gender_metrics[g]['accuracy'] for g in genders]
        bars = ax.bar(genders, accuracies, color=colors, alpha=0.8)
        ax.set_ylabel('Accuracy', fontsize=11)
        ax.set_title('Accuracy by Gender', fontweight='bold')
        ax.set_ylim([0, 1])
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom', fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        # 3. Precision & Recall
        ax = axes[1, 0]
        x = np.arange(len(genders))
        width = 0.35
        precisions = [gender_metrics[g]['precision'] for g in genders]
        recalls = [gender_metrics[g]['recall'] for g in genders]
        ax.bar(x - width/2, precisions, width, label='Precision', color='#4CAF50', alpha=0.8)
        ax.bar(x + width/2, recalls, width, label='Recall', color='#FFC107', alpha=0.8)
        ax.set_ylabel('Score', fontsize=11)
        ax.set_title('Precision & Recall by Gender', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(genders)
        ax.legend()
        ax.set_ylim([0, 1])
        ax.grid(axis='y', alpha=0.3)
        
        # 4. Average Prediction Probability
        ax = axes[1, 1]
        probs = [gender_metrics[g]['avg_probability'] for g in genders]
        bars = ax.bar(genders, probs, color=colors, alpha=0.8)
        ax.set_ylabel('Average Probability', fontsize=11)
        ax.set_title('Avg Admission Probability by Gender', fontweight='bold')
        ax.set_ylim([0, 1])
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom', fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/gender_bias_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/gender_bias_analysis.png")
    
    def visualize_age_bias(self, age_metrics, output_dir):
        """Create age bias visualizations"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Age Group Bias Analysis', fontsize=16, fontweight='bold')
        
        age_groups = list(age_metrics.keys())
        colors = ['#4CAF50', '#FF9800', '#F44336']
        
        # 1. Positive Prediction Rate
        ax = axes[0, 0]
        rates = [age_metrics[g]['positive_rate'] for g in age_groups]
        bars = ax.bar(range(len(age_groups)), rates, color=colors, alpha=0.8)
        ax.set_ylabel('Positive Prediction Rate', fontsize=11)
        ax.set_title('Positive Prediction Rate by Age Group', fontweight='bold')
        ax.set_xticks(range(len(age_groups)))
        ax.set_xticklabels(age_groups, rotation=15)
        ax.set_ylim([0, 1])
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom', fontsize=9)
        ax.grid(axis='y', alpha=0.3)
        
        # 2. Accuracy Comparison
        ax = axes[0, 1]
        accuracies = [age_metrics[g]['accuracy'] for g in age_groups]
        bars = ax.bar(range(len(age_groups)), accuracies, color=colors, alpha=0.8)
        ax.set_ylabel('Accuracy', fontsize=11)
        ax.set_title('Accuracy by Age Group', fontweight='bold')
        ax.set_xticks(range(len(age_groups)))
        ax.set_xticklabels(age_groups, rotation=15)
        ax.set_ylim([0, 1])
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom', fontsize=9)
        ax.grid(axis='y', alpha=0.3)
        
        # 3. Sample Size Distribution
        ax = axes[1, 0]
        counts = [age_metrics[g]['count'] for g in age_groups]
        bars = ax.bar(range(len(age_groups)), counts, color=colors, alpha=0.8)
        ax.set_ylabel('Sample Count', fontsize=11)
        ax.set_title('Sample Distribution by Age Group', fontweight='bold')
        ax.set_xticks(range(len(age_groups)))
        ax.set_xticklabels(age_groups, rotation=15)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=9)
        ax.grid(axis='y', alpha=0.3)
        
        # 4. Average Prediction Probability
        ax = axes[1, 1]
        probs = [age_metrics[g]['avg_probability'] for g in age_groups]
        bars = ax.bar(range(len(age_groups)), probs, color=colors, alpha=0.8)
        ax.set_ylabel('Average Probability', fontsize=11)
        ax.set_title('Avg Admission Probability by Age Group', fontweight='bold')
        ax.set_xticks(range(len(age_groups)))
        ax.set_xticklabels(age_groups, rotation=15)
        ax.set_ylim([0, 1])
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom', fontsize=9)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/age_bias_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/age_bias_analysis.png")
    
    def save_fairness_metrics(self, output_dir='models/bias_analysis'):
        """Save all fairness metrics to CSV"""
        
        # Flatten fairness metrics
        fairness_data = []
        for group, metrics in self.fairness_metrics.items():
            for metric, value in metrics.items():
                fairness_data.append({
                    'group': group,
                    'metric': metric,
                    'value': value
                })
        
        df = pd.DataFrame(fairness_data)
        df.to_csv(f'{output_dir}/fairness_metrics.csv', index=False)
        print(f"\n✓ Saved: {output_dir}/fairness_metrics.csv")
    
    def generate_mitigation_report(self, output_dir='models/bias_analysis'):
        """Generate bias mitigation recommendations"""
        print("\n" + "="*60)
        print("Bias Mitigation Recommendations")
        print("="*60)
        
        report = []
        report.append("="*60)
        report.append("BIAS & FAIRNESS AUDIT - MITIGATION STRATEGIES")
        report.append("="*60)
        report.append("")
        
        # Check gender fairness
        if 'gender' in self.fairness_metrics:
            gender_fair = self.fairness_metrics['gender']
            report.append("1. GENDER BIAS MITIGATION:")
            report.append("")
            
            if not gender_fair['is_fair_demographic']:
                report.append("   ⚠️ Demographic parity violation detected")
                report.append(f"      Difference: {gender_fair['demographic_parity']:.3f}")
                report.append("      Recommendation:")
                report.append("      - Apply reweighting: Assign higher weights to underrepresented predictions")
                report.append("      - Adjust decision threshold per group to equalize positive rates")
                report.append("")
            else:
                report.append("   ✓ Demographic parity satisfied")
                report.append("")
            
            if not gender_fair['is_fair_disparate']:
                report.append("   ⚠️ Disparate impact detected")
                report.append(f"      Ratio: {gender_fair['disparate_impact']:.3f} (should be 0.8-1.25)")
                report.append("      Recommendation:")
                report.append("      - Use group-specific thresholds")
                report.append("      - Consider fairness-aware learning algorithms")
                report.append("")
            else:
                report.append("   ✓ Disparate impact within acceptable range")
                report.append("")
            
            if not gender_fair['is_fair_opportunity']:
                report.append("   ⚠️ Equal opportunity violation detected")
                report.append(f"      Difference in recall: {gender_fair['equal_opportunity']:.3f}")
                report.append("      Recommendation:")
                report.append("      - Calibrate model to equalize true positive rates")
                report.append("      - Post-processing: Adjust predictions to match group TPR")
                report.append("")
            else:
                report.append("   ✓ Equal opportunity satisfied")
                report.append("")
        
        report.append("")
        report.append("2. GENERAL MITIGATION STRATEGIES:")
        report.append("")
        report.append("   A. PRE-PROCESSING:")
        report.append("      - Reweighting: Balance training data across groups")
        report.append("      - Resampling: SMOTE for minority groups")
        report.append("      - Data augmentation: Generate synthetic samples")
        report.append("")
        report.append("   B. IN-PROCESSING:")
        report.append("      - Fairness constraints: Add fairness loss to training")
        report.append("      - Adversarial debiasing: Train with fairness adversary")
        report.append("      - Prejudice remover: Regularize to remove discrimination")
        report.append("")
        report.append("   C. POST-PROCESSING:")
        report.append("      - Threshold optimization: Different thresholds per group")
        report.append("      - Calibration: Adjust probabilities to match group distributions")
        report.append("      - Reject option: Flag high-uncertainty predictions for review")
        report.append("")
        
        report.append("3. IMPLEMENTATION PRIORITY:")
        report.append("")
        report.append("   Priority 1 (Immediate):")
        report.append("   - Monitor predictions across demographic groups")
        report.append("   - Set up automated fairness alerts")
        report.append("")
        report.append("   Priority 2 (Short-term):")
        report.append("   - Implement group-specific decision thresholds")
        report.append("   - Collect more balanced training data")
        report.append("")
        report.append("   Priority 3 (Long-term):")
        report.append("   - Retrain with fairness-aware algorithms")
        report.append("   - Regular fairness audits (quarterly)")
        report.append("")
        
        report.append("4. MONITORING RECOMMENDATIONS:")
        report.append("")
        report.append("   - Track fairness metrics in production")
        report.append("   - Set up alerts for demographic parity > 0.1")
        report.append("   - Regular bias audits with updated data")
        report.append("   - Document all bias findings and mitigations")
        report.append("")
        report.append("="*60)
        
        # Save to file
        report_text = "\n".join(report)
        with open(f'{output_dir}/mitigation_recommendations.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(report_text)
        print(f"\n✓ Saved: {output_dir}/mitigation_recommendations.txt")


def main():
    print("="*60)
    print("Bias & Fairness Audit for Healthcare Prediction")
    print("="*60)
    print()
    
    auditor = BiasAudit()
    
    # Load model and data
    auditor.load_model_and_data()
    
    # Create age groups
    auditor.create_age_groups()
    
    # Analyze class imbalance
    imbalance = auditor.analyze_class_imbalance()
    
    # Analyze gender bias
    gender_metrics = auditor.analyze_gender_bias()
    
    # Analyze age bias
    age_metrics = auditor.analyze_age_bias()
    
    # Save fairness metrics
    auditor.save_fairness_metrics()
    
    # Generate mitigation report
    auditor.generate_mitigation_report()
    
    print("\n" + "="*60)
    print("✅ Bias & Fairness Audit Completed!")
    print("="*60)
    print("\nGenerated files in models/bias_analysis/:")
    print("  - class_imbalance.png")
    print("  - gender_bias_analysis.png")
    print("  - age_bias_analysis.png")
    print("  - fairness_metrics.csv")
    print("  - mitigation_recommendations.txt")
    print("\nReview mitigation_recommendations.txt for action items.")


if __name__ == '__main__':
    main()
