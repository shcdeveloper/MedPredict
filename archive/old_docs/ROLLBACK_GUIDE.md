# Model Versioning & Rollback Guide

## Overview
This guide explains how to version models, rollback to previous versions, and manage model deployments safely.

---

## 📦 Model Versioning Strategy

### Version Naming Convention
```
models/
├── v1.0.0/
│   ├── admission_model.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   ├── feature_names.pkl
│   └── model_metadata.pkl
├── v1.1.0/
│   └── ...
└── current/  (symlink to active version)
```

### Metadata Schema
Each model version includes `model_metadata.pkl` with:
```python
{
    'version': '1.0.0',
    'trained_at': '2026-01-20T10:30:00',
    'model_type': 'RandomForestClassifier',
    'training_dataset': 'patient_data_processed.csv',
    'training_samples': 1000,
    'metrics': {
        'accuracy': 0.89,
        'roc_auc': 0.9378,
        'precision': 0.87,
        'recall': 0.91,
        'f1': 0.89
    },
    'features': ['age', 'heart_rate', 'glucose', 'prior_admission', 'gender_encoded'],
    'hyperparameters': {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42
    },
    'python_version': '3.13.5',
    'dependencies': {
        'scikit-learn': '1.3.0',
        'numpy': '1.24.3',
        'pandas': '2.0.3'
    }
}
```

---

## 🔄 Versioning Workflow

### 1. Create New Model Version

```powershell
# Train new model
python -m api.train_model

# Version the model
$version = "v1.1.0"
New-Item -ItemType Directory -Path "models/$version"
Copy-Item "models/*.pkl" -Destination "models/$version/"

# Update metadata with version
python -c @"
import joblib
from datetime import datetime

metadata = joblib.load('models/$version/model_metadata.pkl')
metadata['version'] = '$version'
metadata['deployed_at'] = datetime.now().isoformat()
joblib.dump(metadata, 'models/$version/model_metadata.pkl')
"@
```

### 2. Tag in Git
```powershell
git add models/$version/
git commit -m "Add model version $version - ROC-AUC: 0.XX"
git tag -a $version -m "Model version $version"
git push origin $version
```

### 3. Deploy New Version
```powershell
# Backup current model
Copy-Item "models/*.pkl" -Destination "models/backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')/"

# Deploy new version
Copy-Item "models/$version/*.pkl" -Destination "models/"

# Restart API
# (API will automatically load new models on restart)
```

---

## ⏮️ Rollback Procedures

### Quick Rollback (Emergency)

**When to use**: Production model is making bad predictions

**Steps**:
```powershell
# 1. Stop the API
# Press Ctrl+C in API terminal or:
Stop-Process -Name "python" -Force

# 2. Restore previous version
$previousVersion = "v1.0.0"
Copy-Item "models/$previousVersion/*.pkl" -Destination "models/" -Force

# 3. Restart API
cd api
python -m uvicorn main:app --reload --port 8000

# 4. Verify health
Invoke-RestMethod http://localhost:8000/health

# 5. Log rollback
$rollbackLog = @{
    timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    from_version = "v1.1.0"
    to_version = $previousVersion
    reason = "High error rate in production"
    performed_by = $env:USERNAME
} | ConvertTo-Json

Add-Content -Path "models/rollback_log.json" -Value $rollbackLog
```

**Estimated Time**: 2-3 minutes

---

### Planned Rollback (Scheduled)

**When to use**: Scheduled maintenance or known issues

**Steps**:
```powershell
# 1. Notify users (if applicable)
# Send notification 30 minutes before

# 2. Enable maintenance mode (optional)
# Update config to return "Under Maintenance" message

# 3. Backup current model
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
New-Item -ItemType Directory -Path "models/backup_$timestamp"
Copy-Item "models/*.pkl" -Destination "models/backup_$timestamp/"

# 4. Switch to previous version
$targetVersion = "v1.0.0"
Copy-Item "models/$targetVersion/*.pkl" -Destination "models/" -Force

# 5. Restart API gracefully
# Wait for current requests to finish (if using --timeout-graceful-shutdown)

# 6. Run smoke tests
python test_api_quick.py

# 7. Monitor for 15 minutes
python monitoring.py --interval 60
```

**Estimated Time**: 15-20 minutes

---

### Automated Rollback (Performance-Based)

**When to use**: Continuous monitoring detects degraded performance

**Trigger Conditions**:
- Response time > 1000ms for 5 consecutive requests
- Error rate > 5% over 10 minutes
- Prediction accuracy drops below threshold

**Implementation**:
```python
# monitoring.py already has basic checks
# Extend with auto-rollback:

def auto_rollback_if_needed(self):
    metrics = self.check_model_performance()
    
    # Check conditions
    if metrics.get('avg_response_time_ms', 0) > 1000:
        print("⚠️  High latency detected - initiating rollback")
        self.execute_rollback(reason="High latency")
        return True
    
    return False

def execute_rollback(self, reason):
    import subprocess
    
    # Log rollback decision
    self.log_alert('auto_rollback', f"Automatic rollback triggered: {reason}", 'critical')
    
    # Execute rollback script
    subprocess.run(['powershell', '-File', 'scripts/rollback.ps1'])
```

---

## 🧪 Testing Before Deployment

### Pre-Deployment Checklist

1. **Unit Tests**
   ```powershell
   pytest tests/ -v
   ```

2. **API Tests**
   ```powershell
   python test_api_quick.py
   ```

