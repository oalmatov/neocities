build:
	uv run build.py

generate:
	uv run generate_poems.py

new-feed:
	uv run new_post.py feed

new-journal:
	uv run new_post.py journal

new-book:
	uv run new_post.py books

new-movie:
	uv run new_post.py movies

new-offering:
	uv run new_post.py barter/offering

new-wanted:
	uv run new_post.py barter/looking-for

format:
	uv run ruff format .
	uv run ruff check --fix .

format-html:
	uv run djlint public template.html --reformat || true

lint:
	uv run ruff check .
