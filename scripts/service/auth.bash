#!/usr/bin/bash

echo "Activating virtual environment"
source .venv/bin/activate

echo "Starting docker compose environment"
echo "runs mongodb server"
docker-compose -f "production/auth service/docker-compose.yml" up -d

echo "Starting auth service application in development mode with hot reloading"
PYTHONPATH=src/ uvicorn src.auth_service.main:app --reload