<?php
/**
 * Logout Page - Destroys user session and redirects to login
 */

// Start session if not already started
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

require_once 'config/auth.php';

// Perform logout
logoutUser();

// Prevent caching of this page
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");

// Redirect to login page
header('Location: index.php?logout=success');
exit;
?>
