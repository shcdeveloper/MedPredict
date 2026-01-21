"""
Dimensionality Reduction Techniques for Healthcare Data
Implements: PCA, SVD, Factor Analysis, t-SNE
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA, TruncatedSVD, FactorAnalysis
from sklearn.manifold import TSNE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib
import os
import warnings
warnings.filterwarnings('ignore')


class DimensionalityReducer:
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
        
        print(f"✓ Data loaded: {self.X_train.shape[1]} features, {len(self.y_train)} samples")
        return self
    
    def method_1_pca(self, n_components=None, output_dir='models/dimensionality_reduction'):
        """Principal Component Analysis"""
        print(f"\n{'='*60}")
        print(f"METHOD 1: Principal Component Analysis (PCA)")
        print(f"{'='*60}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # PCA with all components
        pca_full = PCA()
        pca_full.fit(self.X_train)
        
        explained_variance = pca_full.explained_variance_ratio_
        cumulative_variance = np.cumsum(explained_variance)
        
        # Determine components for 95% variance
        n_95 = np.argmax(cumulative_variance >= 0.95) + 1
        
        print(f"\nExplained Variance:")
        for i in range(min(5, len(explained_variance))):
            print(f"  PC{i+1}: {explained_variance[i]:.4f} ({cumulative_variance[i]:.4f} cumulative)")
        
        print(f"\nComponents needed for 95% variance: {n_95}")
        
        # Plot scree plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Individual variance
        ax1.bar(range(1, len(explained_variance) + 1), explained_variance, color='#FF6D1F')
        ax1.set_xlabel('Principal Component', fontsize=12)
        ax1.set_ylabel('Explained Variance Ratio', fontsize=12)
        ax1.set_title('PCA Scree Plot', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Cumulative variance
        ax2.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, 'b-', linewidth=2)
        ax2.axhline(y=0.95, color='r', linestyle='--', linewidth=2, label='95% Threshold')
        ax2.axvline(x=n_95, color='g', linestyle='--', linewidth=2, label=f'{n_95} Components')
        ax2.set_xlabel('Number of Components', fontsize=12)
        ax2.set_ylabel('Cumulative Explained Variance', fontsize=12)
        ax2.set_title('Cumulative Variance Explained', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/pca_variance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/pca_variance.png")
        
        # Feature loadings for first 3 PCs
        loadings = pca_full.components_[:3, :]
        loadings_df = pd.DataFrame(
            loadings.T,
            columns=[f'PC{i+1}' for i in range(3)],
            index=self.feature_names
        )
        
        print(f"\nTop Feature Loadings (PC1-PC3):")
        for pc in ['PC1', 'PC2', 'PC3']:
            top_features = loadings_df[pc].abs().sort_values(ascending=False).head(3)
            print(f"\n{pc}:")
            for feat, val in top_features.items():
                print(f"  - {feat}: {loadings_df.loc[feat, pc]:.4f}")
        
        # Plot loadings heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(loadings_df.T, cmap='coolwarm', center=0, annot=False, 
                   cbar_kws={'label': 'Loading'}, linewidths=0.5)
        plt.title('PCA Feature Loadings (First 3 Components)', fontsize=14, fontweight='bold')
        plt.xlabel('Features', fontsize=12)
        plt.ylabel('Principal Component', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/pca_loadings.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {output_dir}/pca_loadings.png")
        
        # Save loadings
        loadings_df.to_csv(f'{output_dir}/pca_loadings.csv')
        print(f"✓ Saved: {output_dir}/pca_loadings.csv")
        
        # Evaluate with reduced dimensions
        if n_components is None:
            n_components = n_95
        
        pca = PCA(n_components=n_components)
        X_train_pca = pca.fit_transform(self.X_train)
        X_test_pca = pca.transform(self.X_test)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train_pca, self.y_train)
        y_pred = model.predict(X_test_pca)
        accuracy = accuracy_score(self.y_test, y_pred)
        auc = roc_auc_score(self.y_test, model.predict_proba(X_test_pca)[:, 1])
        
        print(f"\nPerformance with {n_components} components:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  ROC-AUC: {auc:.4f}")
        
        self.results.append({
            'Method': 'PCA',
            'N_Components': n_components,
            'Variance_Explained': cumulative_variance[n_components-1],
            'Accuracy': accuracy,
            'ROC_AUC': auc
        })
        
        return pca, n_95
    
    def method_2_svd(self, n_components=3, output_dir='models/dimensionality_reduction'):
        """Truncated Singular Value Decomposition"""
        print(f"\n{'='*60}")
        print(f"METHOD 2: Truncated SVD")
        print(f"{'='*60}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        svd = TruncatedSVD(n_components=n_components, random_state=42)
        X_train_svd = svd.fit_transform(self.X_train)
        X_test_svd = svd.transform(self.X_test)
        
        explained_variance = svd.explained_variance_ratio_
        cumulative_variance = np.sum(explained_variance)
        
        print(f"\nExplained Variance (n_components={n_components}):")
        for i, var in enumerate(explained_variance):
            print(f"  Component {i+1}: {var:.4f}")
        print(f"  Total: {cumulative_variance:.4f}")
        
        # Evaluate
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train_svd, self.y_train)
        y_pred = model.predict(X_test_svd)
        accuracy = accuracy_score(self.y_test, y_pred)
        auc = roc_auc_score(self.y_test, model.predict_proba(X_test_svd)[:, 1])
        
        print(f"\nPerformance:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  ROC-AUC: {auc:.4f}")
        
        self.results.append({
            'Method': 'Truncated SVD',
            'N_Components': n_components,
            'Variance_Explained': cumulative_variance,
            'Accuracy': accuracy,
            'ROC_AUC': auc
        })
        
        return svd
    
    def method_3_factor_analysis(self, n_components=3, output_dir='models/dimensionality_reduction'):
        """Factor Analysis"""
        print(f"\n{'='*60}")
        print(f"METHOD 3: Factor Analysis")
        print(f"{'='*60}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        fa = FactorAnalysis(n_components=n_components, random_state=42)
        X_train_fa = fa.fit_transform(self.X_train)
        X_test_fa = fa.transform(self.X_test)
        
        # Get factor loadings
        loadings = fa.components_.T
        loadings_df = pd.DataFrame(
            loadings,
            columns=[f'Factor{i+1}' for i in range(n_components)],
            index=self.feature_names
        )
        
        print(f"\nFactor Loadings (n_components={n_components}):")
        for factor in loadings_df.columns:
            print(f"\n{factor} - Top 3 Features:")
            top = loadings_df[factor].abs().sort_values(ascending=False).head(3)
            for feat, val in top.items():
                print(f"  - {feat}: {loadings_df.loc[feat, factor]:.4f}")
        
        # Plot loadings heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(loadings_df.T, cmap='coolwarm', center=0, annot=False,
                   cbar_kws={'label': 'Loading'}, linewidths=0.5)
        plt.title('Factor Analysis Loadings', fontsize=14, fontweight='bold')
        plt.xlabel('Features', fontsize=12)
        plt.ylabel('Factor', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/factor_loadings.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/factor_loadings.png")
        
        # Save loadings
        loadings_df.to_csv(f'{output_dir}/factor_loadings.csv')
        print(f"✓ Saved: {output_dir}/factor_loadings.csv")
        
        # Evaluate
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train_fa, self.y_train)
        y_pred = model.predict(X_test_fa)
        accuracy = accuracy_score(self.y_test, y_pred)
        auc = roc_auc_score(self.y_test, model.predict_proba(X_test_fa)[:, 1])
        
        print(f"\nPerformance:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  ROC-AUC: {auc:.4f}")
        
        self.results.append({
            'Method': 'Factor Analysis',
            'N_Components': n_components,
            'Variance_Explained': None,
            'Accuracy': accuracy,
            'ROC_AUC': auc
        })
        
        return fa
    
    def method_4_tsne(self, n_components=2, perplexity=30, output_dir='models/dimensionality_reduction'):
        """t-SNE Visualization"""
        print(f"\n{'='*60}")
        print(f"METHOD 4: t-SNE (t-Distributed Stochastic Neighbor Embedding)")
        print(f"{'='*60}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nRunning t-SNE (perplexity={perplexity}, n_components={n_components})...")
        print("This may take a moment...")
        
        # Use subset for faster computation
        n_samples = min(1000, len(self.X_train))
        X_sample = self.X_train[:n_samples]
        y_sample = self.y_train[:n_samples]
        
        tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=42, 
                   max_iter=1000, verbose=0)
        X_tsne = tsne.fit_transform(X_sample)
        
        print("✓ t-SNE transformation complete")
        
        # Plot 2D visualization
        plt.figure(figsize=(10, 8))
        colors = ['#1f77b4', '#ff7f0e']  # Blue for 0, Orange for 1
        labels = ['No Admission', 'Admission']
        
        for i, (color, label) in enumerate(zip(colors, labels)):
            mask = y_sample == i
            plt.scatter(
                X_tsne[mask, 0], 
                X_tsne[mask, 1],
                c=color, 
                label=label, 
                alpha=0.6, 
                s=30,
                edgecolors='w',
                linewidths=0.5
            )
        
        plt.xlabel('t-SNE Dimension 1', fontsize=12)
        plt.ylabel('t-SNE Dimension 2', fontsize=12)
        plt.title('t-SNE Visualization of Healthcare Data', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10, loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/tsne_visualization.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\n✓ Saved: {output_dir}/tsne_visualization.png")
        
        # Note: t-SNE is primarily for visualization, not typically used for classification
        print("\nNote: t-SNE is primarily a visualization technique, not for dimensionality")
        print("reduction before classification. The plot shows how well classes separate.")
        
        return tsne
    
    def compare_methods(self, output_dir='models/dimensionality_reduction'):
        """Compare all dimensionality reduction methods"""
        print(f"\n{'='*60}")
        print(f"COMPARISON: All Dimensionality Reduction Methods")
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
            'N_Components': self.X_train.shape[1],
            'Variance_Explained': 1.0,
            'Accuracy': acc_full,
            'ROC_AUC': auc_full
        }
        
        all_results = [baseline] + self.results
        df_results = pd.DataFrame(all_results)
        
        print("\nComparison Results:")
        print(df_results[['Method', 'N_Components', 'Variance_Explained', 'Accuracy', 'ROC_AUC']].to_string(index=False))
        
        # Save comparison
        df_results.to_csv(f'{output_dir}/comparison.csv', index=False)
        print(f"\n✓ Saved: {output_dir}/comparison.csv")
        
        # Plot comparison
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        methods = df_results['Method']
        x_pos = np.arange(len(methods))
        colors = ['#cccccc'] + ['#FF6D1F'] * (len(methods) - 1)
        
        # Accuracy
        axes[0, 0].bar(x_pos, df_results['Accuracy'], color=colors)
        axes[0, 0].set_ylabel('Accuracy', fontsize=11)
        axes[0, 0].set_title('Accuracy Comparison', fontsize=12, fontweight='bold')
        axes[0, 0].set_xticks(x_pos)
        axes[0, 0].set_xticklabels(methods, rotation=45, ha='right', fontsize=9)
        axes[0, 0].set_ylim([df_results['Accuracy'].min() - 0.05, 1.0])
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        axes[0, 0].axhline(y=acc_full, color='r', linestyle='--', alpha=0.5)
        
        # ROC-AUC
        axes[0, 1].bar(x_pos, df_results['ROC_AUC'], color=colors)
        axes[0, 1].set_ylabel('ROC-AUC', fontsize=11)
        axes[0, 1].set_title('ROC-AUC Comparison', fontsize=12, fontweight='bold')
        axes[0, 1].set_xticks(x_pos)
        axes[0, 1].set_xticklabels(methods, rotation=45, ha='right', fontsize=9)
        axes[0, 1].set_ylim([df_results['ROC_AUC'].min() - 0.05, 1.0])
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        axes[0, 1].axhline(y=auc_full, color='r', linestyle='--', alpha=0.5)
        
        # Number of components
        axes[1, 0].bar(x_pos, df_results['N_Components'], color=colors)
        axes[1, 0].set_ylabel('Number of Components', fontsize=11)
        axes[1, 0].set_title('Dimensionality Comparison', fontsize=12, fontweight='bold')
        axes[1, 0].set_xticks(x_pos)
        axes[1, 0].set_xticklabels(methods, rotation=45, ha='right', fontsize=9)
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Variance explained (where applicable)
        variance_data = df_results['Variance_Explained'].fillna(0)
        axes[1, 1].bar(x_pos, variance_data, color=colors)
        axes[1, 1].set_ylabel('Variance Explained', fontsize=11)
        axes[1, 1].set_title('Variance Explained (PCA/SVD)', fontsize=12, fontweight='bold')
        axes[1, 1].set_xticks(x_pos)
        axes[1, 1].set_xticklabels(methods, rotation=45, ha='right', fontsize=9)
        axes[1, 1].set_ylim([0, 1.1])
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/method_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {output_dir}/method_comparison.png")
        
        return df_results


def main():
    print("="*60)
    print("Dimensionality Reduction Analysis")
    print("="*60)
    print()
    
    # Create output directory
    os.makedirs('models/dimensionality_reduction', exist_ok=True)
    
    reducer = DimensionalityReducer()
    reducer.load_data()
    
    # Run all methods
    reducer.method_1_pca()
    reducer.method_2_svd(n_components=3)
    reducer.method_3_factor_analysis(n_components=3)
    reducer.method_4_tsne(n_components=2, perplexity=30)
    reducer.compare_methods()
    
    print("\n" + "="*60)
    print("✅ Dimensionality Reduction Analysis Complete!")
    print("="*60)
    print("\nGenerated files in models/dimensionality_reduction/:")
    print("  - pca_variance.png")
    print("  - pca_loadings.png")
    print("  - factor_loadings.png")
    print("  - tsne_visualization.png")
    print("  - method_comparison.png")
    print("  - comparison.csv")
    print("  - pca_loadings.csv")
    print("  - factor_loadings.csv")


if __name__ == '__main__':
    main()
