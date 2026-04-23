build:
	uv run build.py

generate:
	uv run generate_poems.py

format:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff check .
