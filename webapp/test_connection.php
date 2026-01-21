<?php
/**
 * ERROR DIAGNOSTIC FILE FOR INFINITYFREE
 * Upload this file to your InfinityFree root directory
 * Then visit: http://patty-portfolio.infinityfree.me/test_connection.php
 * 
 * This will show you the EXACT error causing HTTP 500
 */

// Enable ALL error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

echo "<h1>InfinityFree Connection Diagnostic</h1>";
echo "<hr>";

// Test 1: PHP Version
echo "<h2>✓ Test 1: PHP Version</h2>";
echo "<p>PHP Version: " . phpversion() . "</p>";
echo "<p>Server: " . $_SERVER['SERVER_SOFTWARE'] . "</p>";
echo "<hr>";

// Test 2: File Existence
echo "<h2>Test 2: Required Files</h2>";
$files = [
    'config/db.php',
    'config/auth.php',
    'dashboard.php',
    'patients.php',
    'index.php'
];

foreach ($files as $file) {
    if (file_exists($file)) {
        echo "<p>✅ $file - EXISTS</p>";
    } else {
        echo "<p>❌ $file - MISSING!</p>";
    }
}
echo "<hr>";

// Test 3: Database Connection
echo "<h2>Test 3: Database Connection</h2>";

// IMPORTANT: Update these with YOUR InfinityFree credentials!
define('DB_HOST', 'sql300.infinityfree.com');
define('DB_USER', 'if0_39888624');
define('DB_PASS', 'YOUR_PASSWORD_HERE'); // ⚠️ CHANGE THIS!
define('DB_NAME', 'if0_39888624_healthcare_admission');

echo "<p><strong>Attempting connection to:</strong></p>";
echo "<ul>";
echo "<li>Host: " . DB_HOST . "</li>";
echo "<li>User: " . DB_USER . "</li>";
echo "<li>Database: " . DB_NAME . "</li>";
echo "</ul>";

try {
    $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    if ($conn->connect_error) {
        throw new Exception("Connection failed: " . $conn->connect_error);
    }
    
    echo "<p>✅ <strong>DATABASE CONNECTION SUCCESSFUL!</strong></p>";
    
    // Test 4: Check if tables exist
    echo "<hr>";
    echo "<h2>Test 4: Database Tables</h2>";
    
    $tables = ['admin_users', 'patient_requests', 'admin_sessions', 'disease_risk_assessments'];
    
    foreach ($tables as $table) {
        $result = $conn->query("SHOW TABLES LIKE '$table'");
        if ($result && $result->num_rows > 0) {
            echo "<p>✅ Table `$table` exists</p>";
            
            // Count records
            $count_result = $conn->query("SELECT COUNT(*) as count FROM `$table`");
            if ($count_result) {
                $row = $count_result->fetch_assoc();
                echo "<p>&nbsp;&nbsp;&nbsp;→ Records: " . $row['count'] . "</p>";
            }
        } else {
            echo "<p>❌ Table `$table` MISSING!</p>";
        }
    }
    
    // Test 5: Sample query (like dashboard.php uses)
    echo "<hr>";
    echo "<h2>Test 5: Dashboard Query Test</h2>";
    
    $statsQuery = "SELECT 
        COUNT(*) as total_predictions,
        AVG(prediction) as avg_prediction_score,
        SUM(CASE WHEN risk_level IN ('high', 'High') THEN 1 ELSE 0 END) as high_risk_count
    FROM patient_requests";
    
    $result = $conn->query($statsQuery);
    
    if ($result) {
        $stats = $result->fetch_assoc();
        echo "<p>✅ <strong>Dashboard query SUCCESSFUL!</strong></p>";
        echo "<ul>";
        echo "<li>Total Predictions: " . $stats['total_predictions'] . "</li>";
        echo "<li>Avg Score: " . round($stats['avg_prediction_score'], 2) . "</li>";
        echo "<li>High Risk Count: " . $stats['high_risk_count'] . "</li>";
        echo "</ul>";
    } else {
        echo "<p>❌ Dashboard query FAILED: " . $conn->error . "</p>";
    }
    
    $conn->close();
    
} catch (Exception $e) {
    echo "<p>❌ <strong>DATABASE CONNECTION FAILED!</strong></p>";
    echo "<p>Error: " . $e->getMessage() . "</p>";
    echo "<p><strong>Possible causes:</strong></p>";
    echo "<ul>";
    echo "<li>Wrong password in DB_PASS</li>";
    echo "<li>Database not created in InfinityFree</li>";
    echo "<li>Wrong database host (should be sql300.infinityfree.com)</li>";
    echo "<li>SQL file not imported yet</li>";
    echo "</ul>";
}

echo "<hr>";
echo "<h2>📝 Next Steps:</h2>";
echo "<ol>";
echo "<li>If database connection FAILED: Fix credentials in config/db.php</li>";
echo "<li>If tables MISSING: Import healthcare_admission_COMPLETE_INFINITYFREE.sql</li>";
echo "<li>If everything ✅: Your site should work!</li>";
echo "</ol>";

echo "<hr>";
echo "<p><em>Generated: " . date('Y-m-d H:i:s') . "</em></p>";
?>
