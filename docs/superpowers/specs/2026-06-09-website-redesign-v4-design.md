# Website Redesign v4 — Design Spec

Date: 2026-06-09
Branch: `oa/redesign-v4`

## Goal

Replace the current white / Trebuchet MS / fish-pond aesthetic with a dark
terminal-flavored design inspired by meat-computer.com (black background) and
binomech.net (recent-posts homepage). The whole site is restyled; the homepage
is reconceived as a multi-column "altar" dashboard that doubles as navigation,
so the global nav bar is removed.

## Visual language (applies site-wide)

- **Background:** pure black `#000`.
- **Text:** warm cream. Primary `#e9e4d6` / headings `#f2ecdd` / muted `#8c8470`
  / accent green `#7fa86b`.
- **Font:** `JetBrains Mono` (Google Fonts), monospace, terminal feel — but
  labels are blunt plain words, NOT CLI cosplay (no `--flags`, `>`, `$`, `./`).
- **Dates:** always `[YYYY-MM-DD HH:MM]` bracketed format, everywhere
  (feed, journal, books, movies, poems).
- **Ratings:** `n/5` text (no stars).
- **Borders:** none/boxless. Sections are separated by spacing + uppercase green
  section headers + thin dotted hairlines. Inputs/buttons use a 1px dotted
  cream border.
- **Hover:** clickable text (nav-equivalents, links, buttons, book cards, the
  movie/reading rows) invert to a cream fill with black text; rows/cards get a
  soft green wash + thumbnail outline. Feed entries have NO hover effect.
- **Big Other ticker (global, every layout):** the long "Big Other" paragraph
  (currently the eye tooltip text in `baseof.html`) scrolls continuously as a
  marquee in a slim fixed bar at the **bottom** of every page (CSS
  `translateX` loop, text duplicated for a seamless cycle). Muted/green
  monospace, semi-transparent black bg, thin dotted top border, `pointer-events:
  none`, below the eyes (`z-index` < 9999) but above page content. Page content
  gets bottom padding to clear it. This lives in `baseof.html` so it appears on
  every layout.
- **Two fixed overlay layers, on every page:**
  - **Tile texture:** `sitemap-tile-dithered.jpg` repeated, `background-size`
    ~340px, dimmed (`grayscale(1) brightness(.5) contrast(1.1)`), `opacity:.16`,
    `position:fixed`, `z-index:0`, behind content. (No header/footer "bands" —
    that read as old Tumblr.)
  - **Eyes:** two copies of the blinking eye gif (`bob-eye-horror-evil.gif`),
    side by side touching (`gap:0`), centered, `position:fixed`,
    `z-index:9999` (above all content), `pointer-events:none`,
    `mix-blend-mode:screen` (drops the black bg so only the eye composites in),
    `opacity:.07`.

## Assets to add to `static/assets/`

- `eye.gif` — from `~/Downloads/bob-eye-horror-evil.gif` (blinking eye overlay).
- `turtle.gif` — from `~/Desktop/UELO3RPY6HJ32EED74VMSB6KHSDVP5WG.gif`
  (spinning turtle; rendered B&W via `filter:grayscale(1)`).
- `flag.gif` — from `~/Desktop/4UFLPQNOKUTS6KTOHGMOGCVTDS34NQC7.gif`
  (Kazakhstan flag; rendered B&W).
- `sitemap-tile-dithered.jpg` — from `~/Downloads/sitemap-tile-dithered.jpg`.

Old assets (`eye-open-*`, `eye-closed-*`, fish, refrigerator textures, etc.)
can stay for now; only the index fish-pond is retired (see below).

## Homepage (`layouts/index.html`)

Reconceived. No global nav bar. No tagline. The site title `webmar27` types
itself out (CSS steps typewriter, 8ch) with a persistent blinking caret.

**Four equal-width columns** (`flex:1` each; wrap on ≤980px with the feed going
full-width, single column on ≤560px):

1. **Identity column**
   - `webmar27` (animated title)
   - `about` — the existing about blurb text
   - `details` — key/value lines: `relationship: single`, `age: 23`,
     `height: 5'11"`, `location: san francisco` (key green, value cream)
   - `friends` — links: sabjadeliu.neocities.org, bruhjuice.com,
     baljaa.neocities.org (new-tab, hover-fill)
   - flex row of the **flag gif + turtle gif** (both B&W)