3. **Performance Baseline**
   ```powershell
   # Test with sample data
   $body = @{
       age = 65
       gender = "M"
       heart_rate = 95
       glucose = 140.5
       prior_admission = 2
   } | ConvertTo-Json
   
   Measure-Command {
       Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $body -ContentType "application/json"
   }
   ```

4. **Model Comparison**
   ```python
   # Compare new vs old model
   import joblib
   
   old_model = joblib.load('models/v1.0.0/admission_model.pkl')
   new_model = joblib.load('models/v1.1.0/admission_model.pkl')
   
   # Test on validation set
   # Ensure new model improves by at least 1% on key metrics
   ```

---

## 📊 Model Registry

### Manual Registry (Current Implementation)

**File**: `models/model_registry.json`

```json
{
  "models": [
    {
      "version": "v1.0.0",
      "deployed_at": "2026-01-20T10:30:00",
      "status": "deprecated",
      "metrics": {
        "roc_auc": 0.9378,
        "accuracy": 0.89
      }
    },
    {
      "version": "v1.1.0",
      "deployed_at": "2026-01-21T14:00:00",
      "status": "active",
      "metrics": {
        "roc_auc": 0.9412,
        "accuracy": 0.91
      }
    }
  ],
  "active_version": "v1.1.0"
}
```

### Future: MLflow Registry Integration

```python
# Example for future implementation
import mlflow

# Log model
with mlflow.start_run():
    mlflow.sklearn.log_model(model, "admission_model")
    mlflow.log_metrics({
        "roc_auc": 0.9378,
        "accuracy": 0.89
    })
    mlflow.log_params({
        "n_estimators": 100,
        "max_depth": 10
    })

# Register model
mlflow.register_model(
    "runs:/<run_id>/admission_model",
    "HealthcareAdmissionModel"
)

# Promote to production
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="HealthcareAdmissionModel",
    version=1,
    stage="Production"
)
```

---

## 🔐 Rollback Safety Measures

### Pre-Rollback Checks
- ✅ Backup current model
- ✅ Verify target version exists
- ✅ Check compatibility (Python version, dependencies)
- ✅ Review rollback plan with team

### Post-Rollback Validation
- ✅ Health check passes
- ✅ Sample predictions return expected values
- ✅ Response time < 500ms
- ✅ No errors in logs
- ✅ Monitor for 1 hour

### Documentation
- 📝 Log all rollbacks in `models/rollback_log.json`
- 📝 Update incident report
- 📝 Schedule post-mortem meeting

---

## 📈 Version Comparison

```powershell
# Compare two model versions
python -c @"
import joblib
import pandas as pd
from sklearn.metrics import roc_auc_score

# Load models
model_v1 = joblib.load('models/v1.0.0/admission_model.pkl')
model_v2 = joblib.load('models/v1.1.0/admission_model.pkl')

# Load test data
test_data = pd.read_csv('data/processed/test_set.csv')
X_test = test_data.drop('admission', axis=1)
y_test = test_data['admission']

# Compare
print('Version 1.0.0 ROC-AUC:', roc_auc_score(y_test, model_v1.predict_proba(X_test)[:, 1]))
print('Version 1.1.0 ROC-AUC:', roc_auc_score(y_test, model_v2.predict_proba(X_test)[:, 1]))
"@
```

---

## 🚀 Deployment Strategy

### Blue-Green Deployment (Future)

**Setup**:
- Blue environment: Current production model
- Green environment: New model version

**Process**:
1. Deploy new model to Green
2. Run smoke tests
3. Route 10% traffic to Green
4. Monitor for 1 hour
5. If metrics OK, route 100% to Green
6. Keep Blue for 24 hours for quick rollback

### Canary Deployment (Future)

**Process**:
1. Deploy v1.1.0 to 5% of users
2. Monitor metrics for both versions
3. Gradually increase to 25%, 50%, 100%
4. Rollback at any sign of degradation

---

## 📞 Emergency Contacts

**On-Call Engineer**: (Add contact info)
**Rollback Authority**: (Add approval chain)
**Escalation**: (Add escalation path)

---

## 🔧 Rollback Script

**File**: `scripts/rollback.ps1`

```powershell
param(
    [string]$TargetVersion = "v1.0.0",
    [string]$Reason = "Manual rollback"
)

Write-Host "🔄 Starting rollback to $TargetVersion" -ForegroundColor Yellow

# 1. Backup current
$backupDir = "models/backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir
Copy-Item "models/*.pkl" -Destination $backupDir/

# 2. Restore target version
Copy-Item "models/$TargetVersion/*.pkl" -Destination "models/" -Force

# 3. Log rollback
$log = @{
    timestamp = Get-Date -Format "o"
    to_version = $TargetVersion
    reason = $Reason
    performed_by = $env:USERNAME
} | ConvertTo-Json

Add-Content -Path "models/rollback_log.json" -Value $log

Write-Host "✅ Rollback complete" -ForegroundColor Green
Write-Host "⚠️  Please restart the API server" -ForegroundColor Yellow
```

---

## Summary

**Key Takeaways**:
- ✅ Always backup before deployment
- ✅ Version everything (model + metadata)
- ✅ Test before deploying
- ✅ Monitor after deployment
- ✅ Have rollback plan ready
- ✅ Log all changes

**Recovery Time Objectives**:
- Emergency Rollback: < 5 minutes
- Planned Rollback: < 20 minutes
- Automated Rollback: < 2 minutes
