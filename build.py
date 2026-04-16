"""Build script for anatomy site. Reads markdown content and generates static HTML."""

import shutil
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
OUTPUT_DIR = ROOT / "public" / "anatomy"
SECTIONS = ["journal", "books", "movies", "barter"]
REVIEW_SECTIONS = {"books", "movies"}


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
        post["section"] = section
        posts.append(post)

    from datetime import date

    posts.sort(key=lambda p: p["date"] if isinstance(p["date"], date) else date.min, reverse=True)
    return posts


def copy_assets(section: str) -> None:
    """Copy post assets (images etc) to output directory."""
    section_dir = CONTENT_DIR / section
    output_section = OUTPUT_DIR / "posts" / section

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
        thumb_src = f"posts/{section}/{slug}/{post['thumbnail']}"
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
    content_html = post["html"].replace('src="', f'src="posts/{section}/{slug}/')

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


def render_section(section: str, posts: list[dict], is_default: bool) -> str:
    """Render a full section with its grid of cards."""
    display = "" if is_default else ' style="display: none;"'
    cards = "\n".join(render_card(p) for p in posts)

    return f"""
    <section id="{section}" class="section"{display}>
      <div class="grid">
        {cards}
      </div>
    </section>"""


def build() -> None:
    """Build the site."""
    # Load all sections
    all_posts: dict[str, list[dict]] = {}
    for section in SECTIONS:
        all_posts[section] = load_section(section)

    # Copy assets
    posts_output = OUTPUT_DIR / "posts"
    if posts_output.exists():
        shutil.rmtree(posts_output)

    for section in SECTIONS:
        copy_assets(section)

    sections_html = "\n".join(
        render_section(section, all_posts[section], section == SECTIONS[0])
        for section in SECTIONS
    )

    popovers_html = "\n".join(
        render_popover(post)
        for section in SECTIONS
        for post in all_posts[section]
    )

    template = (ROOT / "template.html").read_text()
    html = template.replace("{{sections}}", sections_html).replace("{{popovers}}", popovers_html)

    (OUTPUT_DIR / "index.html").write_text(html)
    print(f"Built {sum(len(p) for p in all_posts.values())} posts across {len(SECTIONS)} sections")


if __name__ == "__main__":
    build()
