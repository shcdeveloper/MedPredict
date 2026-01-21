# MedPredict 🏥

Machine learning system that predicts patient admission probability and multi-disease risk assessment. Built with industry-standard MLOps practices for healthcare professionals.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Patient Admission Prediction**: Predicts the probability of hospital admission based on patient vital signs and medical history
- **Multi-Disease Risk Assessment**: Assesses risk for cardiovascular, respiratory, and metabolic diseases
- **MLOps Best Practices**: 
  - Experiment tracking with MLflow
  - Model versioning and reproducibility
  - Automated training pipelines
  - Comprehensive logging and monitoring
- **REST API**: FastAPI-based API for easy integration with healthcare systems
- **Data Validation**: Pydantic models for robust input validation
- **Clinical Recommendations**: AI-generated recommendations based on predictions

## Architecture

```
MedPredict/
├── src/
│   ├── api/              # FastAPI application
│   ├── data/             # Data loading and preprocessing
│   ├── models/           # ML models and training
│   └── utils/            # Utilities (config, logging)
├── tests/                # Unit and integration tests
├── configs/              # Configuration files
├── models/               # Trained model artifacts
├── notebooks/            # Jupyter notebooks for analysis
└── requirements.txt      # Python dependencies
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/shcdeveloper/MedPredict.git
cd MedPredict

# Run setup script
chmod +x setup.sh
./setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Training Models

```bash
# Run training pipeline
chmod +x train.sh
./train.sh

# Or manually:
python -m src.models.train

# View experiment tracking
mlflow ui
# Navigate to http://localhost:5000
```

### Running the API

```bash
# Start the API server
chmod +x run_api.sh
./run_api.sh

# Or manually:
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# API will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### Running Tests

```bash
# Run all tests
chmod +x run_tests.sh
./run_tests.sh

# Or manually:
pytest tests/ -v --cov=src
```

## API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Make Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 65,
    "gender": "Male",
    "systolic_bp": 145,
    "diastolic_bp": 90,
    "heart_rate": 78,
    "temperature": 37.2,
    "glucose": 135,
    "cholesterol": 220,
    "bmi": 28.5,
    "has_diabetes": 1,
    "has_hypertension": 1,
    "smoking_status": "Former",
    "previous_admissions": 2
  }'
```

### Example Response

```json
{
  "admission_prediction": {
    "admission_required": true,
    "admission_probability": 0.78,
    "risk_category": "High"
  },
  "disease_risk_assessment": {
    "cardiovascular_risk": {
      "risk_level": "High",
      "probability": 0.85
    },
    "respiratory_risk": {
      "risk_level": "Low",
      "probability": 0.32
    },
    "metabolic_risk": {
      "risk_level": "High",
      "probability": 0.71
    }
  },
  "recommendations": [
    "Immediate hospital admission recommended",
    "Cardiovascular assessment recommended - monitor BP and cholesterol",
    "Metabolic assessment required - check glucose and lipid panels",
    "Multi-system evaluation recommended due to multiple high-risk factors"
  ]
}
```

## Models

### Admission Predictor
- **Algorithm**: XGBoost Classifier
- **Features**: Patient demographics, vital signs, lab values, medical history
- **Output**: Binary classification (admission required or not) with probability
- **Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC

### Disease Risk Assessor
- **Algorithm**: Multi-output LightGBM Classifier
- **Features**: Same as admission predictor
- **Output**: Risk assessment for 3 disease categories
  - Cardiovascular risk
  - Respiratory risk
  - Metabolic risk
- **Metrics**: Hamming Loss, per-disease accuracy, precision, recall, F1-score

## Configuration

Configuration is managed through `configs/config.yaml`:

```yaml
model:
  admission_predictor:
    type: "xgboost"
    params:
      n_estimators: 100
      max_depth: 6
      learning_rate: 0.1

mlflow:
  tracking_uri: "mlruns"
  experiment_name: "medpredict"

api:
  host: "0.0.0.0"
  port: 8000
```

## MLOps Features

- **Experiment Tracking**: All training runs tracked with MLflow
- **Model Versioning**: Models saved with metadata and metrics
- **Reproducibility**: Fixed random seeds and configuration management
- **Logging**: Comprehensive logging with Loguru
- **Data Validation**: Input validation with Pydantic
- **Testing**: Unit and integration tests with pytest
- **CI/CD Ready**: Modular architecture for easy deployment

## Development

### Project Structure

- `src/api/`: FastAPI application and API schemas
- `src/data/`: Data loading, generation, and preprocessing
- `src/models/`: ML model implementations and training pipeline
- `src/utils/`: Configuration and logging utilities
- `tests/`: Test suite
- `configs/`: Configuration files

### Adding New Features

1. Create feature branch
2. Add implementation in appropriate module
3. Add tests in `tests/` directory
4. Update documentation
5. Run tests: `pytest tests/`
6. Submit pull request

## Data

The system currently uses synthetic patient data for demonstration. In production:

1. Replace `src/data/loader.py` with your data source
2. Ensure data follows the same schema
3. Update preprocessing if needed
4. Retrain models with production data

### Required Data Fields

- Demographics: age, gender
- Vital Signs: systolic_bp, diastolic_bp, heart_rate, temperature
- Lab Values: glucose, cholesterol, bmi
- Medical History: has_diabetes, has_hypertension, smoking_status, previous_admissions

## License

This project is licensed under the MIT License.

## Disclaimer

⚠️ **Important**: This system is for educational and demonstration purposes only. It should not be used for actual clinical decision-making without proper validation, regulatory approval, and oversight by qualified healthcare professionals.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or support, please open an issue on GitHub.
