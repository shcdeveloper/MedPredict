<?php
require_once 'config/auth.php';
requireLogin();
$user = getCurrentUser();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Prediction - Healthcare Admission System</title>
    <link rel="stylesheet" href="assets/css/admin.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
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
            <a href="predict.php" class="menu-item active">
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
            <h1 class="header-title">New Admission Risk Prediction</h1>
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
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <i class="fas fa-user-md"></i> Patient Information
                    </h2>
                    <span style="font-size: 14px; color: #64748b;">
                        Fill in patient details to assess admission risk
                    </span>
                </div>
                <div class="card-body">
                    <form action="submit_prediction.php" method="POST" id="predictionForm">
                        <!-- Patient Demographics -->
                        <h3 style="margin-bottom: 20px; color: #1e293b; font-size: 16px;">
                            <i class="fas fa-id-card"></i> Demographics
                        </h3>
                        
                        <div class="form-grid">
                            <div class="form-group">
                                <label class="form-label" for="patient_name">
                                    <i class="fas fa-user"></i> Patient Name
                                </label>
                                <input 
                                    type="text" 
                                    id="patient_name" 
                                    name="patient_name" 
                                    class="form-input" 
                                    placeholder="e.g., John Doe"
                                    required
                                >
                                <div class="form-hint">Full name of the patient</div>
                            </div>

                            <div class="form-group">
                                <label class="form-label" for="age">
                                    <i class="fas fa-birthday-cake"></i> Age *
                                </label>
                                <input 
                                    type="number" 
                                    id="age" 
                                    name="age" 
                                    class="form-input" 
                                    min="18" 
                                    max="100" 
                                    placeholder="e.g., 65"
                                    required
                                >
                                <div class="form-hint">Patient age (18-100 years)</div>
                            </div>

                            <div class="form-group">
                                <label class="form-label" for="gender">
                                    <i class="fas fa-venus-mars"></i> Gender *
                                </label>
                                <select id="gender" name="gender" class="form-select" required>
                                    <option value="">Select gender</option>
                                    <option value="M">Male</option>
                                    <option value="F">Female</option>
                                </select>
                                <div class="form-hint">Biological sex</div>
                            </div>
                        </div>

                        <!-- Clinical Parameters -->
                        <h3 style="margin: 32px 0 20px; color: #1e293b; font-size: 16px;">
                            <i class="fas fa-heartbeat"></i> Clinical Parameters
                        </h3>

                        <div class="form-grid">
                            <div class="form-group">
                                <label class="form-label" for="heart_rate">
                                    <i class="fas fa-heart"></i> Heart Rate (bpm) *
                                </label>
                                <input 
                                    type="number" 
                                    id="heart_rate" 
                                    name="heart_rate" 
                                    class="form-input" 
                                    min="40" 
                                    max="200" 
                                    placeholder="e.g., 95"
                                    required
                                >
                                <div class="form-hint">Normal range: 60-100 bpm</div>
                            </div>

                            <div class="form-group">
                                <label class="form-label" for="glucose">
                                    <i class="fas fa-vial"></i> Blood Glucose (mg/dL) *
                                </label>
                                <input 
                                    type="number" 
                                    step="0.1"
                                    id="glucose" 
                                    name="glucose" 
                                    class="form-input" 
                                    min="50" 
                                    max="400" 
                                    placeholder="e.g., 140.5"
                                    required
                                >
                                <div class="form-hint">Normal fasting: 70-100 mg/dL</div>
                            </div>

                            <div class="form-group">
                                <label class="form-label" for="prior_admission">
                                    <i class="fas fa-hospital-user"></i> Prior Admissions *
                                </label>
                                <input 
                                    type="number" 
                                    id="prior_admission" 
                                    name="prior_admission" 
                                    class="form-input" 
                                    min="0" 
                                    max="20" 
                                    placeholder="e.g., 2"
                                    required
                                >
                                <div class="form-hint">Number of previous hospital admissions</div>
                            </div>
                        </div>

                        <!-- Additional Notes -->
                        <div class="form-group full-width" style="margin-top: 24px;">
                            <label class="form-label" for="notes">
                                <i class="fas fa-notes-medical"></i> Clinical Notes (Optional)
                            </label>
                            <textarea 
                                id="notes" 
                                name="notes" 
                                class="form-input" 
                                rows="4" 
                                placeholder="Add any relevant clinical observations..."
                                style="resize: vertical;"
                            ></textarea>
                        </div>

                        <!-- Action Buttons -->
                        <div style="display: flex; gap: 16px; margin-top: 32px;">
                            <button type="submit" class="btn btn-primary" style="flex: 1;">
                                <i class="fas fa-calculator"></i> Calculate Risk Prediction
                            </button>
                            <button type="reset" class="btn btn-outline">
                                <i class="fas fa-redo"></i> Reset Form
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Information Panel -->
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <i class="fas fa-info-circle"></i> Risk Level Guidelines
                    </h2>
                </div>
                <div class="card-body">
                    <div style="display: grid; gap: 16px;">
                        <div style="padding: 16px; background: #d1fae5; border-left: 4px solid #10b981; border-radius: 8px;">
                            <strong style="color: #065f46;">Low Risk (&lt; 30%)</strong>
                            <p style="color: #047857; margin-top: 4px; font-size: 14px;">Regular monitoring recommended. Outpatient care suitable.</p>
                        </div>
                        <div style="padding: 16px; background: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 8px;">
                            <strong style="color: #92400e;">Medium Risk (30-70%)</strong>
                            <p style="color: #b45309; margin-top: 4px; font-size: 14px;">Close monitoring advised. Consider preventive measures.</p>
                        </div>
                        <div style="padding: 16px; background: #fee2e2; border-left: 4px solid #ef4444; border-radius: 8px;">
                            <strong style="color: #991b1b;">High Risk (≥ 70%)</strong>
                            <p style="color: #dc2626; margin-top: 4px; font-size: 14px;">Immediate attention required. Admission likely necessary.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Form validation and user experience enhancements
        document.getElementById('predictionForm').addEventListener('submit', function(e) {
            const age = document.getElementById('age').value;
            const heartRate = document.getElementById('heart_rate').value;
            const glucose = document.getElementById('glucose').value;
            const priorAdmission = document.getElementById('prior_admission').value;

            if (age < 18 || age > 100) {
                alert('Please enter a valid age between 18 and 100');
                e.preventDefault();
                return false;
            }

            if (heartRate < 40 || heartRate > 200) {
                alert('Please enter a valid heart rate between 40 and 200 bpm');
                e.preventDefault();
                return false;
            }

            if (glucose < 50 || glucose > 400) {
                alert('Please enter a valid glucose level between 50 and 400 mg/dL');
                e.preventDefault();
                return false;
            }

            return true;
        });

        // Real-time validation hints
        document.getElementById('heart_rate').addEventListener('input', function() {
            const value = parseFloat(this.value);
            const hint = this.nextElementSibling.nextElementSibling;
            if (value > 0 && value < 60) {
                hint.style.color = '#ef4444';
                hint.textContent = '⚠️ Below normal range';
            } else if (value > 100 && value <= 200) {
                hint.style.color = '#f59e0b';
                hint.textContent = '⚠️ Above normal range';
            } else if (value >= 60 && value <= 100) {
                hint.style.color = '#10b981';
                hint.textContent = '✓ Normal range: 60-100 bpm';
            } else {
                hint.style.color = '#64748b';
                hint.textContent = 'Normal range: 60-100 bpm';
            }
        });

        document.getElementById('glucose').addEventListener('input', function() {
            const value = parseFloat(this.value);
            const hint = this.nextElementSibling.nextElementSibling;
            if (value > 0 && value < 70) {
                hint.style.color = '#ef4444';
                hint.textContent = '⚠️ Below normal range (Hypoglycemia)';
            } else if (value > 100 && value <= 400) {
                hint.style.color = '#f59e0b';
                hint.textContent = '⚠️ Above normal range (Hyperglycemia)';
            } else if (value >= 70 && value <= 100) {
                hint.style.color = '#10b981';
                hint.textContent = '✓ Normal fasting: 70-100 mg/dL';
            } else {
                hint.style.color = '#64748b';
                hint.textContent = 'Normal fasting: 70-100 mg/dL';
            }
        });
    </script>
</body>
</html>
