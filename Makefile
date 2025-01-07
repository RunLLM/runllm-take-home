server:
	@echo "Starting server app..."
	@cd server/server && uvicorn server_app:app --reload --port 5001 --host 0.0.0.0

run-tests:
	@echo "Running tests..."
	@cd tests && pytest -rP .

run-static-checks:
	@echo "Running linters and mypy checks and autofixers..."
	@cd server && poetry check --lock
	@cd server && poetry run ruff check . --fix
	@cd server && poetry run ruff format .
	@cd server && poetry run mypy . --explicit-package-bases

.PHONY: server