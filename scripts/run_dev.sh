#!/bin/bash
# Development server startup script

set -e

echo "Starting SC-AUC-Monitoring development server..."

# Check if we're in the right directory
if [ ! -f "backend/app/main.py" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Create .env if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "Creating .env from .env.example..."
    cp backend/.env.example backend/.env
fi

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "Creating virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
cd backend
source venv/bin/activate
pip install -q -r requirements.txt

# Start the server
echo "Starting server on http://localhost:8000"
echo "API Docs: http://localhost:8000/api/docs"
echo "Press Ctrl+C to stop"
echo ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
