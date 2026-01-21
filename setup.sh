#!/bin/bash
# Setup script for MedPredict

echo "Setting up MedPredict..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p models/trained
mkdir -p logs
mkdir -p data/raw
mkdir -p data/processed

echo "Setup complete!"
echo "To activate the environment, run: source venv/bin/activate"
