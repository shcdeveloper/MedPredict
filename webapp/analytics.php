<?php
require_once 'config/auth.php';
require_once 'config/db.php';

requireLogin();
$user = getCurrentUser();

// Fetch analytics data
try {
    // 1. Admission predictions over time (last 30 days)
    $stmt = $pdo->query("
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as total_predictions,
            SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) as high_risk_count,
            SUM(CASE WHEN risk_level = 'Low' THEN 1 ELSE 0 END) as low_risk_count
        FROM patient_requests
        WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    ");
    $timeSeriesData = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // 2. Age distribution
    $stmt = $pdo->query("
        SELECT 
            CASE 
                WHEN age < 30 THEN '18-29'
                WHEN age >= 30 AND age < 40 THEN '30-39'
                WHEN age >= 40 AND age < 50 THEN '40-49'
                WHEN age >= 50 AND age < 60 THEN '50-59'
                WHEN age >= 60 AND age < 70 THEN '60-69'
                ELSE '70+'
            END as age_group,
            COUNT(*) as count,
            SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) as high_risk
        FROM patient_requests
        GROUP BY age_group
        ORDER BY age_group
    ");
    $ageDistribution = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // 3. Gender distribution
    $stmt = $pdo->query("
        SELECT 
            gender,
            COUNT(*) as count,
            ROUND(AVG(prediction) * 100, 1) as avg_risk
        FROM patient_requests
        GROUP BY gender
    ");
    $genderDistribution = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // 4. Risk level frequency
    $stmt = $pdo->query("
        SELECT 
            risk_level as `condition`,
            COUNT(*) as count,
            ROUND(AVG(prediction) * 100, 1) as avg_risk
        FROM patient_requests
        GROUP BY risk_level
        ORDER BY count DESC
    ");
    $medicalConditions = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // 5. Risk distribution
    $stmt = $pdo->query("
        SELECT 
            risk_level as prediction_result,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM patient_requests), 1) as percentage
        FROM patient_requests
        GROUP BY risk_level
    ");
    $riskDistribution = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // 6. Summary statistics
    $stmt = $pdo->query("
        SELECT 
            COUNT(*) as total_predictions,
            COUNT(DISTINCT user_id) as active_users,
            ROUND(AVG(prediction) * 100, 1) as avg_risk_score,
            MAX(created_at) as last_prediction_date
        FROM patient_requests
    ");
    $summaryStats = $stmt->fetch(PDO::FETCH_ASSOC);
    
} catch (PDOException $e) {
    $error = "Error fetching analytics: " . $e->getMessage();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics - Healthcare Admission System</title>
    <link rel="stylesheet" href="assets/css/admin.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 24px;
            margin-bottom: 24px;
        }
        
        .chart-card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: var(--shadow);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .chart-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        .chart-card.full-width {
            grid-column: 1 / -1;
        }
        
        .chart-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }
        
        .chart-header i {
            font-size: 24px;
            color: var(--primary);
        }
        
        .chart-header h3 {
            font-size: 18px;
            font-weight: 600;
            color: var(--dark);
            margin: 0;
        }
        
        .chart-wrapper {
            position: relative;
            height: 300px;
        }
        
        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }
        
        .stat-card-analytics {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: var(--shadow);
            display: flex;
            flex-direction: column;
            gap: 8px;
            border-left: 4px solid;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .stat-card-analytics:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }
        
        .stat-card-analytics:nth-child(1) {
            border-color: var(--primary);
            background: linear-gradient(135deg, #FFEDD5 0%, #FED7AA 100%);
        }
        
        .stat-card-analytics:nth-child(2) {
            border-color: var(--info);
            background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        }
        
        .stat-card-analytics:nth-child(3) {
            border-color: var(--purple);
            background: linear-gradient(135deg, #EDE9FE 0%, #DDD6FE 100%);
        }
        
        .stat-card-analytics:nth-child(4) {
            border-color: var(--teal);
            background: linear-gradient(135deg, #CCFBF1 0%, #99F6E4 100%);
        }
        
        .stat-card-analytics .stat-value {
            font-size: 32px;
            font-weight: 700;
            color: var(--dark);
        }
        
        .stat-card-analytics .stat-label {
            font-size: 14px;
            color: var(--secondary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        @media (max-width: 768px) {
            .analytics-grid {
                grid-template-columns: 1fr;
            }
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
            <a href="analytics.php" class="menu-item active">
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
            <h1 class="header-title">Analytics & Reports</h1>
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
            <?php if (isset($error)): ?>
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle"></i>
                    <?php echo htmlspecialchars($error); ?>
                </div>
            <?php else: ?>
                <!-- Summary Statistics -->
                <div class="summary-stats">
                    <div class="stat-card-analytics">
                        <div class="stat-value"><?php echo number_format($summaryStats['total_predictions']); ?></div>
                        <div class="stat-label">Total Predictions</div>
                    </div>
                    <div class="stat-card-analytics">
                        <div class="stat-value"><?php echo $summaryStats['active_users']; ?></div>
                        <div class="stat-label">Active Users</div>
                    </div>
                    <div class="stat-card-analytics">
                        <div class="stat-value"><?php echo $summaryStats['avg_risk_score']; ?>%</div>
                        <div class="stat-label">Average Risk Score</div>
                    </div>
                    <div class="stat-card-analytics">
                        <div class="stat-value"><?php echo date('M d', strtotime($summaryStats['last_prediction_date'])); ?></div>
                        <div class="stat-label">Last Activity</div>
                    </div>
                </div>

                <!-- Charts Grid -->
                <div class="analytics-grid">
                    <!-- Predictions Over Time -->
                    <div class="chart-card full-width">
                        <div class="chart-header">
                            <i class="fas fa-chart-line"></i>
                            <h3>Predictions Over Time (Last 30 Days)</h3>
                        </div>
                        <div class="chart-wrapper">
                            <canvas id="timeSeriesChart"></canvas>
                        </div>
                    </div>

                    <!-- Risk Distribution -->
                    <div class="chart-card">
                        <div class="chart-header">
                            <i class="fas fa-chart-pie"></i>
                            <h3>Risk Distribution</h3>
                        </div>
                        <div class="chart-wrapper">
                            <canvas id="riskPieChart"></canvas>
                        </div>
                    </div>

                    <!-- Age Distribution -->
                    <div class="chart-card">
                        <div class="chart-header">
                            <i class="fas fa-chart-bar"></i>
                            <h3>Age Group Distribution</h3>
                        </div>
                        <div class="chart-wrapper">
                            <canvas id="ageChart"></canvas>
                        </div>
                    </div>

                    <!-- Gender Distribution -->
                    <div class="chart-card">
                        <div class="chart-header">
                            <i class="fas fa-venus-mars"></i>
                            <h3>Gender Distribution</h3>
                        </div>
                        <div class="chart-wrapper">
                            <canvas id="genderChart"></canvas>
                        </div>
                    </div>

                    <!-- Risk Levels -->
                    <div class="chart-card">
                        <div class="chart-header">
                            <i class="fas fa-exclamation-triangle"></i>
                            <h3>Risk Levels</h3>
                        </div>
                        <div class="chart-wrapper">
                            <canvas id="conditionsChart"></canvas>
                        </div>
                    </div>
                </div>
            <?php endif; ?>
        </div>
    </div>

    <script>
        // Prepare data for charts
        const timeSeriesData = <?php echo json_encode($timeSeriesData); ?>;
        const ageDistribution = <?php echo json_encode($ageDistribution); ?>;
        const genderDistribution = <?php echo json_encode($genderDistribution); ?>;
        const medicalConditions = <?php echo json_encode($medicalConditions); ?>;
        const riskDistribution = <?php echo json_encode($riskDistribution); ?>;

        // 1. Time Series Chart
        new Chart(document.getElementById('timeSeriesChart'), {
            type: 'line',
            data: {
                labels: timeSeriesData.map(d => d.date),
                datasets: [
                    {
                        label: 'Total Predictions',
                        data: timeSeriesData.map(d => d.total_predictions),
                        borderColor: '#FF6D1F',
                        backgroundColor: 'rgba(255, 109, 31, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'High Risk',
                        data: timeSeriesData.map(d => d.high_risk_count),
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Low Risk',
                        data: timeSeriesData.map(d => d.low_risk_count),
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // 2. Risk Pie Chart
        new Chart(document.getElementById('riskPieChart'), {
            type: 'doughnut',
            data: {
                labels: riskDistribution.map(d => d.prediction_result),
                datasets: [{
                    data: riskDistribution.map(d => d.count),
                    backgroundColor: ['#ef4444', '#10b981', '#f59e0b'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        // 3. Age Distribution Chart
        new Chart(document.getElementById('ageChart'), {
            type: 'bar',
            data: {
                labels: ageDistribution.map(d => d.age_group),
                datasets: [
                    {
                        label: 'Total Patients',
                        data: ageDistribution.map(d => d.count),
                        backgroundColor: 'rgba(255, 109, 31, 0.8)',
                        borderColor: '#FF6D1F',
                        borderWidth: 1
                    },
                    {
                        label: 'High Risk',
                        data: ageDistribution.map(d => d.high_risk),
                        backgroundColor: 'rgba(239, 68, 68, 0.8)',
                        borderColor: '#ef4444',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // 4. Gender Chart
        new Chart(document.getElementById('genderChart'), {
            type: 'bar',
            data: {
                labels: genderDistribution.map(d => d.gender === 'M' ? 'Male' : 'Female'),
                datasets: [{
                    label: 'Patient Count',
                    data: genderDistribution.map(d => d.count),
                    backgroundColor: ['rgba(255, 109, 31, 0.8)', 'rgba(168, 85, 247, 0.8)'],
                    borderColor: ['#FF6D1F', '#a855f7'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // 5. Medical Conditions Chart
        new Chart(document.getElementById('conditionsChart'), {
            type: 'bar',
            data: {
                labels: medicalConditions.map(d => d.condition),
                datasets: [{
                    label: 'Patient Count',
                    data: medicalConditions.map(d => d.count),
                    backgroundColor: [
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(168, 85, 247, 0.8)'
                    ],
                    borderColor: [
                        '#10b981',
                        '#f59e0b',
                        '#ef4444',
                        '#a855f7'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
