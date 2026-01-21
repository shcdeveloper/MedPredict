<?php
require_once 'config/auth.php';
require_once 'config/db.php';

requireLogin();
$user = getCurrentUser();

// Get all disease risk assessments
$conn = getDBConnection();

// Pagination
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$per_page = 20;
$offset = ($page - 1) * $per_page;

// Get total count
$count_result = $conn->query("SELECT COUNT(*) as total FROM disease_risk_assessments");
$total_records = $count_result->fetch_assoc()['total'];
$total_pages = ceil($total_records / $per_page);

// Get assessments with pagination
$sql = "
    SELECT 
        id,
        age,
        gender,
        bmi,
        smoking,
        alcohol,
        exercise,
        family_diabetes,
        family_heart_disease,
        family_hypertension,
        systolic_bp,
        diastolic_bp,
        heart_rate,
        glucose,
        cholesterol,
        hdl,
        ldl,
        triglycerides,
        diabetes_risk,
        diabetes_level,
        heart_disease_risk,
        heart_disease_level,
        hypertension_risk,
        hypertension_level,
        overall_risk,
        created_at
    FROM disease_risk_assessments
    ORDER BY created_at DESC
    LIMIT $per_page OFFSET $offset
";

$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disease Risk Assessments - Healthcare System</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="assets/css/admin.css">
    <style>
        /* Additional styles specific to disease risk table */
        .page-header {
            margin-bottom: 30px;
        }

        .page-title {
            font-size: 28px;
            font-weight: 600;
            color: var(--dark);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .page-subtitle {
            color: var(--secondary);
            font-size: 14px;
        }

        .table-container {
            background: white;
            border-radius: 12px;
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        .table-header {
            padding: 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .table-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--dark);
        }

        .search-box {
            padding: 8px 16px;
            border: 1px solid var(--border);
            border-radius: 6px;
            font-size: 14px;
            width: 300px;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
        }

        .data-table thead {
            background: #f8fafc;
        }

        .data-table th {
            padding: 12px 16px;
            text-align: left;
            font-size: 11px;
            font-weight: 600;
            color: var(--secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
            border-bottom: 2px solid var(--border);
        }

        .data-table tbody tr {
            border-bottom: 1px solid #f1f5f9;
            transition: all 0.2s;
        }

        .data-table tbody tr:hover {
            background: #f8fafc;
        }

        .data-table td {
            padding: 16px;
            font-size: 14px;
            color: var(--dark);
            vertical-align: middle;
        }

        .data-table tr:hover {
            background: #f8fafc;
        }

        .table-wrapper {
            overflow-x: auto;
        }

        .risk-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }

        .risk-low {
            background: #dcfce7;
            color: #166534;
        }

        .risk-medium {
            background: #fef3c7;
            color: #92400e;
        }

        .risk-high {
            background: #fee2e2;
            color: #991b1b;
        }

        .risk-score {
            font-weight: 600;
            font-size: 16px;
        }

        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            padding: 20px;
            border-top: 1px solid var(--border);
        }

        .pagination a, .pagination span {
            padding: 8px 12px;
            border: 1px solid var(--border);
            border-radius: 6px;
            text-decoration: none;
            color: var(--secondary);
            font-size: 14px;
        }

        .pagination a:hover {
            background: #f8fafc;
            border-color: var(--primary);
            color: var(--primary);
        }

        .pagination .active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }

        .view-btn {
            padding: 6px 12px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            text-decoration: none;
            display: inline-block;
        }

        .view-btn:hover {
            background: var(--primary-dark);
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            overflow-y: auto;
        }

        .modal-content {
            background: white;
            margin: 50px auto;
            padding: 0;
            width: 90%;
            max-width: 800px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }

        .modal-header {
            padding: 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-title {
            font-size: 20px;
            font-weight: 600;
            color: var(--dark);
        }

        .close {
            font-size: 28px;
            color: #94a3b8;
            cursor: pointer;
        }

        .close:hover {
            color: #64748b;
        }

        .modal-body {
            padding: 20px;
        }

        .detail-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }

        .detail-section {
            background: #f8fafc;
            padding: 15px;
            border-radius: 8px;
        }

        .detail-section h3 {
            font-size: 14px;
            font-weight: 600;
            color: var(--secondary);
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid var(--border);
        }

        .detail-row:last-child {
            border-bottom: none;
        }

        .detail-label {
            color: var(--secondary);
            font-size: 14px;
        }

        .detail-value {
            color: var(--dark);
            font-weight: 600;
            font-size: 14px;
        }
    </style>
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
                <span>Disease Risk</span>
            </a>
            <a href="disease_risk_table.php" class="menu-item active">
                <i class="fas fa-table"></i>
                <span>Risk Assessments</span>
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
            <h1 class="header-title">Disease Risk Assessments</h1>
            <div class="header-actions">
                <div class="user-menu">
                    <div class="user-avatar">
                        <?php echo strtoupper(substr($user['full_name'], 0, 1)); ?>
                    </div>
                    <div class="user-info">
                        <div class="user-name"><?php echo htmlspecialchars($user['full_name']); ?></div>
                        <div class="user-role"><?php echo ucfirst($user['role']); ?></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Dashboard Content -->
        <div class="dashboard-content">
            <!-- Page Header -->
            <div class="page-header">
                <h1 class="page-title">
                    <i class="fas fa-heartbeat" style="color: var(--primary);"></i>
                    Disease Risk Assessments
                </h1>
                <p class="page-subtitle">View comprehensive health risk assessments for all patients</p>
            </div>

            <!-- Statistics -->
            <?php
            // Get statistics
            $stats = $conn->query("
                SELECT 
                    COUNT(*) as total,
                    AVG(overall_risk) as avg_overall_risk,
                    SUM(CASE WHEN diabetes_level = 'High' THEN 1 ELSE 0 END) as high_diabetes,
                    SUM(CASE WHEN heart_disease_level = 'High' THEN 1 ELSE 0 END) as high_heart,
                    SUM(CASE WHEN hypertension_level = 'High' THEN 1 ELSE 0 END) as high_hypertension
                FROM disease_risk_assessments
            ")->fetch_assoc();
            ?>

            <div class="stats-grid">
                <div class="stat-card primary">
                    <div class="stat-icon"><i class="fas fa-clipboard-list"></i></div>
                    <div class="stat-label">Total Assessments</div>
                    <div class="stat-value"><?php echo number_format($stats['total']); ?></div>
                    <div class="stat-change">
                        <i class="fas fa-database"></i> Complete profiles
                    </div>
                </div>
                <div class="stat-card info">
                    <div class="stat-icon"><i class="fas fa-percent"></i></div>
                    <div class="stat-label">Average Overall Risk</div>
                    <div class="stat-value"><?php echo number_format($stats['avg_overall_risk'] * 100, 1); ?>%</div>
                    <div class="stat-change">
                        Population average
                    </div>
                </div>
                <div class="stat-card high">
                    <div class="stat-icon"><i class="fas fa-syringe"></i></div>
                    <div class="stat-label">High Diabetes Risk</div>
                    <div class="stat-value"><?php echo $stats['high_diabetes']; ?></div>
                    <div class="stat-change">
                        <i class="fas fa-exclamation-triangle"></i> Requires monitoring
                    </div>
                </div>
                <div class="stat-card high">
                    <div class="stat-icon"><i class="fas fa-heart"></i></div>
                    <div class="stat-label">High Heart Disease Risk</div>
                    <div class="stat-value"><?php echo $stats['high_heart']; ?></div>
                    <div class="stat-change">
                        <i class="fas fa-exclamation-triangle"></i> Requires monitoring
                    </div>
                </div>
                <div class="stat-card high">
                    <div class="stat-icon"><i class="fas fa-heartbeat"></i></div>
                    <div class="stat-label">High Hypertension Risk</div>
                    <div class="stat-value"><?php echo $stats['high_hypertension']; ?></div>
                    <div class="stat-change">
                        <i class="fas fa-exclamation-triangle"></i> Requires monitoring
                    </div>
                </div>
            </div>

            <!-- Table -->
            <div class="table-container">
                <div class="table-header">
                    <div class="table-title">
                        <i class="fas fa-table"></i> All Assessments (<?php echo $total_records; ?>)
                    </div>
                    <input type="text" class="search-box" id="searchBox" placeholder="Search by age, gender..." onkeyup="searchTable()">
                </div>

                <div class="table-wrapper">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Age</th>
                                <th>Gender</th>
                                <th>BMI</th>
                                <th>Overall Risk</th>
                                <th>Diabetes</th>
                                <th>Heart Disease</th>
                                <th>Hypertension</th>
                                <th>Glucose</th>
                                <th>BP</th>
                                <th>Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="tableBody">
                            <?php while ($row = $result->fetch_assoc()): ?>
                            <tr>
                                <td><strong>#<?php echo $row['id']; ?></strong></td>
                                <td><?php echo $row['age']; ?> yrs</td>
                                <td>
                                    <i class="fas fa-<?php echo $row['gender'] === 'Male' ? 'mars' : 'venus'; ?>" 
                                       style="color: <?php echo $row['gender'] === 'Male' ? '#3b82f6' : '#ec4899'; ?>;">
                                    </i>
                                    <?php echo $row['gender']; ?>
                                </td>
                                <td><?php echo number_format($row['bmi'], 1); ?></td>
                                <td>
                                    <span class="risk-score" style="color: <?php 
                                        echo $row['overall_risk'] > 0.6 ? 'var(--danger)' : ($row['overall_risk'] > 0.3 ? 'var(--warning)' : 'var(--success)'); 
                                    ?>; font-weight: 700; font-size: 16px;">
                                        <?php echo number_format($row['overall_risk'] * 100, 1); ?>%
                                    </span>
                                </td>
                                <td>
                                    <span class="risk-badge risk-<?php echo strtolower($row['diabetes_level']); ?>">
                                        <?php echo $row['diabetes_level']; ?>
                                    </span>
                                </td>
                                <td>
                                    <span class="risk-badge risk-<?php echo strtolower($row['heart_disease_level']); ?>">
                                        <?php echo $row['heart_disease_level']; ?>
                                    </span>
                                </td>
                                <td>
                                    <span class="risk-badge risk-<?php echo strtolower($row['hypertension_level']); ?>">
                                        <?php echo $row['hypertension_level']; ?>
                                    </span>
                                </td>
                                <td>
                                    <span style="<?php echo $row['glucose'] > 125 ? 'color: var(--danger); font-weight: 600;' : ''; ?>">
                                        <?php echo $row['glucose']; ?> mg/dL
                                    </span>
                                </td>
                                <td>
                                    <span style="<?php echo $row['systolic_bp'] > 140 ? 'color: var(--danger); font-weight: 600;' : ''; ?>">
                                        <?php echo $row['systolic_bp']; ?>/<?php echo $row['diastolic_bp']; ?>
                                    </span>
                                </td>
                                <td style="color: var(--secondary); font-size: 13px;">
                                    <?php echo date('M d, Y', strtotime($row['created_at'])); ?>
                                </td>
                                <td>
                                    <button class="view-btn" onclick='viewDetails(<?php echo json_encode($row); ?>)'>
                                        <i class="fas fa-eye"></i> View
                                    </button>
                                </td>
                            </tr>
                            <?php endwhile; ?>
                        </tbody>
                    </table>
                </div>

                <!-- Pagination -->
                <div class="pagination">
                    <?php if ($page > 1): ?>
                        <a href="?page=<?php echo $page - 1; ?>">
                            <i class="fas fa-chevron-left"></i> Previous
                        </a>
                    <?php endif; ?>

                    <?php for ($i = max(1, $page - 2); $i <= min($total_pages, $page + 2); $i++): ?>
                        <a href="?page=<?php echo $i; ?>" class="<?php echo $i === $page ? 'active' : ''; ?>">
                            <?php echo $i; ?>
                        </a>
                    <?php endfor; ?>

                    <?php if ($page < $total_pages): ?>
                        <a href="?page=<?php echo $page + 1; ?>">
                            Next <i class="fas fa-chevron-right"></i>
                        </a>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal for Details -->
    <div id="detailModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">
                    <i class="fas fa-file-medical"></i> Assessment Details
                </h2>
                <span class="close" onclick="closeModal()">&times;</span>
            </div>
            <div class="modal-body" id="modalBody">
                <!-- Details will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        function searchTable() {
            const input = document.getElementById('searchBox');
            const filter = input.value.toUpperCase();
            const table = document.getElementById('tableBody');
            const rows = table.getElementsByTagName('tr');

            for (let i = 0; i < rows.length; i++) {
                const row = rows[i];
                const text = row.textContent || row.innerText;
                
                if (text.toUpperCase().indexOf(filter) > -1) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            }
        }

        function viewDetails(data) {
            const modal = document.getElementById('detailModal');
            const modalBody = document.getElementById('modalBody');
            
            modalBody.innerHTML = `
                <div class="detail-grid">
                    <div class="detail-section">
                        <h3><i class="fas fa-user"></i> Demographics</h3>
                        <div class="detail-row">
                            <span class="detail-label">Age:</span>
                            <span class="detail-value">${data.age} years</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Gender:</span>
                            <span class="detail-value">${data.gender}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">BMI:</span>
                            <span class="detail-value">${parseFloat(data.bmi).toFixed(1)}</span>
                        </div>
                    </div>

                    <div class="detail-section">
                        <h3><i class="fas fa-smoking"></i> Lifestyle</h3>
                        <div class="detail-row">
                            <span class="detail-label">Smoking:</span>
                            <span class="detail-value">${data.smoking}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Alcohol:</span>
                            <span class="detail-value">${data.alcohol}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Exercise:</span>
                            <span class="detail-value">${data.exercise}</span>
                        </div>
                    </div>

                    <div class="detail-section">
                        <h3><i class="fas fa-dna"></i> Family History</h3>
                        <div class="detail-row">
                            <span class="detail-label">Diabetes:</span>
                            <span class="detail-value">${data.family_diabetes ? 'Yes' : 'No'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Heart Disease:</span>
                            <span class="detail-value">${data.family_heart_disease ? 'Yes' : 'No'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Hypertension:</span>
                            <span class="detail-value">${data.family_hypertension ? 'Yes' : 'No'}</span>
                        </div>
                    </div>

                    <div class="detail-section">
                        <h3><i class="fas fa-heartbeat"></i> Vital Signs</h3>
                        <div class="detail-row">
                            <span class="detail-label">Blood Pressure:</span>
                            <span class="detail-value">${data.systolic_bp}/${data.diastolic_bp} mmHg</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Heart Rate:</span>
                            <span class="detail-value">${data.heart_rate} bpm</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Glucose:</span>
                            <span class="detail-value">${data.glucose} mg/dL</span>
                        </div>
                    </div>

                    <div class="detail-section">
                        <h3><i class="fas fa-vial"></i> Lab Results</h3>
                        <div class="detail-row">
                            <span class="detail-label">Cholesterol:</span>
                            <span class="detail-value">${data.cholesterol} mg/dL</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">HDL:</span>
                            <span class="detail-value">${data.hdl} mg/dL</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">LDL:</span>
                            <span class="detail-value">${data.ldl} mg/dL</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Triglycerides:</span>
                            <span class="detail-value">${data.triglycerides} mg/dL</span>
                        </div>
                    </div>

                    <div class="detail-section">
                        <h3><i class="fas fa-exclamation-triangle"></i> Risk Assessment</h3>
                        <div class="detail-row">
                            <span class="detail-label">Overall Risk:</span>
                            <span class="detail-value" style="color: #FF6D1F; font-size: 18px;">
                                ${(data.overall_risk * 100).toFixed(1)}%
                            </span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Diabetes:</span>
                            <span class="detail-value">
                                <span class="risk-badge risk-${data.diabetes_level.toLowerCase()}">
                                    ${data.diabetes_level} (${(data.diabetes_risk * 100).toFixed(1)}%)
                                </span>
                            </span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Heart Disease:</span>
                            <span class="detail-value">
                                <span class="risk-badge risk-${data.heart_disease_level.toLowerCase()}">
                                    ${data.heart_disease_level} (${(data.heart_disease_risk * 100).toFixed(1)}%)
                                </span>
                            </span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Hypertension:</span>
                            <span class="detail-value">
                                <span class="risk-badge risk-${data.hypertension_level.toLowerCase()}">
                                    ${data.hypertension_level} (${(data.hypertension_risk * 100).toFixed(1)}%)
                                </span>
                            </span>
                        </div>
                    </div>
                </div>
            `;
            
            modal.style.display = 'block';
        }

        function closeModal() {
            document.getElementById('detailModal').style.display = 'none';
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('detailModal');
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        }
    </script>
</body>
</html>
