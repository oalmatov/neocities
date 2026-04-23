# Neocities

Please don't look too closely at the commit history

## Requirements

- https://github.com/astral-sh/uv

## Layout

```
content/
  assets/                      # all post assets (images, videos) — one global folder
  feed/<slug>.md               # one .md per post
  journal/<slug>.md
  books/<slug>.md
  movies/<slug>.md
  barter/offering/<slug>.md
  barter/looking-for/<slug>.md
  poems/<slug>.json            # visitor-submitted poems
public/                        # built output (one index.html per section)
template.html                  # page shell
templates.py                   # html/svg templates
build.py                       # static site generator
new_post.py                    # scaffold + open in nvim
```

## Creating posts

Each post is a single markdown file with YAML frontmatter. reference assets by bare filename; the build rewrites paths to `/posts/<filename>`.

```markdown
---
title: My Post
date: 2026-04-22 13:15:00
thumbnail: some-image.jpg
---

body content here. ![](some-image.jpg)
```

- dates must be full `YYYY-MM-DD HH:MM:SS` so YAML parses them as datetime
- feed posts only need `date:` — embed the image inline in the body
- books/movies use `title`, `date`, `thumbnail`, `rating`, `author`
- set `hidden: true` to skip a post at build time

## Usage

```
make build            # generate public/
make new-feed         # scaffold + open new post in nvim
make new-journal
make new-book
make new-movie
make new-offering     # barter: I can offer
make new-wanted       # barter: I'm looking for
make format           # ruff format + autofix
make format-html      # djlint reformat public/ + template.html
make lint             # ruff check
```
