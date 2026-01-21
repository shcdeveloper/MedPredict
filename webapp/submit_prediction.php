<?php
/**
 * Submit patient data and get prediction from FastAPI (Admin Version)
 */

require_once 'config/auth.php';
require_once 'config/db.php';

requireLogin();
$user = getCurrentUser();

// Initialize variables
$error = null;
$result = null;

// Check if form was submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    // Get and validate form data
    $patient_name = filter_input(INPUT_POST, 'patient_name', FILTER_SANITIZE_STRING);
    $age = filter_input(INPUT_POST, 'age', FILTER_VALIDATE_INT);
    $gender = filter_input(INPUT_POST, 'gender', FILTER_SANITIZE_STRING);
    $heart_rate = filter_input(INPUT_POST, 'heart_rate', FILTER_VALIDATE_INT);
    $glucose = filter_input(INPUT_POST, 'glucose', FILTER_VALIDATE_FLOAT);
    $prior_admission = filter_input(INPUT_POST, 'prior_admission', FILTER_VALIDATE_INT);
    $notes = filter_input(INPUT_POST, 'notes', FILTER_SANITIZE_STRING);
    
    // Validate inputs
    if (!$age || $age < 18 || $age > 100) {
        $error = "Invalid age. Must be between 18 and 100.";
    } elseif (!in_array($gender, ['M', 'F'])) {
        $error = "Invalid gender. Must be M or F.";
    } elseif (!$heart_rate || $heart_rate < 40 || $heart_rate > 200) {
        $error = "Invalid heart rate. Must be between 40 and 200 bpm.";
    } elseif ($glucose === false || $glucose < 50 || $glucose > 400) {
        $error = "Invalid glucose level. Must be between 50 and 400 mg/dL.";
    } elseif ($prior_admission === false || $prior_admission < 0 || $prior_admission > 20) {
        $error = "Invalid prior admissions. Must be between 0 and 20.";
    }
    
    if (!$error) {
        // Prepare data for API
        $patientData = [
            'age' => $age,
            'gender' => $gender,
            'heart_rate' => $heart_rate,
            'glucose' => $glucose,
            'prior_admission' => $prior_admission
        ];
        
        // Call FastAPI prediction endpoint
        $ch = curl_init(API_PREDICT_ENDPOINT);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($patientData));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Accept: application/json'
        ]);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlError = curl_error($ch);
        curl_close($ch);
        
        if ($curlError) {
            $error = "Failed to connect to prediction API. Please ensure the API server is running.";
            error_log("CURL Error: " . $curlError);
        } elseif ($httpCode !== 200) {
            $error = "API returned error code: $httpCode";
            error_log("API Error: " . $response);
        } else {
            $result = json_decode($response, true);
            
            if ($result) {
                // Store result in database with user ID
                $conn = getDBConnection();
                
                if ($conn) {
                    $stmt = $conn->prepare(
                        "INSERT INTO patient_requests 
                        (user_id, patient_name, age, gender, heart_rate, glucose, prior_admission, prediction, risk_level) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    );
                    
                    $probability = $result['admission_probability'];
                    $riskLevel = $result['risk_level'];
                    $userId = $user['id'];
                    
                    $stmt->bind_param(
                        "isisiddss",
                        $userId,
                        $patient_name,
                        $age,
                        $gender,
                        $heart_rate,
                        $glucose,
                        $prior_admission,
                        $probability,
                        $riskLevel
                    );
                    
                    if (!$stmt->execute()) {
                        error_log("Database insert error: " . $stmt->error);
                    }
                    
                    $stmt->close();
                    closeDBConnection($conn);
                }
            } else {
                $error = "Failed to parse API response.";
            }
        }
    }
}

