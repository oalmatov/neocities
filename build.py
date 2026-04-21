"""Build script for anatomy site. Reads markdown content and generates static HTML."""

import shutil
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
PUBLIC_DIR = ROOT / "public"
SECTIONS = ["feed", "journal", "books", "movies", "barter", "poems", "guestbook"]
REVIEW_SECTIONS = {"books", "movies"}

SECTION_TITLES = {
    "feed": "feed",
    "journal": "journal",
    "books": "books",
    "movies": "movies",
    "barter": "barter",
    "poems": "your poems",
    "guestbook": "guestbook",
}


def parse_post(post_path: Path) -> dict:
    """Parse a post.md file into frontmatter dict + html content."""
    text = post_path.read_text()
    parts = text.split("---", 2)
    frontmatter = yaml.safe_load(parts[1])
    body = parts[2].strip()

    slug = post_path.parent.name
    html = markdown.markdown(body)

    return {
        "slug": slug,
        "title": frontmatter.get("title", "Untitled"),
        "date": frontmatter.get("date"),
        "thumbnail": frontmatter.get("thumbnail"),
        "rating": frontmatter.get("rating"),
        "author": frontmatter.get("author"),
        "hidden": frontmatter.get("hidden", False),
        "html": html,
    }


def load_section(section: str) -> list[dict]:
    """Load all posts from a section, sorted by date descending."""
    section_dir = CONTENT_DIR / section

    if not section_dir.exists():
        return []

    posts = []
    for post_dir in sorted(section_dir.iterdir()):
        post_file = post_dir / "post.md"

        if not post_file.exists():
            continue

        post = parse_post(post_file)
        if post.get("hidden"):
            continue
        post["section"] = section
        posts.append(post)

    from datetime import date, datetime

    def sort_key(p):
        d = p["date"]
        if isinstance(d, datetime):
            return d
        if isinstance(d, date):
            return datetime(d.year, d.month, d.day)
        if isinstance(d, int):
            return datetime(d, 1, 1)
        return datetime.min

    posts.sort(key=sort_key, reverse=True)
    return posts


def copy_assets(section: str) -> None:
    """Copy post assets (images etc) to output directory."""
    section_dir = CONTENT_DIR / section
    output_section = PUBLIC_DIR / "posts" / section

    if not section_dir.exists():
        return

    for post_dir in section_dir.iterdir():
        if not post_dir.is_dir():
            continue

        output_post = output_section / post_dir.name

        if output_post.exists():
            shutil.rmtree(output_post)

        shutil.copytree(post_dir, output_post, ignore=shutil.ignore_patterns("post.md"))


def render_stars(rating: int | None) -> str:
    """Render star rating as HTML."""
    if rating is None:
        return ""

    rating = int(rating)
    filled = "★" * rating
    empty = "☆" * (5 - rating)
    return f'<span class="card-rating">{filled}{empty}</span>'


def render_card(post: dict) -> str:
    """Render a single card in the grid."""
    section = post["section"]
    slug = post["slug"]
    post_id = f"{section}-{slug}"

    thumb_html = ""
    if post["thumbnail"]:
        thumb_src = f"/posts/{section}/{slug}/{post['thumbnail']}"
        thumb_html = f'<img class="card-thumb" src="{thumb_src}" alt="" />'
    else:
        thumb_html = '<div class="card-thumb card-thumb-placeholder"></div>'

    date_html = ""
    if post["date"]:
        date = post["date"]
        date_str = date.strftime("%b %-d, %Y") if hasattr(date, "strftime") else str(date)
        date_html = f'<span class="card-date">{date_str}</span>'

    stars_html = render_stars(post.get("rating"))

    author_html = ""
    if post.get("author"):
        author_html = f'<span class="card-date">{post["author"]}</span>'

    has_content = post["html"].strip() != ""
    data_attr = f' data-post="{post_id}"' if has_content else ""
    clickable = " card-clickable" if has_content else ""

    return f"""
        <div class="card{clickable}"{data_attr}>
          {thumb_html}
          <div class="card-info">
            <span class="card-title">{post['title']}</span>
            {stars_html}
            {author_html}
            {date_html}
          </div>
        </div>"""


