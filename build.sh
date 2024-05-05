#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

#install npm dependencies
npm install

# Apply any outstanding database migrations
python manage.py migrate

python makemigrations utils

python manage.py migrate utils

# Convert static asset files
python manage.py collectstatic --no-input

ls -l

# Make users and data
# python generate.py shell
