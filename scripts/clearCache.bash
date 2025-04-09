#!/usr/bin/bash

echo "Clearing pytest cache"
find . -name ".pytest_cache" -type d -exec rm -rf {} +

echo "Clearing pycache"
find . -name "__pycache__" -type d -exec rm -rf {} +

echo "Clearing mypy cache"
find . -name ".mypy_cache" -type d -exec rm -rf {} +
