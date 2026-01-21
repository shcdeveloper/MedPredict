# Quick Start Guide

## Automated Setup

Run the setup script to automatically configure the project:

```powershell
python setup.py
```

This will:
1. Check Python version
2. Install all dependencies
3. Generate sample data
4. Train the ML model

## Manual Setup

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Generate Data
```powershell
python data/generate_data.py
```

### 3. Train Model
```powershell
python -m api.train_model
```

### 4. Setup Database
- Start XAMPP
- Open phpMyAdmin: http://localhost/phpmyadmin
- Execute: `database/setup.sql`

### 5. Start API Server
```powershell
cd api
uvicorn main:app --reload
```

### 6. Deploy Web App
- Copy `webapp/` to `C:\xampp\htdocs\`
- Access: http://localhost/webapp/

## Testing

### Test API
```powershell
pytest tests/ -v
```

### Test API Manually
```powershell
# Check health
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"age\":65,\"gender\":\"M\",\"heart_rate\":95,\"glucose\":140.5,\"prior_admission\":2}"
```

## Jupyter Notebooks

```powershell
jupyter notebook notebooks/
```

Available notebooks:
- `01_exploratory_data_analysis.ipynb` - Data exploration
- `02_model_training.ipynb` - Model training walkthrough
- `03_model_explainability.ipynb` - SHAP analysis

## Troubleshooting

### Model Not Found Error
```powershell
python -m api.train_model
```

### API Connection Error
- Ensure FastAPI is running on port 8000
- Check firewall settings

### Database Connection Error
- Verify XAMPP MySQL is running
- Check credentials in `webapp/config/db.php`

### Module Import Errors
```powershell
pip install -r requirements.txt --upgrade
```

## Project Structure
```
careApp/
├── data/              # Dataset files
├── models/            # Trained models
├── api/               # FastAPI backend
├── webapp/            # PHP frontend
├── notebooks/         # Jupyter analysis
├── database/          # SQL scripts
├── tests/             # Unit tests
└── docs/              # Documentation
```
