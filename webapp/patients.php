<?php
require_once 'config/auth.php';
require_once 'config/db.php';

requireLogin();
$user = getCurrentUser();

// Get all patient records
$conn = getDBConnection();
$patients = [];

if ($conn) {
    $result = $conn->query("SELECT * FROM recent_predictions");
    if ($result) {
        while ($row = $result->fetch_assoc()) {
            $patients[] = $row;
        }
    }
    closeDBConnection($conn);
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Patient History - Healthcare Admission System</title>
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
            <a href="patients.php" class="menu-item active">
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
        <div class="top-header">
            <h1 class="header-title">Patient History</h1>
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

        <div class="dashboard-content">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <i class="fas fa-history"></i> All Patient Records
                    </h2>
                    <div style="display: flex; gap: 12px;">
                        <input type="text" id="searchInput" placeholder="Search patients..." class="form-input" style="width: 300px;">
                        <a href="predict.php" class="btn btn-primary">
                            <i class="fas fa-plus"></i> New Prediction
                        </a>
                    </div>
                </div>
                <div class="card-body">
                    <?php if (count($patients) > 0): ?>
                    <div class="table-container">
                        <table class="data-table" id="patientsTable">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Patient Name</th>
                                    <th>Age</th>
                                    <th>Gender</th>
                                    <th>Risk Level</th>
                                    <th>Probability</th>
                                    <th>Clinician</th>
                                    <th>Date</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($patients as $row): ?>
                                <tr>
                                    <td><strong>#<?php echo $row['id']; ?></strong></td>
                                    <td><?php echo htmlspecialchars($row['patient_name'] ?? 'Anonymous'); ?></td>
                                    <td><?php echo $row['age']; ?></td>
                                    <td><?php echo $row['gender']; ?></td>
                                    <td>
                                        <span class="badge badge-<?php echo strtolower($row['risk_level']); ?>">
                                            <?php echo $row['risk_level']; ?>
                                        </span>
                                    </td>
                                    <td><strong><?php echo number_format($row['prediction'] * 100, 1); ?>%</strong></td>
                                    <td><?php echo htmlspecialchars($row['clinician_name'] ?? 'N/A'); ?></td>
                                    <td><?php echo date('M d, Y H:i', strtotime($row['created_at'])); ?></td>
                                    <td>
                                        <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;">
                                            <i class="fas fa-eye"></i> View
                                        </button>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                    <?php else: ?>
                    <div style="text-align: center; padding: 60px 20px; color: #64748b;">
                        <i class="fas fa-inbox" style="font-size: 64px; margin-bottom: 20px; opacity: 0.3;"></i>
                        <h3 style="margin-bottom: 12px;">No patient records found</h3>
                        <p style="margin-bottom: 24px;">Start by making your first prediction</p>
                        <a href="predict.php" class="btn btn-primary">
                            <i class="fas fa-plus-circle"></i> New Prediction
                        </a>
                    </div>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Simple search functionality
        document.getElementById('searchInput').addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const table = document.getElementById('patientsTable');
            const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
            
            for (let i = 0; i < rows.length; i++) {
                const row = rows[i];
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            }
        });
    </script>
</body>
</html>
