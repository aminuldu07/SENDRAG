#!/bin/bash

# Activate your poetry virtual environment (replace path if different)
source /Users/amin/Library/Caches/pypoetry/virtualenvs/sendrag-s8hi-jRC-py3.13/bin/activate

# Start backend in background
echo "Starting backend..."
#uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload &
poetry run uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

trap "echo 'Stopping backend...'; kill $BACKEND_PID; exit" SIGINT SIGTERM

# Wait for backend to be ready (max 20 attempts)
echo "Waiting for backend to be ready..."
for i in {1..20}; do
    if curl -s http://localhost:8000/docs > /dev/null; then
        echo "Backend is up!"
        break
    else
        echo "Waiting... ($i)"
        sleep 1
    fi
done

if ! curl -s http://localhost:8000/docs > /dev/null; then
    echo "Backend did not start in time, killing process and exiting."
    kill $BACKEND_PID
    exit 1
fi

# Start frontend (Streamlit)
echo "Starting frontend..."
poetry run streamlit run ui/app.py

# When frontend exits, kill backend
echo "Stopping backend..."
kill $BACKEND_PID
echo "Done."