def render_popover(post: dict) -> str:
    """Render a hidden popover div for a post. Returns empty string if no content."""
    if not post["html"].strip():
        return ""

    section = post["section"]
    slug = post["slug"]
    post_id = f"{section}-{slug}"

    # Rewrite image paths in content
    content_html = post["html"].replace('src="', f'src="/posts/{section}/{slug}/')

    stars_html = render_stars(post.get("rating"))

    date_html = ""
    if post["date"]:
        date = post["date"]
        date_str = date.strftime("%b %-d, %Y") if hasattr(date, "strftime") else str(date)
        date_html = f'<p class="popover-date">{date_str}</p>'

    author_html = ""
    if post.get("author"):
        author_html = f'<p class="popover-date">{post["author"]}</p>'

    return f"""
    <div class="popover-data" id="popover-{post_id}" style="display: none;">
      <h2>{post['title']}</h2>
      {stars_html}
      {author_html}
      {date_html}
      <div class="popover-body">{content_html}</div>
    </div>"""


def load_feed() -> list[dict]:
    """Load feed entries, sorted by date descending."""
    from datetime import date, datetime

    feed_dir = CONTENT_DIR / "feed"

    if not feed_dir.exists():
        return []

    entries = []
    for entry_dir in sorted(feed_dir.iterdir()):
        post_file = entry_dir / "post.md"

        if not post_file.exists():
            continue

        text = post_file.read_text()
        parts = text.split("---", 2)
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        html = markdown.markdown(body)

        if frontmatter.get("hidden"):
            continue

        entries.append({
            "slug": entry_dir.name,
            "date": frontmatter.get("date"),
            "image": frontmatter.get("image"),
            "html": html,
        })

    def feed_sort_key(e):
        d = e["date"]
        if isinstance(d, datetime):
            return d
        if isinstance(d, date):
            return datetime(d.year, d.month, d.day)
        return datetime.min

    entries.sort(key=feed_sort_key, reverse=True)
    return entries


def render_feed(entries: list[dict]) -> str:
    """Render the feed as a compact grid."""
    if not entries:
        return ""

    items = []
    for entry in entries:
        slug = entry["slug"]

        image_html = ""
        if entry["image"]:
            src = f"/posts/feed/{slug}/{entry['image']}"
            image_html = f'<img class="feed-image" src="{src}" alt="" />'

        date_html = ""
        if entry["date"]:
            d = entry["date"]
            from datetime import datetime
            if isinstance(d, datetime):
                date_str = d.strftime("%b %-d, %Y %-I:%M %p")
            elif hasattr(d, "strftime"):
                date_str = d.strftime("%b %-d, %Y")
            else:
                date_str = str(d)
            date_html = f'<span class="feed-date">{date_str}</span>'

        text_html = ""
        if entry["html"].strip():
            content = entry["html"].replace('src="', f'src="/posts/feed/{slug}/')
            text_html = f'<div class="feed-text">{content}</div>'

        items.append(f"""
        <div class="feed-item">
          {image_html}
          {text_html}
          {date_html}
        </div>""")

    return f"""
      <div class="feed">
        {"".join(items)}
      </div>"""


def render_barter_section(all_posts: dict) -> str:
    """Render the barter section with two side-by-side grids."""
    offering = all_posts.get("barter/offering", [])
    looking_for = all_posts.get("barter/looking-for", [])

    offering_cards = "\n".join(render_card(p) for p in offering)
    looking_for_cards = "\n".join(render_card(p) for p in looking_for)

    return f"""
    <section id="barter" class="section">
      <div class="barter-columns">
        <div class="barter-column">
          <h2>I can offer...</h2>
          <div class="grid">
            {offering_cards}
          </div>
        </div>
        <div class="barter-column">
          <h2>I am looking for...</h2>
          <div class="grid">
            {looking_for_cards}
          </div>
        </div>
      </div>
    </section>"""


def render_section(section: str, posts: list[dict], prefix_html: str = "") -> str:
    """Render a full section with its grid of cards."""
    cards = "\n".join(render_card(p) for p in posts)

    return f"""
    <section id="{section}" class="section">
      {prefix_html}
      <div class="grid">
        {cards}
      </div>
    </section>"""


def render_poems_section() -> str:
    """Render the poems section as a grid."""
    import html
    import json as json_module

    poems_dir = CONTENT_DIR / "poems"
    items = []
    if poems_dir.exists():
        for item in sorted(poems_dir.iterdir()):
            ext = item.suffix.lower()
            if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
                items.append(f'<div class="poem-tile"><img class="poem-image" src="/posts/poems/{item.name}" alt="" /></div>')
            elif ext == ".json":
                data = json_module.loads(item.read_text())
                if isinstance(data, list):
                    words = data
                    name = None
                    website = None
                else:
                    words = data.get("words", [])
                    name = data.get("name")
                    website = data.get("website")

                credit = ""
                if name:
                    label = html.escape(name)
                    if website:
                        credit = f'<p class="poem-credit"><a href="{html.escape(website)}" target="_blank">{label}</a></p>'
                    else:
                        credit = f'<p class="poem-credit">{label}</p>'

                items.append(
                    f'<div class="poem-tile"><div class="poem-image">{json_to_svg(words)}</div>{credit}</div>'
                )

    body = "\n        ".join(items)

    return f"""
    <section id="poems" class="section">
      <p class="poems-preface">i'll try my best to check my mail and update this page with your poems</p>
      <div class="poems-grid">
        {body}
      </div>
    </section>"""


