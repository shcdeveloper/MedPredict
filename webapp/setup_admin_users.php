<?php
/**
 * Setup Admin Users with Proper Password Hashing
 * Run this file once to create admin accounts
 * Access: http://localhost/webapp/setup_admin_users.php
 */

require_once 'config/db.php';

// Security: Remove this file after running!
$setupComplete = false;

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Setup</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .error { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .info { background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .code { background: #f4f4f4; padding: 10px; border-radius: 5px; font-family: monospace; margin: 10px 0; }
        button { background: #007bff; color: white; border: none; padding: 12px 24px; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🏥 Admin User Setup</h1>

<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['setup'])) {
    $conn = getDBConnection();
    
    if (!$conn) {
        echo '<div class="error"><strong>Error:</strong> Could not connect to database. Make sure XAMPP MySQL is running.</div>';
        exit;
    }
    
    // Check if admin_users table exists
    $result = $conn->query("SHOW TABLES LIKE 'admin_users'");
    
    if ($result->num_rows === 0) {
        echo '<div class="info"><strong>Creating admin_users table...</strong></div>';
        
        // Create admin_users table
        $createTable = "
        CREATE TABLE admin_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            role ENUM('doctor', 'clinician', 'admin') DEFAULT 'clinician',
            is_active BOOLEAN DEFAULT TRUE,
            last_login TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_username (username),
            INDEX idx_email (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
        
        if ($conn->query($createTable)) {
            echo '<div class="success">✓ Table admin_users created successfully</div>';
        } else {
            echo '<div class="error">Error creating table: ' . $conn->error . '</div>';
        }
        
        // Create admin_sessions table
        $createSessions = "
        CREATE TABLE IF NOT EXISTS admin_sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            session_token VARCHAR(64) UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE CASCADE,
            INDEX idx_session_token (session_token)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
        
        if ($conn->query($createSessions)) {
            echo '<div class="success">✓ Table admin_sessions created successfully</div>';
        }
        
        // Add columns to patient_requests
        $conn->query("ALTER TABLE patient_requests ADD COLUMN IF NOT EXISTS user_id INT NULL AFTER id");
        $conn->query("ALTER TABLE patient_requests ADD COLUMN IF NOT EXISTS patient_name VARCHAR(100) NULL AFTER user_id");
        echo '<div class="success">✓ Updated patient_requests table</div>';
    }
    
    // Clear existing users (for clean setup)
    $conn->query("DELETE FROM admin_users");
    
    // Create default admin accounts with properly hashed passwords
    $users = [
        ['admin', 'admin123', 'System Administrator', 'admin@hospital.com', 'admin'],
        ['dr.smith', 'admin123', 'Dr. John Smith', 'dr.smith@hospital.com', 'doctor'],
        ['clinician1', 'admin123', 'Sarah Johnson', 'sarah.j@hospital.com', 'clinician']
    ];
    
    echo '<div class="info"><strong>Creating admin accounts...</strong></div>';
    
    $stmt = $conn->prepare("INSERT INTO admin_users (username, password_hash, full_name, email, role) VALUES (?, ?, ?, ?, ?)");
    
    foreach ($users as $user) {
        $username = $user[0];
        $password = $user[1];
        $fullName = $user[2];
        $email = $user[3];
        $role = $user[4];
        
        // Hash the password using PHP's password_hash
        $passwordHash = password_hash($password, PASSWORD_DEFAULT);
        
        $stmt->bind_param("sssss", $username, $passwordHash, $fullName, $email, $role);
        
        if ($stmt->execute()) {
            echo '<div class="success">✓ Created user: <strong>' . htmlspecialchars($username) . '</strong> (Password: ' . htmlspecialchars($password) . ')</div>';
        } else {
            echo '<div class="error">Error creating user ' . htmlspecialchars($username) . ': ' . $stmt->error . '</div>';
        }
    }
    
    $stmt->close();
    
    // Display created users
    echo '<h2>Created Admin Accounts:</h2>';
    echo '<table>';
    echo '<tr><th>Username</th><th>Password</th><th>Full Name</th><th>Role</th></tr>';
    
    $result = $conn->query("SELECT username, full_name, email, role FROM admin_users");
    while ($row = $result->fetch_assoc()) {
        echo '<tr>';
        echo '<td><strong>' . htmlspecialchars($row['username']) . '</strong></td>';
        echo '<td>admin123</td>';
        echo '<td>' . htmlspecialchars($row['full_name']) . '</td>';
        echo '<td>' . htmlspecialchars($row['role']) . '</td>';
        echo '</tr>';
    }
    echo '</table>';
    
    echo '<div class="success" style="margin-top: 30px;">';
    echo '<h3>✅ Setup Complete!</h3>';
    echo '<p><strong>You can now login at:</strong> <a href="login.php">login.php</a></p>';
    echo '<p><strong>⚠️ IMPORTANT:</strong> Delete this file (setup_admin_users.php) for security!</p>';
    echo '</div>';
    
    $setupComplete = true;
    
    closeDBConnection($conn);
}

if (!$setupComplete) {
    ?>
    <div class="info">
        <strong>This script will:</strong>
        <ul>
            <li>Create the admin_users table</li>
            <li>Create the admin_sessions table</li>
            <li>Create 3 default admin accounts with proper password hashing</li>
            <li>Update the patient_requests table</li>
        </ul>
        <p><strong>Make sure XAMPP MySQL is running before clicking setup!</strong></p>
    </div>
    
    <form method="POST">
        <button type="submit" name="setup">🚀 Run Admin Setup</button>
    </form>
    
    <div class="info" style="margin-top: 30px;">
        <h3>Default Accounts (after setup):</h3>
        <table>
            <tr>
                <th>Username</th>
                <th>Password</th>
                <th>Role</th>
            </tr>
            <tr>
                <td><strong>admin</strong></td>
                <td>admin123</td>
                <td>Administrator</td>
            </tr>
            <tr>
                <td><strong>dr.smith</strong></td>
                <td>admin123</td>
                <td>Doctor</td>
            </tr>
            <tr>
                <td><strong>clinician1</strong></td>
                <td>admin123</td>
                <td>Clinician</td>
            </tr>
        </table>
    </div>
    <?php
}
?>
</body>
</html>
