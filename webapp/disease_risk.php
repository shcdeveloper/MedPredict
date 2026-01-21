<?php
require_once 'config/auth.php';
require_once 'config/db.php';

requireLogin();
$user = getCurrentUser();

$prediction_result = null;
$error = null;

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Collect form data
    $data = [
        'age' => intval($_POST['age']),
        'gender' => $_POST['gender'],
        'bmi' => floatval($_POST['bmi']),
        'smoking' => $_POST['smoking'],
        'alcohol' => $_POST['alcohol'],
        'exercise' => $_POST['exercise'],
        'family_diabetes' => intval($_POST['family_diabetes']),
        'family_heart_disease' => intval($_POST['family_heart_disease']),
        'family_hypertension' => intval($_POST['family_hypertension']),
        'systolic_bp' => floatval($_POST['systolic_bp']),
        'diastolic_bp' => floatval($_POST['diastolic_bp']),
        'heart_rate' => floatval($_POST['heart_rate']),
        'glucose' => floatval($_POST['glucose']),
        'cholesterol' => floatval($_POST['cholesterol']),
        'hdl' => floatval($_POST['hdl']),
        'ldl' => floatval($_POST['ldl']),
        'triglycerides' => floatval($_POST['triglycerides'])
    ];
    
    // Call API
    $api_url = 'http://localhost:8000/predict-disease';
    $options = [
        'http' => [
            'header'  => "Content-type: application/json\r\n",
            'method'  => 'POST',
            'content' => json_encode($data),
            'ignore_errors' => true
        ]
    ];
    
    $context  = stream_context_create($options);
    $result = @file_get_contents($api_url, false, $context);
    
    if ($result === FALSE) {
        $error = "Unable to connect to prediction API. Please ensure the API server is running on port 8000.";
    } else {
        $prediction_result = json_decode($result, true);
        
        // Check for API errors
        if ($prediction_result && isset($prediction_result['detail'])) {
            // Handle both string and array error messages
            $error_detail = is_array($prediction_result['detail']) ? json_encode($prediction_result['detail']) : $prediction_result['detail'];
            $error = "Prediction Error: " . $error_detail;
            $prediction_result = null;
        } elseif (!$prediction_result || !isset($prediction_result['diabetes_risk'])) {
            $error = "Invalid response from API. Response: " . substr($result, 0, 200);
            $prediction_result = null;
        } else {
            // Save to database
            try {
                $pdo = getPDOConnection();
                $stmt = $pdo->prepare("
                    INSERT INTO disease_risk_assessments (
                        assessed_by, age, gender, bmi, smoking, alcohol, exercise,
                        family_diabetes, family_heart_disease, family_hypertension,
                        systolic_bp, diastolic_bp, heart_rate,
                        glucose, cholesterol, hdl, ldl, triglycerides,
                        diabetes_risk, diabetes_level,
                        heart_disease_risk, heart_disease_level,
                        hypertension_risk, hypertension_level,
                        overall_risk
                    ) VALUES (
                        :assessed_by, :age, :gender, :bmi, :smoking, :alcohol, :exercise,
                        :family_diabetes, :family_heart_disease, :family_hypertension,
                        :systolic_bp, :diastolic_bp, :heart_rate,
                        :glucose, :cholesterol, :hdl, :ldl, :triglycerides,
                        :diabetes_risk, :diabetes_level,
                        :heart_disease_risk, :heart_disease_level,
                        :hypertension_risk, :hypertension_level,
                        :overall_risk
                    )
                ");
                
                $stmt->execute([
                    ':assessed_by' => $user['username'],
                    ':age' => $data['age'],
                    ':gender' => $data['gender'],
                    ':bmi' => $data['bmi'],
                    ':smoking' => $data['smoking'],
                    ':alcohol' => $data['alcohol'],
                    ':exercise' => $data['exercise'],
                    ':family_diabetes' => $data['family_diabetes'],
                    ':family_heart_disease' => $data['family_heart_disease'],
                    ':family_hypertension' => $data['family_hypertension'],
                    ':systolic_bp' => $data['systolic_bp'],
                    ':diastolic_bp' => $data['diastolic_bp'],
                    ':heart_rate' => $data['heart_rate'],
                    ':glucose' => $data['glucose'],
                    ':cholesterol' => $data['cholesterol'],
                    ':hdl' => $data['hdl'],
                    ':ldl' => $data['ldl'],
                    ':triglycerides' => $data['triglycerides'],
                    ':diabetes_risk' => $prediction_result['diabetes_risk'],
                    ':diabetes_level' => $prediction_result['diabetes_level'],
                    ':heart_disease_risk' => $prediction_result['heart_disease_risk'],
                    ':heart_disease_level' => $prediction_result['heart_disease_level'],
                    ':hypertension_risk' => $prediction_result['hypertension_risk'],
                    ':hypertension_level' => $prediction_result['hypertension_level'],
                    ':overall_risk' => $prediction_result['overall_risk']
                ]);
            } catch (PDOException $e) {
                // Log error but don't fail the prediction display
                error_log("Failed to save disease risk assessment: " . $e->getMessage());
            }
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disease Risk Assessment - Healthcare System</title>
    <link rel="stylesheet" href="assets/css/admin.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .risk-form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        
        .form-section {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: var(--shadow);
        }
        
        .form-section h3 {
            margin: 0 0 20px 0;
            color: var(--dark);
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--primary);
        }
        
        .form-section h3 i {
            color: var(--primary);
        }
        
        .risk-results {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 32px;
        }
        
        .risk-card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: var(--shadow);
            border-left: 4px solid;
        }
        
        .risk-card.diabetes { border-color: #f59e0b; }
        .risk-card.heart { border-color: #ef4444; }
        .risk-card.hypertension { border-color: #8b5cf6; }
        
        .risk-card h4 {
            margin: 0 0 16px 0;
            color: var(--dark);
            font-size: 18px;
        }
        
        .risk-meter {
            position: relative;
            height: 60px;
            background: #f1f5f9;
            border-radius: 30px;
            overflow: hidden;
            margin: 16px 0;
        }
        
        .risk-meter-fill {
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            transition: width 0.5s ease;
        }
        
        .risk-meter-fill.low { background: linear-gradient(90deg, #10b981, #34d399); }
        .risk-meter-fill.medium { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
        .risk-meter-fill.high { background: linear-gradient(90deg, #ef4444, #f87171); }
        
        .recommendations {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: var(--shadow);
            margin-top: 24px;
        }
        
        .recommendations h3 {
            margin: 0 0 16px 0;
            color: var(--dark);
            font-size: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .recommendations ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .recommendations li {
            padding: 12px;
            margin-bottom: 8px;
            background: #f8fafc;
            border-left: 3px solid var(--primary);
            border-radius: 4px;
        }
        
        .recommendations li i {
            color: var(--primary);
            margin-right: 8px;
        }
        
        .overall-risk {
            background: white;
            padding: 32px;
            border-radius: 12px;
            box-shadow: var(--shadow-lg);
            text-align: center;
            margin-bottom: 24px;
        }
        
        .overall-risk h2 {
            margin: 0 0 16px 0;
            font-size: 24px;
        }
        
        .overall-risk .risk-badge {
            display: inline-block;
            padding: 12px 32px;
            border-radius: 50px;
            font-size: 24px;
            font-weight: 700;
            color: white;
        }
        
        .overall-risk .risk-badge.low { background: linear-gradient(135deg, #10b981, #059669); }
        .overall-risk .risk-badge.moderate { background: linear-gradient(135deg, #3b82f6, #2563eb); }
        .overall-risk .risk-badge.elevated { background: linear-gradient(135deg, #f59e0b, #d97706); }
        .overall-risk .risk-badge.critical { background: linear-gradient(135deg, #ef4444, #dc2626); }
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
            <a href="disease_risk.php" class="menu-item active">
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
            <a href="ml_insights.php" class="menu-item">
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
            <h1 class="header-title">Disease Risk Assessment</h1>
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
            <?php if ($error): ?>
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle"></i>
                    <?php echo htmlspecialchars($error); ?>
                </div>
            <?php endif; ?>

            <?php if ($prediction_result && isset($prediction_result['diabetes_risk'])): ?>
                <!-- Overall Risk -->
                <div class="overall-risk">
                    <h2>Overall Health Risk Assessment</h2>
                    <div class="risk-badge <?php echo strtolower($prediction_result['overall_risk'] ?? 'low'); ?>">
                        <?php echo strtoupper($prediction_result['overall_risk'] ?? 'UNKNOWN'); ?>
                    </div>
                </div>

                <!-- Disease Risk Cards -->
                <div class="risk-results">
                    <!-- Diabetes -->
                    <div class="risk-card diabetes">
                        <h4><i class="fas fa-syringe"></i> Diabetes Risk</h4>
                        <div class="risk-meter">
                            <div class="risk-meter-fill <?php echo strtolower($prediction_result['diabetes_level'] ?? 'low'); ?>" 
                                 style="width: <?php echo ($prediction_result['diabetes_risk'] * 100); ?>%">
                                <?php echo round($prediction_result['diabetes_risk'] * 100); ?>%
                            </div>
                        </div>
                        <p><strong>Risk Level:</strong> <span class="badge"><?php echo $prediction_result['diabetes_level'] ?? 'Unknown'; ?></span></p>
                    </div>

                    <!-- Heart Disease -->
                    <div class="risk-card heart">
                        <h4><i class="fas fa-heart"></i> Heart Disease Risk</h4>
                        <div class="risk-meter">
                            <div class="risk-meter-fill <?php echo strtolower($prediction_result['heart_disease_level'] ?? 'low'); ?>" 
                                 style="width: <?php echo ($prediction_result['heart_disease_risk'] * 100); ?>%">
                                <?php echo round($prediction_result['heart_disease_risk'] * 100); ?>%
                            </div>
                        </div>
                        <p><strong>Risk Level:</strong> <span class="badge"><?php echo $prediction_result['heart_disease_level'] ?? 'Unknown'; ?></span></p>
                    </div>

                    <!-- Hypertension -->
                    <div class="risk-card hypertension">
                        <h4><i class="fas fa-heartbeat"></i> Hypertension Risk</h4>
                        <div class="risk-meter">
                            <div class="risk-meter-fill <?php echo strtolower($prediction_result['hypertension_level'] ?? 'low'); ?>" 
                                 style="width: <?php echo ($prediction_result['hypertension_risk'] * 100); ?>%">
                                <?php echo round($prediction_result['hypertension_risk'] * 100); ?>%
                            </div>
                        </div>
                        <p><strong>Risk Level:</strong> <span class="badge"><?php echo $prediction_result['hypertension_level'] ?? 'Unknown'; ?></span></p>
                    </div>
                </div>

                <!-- Recommendations -->
                <div class="recommendations">
                    <h3><i class="fas fa-clipboard-list"></i> Personalized Recommendations</h3>
                    <ul>
                        <?php 
                        $recommendations = $prediction_result['recommendations'] ?? [];
                        if (!empty($recommendations)):
                            foreach ($recommendations as $recommendation): 
                        ?>
                            <li>
                                <i class="fas fa-check-circle"></i>
                                <?php echo htmlspecialchars($recommendation); ?>
                            </li>
                        <?php 
                            endforeach;
                        else:
                        ?>
                            <li><i class="fas fa-info-circle"></i> No specific recommendations at this time.</li>
                        <?php endif; ?>
                    </ul>
                </div>
            <?php endif; ?>

            <!-- Assessment Form -->
            <div class="card" style="margin-top: 24px;">
                <div class="card-header">
                    <h2 class="card-title">
                        <i class="fas fa-file-medical"></i>
                        Comprehensive Health Assessment
                    </h2>
                </div>
                <div class="card-body">
                    <form method="POST" action="disease_risk.php">
                        <div class="risk-form-grid">
                            <!-- Demographics -->
                            <div class="form-section">
                                <h3><i class="fas fa-user"></i> Demographics</h3>
                                <div class="form-group">
                                    <label class="form-label">Age</label>
                                    <input type="number" name="age" class="form-input" min="18" max="100" required value="<?php echo $_POST['age'] ?? ''; ?>">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Gender</label>
                                    <select name="gender" class="form-input" required>
                                        <option value="">Select...</option>
                                        <option value="Male" <?php echo (isset($_POST['gender']) && $_POST['gender'] == 'Male') ? 'selected' : ''; ?>>Male</option>
                                        <option value="Female" <?php echo (isset($_POST['gender']) && $_POST['gender'] == 'Female') ? 'selected' : ''; ?>>Female</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">BMI</label>
                                    <input type="number" name="bmi" class="form-input" step="0.1" min="15" max="50" required value="<?php echo $_POST['bmi'] ?? ''; ?>">
                                    <small>Body Mass Index (15-50)</small>
                                </div>
                            </div>

                            <!-- Lifestyle -->
                            <div class="form-section">
                                <h3><i class="fas fa-running"></i> Lifestyle Factors</h3>
                                <div class="form-group">
                                    <label class="form-label">Smoking Status</label>
                                    <select name="smoking" class="form-input" required>
                                        <option value="">Select...</option>
                                        <option value="Never" <?php echo (isset($_POST['smoking']) && $_POST['smoking'] == 'Never') ? 'selected' : ''; ?>>Never</option>
                                        <option value="Former" <?php echo (isset($_POST['smoking']) && $_POST['smoking'] == 'Former') ? 'selected' : ''; ?>>Former</option>
                                        <option value="Current" <?php echo (isset($_POST['smoking']) && $_POST['smoking'] == 'Current') ? 'selected' : ''; ?>>Current</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Alcohol Consumption</label>
                                    <select name="alcohol" class="form-input" required>
                                        <option value="">Select...</option>
                                        <option value="None" <?php echo (isset($_POST['alcohol']) && $_POST['alcohol'] == 'None') ? 'selected' : ''; ?>>None</option>
                                        <option value="Moderate" <?php echo (isset($_POST['alcohol']) && $_POST['alcohol'] == 'Moderate') ? 'selected' : ''; ?>>Moderate</option>
                                        <option value="Heavy" <?php echo (isset($_POST['alcohol']) && $_POST['alcohol'] == 'Heavy') ? 'selected' : ''; ?>>Heavy</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Exercise Level</label>
                                    <select name="exercise" class="form-input" required>
                                        <option value="">Select...</option>
                                        <option value="Sedentary" <?php echo (isset($_POST['exercise']) && $_POST['exercise'] == 'Sedentary') ? 'selected' : ''; ?>>Sedentary</option>
                                        <option value="Light" <?php echo (isset($_POST['exercise']) && $_POST['exercise'] == 'Light') ? 'selected' : ''; ?>>Light</option>
                                        <option value="Moderate" <?php echo (isset($_POST['exercise']) && $_POST['exercise'] == 'Moderate') ? 'selected' : ''; ?>>Moderate</option>
                                        <option value="Active" <?php echo (isset($_POST['exercise']) && $_POST['exercise'] == 'Active') ? 'selected' : ''; ?>>Active</option>
                                    </select>
                                </div>
                            </div>

                            <!-- Family History -->
                            <div class="form-section">
                                <h3><i class="fas fa-dna"></i> Family History</h3>
                                <div class="form-group">
                                    <label class="form-label">
                                        <input type="checkbox" name="family_diabetes" value="1" <?php echo (isset($_POST['family_diabetes']) && $_POST['family_diabetes'] == '1') ? 'checked' : ''; ?>>
                                        Diabetes in Family
                                    </label>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">
                                        <input type="checkbox" name="family_heart_disease" value="1" <?php echo (isset($_POST['family_heart_disease']) && $_POST['family_heart_disease'] == '1') ? 'checked' : ''; ?>>
                                        Heart Disease in Family
                                    </label>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">
                                        <input type="checkbox" name="family_hypertension" value="1" <?php echo (isset($_POST['family_hypertension']) && $_POST['family_hypertension'] == '1') ? 'checked' : ''; ?>>
                                        Hypertension in Family
                                    </label>
                                </div>
                            </div>

                            <!-- Vital Signs -->
                            <div class="form-section">
                                <h3><i class="fas fa-heartbeat"></i> Vital Signs</h3>
                                <div class="form-group">
                                    <label class="form-label">Systolic BP (mmHg)</label>
                                    <input type="number" name="systolic_bp" class="form-input" min="80" max="220" required value="<?php echo $_POST['systolic_bp'] ?? ''; ?>">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Diastolic BP (mmHg)</label>
                                    <input type="number" name="diastolic_bp" class="form-input" min="50" max="140" required value="<?php echo $_POST['diastolic_bp'] ?? ''; ?>">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Heart Rate (bpm)</label>
                                    <input type="number" name="heart_rate" class="form-input" min="40" max="150" required value="<?php echo $_POST['heart_rate'] ?? ''; ?>">
                                </div>
                            </div>

                            <!-- Lab Results -->
                            <div class="form-section">
                                <h3><i class="fas fa-flask"></i> Lab Results</h3>
                                <div class="form-group">
                                    <label class="form-label">Glucose (mg/dL)</label>
                                    <input type="number" name="glucose" class="form-input" min="50" max="400" required value="<?php echo $_POST['glucose'] ?? ''; ?>">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Total Cholesterol (mg/dL)</label>
                                    <input type="number" name="cholesterol" class="form-input" min="100" max="400" required value="<?php echo $_POST['cholesterol'] ?? ''; ?>">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">HDL Cholesterol (mg/dL)</label>
                                    <input type="number" name="hdl" class="form-input" min="20" max="120" required value="<?php echo $_POST['hdl'] ?? ''; ?>">
                                </div>
                            </div>

                            <!-- Additional Labs -->
                            <div class="form-section">
                                <h3><i class="fas fa-vial"></i> Additional Labs</h3>
                                <div class="form-group">
                                    <label class="form-label">LDL Cholesterol (mg/dL)</label>
                                    <input type="number" name="ldl" class="form-input" min="40" max="300" required value="<?php echo $_POST['ldl'] ?? ''; ?>">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Triglycerides (mg/dL)</label>
                                    <input type="number" name="triglycerides" class="form-input" min="30" max="500" required value="<?php echo $_POST['triglycerides'] ?? ''; ?>">
                                </div>
                            </div>
                        </div>

                        <button type="submit" class="btn btn-primary btn-lg" style="width: 100%; margin-top: 24px;">
                            <i class="fas fa-chart-line"></i> Calculate Disease Risk
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Hidden fields for unchecked checkboxes
        document.querySelector('form').addEventListener('submit', function(e) {
            if (!document.querySelector('input[name="family_diabetes"]').checked) {
                let input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'family_diabetes';
                input.value = '0';
                this.appendChild(input);
            }
            if (!document.querySelector('input[name="family_heart_disease"]').checked) {
                let input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'family_heart_disease';
                input.value = '0';
                this.appendChild(input);
            }
            if (!document.querySelector('input[name="family_hypertension"]').checked) {
                let input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'family_hypertension';
                input.value = '0';
                this.appendChild(input);
            }
        });
    </script>
</body>
</html>
