#!/bin/sh

# Check if required volumes are mounted
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    exit 1
fi

if [ ! -d logs ]; then
    echo "Error: logs directory not found" 
    exit 1
fi

if [ ! -f requirements.txt ]; then
    echo "Error: requirements.txt not found"
    exit 1
fi

if [ ! -d shared_lib ]; then
    echo "Error: shared_lib directory not found"
    exit 1
fi

# Create and activate virtual environment
python3 -m venv venv
. venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run service
python3 start_service.py