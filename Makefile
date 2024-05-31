.PHONY: start-celery stop-celery run-app

# Start the Celery worker
start-celery:
	@echo "Starting Celery worker..."
	@celery -A app.tasks.celery_app worker --loglevel=info

# Stop the Celery worker
stop-celery:
	@echo "Stopping Celery worker..."
	@kill -9 $(shell ps aux | grep celery | grep -v grep | awk '{print $2}' | tr '\n' ' ') > /dev/null 2>&1 || true

# Run the Python application
run-app:
	@echo "Running Python application..."
	@python3 -m app.main
