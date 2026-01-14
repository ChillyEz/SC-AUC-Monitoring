.PHONY: update-items-db
update-items-db:
	python scripts/update_items_db.py --force

.PHONY: update-items-db-ru
update-items-db-ru:
	python scripts/update_items_db.py --realms ru --force

.PHONY: dev
dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

.PHONY: test
test:
	cd backend && pytest

.PHONY: format
format:
	cd backend && black app/ && isort app/

.PHONY: lint
lint:
	cd backend && ruff check app/ && black --check app/

.PHONY: install
install:
	cd backend && pip install -r requirements.txt -r requirements-dev.txt

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make update-items-db      - Update items database (all realms)"
	@echo "  make update-items-db-ru   - Update items database (RU realm only)"
	@echo "  make dev                  - Run development server"
	@echo "  make test                 - Run tests"
	@echo "  make format               - Format code with black and isort"
	@echo "  make lint                 - Lint code with ruff and black"
	@echo "  make install              - Install dependencies"
