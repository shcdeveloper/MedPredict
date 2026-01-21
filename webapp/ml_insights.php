<?php
require_once 'config/auth.php';
require_once 'config/db.php';

requireLogin();
$user = getCurrentUser();

// Helper function to check and get image paths
function getImagePath($relativePath) {
    // Models folder is now inside webapp directory
    $fullPath = __DIR__ . '/models/' . str_replace('/models/', '', $relativePath);
    $urlPath = 'models/' . str_replace('/models/', '', $relativePath);
    return [
        'exists' => file_exists($fullPath),
        'path' => $fullPath,
        'url' => $urlPath
    ];
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ML Insights - Healthcare Admission System</title>
    <link rel="stylesheet" href="assets/css/admin.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .insights-section {
            margin-bottom: 40px;
        }
        
        .section-header {
            margin-bottom: 24px;
        }
        
        .section-title {
            font-size: 24px;
            font-weight: 600;
            color: var(--dark);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .section-description {
            color: var(--secondary);
            font-size: 14px;
            line-height: 1.6;
        }
        
        .viz-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 24px;
        }
        
        .viz-card {
            background: white;
            border-radius: 12px;
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .viz-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }
        
        .viz-header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 16px 20px;
            font-weight: 600;
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .viz-content {
            padding: 20px;
        }
        
        .viz-content img {
            width: 100%;
            height: auto;
            border-radius: 8px;
            border: 1px solid var(--border);
        }
        
        .viz-description {
            color: var(--secondary);
            font-size: 13px;
            margin-top: 12px;
            line-height: 1.6;
        }
        
        .download-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 12px;
            padding: 8px 16px;
            background: var(--primary);
            color: white;
            border-radius: 6px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
            transition: background 0.2s;
        }
        
        .download-btn:hover {
            background: var(--primary-dark);
        }
        
        .no-image {
            background: var(--light);
            padding: 60px 20px;
            text-align: center;
            color: var(--secondary);
            border-radius: 8px;
            border: 2px dashed var(--border);
        }
        
        .no-image i {
            font-size: 48px;
            color: var(--border);
            margin-bottom: 16px;
        }
        
        .info-box {
            background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
            border-left: 4px solid var(--primary);
            padding: 20px;
            margin: 24px 0;
            border-radius: 8px;
        }
        
        .info-box-title {
            color: var(--primary);
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .info-box p {
            color: var(--secondary);
            margin: 8px 0;
            font-size: 14px;
            line-height: 1.6;
        }
        
        .info-box code {
            background: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            color: var(--primary);
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <!-- Sidebar -->
    <div class="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-logo">
                <i class="fas fa-hospital"></i>
                <span>MedPredict</span>
            </div>
        </div>
        <nav class="sidebar-menu">
            <a href="dashboard.php" class="menu-item">
                <i class="fas fa-chart-line"></i>
                <span>Dashboard</span>
            </a>
            <a href="predict.php" class="menu-item">
                <i class="fas fa-stethoscope"></i>
                <span>Admission Prediction</span>
            </a>
            <a href="disease_risk.php" class="menu-item">
                <i class="fas fa-heartbeat"></i>
                <span>Disease Risk Assessment</span>
            </a>
            <a href="disease_risk_table.php" class="menu-item">
                <i class="fas fa-table"></i>
                <span>Risk Assessments Table</span>
            </a>
            <a href="patients.php" class="menu-item">
                <i class="fas fa-users"></i>
                <span>Patient History</span>
            </a>
            <a href="analytics.php" class="menu-item">
                <i class="fas fa-chart-bar"></i>
                <span>Analytics</span>
            </a>
            <a href="ml_insights.php" class="menu-item active">
                <i class="fas fa-brain"></i>
                <span>ML Insights</span>
            </a>
        </nav>
        <div class="sidebar-footer">
            <a href="logout.php" class="menu-item">
                <i class="fas fa-sign-out-alt"></i>
                <span>Logout</span>
            </a>
        </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
        <!-- Top Header -->
        <div class="top-header">
            <h1 class="header-title">Machine Learning Insights</h1>
            <div class="header-actions">
                <div class="user-menu">
                    <div class="user-avatar">
                        <?php echo strtoupper(substr($user['full_name'], 0, 1)); ?>
                    </div>
                    <div class="user-info">
                        <div class="user-name"><?php echo htmlspecialchars($user['full_name']); ?></div>
                        <div class="user-role"><?php echo htmlspecialchars($user['role']); ?></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Dashboard Content -->
        <div class="dashboard-content">
                <!-- Information Box -->
                <div class="info-box">
                    <div class="info-box-title">
                        <i class="fas fa-info-circle"></i>
                        About ML Insights
                    </div>
                    <p>This dashboard provides comprehensive analysis of the machine learning models used in the Healthcare Admission System. 
                    It includes model explainability (SHAP & LIME), feature selection comparisons, and dimensionality 
                    reduction techniques to understand which patient features are most important for predictions.</p>
                    <p><strong>Note:</strong> Run the analysis scripts to generate visualizations if images are not displayed.</p>
                </div>

                <!-- SECTION 1: Explainability -->
                <div class="insights-section">
                    <div class="section-header">
                        <h2 class="section-title">
                            <i class="fas fa-search"></i>
                            Model Explainability (SHAP & LIME)
                        </h2>
                        <p class="section-description">
                            Understanding which features drive predictions is crucial for trust and clinical adoption. 
                            SHAP (SHapley Additive exPlanations) and LIME (Local Interpretable Model-agnostic Explanations) 
                            provide insights into model decisions at both global and individual prediction levels.
                        </p>
                    </div>

                    <div class="viz-grid">
                        <!-- SHAP Summary -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-chart-bar"></i>
                                SHAP Summary Plot
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/explainability/shap_summary_plot.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="SHAP Summary Plot">
                                    <p class="viz-description">
                                        Shows the impact of each feature on model predictions. Each dot represents 
                                        a patient, colored by feature value (red=high, blue=low). Features are 
                                        ranked by importance from top to bottom.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-chart-bar"></i>
                                        <p>Visualization not found</p>
                                        <p style="font-size: 12px; margin-top: 8px;">Run: <code>python api/train_with_explainability.py</code></p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- SHAP Importance Bar -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-sort-amount-down"></i>
                                SHAP Feature Importance
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/explainability/shap_importance_bar.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="SHAP Importance">
                                    <p class="viz-description">
                                        Mean absolute SHAP values showing average feature importance across all 
                                        predictions. Higher values indicate greater impact on the model's decisions.
                                    </p>
                                    <a href="<?php echo $img_path; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- LIME Explanation -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-lightbulb"></i>
                                LIME Local Explanation
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/explainability/lime_explanation.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="LIME Explanation">
                                    <p class="viz-description">
                                        LIME creates a local linear approximation of the model around a specific 
                                        prediction, showing which features contributed most to that decision.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SECTION 2: Feature Selection -->
                <div class="insights-section">
                    <div class="section-header">
                        <h2 class="section-title">
                            <i class="fas fa-filter"></i>
                            Feature Selection Methods
                        </h2>
                        <p class="section-description">
                            Feature selection identifies the most informative features, improving model performance 
                            and reducing computational cost. We compare filter (univariate), wrapper (RFE), and 
                            embedded (importance-based) methods.
                        </p>
                    </div>

                    <div class="viz-grid">
                        <!-- RFECV Scores -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-sync-alt"></i>
                                RFECV: Optimal Feature Count
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/feature_selection/rfecv_scores.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="RFECV Scores">
                                    <p class="viz-description">
                                        Recursive Feature Elimination with Cross-Validation (RFECV) identifies 
                                        the optimal number of features by iteratively removing the least important 
                                        ones and evaluating model performance.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-sync-alt"></i>
                                        <p>Visualization not found</p>
                                        <p style="font-size: 12px; margin-top: 8px;">Run: <code>python api/feature_selection.py</code></p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- Feature Importances -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-star"></i>
                                Random Forest Feature Importances
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/feature_selection/feature_importances.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="Feature Importances">
                                    <p class="viz-description">
                                        Embedded feature importance from Random Forest. Orange bars indicate 
                                        features selected above the threshold. This method evaluates feature 
                                        importance during model training.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- Correlation Matrix -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-project-diagram"></i>
                                Feature Correlation Matrix
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/feature_selection/correlation_matrix.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="Correlation Matrix">
                                    <p class="viz-description">
                                        Correlation analysis identifies redundant features. Highly correlated 
                                        features (>0.8) can be removed to reduce multicollinearity and improve 
                                        model interpretability.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- Method Comparison -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-balance-scale"></i>
                                Feature Selection: Method Comparison
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/feature_selection/method_comparison.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="Method Comparison">
                                    <p class="viz-description">
                                        Compares accuracy and ROC-AUC across all feature selection methods. 
                                        Helps identify which approach provides the best balance between 
                                        feature reduction and model performance.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SECTION 3: Dimensionality Reduction -->
                <div class="insights-section">
                    <div class="section-header">
                        <h2 class="section-title">
                            <i class="fas fa-compress-arrows-alt"></i>
                            Dimensionality Reduction
                        </h2>
                        <p class="section-description">
                            Dimensionality reduction transforms high-dimensional data into lower dimensions while 
                            preserving important information. Useful for visualization, noise reduction, and 
                            computational efficiency.
                        </p>
                    </div>

                    <div class="viz-grid">
                        <!-- PCA Variance -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-chart-line"></i>
                                PCA: Explained Variance
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/dimensionality_reduction/pca_variance.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="PCA Variance">
                                    <p class="viz-description">
                                        Principal Component Analysis (PCA) variance plots show how much 
                                        information each component captures. The scree plot (left) and cumulative 
                                        variance (right) help determine optimal dimensionality.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-chart-line"></i>
                                        <p>Visualization not found</p>
                                        <p style="font-size: 12px; margin-top: 8px;">Run: <code>python api/dimensionality_reduction.py</code></p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- PCA Loadings -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-table"></i>
                                PCA Feature Loadings
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/dimensionality_reduction/pca_loadings.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="PCA Loadings">
                                    <p class="viz-description">
                                        Feature loadings show how original features contribute to principal 
                                        components. Red indicates positive contribution, blue negative. Helps 
                                        interpret what each component represents.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- Factor Analysis -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-th"></i>
                                Factor Analysis Loadings
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/dimensionality_reduction/factor_loadings.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="Factor Loadings">
                                    <p class="viz-description">
                                        Factor Analysis identifies latent factors underlying the data. Similar 
                                        to PCA but assumes a specific model for the covariance structure of 
                                        the data.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- t-SNE -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-dot-circle"></i>
                                t-SNE Visualization
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/dimensionality_reduction/tsne_visualization.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="t-SNE Visualization">
                                    <p class="viz-description">
                                        t-SNE (t-Distributed Stochastic Neighbor Embedding) projects 
                                        high-dimensional data into 2D for visualization. Good class separation 
                                        indicates the features capture meaningful patterns.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- Method Comparison -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-chart-area"></i>
                                Dimensionality Reduction: Method Comparison
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/dimensionality_reduction/method_comparison.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="Method Comparison">
                                    <p class="viz-description">
                                        Compares accuracy, ROC-AUC, dimensionality, and variance explained across 
                                        all reduction methods. Shows the trade-off between dimensionality and 
                                        model performance.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SECTION 4: Bias & Fairness Analysis -->
                <div class="insights-section">
                    <div class="section-header">
                        <h2 class="section-title">
                            <i class="fas fa-balance-scale"></i>
                            Bias & Fairness Analysis
                        </h2>
                        <p class="section-description">
                            Comprehensive audit of model predictions across demographic groups. Analyzes fairness 
                            metrics, detects potential biases, and provides mitigation strategies to ensure 
                            equitable healthcare predictions.
                        </p>
                    </div>

                    <div class="viz-grid">
                        <!-- Class Imbalance -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-chart-pie"></i>
                                Class Imbalance Analysis
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/bias_analysis/class_imbalance.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="Class Imbalance">
                                    <p class="viz-description">
                                        Distribution of admission vs non-admission cases in training data. 
                                        Severe imbalance can cause model bias toward the majority class.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Analysis not found</p>
                                        <p style="font-size: 12px; margin-top: 8px;">Run: <code>python api/bias_fairness_audit.py</code></p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- Gender Bias -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-venus-mars"></i>
                                Gender Bias Analysis
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/bias_analysis/gender_bias_analysis.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="Gender Bias">
                                    <p class="viz-description">
                                        Compares model predictions across gender groups. Includes fairness metrics: 
                                        demographic parity, disparate impact ratio, and equal opportunity.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- Age Bias -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-users"></i>
                                Age Group Bias Analysis
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/bias_analysis/age_bias_analysis.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="Age Bias">
                                    <p class="viz-description">
                                        Analyzes predictions across age groups (Young 18-40, Middle 41-60, Senior 61+). 
                                        Identifies age-related disparities in model performance.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- Fairness Metrics Report -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-file-alt"></i>
                                Fairness Metrics Summary
                            </div>
                            <div class="viz-content">
                                <?php 
                                $csv_path = __DIR__ . '/models/bias_analysis/fairness_metrics.csv';
                                if (file_exists($csv_path)): 
                                    $csv_data = array_map('str_getcsv', file($csv_path));
                                    $headers = array_shift($csv_data);
                                ?>
                                    <div style="overflow-x: auto; max-height: 300px; margin-bottom: 15px;">
                                        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                                            <thead style="background: #FF6D1F; color: white; position: sticky; top: 0;">
                                                <tr>
                                                    <?php foreach ($headers as $header): ?>
                                                        <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">
                                                            <?php echo htmlspecialchars($header); ?>
                                                        </th>
                                                    <?php endforeach; ?>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <?php foreach ($csv_data as $row): ?>
                                                    <tr style="border-bottom: 1px solid #eee;">
                                                        <?php foreach ($row as $cell): ?>
                                                            <td style="padding: 8px; border: 1px solid #ddd;">
                                                                <?php 
                                                                    // Format boolean values
                                                                    if (strtolower($cell) === 'true') {
                                                                        echo '<span style="color: #4CAF50; font-weight: bold;">✓ Pass</span>';
                                                                    } elseif (strtolower($cell) === 'false') {
                                                                        echo '<span style="color: #F44336; font-weight: bold;">✗ Fail</span>';
                                                                    } elseif (is_numeric($cell)) {
                                                                        echo number_format((float)$cell, 4);
                                                                    } else {
                                                                        echo htmlspecialchars($cell);
                                                                    }
                                                                ?>
                                                            </td>
                                                        <?php endforeach; ?>
                                                    </tr>
                                                <?php endforeach; ?>
                                            </tbody>
                                        </table>
                                    </div>
                                    <p class="viz-description">
                                        Quantitative fairness metrics including demographic parity, disparate impact, 
                                        and equal opportunity across demographic groups.
                                    </p>
                                    <a href="models/bias_analysis/fairness_metrics.csv" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download CSV
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Metrics not found</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- Mitigation Recommendations -->
                        <div class="viz-card" style="grid-column: span 2;">
                            <div class="viz-header">
                                <i class="fas fa-lightbulb"></i>
                                Bias Mitigation Recommendations
                            </div>
                            <div class="viz-content">
                                <?php 
                                $report_path = __DIR__ . '/models/bias_analysis/mitigation_recommendations.txt';
                                if (file_exists($report_path)): 
                                    $report = file_get_contents($report_path);
                                ?>
                                    <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; max-height: 400px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 12px; white-space: pre-wrap; line-height: 1.6;">
<?php echo htmlspecialchars($report); ?>
                                    </div>
                                    <p class="viz-description" style="margin-top: 15px;">
                                        Comprehensive recommendations for addressing identified biases including 
                                        pre-processing, in-processing, and post-processing mitigation strategies.
                                    </p>
                                    <a href="models/bias_analysis/mitigation_recommendations.txt" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download Report
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Report not found</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SECTION 5: Advanced Explainability (PDP & ICE) -->
                <div class="insights-section">
                    <div class="section-header">
                        <h2 class="section-title">
                            <i class="fas fa-chart-line"></i>
                            Advanced Explainability (PDP & ICE)
                        </h2>
                        <p class="section-description">
                            Partial Dependence Plots (PDP) and Individual Conditional Expectation (ICE) curves 
                            show how features affect model predictions at both population and individual levels.
                        </p>
                    </div>

                    <div class="viz-grid">
                        <!-- PDP All Features -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-chart-area"></i>
                                Partial Dependence Plots (PDP)
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/explainability/pdp_all_features.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="PDP All Features">
                                    <p class="viz-description">
                                        Shows the average effect of each feature on admission predictions. 
                                        Marginalizes out other features to isolate individual feature impact.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                        <p style="font-size: 12px; margin-top: 8px;">Run: <code>python api/pdp_ice_analysis.py</code></p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- ICE All Features -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-stream"></i>
                                ICE Plots (Individual Curves)
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/explainability/ice_all_features.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="ICE All Features">
                                    <p class="viz-description">
                                        Individual Conditional Expectation curves show how predictions change 
                                        for individual patients. Reveals heterogeneity in feature effects.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- Combined PDP + ICE -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-layer-group"></i>
                                Combined PDP + ICE
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/explainability/pdp_ice_combined.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="PDP ICE Combined">
                                    <p class="viz-description">
                                        Overlays individual patient curves (ICE) with population average (PDP). 
                                        Shows both average trends and individual variability.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- 2D Feature Interactions -->
                        <div class="viz-card">
                            <div class="viz-header">
                                <i class="fas fa-th"></i>
                                2D Feature Interactions
                            </div>
                            <div class="viz-content">
                                <?php 
                                $img = getImagePath('/models/explainability/pdp_2d_interactions.png');
                                if ($img['exists']): ?>
                                    <img src="<?php echo $img['url']; ?>" alt="2D PDP Interactions">
                                    <p class="viz-description">
                                        2D Partial Dependence Plots reveal how pairs of features interact to 
                                        affect predictions. Contour maps show joint feature effects.
                                    </p>
                                    <a href="<?php echo $img['url']; ?>" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Not generated</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>

                        <!-- PDP/ICE Summary Report -->
                        <div class="viz-card" style="grid-column: span 2;">
                            <div class="viz-header">
                                <i class="fas fa-file-medical"></i>
                                Clinical Interpretation Summary
                            </div>
                            <div class="viz-content">
                                <?php 
                                $summary_path = __DIR__ . '/models/explainability/pdp_ice_summary.txt';
                                if (file_exists($summary_path)): 
                                    $summary = file_get_contents($summary_path);
                                ?>
                                    <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; max-height: 400px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 12px; white-space: pre-wrap; line-height: 1.6;">
<?php echo htmlspecialchars($summary); ?>
                                    </div>
                                    <p class="viz-description" style="margin-top: 15px;">
                                        Clinical interpretation of PDP/ICE findings including feature impact 
                                        rankings and recommendations for healthcare decision-making.
                                    </p>
                                    <a href="models/explainability/pdp_ice_summary.txt" download class="download-btn">
                                        <i class="fas fa-download"></i>
                                        Download Summary
                                    </a>
                                <?php else: ?>
                                    <div class="no-image">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <p>Summary not found</p>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Run Analysis Section -->
                <div class="info-box" style="margin-top: 40px;">
                    <div class="info-box-title">
                        <i class="fas fa-terminal"></i>
                        Generate Visualizations
                    </div>
                    <p>If visualizations are missing, run these commands in your terminal:</p>
                    <p><code>python api/train_with_explainability.py</code> - Generate SHAP & LIME explanations</p>
                    <p><code>python api/feature_selection.py</code> - Run feature selection methods</p>
                    <p><code>python api/dimensionality_reduction.py</code> - Run dimensionality reduction analysis</p>
                    <p><code>python api/bias_fairness_audit.py</code> - Run bias & fairness audit</p>
                    <p><code>python api/pdp_ice_analysis.py</code> - Generate PDP & ICE plots</p>
                    <p style="margin-top: 10px;"><strong>Prerequisites:</strong> <code>pip install shap lime matplotlib seaborn</code></p>
                </div>

            </div>
        </div>
    </body>
</html>
