#!/bin/bash
# Training script for MedPredict models

echo "Starting MedPredict model training..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run training pipeline
python -m src.models.train

echo "Training complete! Models saved to models/trained/"
echo "View MLflow UI with: mlflow ui"
