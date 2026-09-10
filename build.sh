#!/usr/bin/env bash
# ============================================================
# Build script for Render.com
# Runs automatically during the Render deploy pipeline.
# ============================================================
set -o errexit   # Exit on error

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
