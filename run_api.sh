#!/bin/bash
# Run API server

echo "Starting MedPredict API server..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run API server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
