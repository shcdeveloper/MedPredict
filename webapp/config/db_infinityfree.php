<?php
/**
 * INFINITYFREE Database Configuration
 * INSTRUCTIONS: Copy this file's contents to your config/db.php on InfinityFree
 */

// ============================================================
// INFINITYFREE DATABASE CREDENTIALS
// ⚠️ UPDATE THESE WITH YOUR ACTUAL INFINITYFREE CREDENTIALS!
// ============================================================

// Database credentials - InfinityFree
define('DB_HOST', 'sql300.infinityfree.com');  // InfinityFree MySQL host
define('DB_USER', 'if0_39888624');              // Your InfinityFree database username
define('DB_PASS', 'YOUR_PASSWORD_HERE');        // ⚠️ CHANGE THIS to your actual password!
define('DB_NAME', 'if0_39888624_healthcare_admission');  // Your database name
define('DB_PORT', 3306);

// API Configuration - Render.com
define('API_URL', 'https://medpredict-gkaa.onrender.com');  // Your Render API URL
define('API_PREDICT_ENDPOINT', API_URL . '/predict');

// Create database connection (mysqli)
function getDBConnection() {
    try {
        $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT);
        
        if ($conn->connect_error) {
            // Log error but don't expose details to users
            error_log("Database connection error: " . $conn->connect_error);
            throw new Exception("Unable to connect to database. Please contact administrator.");
        }
        
        $conn->set_charset("utf8mb4");
        return $conn;
        
    } catch (Exception $e) {
        error_log("Database connection error: " . $e->getMessage());
        // Show friendly error to users
        die("Database connection failed. Please try again later.");
    }
}

// Create PDO database connection
function getPDOConnection() {
    try {
        $dsn = "mysql:host=" . DB_HOST . ";port=" . DB_PORT . ";dbname=" . DB_NAME . ";charset=utf8mb4";
        $options = [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ];
        
        $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
        return $pdo;
        
    } catch (PDOException $e) {
        error_log("PDO connection error: " . $e->getMessage());
        die("Database connection failed. Please try again later.");
    }
}

// Test connection on first load (optional - remove in production)
if (!defined('SKIP_DB_TEST')) {
    $testConn = getDBConnection();
    if ($testConn) {
        $testConn->close();
    }
}
?>
