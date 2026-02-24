#!/usr/bin/env bash
# Render build script — builds both Python backend and React frontend

set -o errexit  # Exit on error

echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Installing Node.js dependencies..."
cd frontend
npm install

echo "==> Building React frontend..."
npm run build

echo "==> Build complete!"
cd ..