2. **Feed column** — the paginated feed itself lives here (see Feed below):
   recent feed entries (flowing, hairline-separated, no boxes) + pagination
   (`page 1 / 8   older`).
3. **Modules column** — each is an uppercase green clickable section header
   (links to the full page) + content:
   - `now playing` — Spotify embed (pinned track/album, dark theme iframe)
   - `latest journal entry` — newest journal entry title + snippet + "read entry"
   - `last movie` — newest movie: thumb, title, `[date] · n/5`
   - `currently reading` — single most-recent book: thumb, title, author,
     `[date] · n/5`
4. **Third column** — section headers + content:
   - `last fridge poem` — newest poem rendered in the new text style + credit
   - `barter` — blurb + a **barter with me** button (links to /barter/)
   - `guestbook` — the existing guestbook embed, inlined and restyled to fit
     (external service handles submissions; the inline form is the embed)

**Section headers are the navigation.** Every section links to its full page,
replacing the removed nav bar.

### Architecture note: feed-on-root

The original plan was "recent posts on root → link to a separate paginated
`/feed/`." Final decision: the **feed column on the homepage is the paginated
feed** (Hugo `.Paginate`). Page 1 is `/`; `older` goes to `/page/2/` etc. The
modules + identity + third columns appear on **page 1 only**; deeper pages are
feed-only (decision: keeps deep pages clean). The standalone `/feed/` route is
retired (the root is the feed). The current "keep perceiving" link and
`like-splatter` behavior in the feed are preserved.

## Inner pages

All restyled to the visual language above (black/cream/mono, boxless, eyes +
tile overlays, `[date]` format, `n/5`). Each inner page has a small breadcrumb
`webmar27 / <section>` (clickable home) instead of the old nav bar.

- **Books** (`layouts/_default/list.html` for books / existing books layout):
  grid of book entries — cover, title, author, `[date] · n/5`. No magnet/box
  framing; covers are plain with subtle fill, hover outlines the cover +
  underlines the title.
- **Movies:** same grid treatment as books (cover, title, `[date] · n/5`).
- **Journal** (`layouts/journal/list.html`): keep the two-pane structure —
  left sidebar list grouped `year / month` (hover-fill links, active brightened)
  + right reading pane (title, `[date]`, body in readable cream). Restyle only.
- **Fridge poems** (`layouts/fridge-poems/list.html` + `cmd/render-poems`):
  drop the fridge-magnet look and the refrigerator texture. The compose canvas
  becomes draggable **cream word tokens on black** (keep existing drag + share
  logic). The submitted gallery shows each poem as its own scatter on black.
  **`cmd/render-poems/main.go` must be updated** to regenerate the poem SVGs in
  the new style (transparent/black bg, cream monospace words) instead of
  magnets, then all SVGs in `static/poems/` regenerated.
- **Barter** (`layouts/barter/list.html`): two columns (`i can offer` /
  `i am looking for`) as `[ ]` checklist rows (hover green wash), plus the
  existing message textarea + `send offer` button restyled.
- **About / guestbook:** about content is surfaced on the homepage; the
  standalone pages still restyle to match. Guestbook remains the external embed.

## Out of scope / retired

- The floating fish-pond index — **retired entirely** (no `/pond/` page).
- The global nav bar — removed (modules/section-headers are the nav).
- Live Spotify "recently played" — not possible on static hosting; the embed is
  a **manually pinned** track/album/playlist.
- Real guestbook backend — unchanged (keeps the external embed).

## Reference

Full clickable mockups (the agreed-on look) are in
`.superpowers/brainstorm/51844-1781043323/content/` — `pages.html` (index +
books) and `extras.html` (poems + journal + barter), generated by the
`build_pages.py` / `build_poems.py` scripts there. These are the source of truth
for spacing, colors, and markup structure.

## Constraints

- Hugo static site; no backend. Neocities hosting.
- Desktop-first (the site already gates small screens in places); keep the
  responsive column-wrapping described above.
