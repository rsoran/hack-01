.PHONY: help install run run-docker run-docker-dev stop build test clean

help:
	@echo "Cooking To-Do List Generator - Development Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install          Install Python dependencies"
	@echo "  run              Run app locally (development)"
	@echo "  run-docker       Run app in Docker (production)"
	@echo "  run-docker-dev   Run app in Docker (development with hot reload)"
	@echo "  stop             Stop Docker containers"
	@echo "  build            Build Docker image"
	@echo "  test             Run tests"
	@echo "  clean            Clean up generated files"
	@echo "  setup            Complete setup for first run"
	@echo "  logs             View Docker logs"

setup: install
	@echo "✓ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Update .env with your Google API key"
	@echo "2. Run: make run (for local) or make run-docker (for Docker)"
	@echo "3. Open: http://localhost:5000"

install:
	@echo "Installing dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "✓ Dependencies installed"

run:
	@echo "Starting application locally..."
	cd backend && python app.py

run-docker:
	@echo "Starting application with Docker (production)..."
	docker-compose up -d
	@echo "✓ App running at http://localhost:5000"

run-docker-dev:
	@echo "Starting application with Docker (development)..."
	docker-compose -f docker-compose.dev.yml up
	@echo "✓ App running at http://localhost:5000 (with hot reload)"

stop:
	@echo "Stopping Docker containers..."
	docker-compose down
	@echo "✓ Containers stopped"

build:
	@echo "Building Docker image..."
	docker-compose build
	@echo "✓ Image built"

test:
	@echo "Running tests..."
	cd backend && pytest tests/
	@echo "✓ Tests complete"

logs:
	@echo "Displaying logs..."
	docker-compose logs -f

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf backend/.pytest_cache 2>/dev/null || true
	rm -rf .venv 2>/dev/null || true
	@echo "✓ Cleanup complete"

.DEFAULT_GOAL := help
