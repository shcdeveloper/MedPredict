"""
Test script to verify API is working
"""
import requests
import json

# Test health endpoint
print("Testing API Health...")
try:
    response = requests.get("http://localhost:8000/health")
    print(f"✓ Health Check: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure API is running: uvicorn main:app --reload")
    exit(1)

# Test prediction endpoint
print("\nTesting Prediction...")
data = {
    "age": 65,
    "gender": "M",
    "heart_rate": 95,
    "glucose": 140.5,
    "prior_admission": 2
}

try:
    response = requests.post("http://localhost:8000/predict", json=data)
    result = response.json()
    print(f"✓ Prediction Result:")
    print(f"  - Admission Probability: {result['admission_probability']}")
    print(f"  - Risk Level: {result['risk_level']}")
    print(f"  - Message: {result['message']}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n✅ API is working correctly!")
print("\nNext steps:")
print("1. Make sure XAMPP MySQL is running")
print("2. Run database/setup.sql in phpMyAdmin")
print("3. Open http://localhost/webapp/ in your browser")