// If no POST data, redirect to predict page
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: predict.php');
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prediction Result - Healthcare Admission System</title>
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
                <span>New Prediction</span>
            </a>
            <a href="patients.php" class="menu-item">
                <i class="fas fa-users"></i>
                <span>Patient History</span>
            </a>
            <a href="analytics.php" class="menu-item">
                <i class="fas fa-chart-bar"></i>
                <span>Analytics</span>
            </a>
            <?php if ($user['role'] === 'admin'): ?>
            <a href="users.php" class="menu-item">
                <i class="fas fa-user-shield"></i>
                <span>User Management</span>
            </a>
            <?php endif; ?>
            <a href="settings.php" class="menu-item">
                <i class="fas fa-cog"></i>
                <span>Settings</span>
            </a>
            <a href="logout.php" class="menu-item" style="margin-top: auto;">
                <i class="fas fa-sign-out-alt"></i>
                <span>Logout</span>
            </a>
        </nav>
    </div>

    <!-- Main Content -->
    <div class="main-content">
        <!-- Top Header -->
        <div class="top-header">
            <h1 class="header-title">Prediction Result</h1>
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
                    <strong>Error:</strong> <?php echo htmlspecialchars($error); ?>
                </div>
                <a href="predict.php" class="btn btn-primary">
                    <i class="fas fa-arrow-left"></i> Back to Prediction Form
                </a>
            <?php elseif ($result): ?>
                <!-- Success Alert -->
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i>
                    Prediction completed successfully and saved to patient records.
                </div>

                <!-- Prediction Result Card -->
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">
                            <i class="fas fa-chart-pie"></i> Admission Risk Assessment
                        </h2>
                    </div>
                    <div class="card-body">
                        <!-- Risk Level Display -->
                        <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; margin-bottom: 32px;">
                            <div style="font-size: 72px; font-weight: 700; margin-bottom: 16px;">
                                <?php echo number_format($result['admission_probability'] * 100, 1); ?>%
                            </div>
                            <div style="margin-bottom: 20px;">
                                <span class="badge badge-<?php echo strtolower($result['risk_level']); ?>" style="font-size: 18px; padding: 8px 24px;">
                                    <?php echo strtoupper($result['risk_level']); ?> RISK
                                </span>
                            </div>
                            <p style="font-size: 16px; opacity: 0.95; max-width: 600px; margin: 0 auto;">
                                <?php echo htmlspecialchars($result['message']); ?>
                            </p>
                        </div>

                        <!-- Patient Information -->
                        <h3 style="margin-bottom: 20px; color: #1e293b; font-size: 16px;">
                            <i class="fas fa-user-md"></i> Patient Information
                        </h3>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 24px; background: #f8fafc; border-radius: 8px;">
                            <div>
                                <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">Patient Name</div>
                                <div style="font-weight: 600; color: #1e293b;"><?php echo htmlspecialchars($patient_name ?? 'Anonymous'); ?></div>
                            </div>
                            <div>
                                <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">Age</div>
                                <div style="font-weight: 600; color: #1e293b;"><?php echo $age; ?> years</div>
                            </div>
                            <div>
                                <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">Gender</div>
                                <div style="font-weight: 600; color: #1e293b;"><?php echo $gender === 'M' ? 'Male' : 'Female'; ?></div>
                            </div>
                            <div>
                                <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">Heart Rate</div>
                                <div style="font-weight: 600; color: #1e293b;"><?php echo $heart_rate; ?> bpm</div>
                            </div>
                            <div>
                                <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">Blood Glucose</div>
                                <div style="font-weight: 600; color: #1e293b;"><?php echo $glucose; ?> mg/dL</div>
                            </div>
                            <div>
                                <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">Prior Admissions</div>
                                <div style="font-weight: 600; color: #1e293b;"><?php echo $prior_admission; ?></div>
                            </div>
                        </div>

                        <!-- Action Buttons -->
                        <div style="display: flex; gap: 16px; margin-top: 32px;">
                            <a href="predict.php" class="btn btn-primary">
                                <i class="fas fa-plus"></i> New Prediction
                            </a>
                            <a href="patients.php" class="btn btn-secondary">
                                <i class="fas fa-list"></i> View All Patients
                            </a>
                            <a href="dashboard.php" class="btn btn-outline">
                                <i class="fas fa-home"></i> Dashboard
                            </a>
                            <button onclick="window.print()" class="btn btn-outline">
                                <i class="fas fa-print"></i> Print Report
                            </button>
                        </div>
                    </div>
                </div>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>
