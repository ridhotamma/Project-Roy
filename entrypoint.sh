#!/bin/bash

# Start the Celery worker in the background
celery -A tasks.celery_app worker --loglevel=info &

# Start the Celery beat scheduler in the background
celery -A tasks.celery_app beat --loglevel=info &

# Start the FastAPI app in the background
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Wait for all background processes to finish
wait
