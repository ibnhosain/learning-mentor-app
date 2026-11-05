#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
# Seed শুধু প্রথমবার চালাবে (data না থাকলে)
python manage.py seed_curriculum
