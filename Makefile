.PHONY: start-celery stop-celery start-celery-beat stop-celery-beat run-app run-frontend run-backend start-dev

# Start the Celery worker
start-celery:
	@echo "Starting Celery worker..."
	@celery -A tasks.celery_app worker --loglevel=info

# Stop the Celery worker
stop-celery:
	@echo "Stopping Celery worker..."
	@kill -9 $(shell ps aux | grep 'celery worker' | grep -v grep | awk '{print $2}' | tr '\n' ' ') > /dev/null 2>&1 || true

# Start the Celery beat scheduler
start-celery-beat:
	@echo "Starting Celery beat scheduler..."
	@celery -A tasks.celery_app beat --loglevel=info

# Stop the Celery beat scheduler
stop-celery-beat:
	@echo "Stopping Celery beat scheduler..."
	@kill -9 $(shell ps aux | grep 'celery beat' | grep -v grep | awk '{print $2}' | tr '\n' ' ') > /dev/null 2>&1 || true

# Run the Python application (FastAPI backend)
run-backend:
	@echo "Running FastAPI backend..."
	@uvicorn app.main:app --reload

# Run the Frontend application
run-frontend:
	@echo "Running Frontend application..."
	@cd frontend && npm run dev

# Start both Frontend and Backend in development mode
start-dev:
	@echo "Starting Frontend and Backend concurrently..."
	@npx concurrently "make run-backend" "make run-frontend"
