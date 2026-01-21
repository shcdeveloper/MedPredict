"""
Feature Selection Methods for Healthcare Prediction
Implements: Filter, Wrapper, and Embedded methods
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import (
    SelectKBest, f_classif, mutual_info_classif,
    RFE, RFECV, SelectFromModel
)
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib
import os
import warnings
warnings.filterwarnings('ignore')


class FeatureSelector:
    def __init__(self):
        self.feature_names = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.results = []
        
    def load_data(self):
        """Load and preprocess data"""
        print("Loading data...")
        df = pd.read_csv('data/processed/patient_data_processed.csv')
        
        X = df.drop('admission', axis=1)
        y = df['admission']
        
        # Encode gender
        X['gender_encoded'] = self.label_encoder.fit_transform(X['gender'])
        X = X.drop('gender', axis=1)
        
        self.feature_names = X.columns.tolist()
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale
        self.X_train = self.scaler.fit_transform(X_train)
        self.X_test = self.scaler.transform(X_test)
        self.y_train = y_train.values
        self.y_test = y_test.values
        
        print(f"✓ Data loaded: {len(self.feature_names)} features")
        return self
    
    def method_1_univariate_selection(self, k=3):
        """Filter Method: Univariate Feature Selection"""
        print(f"\n{'='*60}")
        print(f"METHOD 1: Univariate Selection (Filter Method)")
        print(f"{'='*60}")
        
        # ANOVA F-test
        print(f"\nA. ANOVA F-test (SelectKBest, k={k})")
        selector_f = SelectKBest(score_func=f_classif, k=k)
        X_train_f = selector_f.fit_transform(self.X_train, self.y_train)
        X_test_f = selector_f.transform(self.X_test)
        
        selected_features_f = [self.feature_names[i] for i in selector_f.get_support(indices=True)]
        scores_f = selector_f.scores_
        
        print(f"Selected Features:")
        for feat, score in zip(selected_features_f, scores_f[selector_f.get_support()]):
            print(f"  - {feat}: F-score = {score:.2f}")
        
        # Evaluate
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train_f, self.y_train)
        y_pred = model.predict(X_test_f)
        accuracy = accuracy_score(self.y_test, y_pred)
        auc = roc_auc_score(self.y_test, model.predict_proba(X_test_f)[:, 1])
        
        print(f"Performance: Accuracy={accuracy:.4f}, ROC-AUC={auc:.4f}")
        
        self.results.append({
            'Method': 'Univariate (F-test)',
            'N_Features': k,
            'Features': ', '.join(selected_features_f),
            'Accuracy': accuracy,
            'ROC_AUC': auc
        })
        
        # Mutual Information
        print(f"\nB. Mutual Information (SelectKBest, k={k})")
        selector_mi = SelectKBest(score_func=mutual_info_classif, k=k)
        X_train_mi = selector_mi.fit_transform(self.X_train, self.y_train)
        X_test_mi = selector_mi.transform(self.X_test)
        
        selected_features_mi = [self.feature_names[i] for i in selector_mi.get_support(indices=True)]
        scores_mi = selector_mi.scores_
        
        print(f"Selected Features:")
        for feat, score in zip(selected_features_mi, scores_mi[selector_mi.get_support()]):
            print(f"  - {feat}: MI-score = {score:.4f}")
        
        model.fit(X_train_mi, self.y_train)
        y_pred = model.predict(X_test_mi)
        accuracy = accuracy_score(self.y_test, y_pred)
        auc = roc_auc_score(self.y_test, model.predict_proba(X_test_mi)[:, 1])
        
        print(f"Performance: Accuracy={accuracy:.4f}, ROC-AUC={auc:.4f}")
        
        self.results.append({
            'Method': 'Univariate (MI)',
            'N_Features': k,
            'Features': ', '.join(selected_features_mi),
            'Accuracy': accuracy,
            'ROC_AUC': auc
        })
        
        return selected_features_f, selected_features_mi
    
    def method_2_recursive_feature_elimination(self, n_features=3):
        """Wrapper Method: Recursive Feature Elimination"""
        print(f"\n{'='*60}")
        print(f"METHOD 2: Recursive Feature Elimination (Wrapper Method)")
        print(f"{'='*60}")
        
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        
        # RFE
        print(f"\nRFE with n_features={n_features}")
        rfe = RFE(estimator=model, n_features_to_select=n_features, step=1)
        rfe.fit(self.X_train, self.y_train)
        
        selected_features = [self.feature_names[i] for i in rfe.get_support(indices=True)]
        rankings = rfe.ranking_
        
        print(f"Selected Features:")
        for feat in selected_features:
            print(f"  - {feat}")
        
        print(f"\nAll Feature Rankings:")
        ranking_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Rank': rankings
        }).sort_values('Rank')
        print(ranking_df.to_string(index=False))
        
        # Evaluate
        X_train_rfe = rfe.transform(self.X_train)
        X_test_rfe = rfe.transform(self.X_test)
        
        model.fit(X_train_rfe, self.y_train)
        y_pred = model.predict(X_test_rfe)
        accuracy = accuracy_score(self.y_test, y_pred)
        auc = roc_auc_score(self.y_test, model.predict_proba(X_test_rfe)[:, 1])
        
        print(f"\nPerformance: Accuracy={accuracy:.4f}, ROC-AUC={auc:.4f}")
        
        self.results.append({
            'Method': 'RFE',
            'N_Features': n_features,
            'Features': ', '.join(selected_features),
            'Accuracy': accuracy,
            'ROC_AUC': auc
        })
        
        return selected_features, rankings
    
    def method_3_rfecv(self, output_dir='models/feature_selection'):
        """Wrapper Method: RFE with Cross-Validation"""
        print(f"\n{'='*60}")
        print(f"METHOD 3: RFE with Cross-Validation")
        print(f"{'='*60}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        
        print("\nRunning RFECV (this may take a moment)...")
        rfecv = RFECV(
            estimator=model,
            step=1,
            cv=5,
            scoring='roc_auc',
            n_jobs=-1
        )
        rfecv.fit(self.X_train, self.y_train)
        
        optimal_n = rfecv.n_features_
        selected_features = [self.feature_names[i] for i in rfecv.get_support(indices=True)]
        
        print(f"\nOptimal number of features: {optimal_n}")
        print(f"Selected Features:")
        for feat in selected_features:
            print(f"  - {feat}")
        
        # Plot CV scores
        plt.figure(figsize=(10, 6))
        n_features_range = range(1, len(rfecv.cv_results_['mean_test_score']) + 1)
        plt.plot(n_features_range, rfecv.cv_results_['mean_test_score'], 'b-', linewidth=2)
        plt.fill_between(
            n_features_range,
            rfecv.cv_results_['mean_test_score'] - rfecv.cv_results_['std_test_score'],
            rfecv.cv_results_['mean_test_score'] + rfecv.cv_results_['std_test_score'],
            alpha=0.2
        )
        plt.xlabel('Number of Features', fontsize=12)
        plt.ylabel('Cross-Validation Score (ROC-AUC)', fontsize=12)
        plt.title('RFECV: Optimal Number of Features', fontsize=14, fontweight='bold')
        plt.axvline(x=optimal_n, color='r', linestyle='--', linewidth=2, label=f'Optimal = {optimal_n}')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/rfecv_scores.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/rfecv_scores.png")
        
        # Evaluate
        X_train_rfecv = rfecv.transform(self.X_train)
        X_test_rfecv = rfecv.transform(self.X_test)
        
        model.fit(X_train_rfecv, self.y_train)
        y_pred = model.predict(X_test_rfecv)
        accuracy = accuracy_score(self.y_test, y_pred)
        auc = roc_auc_score(self.y_test, model.predict_proba(X_test_rfecv)[:, 1])
        
        print(f"Performance: Accuracy={accuracy:.4f}, ROC-AUC={auc:.4f}")
        
        self.results.append({
            'Method': 'RFECV',
            'N_Features': optimal_n,
            'Features': ', '.join(selected_features),
            'Accuracy': accuracy,
            'ROC_AUC': auc
        })
        
        return selected_features, optimal_n
    
    def method_4_feature_importance(self, threshold='median', output_dir='models/feature_selection'):
        """Embedded Method: Feature Importance Selection"""
        print(f"\n{'='*60}")
        print(f"METHOD 4: Feature Importance Selection (Embedded Method)")
        print(f"{'='*60}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(self.X_train, self.y_train)
        
        # Get feature importances
        importances = model.feature_importances_
        
        # Select from model
        selector = SelectFromModel(model, threshold=threshold, prefit=True)
        X_train_selected = selector.transform(self.X_train)
        X_test_selected = selector.transform(self.X_test)
        
        selected_features = [self.feature_names[i] for i in selector.get_support(indices=True)]
        
        print(f"\nThreshold: {threshold}")
        print(f"Selected Features ({len(selected_features)}):")
        for feat in selected_features:
            idx = self.feature_names.index(feat)
            print(f"  - {feat}: {importances[idx]:.4f}")
        
        # Plot feature importances
        plt.figure(figsize=(10, 6))
        indices = np.argsort(importances)[::-1]
        colors = ['#FF6D1F' if self.feature_names[i] in selected_features else '#cccccc' for i in indices]
        
        plt.bar(range(len(importances)), importances[indices], color=colors)
        plt.xticks(range(len(importances)), [self.feature_names[i] for i in indices], 
                   rotation=45, ha='right', fontsize=10)
        plt.xlabel('Features', fontsize=12)
        plt.ylabel('Importance', fontsize=12)
        plt.title('Feature Importances (Random Forest)', fontsize=14, fontweight='bold')
        
        threshold_val = np.median(importances) if threshold == 'median' else float(threshold)
        plt.axhline(y=threshold_val, color='r', linestyle='--', linewidth=2, 
                   label=f'Threshold: {threshold}')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/feature_importances.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/feature_importances.png")
        
        # Save importance values
        importance_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        importance_df.to_csv(f'{output_dir}/feature_importance_values.csv', index=False)
        print(f"✓ Saved: {output_dir}/feature_importance_values.csv")
        
        # Evaluate
        model_new = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model_new.fit(X_train_selected, self.y_train)
        y_pred = model_new.predict(X_test_selected)
        accuracy = accuracy_score(self.y_test, y_pred)
        auc = roc_auc_score(self.y_test, model_new.predict_proba(X_test_selected)[:, 1])
        
        print(f"Performance: Accuracy={accuracy:.4f}, ROC-AUC={auc:.4f}")
        
        self.results.append({
            'Method': 'Feature Importance',
            'N_Features': len(selected_features),
            'Features': ', '.join(selected_features),
            'Accuracy': accuracy,
            'ROC_AUC': auc
        })
        
        return selected_features, importances
    
    def method_5_correlation_analysis(self, threshold=0.8, output_dir='models/feature_selection'):
        """Filter Method: Correlation Analysis"""
        print(f"\n{'='*60}")
        print(f"METHOD 5: Correlation Analysis")
        print(f"{'='*60}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Calculate correlation matrix
        X_df = pd.DataFrame(self.X_train, columns=self.feature_names)
        corr_matrix = X_df.corr().abs()
        
        # Find highly correlated pairs
        upper_triangle = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        to_drop = [col for col in upper_triangle.columns if any(upper_triangle[col] > threshold)]
        
        print(f"\nCorrelation threshold: {threshold}")
        print(f"Highly Correlated Features to Remove:")
        if to_drop:
            for feat in to_drop:
                # Find what it's correlated with
                corr_with = upper_triangle[feat][upper_triangle[feat] > threshold]
                for other_feat, corr_val in corr_with.items():
                    print(f"  - {feat} ↔ {other_feat}: {corr_val:.3f}")
        else:
            print("  None found (all correlations below threshold)")
        
        # Plot correlation heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
        plt.title('Feature Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/correlation_matrix.png")
        
        # Save correlation matrix
        corr_matrix.to_csv(f'{output_dir}/correlation_matrix.csv')
        print(f"✓ Saved: {output_dir}/correlation_matrix.csv")
        
        return to_drop, corr_matrix
    
    def compare_all_methods(self, output_dir='models/feature_selection'):
        """Compare all feature selection methods"""
        print(f"\n{'='*60}")
        print(f"COMPARISON: All Feature Selection Methods")
        print(f"{'='*60}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Add baseline (all features)
        model_full = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model_full.fit(self.X_train, self.y_train)
        y_pred_full = model_full.predict(self.X_test)
        acc_full = accuracy_score(self.y_test, y_pred_full)
        auc_full = roc_auc_score(self.y_test, model_full.predict_proba(self.X_test)[:, 1])
        
        baseline = {
            'Method': 'All Features (Baseline)',
            'N_Features': len(self.feature_names),
            'Features': ', '.join(self.feature_names),
            'Accuracy': acc_full,
            'ROC_AUC': auc_full
        }
        
        all_results = [baseline] + self.results
        df_results = pd.DataFrame(all_results)
        
        print("\nComparison Results:")
        print(df_results[['Method', 'N_Features', 'Accuracy', 'ROC_AUC']].to_string(index=False))
        
        # Save comparison
        df_results.to_csv(f'{output_dir}/comparison.csv', index=False)
        print(f"\n✓ Saved: {output_dir}/comparison.csv")
        
        # Plot comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        methods = df_results['Method']
        x_pos = np.arange(len(methods))
        
        # Accuracy comparison
        colors = ['#cccccc'] + ['#FF6D1F'] * (len(methods) - 1)
        ax1.bar(x_pos, df_results['Accuracy'], color=colors)
        ax1.set_ylabel('Accuracy', fontsize=12)
        ax1.set_title('Accuracy Comparison', fontsize=14, fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(methods, rotation=45, ha='right', fontsize=9)
        ax1.set_ylim([df_results['Accuracy'].min() - 0.05, 1.0])
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.axhline(y=acc_full, color='r', linestyle='--', alpha=0.5, label='Baseline')
        
        # ROC-AUC comparison
        ax2.bar(x_pos, df_results['ROC_AUC'], color=colors)
        ax2.set_ylabel('ROC-AUC', fontsize=12)
        ax2.set_title('ROC-AUC Comparison', fontsize=14, fontweight='bold')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(methods, rotation=45, ha='right', fontsize=9)
        ax2.set_ylim([df_results['ROC_AUC'].min() - 0.05, 1.0])
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.axhline(y=auc_full, color='r', linestyle='--', alpha=0.5, label='Baseline')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/method_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {output_dir}/method_comparison.png")
        
        return df_results


def main():
    print("="*60)
    print("Feature Selection Analysis")
    print("="*60)
    print()
    
    # Create output directory
    os.makedirs('models/feature_selection', exist_ok=True)
    
    selector = FeatureSelector()
    selector.load_data()
    
    # Run all methods
    selector.method_1_univariate_selection(k=3)
    selector.method_2_recursive_feature_elimination(n_features=3)
    selector.method_3_rfecv()
    selector.method_4_feature_importance(threshold='median')
    selector.method_5_correlation_analysis(threshold=0.8)
    selector.compare_all_methods()
    
    print("\n" + "="*60)
    print("✅ Feature Selection Analysis Complete!")
    print("="*60)
    print("\nGenerated files in models/feature_selection/:")
    print("  - rfecv_scores.png")
    print("  - feature_importances.png")
    print("  - correlation_matrix.png")
    print("  - method_comparison.png")
    print("  - comparison.csv")
    print("  - feature_importance_values.csv")
    print("  - correlation_matrix.csv")


if __name__ == '__main__':
    main()
