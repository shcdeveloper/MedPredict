"""
Partial Dependence Plot (PDP) and Individual Conditional Expectation (ICE) Analysis
Shows how features affect model predictions
"""

import pandas as pd
import numpy as np
import joblib
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.inspection import PartialDependenceDisplay, partial_dependence

import warnings
warnings.filterwarnings('ignore')


class PDPICEAnalyzer:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = None
        self.X = None
        self.y = None
        
    def load_model_and_data(self):
        """Load trained model and data"""
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
        self.y = df['admission']
        
        # Encode gender
        X['gender_encoded'] = self.label_encoder.transform(X['gender'])
        X_features = X[self.feature_names]
        
        # Scale features
        self.X = self.scaler.transform(X_features)
        
        print(f"✓ Loaded {len(df)} records")
        print(f"✓ Features: {self.feature_names}")
        
    def generate_pdp_plots(self, output_dir='models/explainability'):
        """Generate Partial Dependence Plots for all features"""
        print("\n" + "="*60)
        print("Generating Partial Dependence Plots (PDP)")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate PDP for each feature individually
        print("\nGenerating individual PDPs...")
        
        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        fig.suptitle('Partial Dependence Plots (PDP) - Feature Impact on Admission Prediction', 
                     fontsize=16, fontweight='bold')
        
        axes = axes.ravel()
        
        for idx, feature_idx in enumerate(range(len(self.feature_names))):
            feature_name = self.feature_names[feature_idx]
            
            print(f"  Computing PDP for: {feature_name}")
            
            # Calculate partial dependence
            pd_result = partial_dependence(
                self.model, 
                self.X, 
                features=[feature_idx],
                kind='average',
                grid_resolution=50
            )
            
            # Plot
            ax = axes[idx]
            ax.plot(pd_result['grid_values'][0], pd_result['average'][0], 
                   linewidth=2.5, color='#FF6D1F')
            
            # Fill area under curve
            ax.fill_between(pd_result['grid_values'][0], 
                           pd_result['average'][0], 
                           alpha=0.3, color='#FF6D1F')
            
            ax.set_xlabel(feature_name, fontsize=11, fontweight='bold')
            ax.set_ylabel('Partial Dependence', fontsize=11)
            ax.set_title(f'PDP: {feature_name}', fontsize=12, fontweight='bold')
            ax.grid(alpha=0.3)
            ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        
        # Hide unused subplot
        if len(self.feature_names) < len(axes):
            axes[-1].axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/pdp_all_features.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/pdp_all_features.png")
        
    def generate_ice_plots(self, output_dir='models/explainability', n_samples=50):
        """Generate Individual Conditional Expectation (ICE) plots"""
        print("\n" + "="*60)
        print("Generating ICE Plots (Individual Conditional Expectation)")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Sample subset for ICE (to avoid clutter)
        sample_indices = np.random.choice(len(self.X), size=min(n_samples, len(self.X)), replace=False)
        X_sample = self.X[sample_indices]
        
        print(f"\nUsing {len(X_sample)} samples for ICE plots...")
        
        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        fig.suptitle('ICE Plots - Individual Patient Prediction Curves', 
                     fontsize=16, fontweight='bold')
        
        axes = axes.ravel()
        
        for idx, feature_idx in enumerate(range(len(self.feature_names))):
            feature_name = self.feature_names[feature_idx]
            
            print(f"  Computing ICE for: {feature_name}")
            
            # Calculate ICE (individual curves)
            pd_result = partial_dependence(
                self.model,
                X_sample,
                features=[feature_idx],
                kind='individual',
                grid_resolution=50
            )
            
            # Plot individual curves
            ax = axes[idx]
            
            # Plot each individual curve in light blue
            for i in range(pd_result['individual'][0].shape[0]):
                ax.plot(pd_result['grid_values'][0], 
                       pd_result['individual'][0][i],
                       color='#2196F3', 
                       alpha=0.15,
                       linewidth=1)
            
            # Plot average PDP on top in orange
            pd_avg = partial_dependence(
                self.model,
                self.X,
                features=[feature_idx],
                kind='average',
                grid_resolution=50
            )
            
            ax.plot(pd_avg['grid_values'][0], 
                   pd_avg['average'][0],
                   color='#FF6D1F',
                   linewidth=3,
                   label='Average PDP',
                   zorder=100)
            
            ax.set_xlabel(feature_name, fontsize=11, fontweight='bold')
            ax.set_ylabel('Prediction', fontsize=11)
            ax.set_title(f'ICE: {feature_name}', fontsize=12, fontweight='bold')
            ax.grid(alpha=0.3)
            ax.legend(loc='best', fontsize=9)
            ax.axhline(y=0.5, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Decision Threshold')
        
        # Hide unused subplot
        if len(self.feature_names) < len(axes):
            axes[-1].axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/ice_all_features.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/ice_all_features.png")
        
    def generate_combined_pdp_ice(self, output_dir='models/explainability'):
        """Generate combined PDP+ICE plot for top features"""
        print("\n" + "="*60)
        print("Generating Combined PDP + ICE Plot")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Use top 4 most important features
        # For this example, we'll use the first 4 features
        top_features = list(range(min(4, len(self.feature_names))))
        
        print(f"\nGenerating combined plot for top features...")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('PDP + ICE Combined - Top Features Impact Analysis', 
                     fontsize=16, fontweight='bold')
        
        axes = axes.ravel()
        
        # Sample for ICE
        n_samples = 50
        sample_indices = np.random.choice(len(self.X), size=min(n_samples, len(self.X)), replace=False)
        X_sample = self.X[sample_indices]
        
        for plot_idx, feature_idx in enumerate(top_features):
            feature_name = self.feature_names[feature_idx]
            
            print(f"  Processing: {feature_name}")
            
            ax = axes[plot_idx]
            
            # ICE curves (individual)
            pd_ice = partial_dependence(
                self.model,
                X_sample,
                features=[feature_idx],
                kind='individual',
                grid_resolution=50
            )
            
            # Plot ICE curves
            for i in range(pd_ice['individual'][0].shape[0]):
                ax.plot(pd_ice['grid_values'][0],
                       pd_ice['individual'][0][i],
                       color='lightblue',
                       alpha=0.2,
                       linewidth=0.8)
            
            # PDP curve (average)
            pd_avg = partial_dependence(
                self.model,
                self.X,
                features=[feature_idx],
                kind='average',
                grid_resolution=50
            )
            
            # Plot PDP
            ax.plot(pd_avg['grid_values'][0],
                   pd_avg['average'][0],
                   color='#FF6D1F',
                   linewidth=3.5,
                   label='Average Effect (PDP)',
                   zorder=100)
            
            # Add confidence band (std of ICE curves)
            ice_std = np.std(pd_ice['individual'][0], axis=0)
            
            # Ensure ice_std matches pd_avg length
            if len(ice_std) != len(pd_avg['average'][0]):
                # Interpolate if needed
                ice_std = np.interp(
                    pd_avg['grid_values'][0],
                    pd_ice['grid_values'][0],
                    ice_std
                )
            
            ax.fill_between(pd_avg['grid_values'][0],
                           pd_avg['average'][0] - ice_std,
                           pd_avg['average'][0] + ice_std,
                           color='#FF6D1F',
                           alpha=0.2,
                           label='±1 Std Dev')
            
            # Formatting
            ax.set_xlabel(feature_name, fontsize=12, fontweight='bold')
            ax.set_ylabel('Prediction (Admission Probability)', fontsize=11)
            ax.set_title(f'{feature_name}', fontsize=13, fontweight='bold')
            ax.grid(alpha=0.3)
            ax.axhline(y=0.5, color='red', linestyle='--', linewidth=1.5, 
                      alpha=0.7, label='Decision Threshold')
            ax.legend(loc='best', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/pdp_ice_combined.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/pdp_ice_combined.png")
        
    def generate_2d_pdp(self, output_dir='models/explainability'):
        """Generate 2D Partial Dependence Plot for feature interactions"""
        print("\n" + "="*60)
        print("Generating 2D PDP (Feature Interactions)")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Select top 2 features for interaction (age and glucose as example)
        # Adjust based on your most important features
        if len(self.feature_names) >= 2:
            feature_pairs = [
                (0, 2),  # age and glucose
                (1, 2),  # heart_rate and glucose
            ]
            
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            fig.suptitle('2D Partial Dependence - Feature Interactions', 
                        fontsize=16, fontweight='bold')
            
            for idx, (feat1, feat2) in enumerate(feature_pairs):
                if feat1 < len(self.feature_names) and feat2 < len(self.feature_names):
                    feat1_name = self.feature_names[feat1]
                    feat2_name = self.feature_names[feat2]
                    
                    print(f"  Computing 2D PDP for: {feat1_name} × {feat2_name}")
                    
                    ax = axes[idx]
                    
                    # Calculate 2D partial dependence
                    pd_result = partial_dependence(
                        self.model,
                        self.X,
                        features=[(feat1, feat2)],
                        grid_resolution=30
                    )
                    
                    # Create contour plot
                    XX, YY = np.meshgrid(pd_result['grid_values'][0], 
                                        pd_result['grid_values'][1])
                    Z = pd_result['average'][0].T
                    
                    contour = ax.contourf(XX, YY, Z, levels=20, cmap='RdYlBu_r', alpha=0.8)
                    cbar = plt.colorbar(contour, ax=ax)
                    cbar.set_label('Admission Probability', fontsize=10)
                    
                    # Add contour lines
                    ax.contour(XX, YY, Z, levels=10, colors='black', alpha=0.3, linewidths=0.5)
                    
                    ax.set_xlabel(feat1_name, fontsize=12, fontweight='bold')
                    ax.set_ylabel(feat2_name, fontsize=12, fontweight='bold')
                    ax.set_title(f'{feat1_name} × {feat2_name}', fontsize=13, fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(f'{output_dir}/pdp_2d_interactions.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"\n✓ Saved: {output_dir}/pdp_2d_interactions.png")
        else:
            print("  ⚠️ Not enough features for 2D PDP")
    
    def generate_summary_report(self, output_dir='models/explainability'):
        """Generate text summary of PDP/ICE findings"""
        print("\n" + "="*60)
        print("Generating PDP/ICE Summary Report")
        print("="*60)
        
        report = []
        report.append("="*60)
        report.append("PDP & ICE ANALYSIS SUMMARY")
        report.append("="*60)
        report.append("")
        report.append("1. PARTIAL DEPENDENCE PLOTS (PDP):")
        report.append("")
        report.append("   Definition:")
        report.append("   - Shows the average effect of a feature on predictions")
        report.append("   - Marginalizes out the effect of all other features")
        report.append("   - Useful for understanding feature-prediction relationship")
        report.append("")
        report.append("   Key Insights:")
        
        # Analyze each feature
        for idx, feature_name in enumerate(self.feature_names):
            pd_result = partial_dependence(
                self.model,
                self.X,
                features=[idx],
                kind='average',
                grid_resolution=50
            )
            
            avg_values = pd_result['average'][0]
            grid_values = pd_result['grid_values'][0]
            
            # Find trend
            if avg_values[-1] > avg_values[0]:
                trend = "increases"
                impact = "positive"
            elif avg_values[-1] < avg_values[0]:
                trend = "decreases"
                impact = "negative"
            else:
                trend = "remains stable"
                impact = "minimal"
            
            # Calculate range
            value_range = avg_values.max() - avg_values.min()
            
            report.append(f"   - {feature_name}:")
            report.append(f"     * Trend: Prediction {trend} as {feature_name} increases")
            report.append(f"     * Impact strength: {value_range:.3f} ({impact})")
            report.append("")
        
        report.append("")
        report.append("2. ICE PLOTS (Individual Conditional Expectation):")
        report.append("")
        report.append("   Definition:")
        report.append("   - Shows prediction curves for individual patients")
        report.append("   - Each line represents one patient's prediction trend")
        report.append("   - Reveals heterogeneity in feature effects")
        report.append("")
        report.append("   Key Insights:")
        report.append("   - Wide spread of ICE curves = feature effects vary by patient")
        report.append("   - Parallel ICE curves = consistent feature effect")
        report.append("   - Crossing curves = feature interactions present")
        report.append("")
        
        report.append("")
        report.append("3. CLINICAL INTERPRETATION:")
        report.append("")
        report.append("   Model Decision Process:")
        report.append("   - Features work together to predict admission risk")
        report.append("   - PDP shows average population-level effects")
        report.append("   - ICE reveals individual patient variability")
        report.append("")
        report.append("   Usage Recommendations:")
        report.append("   - Use PDP for policy/protocol decisions")
        report.append("   - Use ICE for understanding individual patient predictions")
        report.append("   - Consider 2D PDP for feature interaction insights")
        report.append("")
        
        report.append("="*60)
        report.append("Generated by: PDP/ICE Analysis Module")
        report.append("="*60)
        
        # Save report
        report_text = "\n".join(report)
        with open(f'{output_dir}/pdp_ice_summary.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(report_text)
        print(f"\n✓ Saved: {output_dir}/pdp_ice_summary.txt")


def main():
    print("="*60)
    print("PDP & ICE Analysis for Healthcare Admission Prediction")
    print("="*60)
    print()
    
    analyzer = PDPICEAnalyzer()
    
    # Load model and data
    analyzer.load_model_and_data()
    
    # Generate PDP plots
    analyzer.generate_pdp_plots()
    
    # Generate ICE plots
    analyzer.generate_ice_plots(n_samples=50)
    
    # Generate combined PDP+ICE
    analyzer.generate_combined_pdp_ice()
    
    # Generate 2D PDP for interactions
    analyzer.generate_2d_pdp()
    
    # Generate summary report
    analyzer.generate_summary_report()
    
    print("\n" + "="*60)
    print("✅ PDP & ICE Analysis Completed!")
    print("="*60)
    print("\nGenerated files in models/explainability/:")
    print("  - pdp_all_features.png        (Partial Dependence Plots)")
    print("  - ice_all_features.png        (Individual Conditional Expectation)")
    print("  - pdp_ice_combined.png        (Combined PDP+ICE for top features)")
    print("  - pdp_2d_interactions.png     (2D Feature Interactions)")
    print("  - pdp_ice_summary.txt         (Analysis Summary)")


if __name__ == '__main__':
    main()
