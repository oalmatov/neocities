build:
	uv run --with markdown --with pyyaml python build.py

generate:
	uv run python generate_poems.py
