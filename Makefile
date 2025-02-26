server:
	@echo "Starting server app..."
	uvicorn server.server_app:app --reload --port 5001 --host 0.0.0.0

run-tests:
	@echo "Running tests..."
	pytest -rP tests/

run-static-checks:
	@echo "Running linters and mypy checks and autofixers..."
	@cd server && poetry check --lock
	@cd server && poetry run ruff check . --fix
	@cd server && poetry run ruff format .
	@cd server && poetry run mypy . --explicit-package-bases

.PHONY: server