POEM_CANVAS_WIDTH = 504
POEM_CANVAS_HEIGHT = 600


def json_to_svg(words: list[dict]) -> str:
    """Convert a list of positioned word magnets (from localStorage JSON) to SVG."""
    import html

    tiles = []
    for w in words:
        text = html.escape(w["text"])
        # Approximate width: ~10px per char + 20px padding
        text_width = len(w["text"]) * 9 + 20
        rect_height = 24
        tiles.append(
            f'<g transform="translate({w["x"]},{w["y"]}) rotate({w["rotation"]})">'
            f'<rect width="{text_width}" height="{rect_height}" fill="#faf7ef" '
            f'stroke="black" stroke-width="1.5"/>'
            f'<text x="{text_width / 2}" y="16" text-anchor="middle" '
            f'font-family="serif" font-size="14" fill="black">{text}</text>'
            f'</g>'
        )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {POEM_CANVAS_WIDTH} {POEM_CANVAS_HEIGHT}" '
        f'preserveAspectRatio="xMidYMid meet">'
        f'<image href="/assets/refrigerator-texture.jpg" '
        f'width="{POEM_CANVAS_WIDTH}" height="{POEM_CANVAS_HEIGHT}" '
        f'preserveAspectRatio="xMidYMid slice"/>'
        + "".join(tiles)
        + '</svg>'
    )


def copy_poems() -> None:
    """Copy poem images to output."""
    poems_dir = CONTENT_DIR / "poems"
    output_poems = PUBLIC_DIR / "posts" / "poems"

    if not poems_dir.exists():
        return

    output_poems.mkdir(parents=True, exist_ok=True)
    for item in poems_dir.iterdir():
        if item.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            shutil.copy2(item, output_poems / item.name)


def render_section_content(section: str, all_posts: dict, feed_html: str) -> tuple[str, str]:
    """Return (content_html, popovers_html) for a section."""
    if section == "barter":
        content = render_barter_section(all_posts)
        popovers = "\n".join(
            render_popover(p)
            for p in all_posts.get("barter/offering", []) + all_posts.get("barter/looking-for", [])
        )
    elif section == "feed":
        content = f"""
    <section id="feed" class="section">
      {feed_html}
    </section>"""
        popovers = ""
    elif section == "guestbook":
        content = """
    <section id="guestbook" class="section">
      <iframe src="https://webmar27.atabook.org" class="guestbook-frame"></iframe>
    </section>"""
        popovers = ""
    elif section == "poems":
        content = render_poems_section()
        popovers = ""
    else:
        content = render_section(section, all_posts[section])
        popovers = "\n".join(render_popover(p) for p in all_posts[section])

    return content, popovers


def build() -> None:
    """Build the site."""
    # Load all sections
    all_posts: dict[str, list[dict]] = {}
    for section in SECTIONS:
        if section == "barter":
            all_posts["barter/offering"] = load_section("barter/offering")
            all_posts["barter/looking-for"] = load_section("barter/looking-for")
        else:
            all_posts[section] = load_section(section)

    # Load feed
    feed_entries = load_feed()

    # Copy post assets
    posts_output = PUBLIC_DIR / "posts"
    if posts_output.exists():
        shutil.rmtree(posts_output)

    for section in SECTIONS:
        if section == "barter":
            copy_assets("barter/offering")
            copy_assets("barter/looking-for")
        elif section == "poems":
            copy_poems()
        else:
            copy_assets(section)

    copy_assets("feed")

    # Render feed
    feed_html = render_feed(feed_entries)

    # Generate per-section pages
    template = (ROOT / "template.html").read_text()

    for section in SECTIONS:
        content, popovers = render_section_content(section, all_posts, feed_html)
        title = SECTION_TITLES.get(section, section)

        html = (
            template
            .replace("{{title}}", title)
            .replace("{{content}}", content)
            .replace("{{popovers}}", popovers)
        )

        section_dir = PUBLIC_DIR / section
        section_dir.mkdir(parents=True, exist_ok=True)
        (section_dir / "index.html").write_text(html)

    total_posts = sum(len(p) for p in all_posts.values())
    print(f"Built {total_posts} posts across {len(SECTIONS)} sections")


if __name__ == "__main__":
    build()
