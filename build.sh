#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install python dependencies
pip install -r requirements.txt

# Collect static files for WhiteNoise
python backend/manage.py collectstatic --no-input

# Run database migrations
python backend/manage.py migrate
