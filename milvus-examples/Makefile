# Makefile for Milvus Learning Curriculum

.PHONY: help install setup start stop restart logs clean test format lint

help:
	@echo "Milvus Learning Curriculum - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make setup       - Full setup (install + env)"
	@echo ""
	@echo "Docker:"
	@echo "  make start       - Start Milvus and services"
	@echo "  make stop        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make logs        - View Milvus logs"
	@echo ""
	@echo "Development:"
	@echo "  make test        - Run tests"
	@echo "  make format      - Format code (black, isort)"
	@echo "  make lint        - Lint code (flake8, mypy)"
	@echo "  make clean       - Clean temporary files"
	@echo ""
	@echo "Learning:"
	@echo "  make demo        - Run Level 1 demo"
	@echo "  make level1      - Run all Level 1 examples"

install:
	pip install -r requirements.txt

setup: install
	cp -n .env.example .env || true
	mkdir -p logs

start:
	docker compose up -d
	@echo "Waiting for Milvus to be ready..."
	@sleep 5
	docker compose ps

stop:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f milvus

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache .mypy_cache htmlcov .coverage
	rm -rf build dist *.egg-info

test:
	pytest

format:
	black .
	isort .

lint:
	flake8 . --max-line-length=100 --exclude=venv,env
	mypy . --exclude venv --exclude env

demo:
	cd level_1_basics && python 01_connection_setup.py --mode single
	cd level_1_basics && python 02_collection_management.py --action demo

level1:
	cd level_1_basics && python 01_connection_setup.py --mode all
	cd level_1_basics && python 02_collection_management.py --action demo
	cd level_1_basics && python 03_data_insertion.py --size small
	cd level_1_basics && python 04_basic_search.py --topk 10
