<?php
require_once 'config/auth.php';

// Redirect if already logged in
if (isLoggedIn()) {
    header('Location: dashboard.php');
    exit;
}

$error = '';

// Handle login
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_STRING);
    $password = $_POST['password'] ?? '';
    
    if (empty($username) || empty($password)) {
        $error = 'Please enter both username and password';
    } else {
        $result = loginUser($username, $password);
        if ($result['success']) {
            header('Location: dashboard.php');
            exit;
        } else {
            $error = $result['message'];
        }
    }
}

$success = '';
if (isset($_GET['logout']) && $_GET['logout'] === 'success') {
    $success = 'You have been successfully logged out.';
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Healthcare Admission Prediction System</title>
    <link rel="stylesheet" href="assets/css/admin.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="login-container">
        <div class="login-card">
            <div class="login-header">
                <div style="font-size: 48px; color: #FF6D1F; margin-bottom: 16px;">
                    <i class="fas fa-hospital"></i>
                </div>
                <h1 class="login-title">Healthcare Admission System</h1>
                <p class="login-subtitle">Sign in to access the clinical dashboard</p>
            </div>

            <?php if ($success): ?>
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i>
                    <?php echo htmlspecialchars($success); ?>
                </div>
            <?php endif; ?>

            <?php if ($error): ?>
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle"></i>
                    <?php echo htmlspecialchars($error); ?>
                </div>
            <?php endif; ?>

            <form method="POST" action="index.php">
                <div class="form-group">
                    <label class="form-label" for="username">
                        <i class="fas fa-user"></i> Username
                    </label>
                    <input 
                        type="text" 
                        id="username" 
                        name="username" 
                        class="form-input" 
                        placeholder="Enter your username"
                        required
                        autofocus
                    >
                </div>

                <div class="form-group">
                    <label class="form-label" for="password">
                        <i class="fas fa-lock"></i> Password
                    </label>
                    <input 
                        type="password" 
                        id="password" 
                        name="password" 
                        class="form-input" 
                        placeholder="Enter your password"
                        required
                    >
                </div>

                <button type="submit" class="btn btn-primary btn-block mt-4">
                    <i class="fas fa-sign-in-alt"></i> Sign In
                </button>
            </form>

            <div style="margin-top: 32px; padding-top: 24px; border-top: 1px solid #e2e8f0; text-align: center;">
                <p style="font-size: 12px; color: #64748b; margin-bottom: 12px;">
                    <strong>Demo Credentials:</strong>
                </p>
                <div style="font-size: 12px; color: #64748b; line-height: 1.8;">
                    <div><strong>Admin:</strong> admin / admin123</div>
                    <div><strong>Doctor:</strong> dr.smith / admin123</div>
                    <div><strong>Clinician:</strong> clinician1 / admin123</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
