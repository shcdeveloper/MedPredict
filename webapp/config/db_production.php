<?php
/**
 * PRODUCTION Database Configuration - InfinityFree
 * 
 * DEPLOYMENT INSTRUCTIONS:
 * 1. Rename this file to db.php when uploading to InfinityFree
 * 2. Update DB_PASS with your actual InfinityFree password
 * 3. Upload via FTP to /htdocs/config/
 */

// InfinityFree Database credentials
define('DB_HOST', 'sql300.infinityfree.com');
define('DB_USER', 'if0_39888624');
define('DB_PASS', 'YOUR_INFINITYFREE_PASSWORD_HERE'); // ⚠️ UPDATE THIS!
define('DB_NAME', 'if0_39888624_healthcare_admission');
define('DB_PORT', 3306);

// API Configuration - Render.com
define('API_URL', 'https://medpredict-gkaa.onrender.com');
define('API_PREDICT_ENDPOINT', API_URL . '/predict');

// Create database connection (mysqli)
function getDBConnection() {
    try {
        $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT);
        
        if ($conn->connect_error) {
            error_log("Database connection error: " . $conn->connect_error);
            throw new Exception("Unable to connect to database. Please contact administrator.");
        }
        
        $conn->set_charset("utf8mb4");
        return $conn;
        
    } catch (Exception $e) {
        error_log("Database connection error: " . $e->getMessage());
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
?>
