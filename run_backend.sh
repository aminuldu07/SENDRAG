#!/bin/bash

# Activate poetry virtual environment
source /Users/amin/Library/Caches/pypoetry/virtualenvs/sendrag-*/bin/activate

echo "Starting backend..."
poetry run uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
