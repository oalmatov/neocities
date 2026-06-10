# Neocities

Please don't look too closely at the commit history.

## Requirements

- [Hugo](https://gohugo.io) (extended) — `brew install hugo`
- [Go](https://go.dev) — `brew install go`

## Usage

```
make build   # render poems + hugo build
make serve   # dev server at localhost:1313
make words   # regenerate data/fridge_words.yaml (fresh random scatter)
make clean   # rm public/ resources/

make new-feed slug=foo   # also: new-journal, new-books, new-movies
```

## Layout

- `content/<section>/<slug>/index.md` — page bundles (post + its images/videos in one folder)
- `data/` — `barter.yaml`, `poems/*.json` (submissions), and generated `poems_manifest.yaml` + `fridge_words.yaml`
- `assets/styles.css` — Hugo Pipes (fingerprinted); `static/` — verbatim passthrough
- `layouts/` — templates, partials, and the `video` / `carousel` shortcodes
- `cmd/render-poems`, `cmd/generate-words` — data generators

## Authoring notes

- Markdown references bundle assets by bare filename.
- Videos: `{{< video "clip.mp4" >}}`. Carousels: wrap consecutive images in `{{< carousel >}}…{{< /carousel >}}`.

## Deployment

`.github/workflows/deploy.yml` builds and pushes to Neocities on every push to `main` (needs repo secret `NEOCITIES_TOKEN`). Build output is not committed.
