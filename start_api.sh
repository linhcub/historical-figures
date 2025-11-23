#!/bin/bash
set -e

# Ensure script runs from project root (where this script lives)
cd "$(dirname "$0")"

# Activate the virtualenv
source venv/bin/activate

# Ensure Python can import the 'api' package by adding 'src' to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Start Uvicorn (replace the shell with the process)
exec uvicorn src.api.app:app --reload
