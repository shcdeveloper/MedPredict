<?php
/**
 * Database Configuration for InfinityFree
 * 
 * IMPORTANT: After uploading to InfinityFree, replace the values below with YOUR actual credentials
 * You can find these in InfinityFree Control Panel → MySQL Databases
 */

// InfinityFree Database credentials
// REPLACE THESE WITH YOUR ACTUAL INFINITYFREE CREDENTIALS!
define('DB_HOST', 'sql300.infinityfree.com');  // Your InfinityFree DB host (e.g., sql###.infinityfree.com)
define('DB_USER', 'if0_39888624');              // Your InfinityFree DB username (e.g., if0_########)
define('DB_PASS', 'YOUR_DATABASE_PASSWORD');    // Your InfinityFree DB password
define('DB_NAME', 'if0_39888624_healthcare');   // Your InfinityFree DB name (e.g., if0_########_healthcare)
define('DB_PORT', 3306);

// API Configuration (Render.com)
define('API_URL', 'https://medpredict-gkaa.onrender.com');
define('API_PREDICT_ENDPOINT', API_URL . '/predict');
define('API_DISEASE_ENDPOINT', API_URL . '/predict-disease');

// Create database connection (mysqli)
function getDBConnection() {
    try {
        $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT);
        
        if ($conn->connect_error) {
            throw new Exception("Connection failed: " . $conn->connect_error);
        }
        
        $conn->set_charset("utf8mb4");
        return $conn;
        
    } catch (Exception $e) {
        error_log("Database connection error: " . $e->getMessage());
        // Show friendly error message (don't expose credentials)
        die("Database connection failed. Please check your configuration.");
        return null;
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
        die("Database connection failed. Please check your configuration.");
        return null;
    }
}

// Close database connection
function closeDBConnection($conn) {
    if ($conn && $conn instanceof mysqli) {
        $conn->close();
    }
}

// Close PDO connection
function closePDOConnection($pdo) {
    $pdo = null;
}

/**
 * HOW TO FIND YOUR INFINITYFREE CREDENTIALS:
 * 
 * 1. Login to InfinityFree Control Panel (cPanel)
 * 2. Go to "MySQL Databases" section
 * 3. You'll see:
 *    - Database Host: sql###.infinityfree.com (copy this to DB_HOST)
 *    - Database Name: if0_########_healthcare (copy this to DB_NAME)
 *    - Database User: if0_######## (copy this to DB_USER)
 *    - Database Password: (you set this when creating the database)
 * 
 * 4. Replace the values above with your actual credentials
 * 5. Save this file as config/db.php on InfinityFree
 */
?>
