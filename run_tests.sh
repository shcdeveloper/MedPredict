#!/bin/bash
# Run tests

echo "Running MedPredict tests..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run pytest with coverage
pytest tests/ -v --cov=src --cov-report=html --cov-report=term

echo "Tests complete! Coverage report saved to htmlcov/"
