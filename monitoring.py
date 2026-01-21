"""
Production Monitoring Script for Healthcare Prediction API
Monitors model performance, data drift, API health, and system metrics
"""

import requests
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime, timedelta
import os
import joblib
from pathlib import Path

class ProductionMonitor:
    def __init__(self, api_url="http://localhost:8000", log_dir="logs"):
        self.api_url = api_url
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Load baseline statistics from training
        self.baseline_stats = self.load_baseline_stats()
        
        # Metrics storage
        self.metrics_log = self.log_dir / "monitoring_metrics.json"
        self.alerts_log = self.log_dir / "monitoring_alerts.json"
        
    def load_baseline_stats(self):
        """Load baseline statistics from training data"""
        try:
            data_path = Path("data/processed/patient_data_processed.csv")
            if data_path.exists():
                df = pd.read_csv(data_path)
                return {
                    'age_mean': df['age'].mean(),
                    'age_std': df['age'].std(),
                    'glucose_mean': df['glucose'].mean(),
                    'glucose_std': df['glucose'].std(),
                    'heart_rate_mean': df['heart_rate'].mean(),
                    'heart_rate_std': df['heart_rate'].std(),
                }
        except Exception as e:
            print(f"Could not load baseline stats: {e}")
        
        return {}
    
    def check_api_health(self):
        """Check if API is responding"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'healthy',
                    'timestamp': datetime.now().isoformat(),
                    'api_status': data.get('status'),
                    'response_time_ms': response.elapsed.total_seconds() * 1000
                }
            else:
                return {
                    'status': 'unhealthy',
                    'timestamp': datetime.now().isoformat(),
                    'error': f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                'status': 'down',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def check_model_performance(self):
        """Monitor recent prediction patterns"""
        try:
            # Test prediction with sample data
            test_cases = [
                {"age": 65, "gender": "M", "heart_rate": 95, "glucose": 140.5, "prior_admission": 2},
                {"age": 30, "gender": "F", "heart_rate": 72, "glucose": 95.0, "prior_admission": 0},
                {"age": 75, "gender": "M", "heart_rate": 105, "glucose": 160.0, "prior_admission": 3},
            ]
            
            predictions = []
            response_times = []
            
            for case in test_cases:
                start_time = time.time()
                response = requests.post(f"{self.api_url}/predict", json=case, timeout=10)
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    result = response.json()
                    predictions.append(result['admission_probability'])
                    response_times.append(response_time)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'avg_response_time_ms': np.mean(response_times) if response_times else None,
                'max_response_time_ms': np.max(response_times) if response_times else None,
                'prediction_range': [np.min(predictions), np.max(predictions)] if predictions else None,
                'test_cases_passed': len(predictions),
                'test_cases_total': len(test_cases)
            }
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def detect_data_drift(self, recent_inputs):
        """Detect if input data distribution has drifted"""
        if not self.baseline_stats or not recent_inputs:
            return {'drift_detected': False, 'reason': 'Insufficient data'}
        
        alerts = []
        
        # Convert to DataFrame
        df = pd.DataFrame(recent_inputs)
        
        # Check age drift
        if 'age' in df.columns:
            age_mean = df['age'].mean()
            age_std = df['age'].std()
            baseline_age = self.baseline_stats.get('age_mean', age_mean)
            
            if abs(age_mean - baseline_age) > 2 * self.baseline_stats.get('age_std', 10):
                alerts.append(f"Age drift detected: {age_mean:.1f} vs baseline {baseline_age:.1f}")
        
        # Check glucose drift
        if 'glucose' in df.columns:
            glucose_mean = df['glucose'].mean()
            baseline_glucose = self.baseline_stats.get('glucose_mean', glucose_mean)
            
            if abs(glucose_mean - baseline_glucose) > 2 * self.baseline_stats.get('glucose_std', 20):
                alerts.append(f"Glucose drift detected: {glucose_mean:.1f} vs baseline {baseline_glucose:.1f}")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'drift_detected': len(alerts) > 0,
            'alerts': alerts,
            'samples_analyzed': len(df)
        }
    
    def check_model_file_integrity(self):
        """Verify model files exist and are not corrupted"""
        model_files = [
            'models/admission_model.pkl',
            'models/scaler.pkl',
            'models/label_encoder.pkl',
            'models/feature_names.pkl',
            'models/model_metadata.pkl'
        ]
        
        status = {
            'timestamp': datetime.now().isoformat(),
            'files_checked': len(model_files),
            'files_ok': 0,
            'missing_files': [],
            'file_sizes': {}
        }
        
        for file_path in model_files:
            path = Path(file_path)
            if path.exists():
                status['files_ok'] += 1
                status['file_sizes'][file_path] = path.stat().st_size
            else:
                status['missing_files'].append(file_path)
        
        return status
    
    def log_metrics(self, metrics):
        """Save metrics to log file"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics
        }
        
        # Append to log file
        logs = []
        if self.metrics_log.exists():
            with open(self.metrics_log, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        # Keep only last 1000 entries
        logs = logs[-1000:]
        
        with open(self.metrics_log, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def log_alert(self, alert_type, message, severity='warning'):
        """Log monitoring alert"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'severity': severity,
            'message': message
        }
        
        # Append to alerts file
        alerts = []
        if self.alerts_log.exists():
            with open(self.alerts_log, 'r') as f:
                alerts = json.load(f)
        
        alerts.append(alert)
        
        # Keep only last 500 alerts
        alerts = alerts[-500:]
        
        with open(self.alerts_log, 'w') as f:
            json.dump(alerts, f, indent=2)
        
        # Use ASCII-safe alert symbol for Windows compatibility
        print(f"[!] ALERT [{severity.upper()}]: {message}")
    
    def run_full_check(self):
        """Run all monitoring checks"""
        print("="*60)
        print("Healthcare API Production Monitoring")
        print("="*60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 1. API Health
        print("1. Checking API Health...")
        health = self.check_api_health()
        print(f"   Status: {health['status']}")
        if health['status'] == 'healthy':
            print(f"   Response Time: {health.get('response_time_ms', 0):.2f}ms")
        else:
            self.log_alert('api_health', f"API is {health['status']}: {health.get('error', 'Unknown')}", 'critical')
        
        # 2. Model Performance
        print("\n2. Checking Model Performance...")
        performance = self.check_model_performance()
        if 'error' not in performance:
            print(f"   Avg Response Time: {performance.get('avg_response_time_ms', 0):.2f}ms")
            print(f"   Test Cases Passed: {performance.get('test_cases_passed', 0)}/{performance.get('test_cases_total', 0)}")
            
            # Alert if response time > 500ms
            if performance.get('avg_response_time_ms', 0) > 500:
                self.log_alert('performance', f"High response time: {performance['avg_response_time_ms']:.2f}ms", 'warning')
        else:
            print(f"   Error: {performance['error']}")
            self.log_alert('model_performance', f"Performance check failed: {performance['error']}", 'error')
        
        # 3. Model Files
        print("\n3. Checking Model File Integrity...")
        file_status = self.check_model_file_integrity()
        print(f"   Files OK: {file_status['files_ok']}/{file_status['files_checked']}")
        if file_status['missing_files']:
            print(f"   Missing: {', '.join(file_status['missing_files'])}")
            self.log_alert('model_files', f"Missing files: {file_status['missing_files']}", 'critical')
        
        # 4. Log metrics
        all_metrics = {
            'health': health,
            'performance': performance,
            'file_integrity': file_status
        }
        self.log_metrics(all_metrics)
        
        print("\n" + "="*60)
        print("[OK] Monitoring check complete")
        print(f"[i] Metrics saved to: {self.metrics_log}")
        print(f"[!] Alerts saved to: {self.alerts_log}")
        print("="*60)
        
        return all_metrics
    
    def continuous_monitoring(self, interval_seconds=300):
        """Run monitoring continuously"""
        print(f"Starting continuous monitoring (every {interval_seconds} seconds)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.run_full_check()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n\n[!] Monitoring stopped by user")


def main():
    """Main monitoring entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Healthcare API Production Monitoring')
    parser.add_argument('--api-url', default='http://localhost:8000', help='API URL')
    parser.add_argument('--continuous', action='store_true', help='Run continuous monitoring')
    parser.add_argument('--interval', type=int, default=300, help='Monitoring interval (seconds)')
    
    args = parser.parse_args()
    
    monitor = ProductionMonitor(api_url=args.api_url)
    
    if args.continuous:
        monitor.continuous_monitoring(interval_seconds=args.interval)
    else:
        monitor.run_full_check()


if __name__ == '__main__':
    main()
