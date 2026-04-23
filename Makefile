build:
	uv run build.py

generate:
	uv run generate_poems.py

format:
	uv run ruff format .
	uv run ruff check --fix .

format-html:
	uv run djlint public template.html --reformat || true

lint:
	uv run ruff check .
