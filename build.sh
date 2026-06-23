#!/usr/bin/env bash

set -o errexit

python -m pip install -r requirements.txt

if [ -z "$SECRET_KEY" ]; then
  echo "WARNING: SECRET_KEY is not set. Using a temporary build-only value."
  echo "Set a real SECRET_KEY in Render Environment before relying on this deployment."
  export SECRET_KEY="temporary-render-build-secret-not-for-runtime"
fi

python manage.py collectstatic --no-input
python manage.py migrate --no-input
