<?php
/**
 * Submit patient data and get prediction from FastAPI
 */

require_once 'config/db.php';

// Initialize variables
$error = null;
$result = null;

// Check if form was submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    // Get and validate form data
    $age = filter_input(INPUT_POST, 'age', FILTER_VALIDATE_INT);
    $gender = filter_input(INPUT_POST, 'gender', FILTER_SANITIZE_STRING);
    $heart_rate = filter_input(INPUT_POST, 'heart_rate', FILTER_VALIDATE_INT);
    $glucose = filter_input(INPUT_POST, 'glucose', FILTER_VALIDATE_FLOAT);
    $prior_admission = filter_input(INPUT_POST, 'prior_admission', FILTER_VALIDATE_INT);
    
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
            $error = "Failed to connect to prediction API. Please ensure the API is running.";
            error_log("CURL Error: " . $curlError);
        } elseif ($httpCode !== 200) {
            $error = "API returned error code: $httpCode";
            error_log("API Error: " . $response);
        } else {
            $result = json_decode($response, true);
            
            if ($result) {
                // Store result in database
                $conn = getDBConnection();
                
                if ($conn) {
                    $stmt = $conn->prepare(
                        "INSERT INTO patient_requests 
                        (age, gender, heart_rate, glucose, prior_admission, prediction, risk_level) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)"
                    );
                    
                    $probability = $result['admission_probability'];
                    $riskLevel = $result['risk_level'];
                    
                    $stmt->bind_param(
                        "isiidds",
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

// If no POST data, redirect to home
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index.php');
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prediction Result - Healthcare Admission</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 Healthcare Admission Prediction</h1>
            <p>AI-Powered Patient Admission Risk Assessment</p>
        </div>

        <?php if ($error): ?>
            <div class="card">
                <div class="alert alert-error">
                    <strong>❌ Error:</strong> <?php echo htmlspecialchars($error); ?>
                </div>
                <a href="index.php" class="btn">← Back to Form</a>
            </div>
        <?php elseif ($result): ?>
            <div class="result-card">
                <h2>📊 Prediction Result</h2>
                
                <div class="probability">
                    <?php echo number_format($result['admission_probability'] * 100, 1); ?>%
                </div>
                
                <div class="risk-badge risk-<?php echo strtolower($result['risk_level']); ?>">
                    <?php echo strtoupper($result['risk_level']); ?> RISK
                </div>
                
                <div class="message">
                    <?php echo htmlspecialchars($result['message']); ?>
                </div>
                
                <div style="margin-top: 30px; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.3);">
                    <h3 style="margin-bottom: 15px;">Patient Information</h3>
                    <div style="text-align: left; display: inline-block;">
                        <p>👤 Age: <?php echo $age; ?> years</p>
                        <p>⚧ Gender: <?php echo $gender === 'M' ? 'Male' : 'Female'; ?></p>
                        <p>❤️ Heart Rate: <?php echo $heart_rate; ?> bpm</p>
                        <p>🩸 Glucose: <?php echo $glucose; ?> mg/dL</p>
                        <p>🏥 Prior Admissions: <?php echo $prior_admission; ?></p>
                    </div>
                </div>
                
                <a href="index.php" class="back-link">← New Prediction</a>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>
