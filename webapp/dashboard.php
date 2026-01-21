<?php
require_once 'config/auth.php';
require_once 'config/db.php';

requireLogin();
$user = getCurrentUser();

// Get dashboard statistics
$conn = getDBConnection();
$stats = [];

if ($conn) {
    $result = $conn->query("SELECT * FROM dashboard_stats");
    if ($result && $result->num_rows > 0) {
        $stats = $result->fetch_assoc();
    }
    
    // Get recent predictions
    $recent = $conn->query("SELECT * FROM recent_predictions LIMIT 10");
    
    closeDBConnection($conn);
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Healthcare Admission System</title>
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
            <a href="dashboard.php" class="menu-item active">
                <i class="fas fa-chart-line"></i>
                <span>Dashboard</span>
            </a>
            <a href="predict.php" class="menu-item">
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
            <h1 class="header-title">Dashboard</h1>
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
            <!-- Stats Grid -->
            <div class="stats-grid">
                <div class="stat-card primary">
                    <div class="stat-icon"><i class="fas fa-clipboard-list"></i></div>
                    <div class="stat-label">Total Predictions</div>
                    <div class="stat-value"><?php echo $stats['total_predictions'] ?? 0; ?></div>
                    <div class="stat-change">
                        <i class="fas fa-arrow-up"></i> Active system
                    </div>
                </div>

                <div class="stat-card high">
                    <div class="stat-icon"><i class="fas fa-exclamation-triangle"></i></div>
                    <div class="stat-label">High Risk Patients</div>
                    <div class="stat-value"><?php echo $stats['high_risk_count'] ?? 0; ?></div>
                    <div class="stat-change">
                        Requires attention
                    </div>
                </div>

                <div class="stat-card medium">
                    <div class="stat-icon"><i class="fas fa-user-clock"></i></div>
                    <div class="stat-label">Medium Risk</div>
                    <div class="stat-value"><?php echo $stats['medium_risk_count'] ?? 0; ?></div>
                    <div class="stat-change">
                        Monitor closely
                    </div>
                </div>

                <div class="stat-card low">
                    <div class="stat-icon"><i class="fas fa-check-circle"></i></div>
                    <div class="stat-label">Low Risk</div>
                    <div class="stat-value"><?php echo $stats['low_risk_count'] ?? 0; ?></div>
                    <div class="stat-change">
                        <i class="fas fa-thumbs-up"></i> Good status
                    </div>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Quick Actions</h2>
                </div>
                <div class="card-body">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
                        <a href="predict.php" class="btn btn-primary" style="text-decoration: none;">
                            <i class="fas fa-plus-circle"></i>
                            New Prediction
                        </a>
                        <a href="patients.php" class="btn btn-secondary" style="text-decoration: none;">
                            <i class="fas fa-list"></i>
                            View All Patients
                        </a>
                        <a href="analytics.php" class="btn btn-outline" style="text-decoration: none;">
                            <i class="fas fa-chart-pie"></i>
                            View Analytics
                        </a>
                    </div>
                </div>
            </div>

            <!-- Recent Predictions -->
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Recent Predictions</h2>
                    <a href="patients.php" class="btn btn-outline">View All</a>
                </div>
                <div class="card-body">
                    <?php if (isset($recent) && $recent->num_rows > 0): ?>
                    <div class="table-container">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Patient Name</th>
                                    <th>Age/Gender</th>
                                    <th>Risk Level</th>
                                    <th>Probability</th>
                                    <th>Clinician</th>
                                    <th>Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php while ($row = $recent->fetch_assoc()): ?>
                                <tr>
                                    <td>#<?php echo $row['id']; ?></td>
                                    <td><?php echo htmlspecialchars($row['patient_name'] ?? 'Anonymous'); ?></td>
                                    <td><?php echo $row['age']; ?> / <?php echo $row['gender']; ?></td>
                                    <td>
                                        <span class="badge badge-<?php echo strtolower($row['risk_level']); ?>">
                                            <?php echo $row['risk_level']; ?>
                                        </span>
                                    </td>
                                    <td><?php echo number_format($row['prediction'] * 100, 1); ?>%</td>
                                    <td><?php echo htmlspecialchars($row['clinician_name'] ?? 'N/A'); ?></td>
                                    <td><?php echo date('M d, Y H:i', strtotime($row['created_at'])); ?></td>
                                </tr>
                                <?php endwhile; ?>
                            </tbody>
                        </table>
                    </div>
                    <?php else: ?>
                    <div style="text-align: center; padding: 40px; color: #64748b;">
                        <i class="fas fa-inbox" style="font-size: 48px; margin-bottom: 16px; opacity: 0.3;"></i>
                        <p>No predictions yet. <a href="predict.php">Make your first prediction</a></p>
                    </div>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
