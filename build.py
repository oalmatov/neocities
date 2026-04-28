"""Build script for the neocities site. Reads markdown content and generates static HTML."""

import html
import json
import shutil
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Literal

import markdown
import yaml

from templates import (
    BARTER_PAGE_TEMPLATE,
    CARD_AUTHOR_TEMPLATE,
    CARD_DATE_TEMPLATE,
    CARD_TEMPLATE,
    CARD_THUMB_PLACEHOLDER,
    CARD_THUMB_TEMPLATE,
    FEED_DATE_TEMPLATE,
    FEED_ITEM_TEMPLATE,
    FEED_PAGE_TEMPLATE,
    GRID_PAGE_TEMPLATE,
    GUESTBOOK_PAGE_TEMPLATE,
    POEM_CREDIT_LINK_TEMPLATE,
    POEM_CREDIT_TEMPLATE,
    POEM_JSON_TILE_TEMPLATE,
    POEM_MONTH_TEMPLATE,
    POEMS_PAGE_TEMPLATE,
    POPOVER_AUTHOR_TEMPLATE,
    POPOVER_DATE_TEMPLATE,
    POPOVER_TEMPLATE,
    STARS_TEMPLATE,
    SVG_TEMPLATE,
    SVG_WORD_TEMPLATE,
)

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
PUBLIC_DIR = ROOT / "public"

POEM_CANVAS_WIDTH = 504
POEM_CANVAS_HEIGHT = 900

IMAGE_EXTS = frozenset({".jpg", ".jpeg", ".png", ".gif", ".webp"})

GridSectionName = Literal["journal", "books", "movies"]
SectionName = GridSectionName | Literal["feed", "barter", "poems", "guestbook"]


# ----- types -----


@dataclass
class Post:
    """A single content post, parsed from a .md file with YAML frontmatter."""

    slug: str
    section: str
    html: str
    title: str = "Untitled"
    date: datetime = datetime.min
    thumbnail: str | None = None
    rating: int | None = None
    author: str | None = None
    hidden: bool = False

    @property
    def id(self) -> str:
        return f"{self.section}-{self.slug}"


@dataclass
class Section:
    """One entry in the site's section dispatch table."""

    title: str
    render: Callable[[], tuple[str, str]]  # returns (content_html, popovers_html)


# ----- helpers -----


def format_date(d: datetime) -> str:
    if d == datetime.min:
        return ""
    fmt = "%b %-d, %Y %-I:%M %p" if (d.hour or d.minute) else "%b %-d, %Y"
    return d.strftime(fmt)


def rewrite_asset_urls(html_text: str) -> str:
    """Rewrite bare src="foo.jpg" references to absolute /posts/foo.jpg."""
    return html_text.replace('src="', 'src="/posts/')


# ----- I/O -----


def parse_post(post_path: Path, section: str) -> Post:
    """Parse a .md file into a Post.

    Frontmatter dates must be full `YYYY-MM-DD HH:MM:SS` so YAML parses them as datetime.
    """
    text = post_path.read_text()
    _, fm_text, body = text.split("---", 2)
    frontmatter = yaml.safe_load(fm_text) or {}

    raw_rating = frontmatter.get("rating")
    return Post(
        slug=post_path.stem,
        section=section,
        html=markdown.markdown(body.strip()),
        title=frontmatter.get("title", "Untitled"),
        date=frontmatter.get("date") or datetime.min,
        thumbnail=frontmatter.get("thumbnail"),
        rating=int(raw_rating) if raw_rating is not None else None,
        author=frontmatter.get("author"),
        hidden=frontmatter.get("hidden", False),
    )


def load_section(section: str) -> list[Post]:
    """Load all posts from a section, sorted by date descending. Honors frontmatter `hidden:`."""
    posts = [
        post
        for md in sorted((CONTENT_DIR / section).glob("*.md"))
        if not (post := parse_post(md, section)).hidden
    ]
    posts.sort(key=lambda p: p.date, reverse=True)
    return posts


def copy_files(src: Path, dst: Path, suffixes: frozenset[str] = frozenset()) -> None:
    """Copy files from src into dst (non-recursive).

    If suffixes is non-empty, only copy files whose (lowercased) suffix is in the set.
    """
    if not src.exists():
        return

    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if not item.is_file() or (suffixes and item.suffix.lower() not in suffixes):
            continue
        shutil.copy2(item, dst / item.name)


# ----- card + popover (shared by grid sections) -----


def render_stars(rating: int | None) -> str:
    if rating is None:
        return ""
    return STARS_TEMPLATE.format(filled="★" * rating, empty="☆" * (5 - rating))


def render_card(post: Post) -> str:
    thumb_html = (
        CARD_THUMB_TEMPLATE.format(thumbnail=post.thumbnail)
        if post.thumbnail
        else CARD_THUMB_PLACEHOLDER
    )
    date_str = format_date(post.date)
    date_html = CARD_DATE_TEMPLATE.format(date=date_str) if date_str else ""
    author_html = CARD_AUTHOR_TEMPLATE.format(author=post.author) if post.author else ""

    has_content = post.html.strip() != ""
    return CARD_TEMPLATE.format(
        clickable=" card-clickable" if has_content else "",
        data_attr=f' data-post="{post.id}"' if has_content else "",
        thumb_html=thumb_html,
        title=post.title,
        stars_html=render_stars(post.rating),
        author_html=author_html,
        date_html=date_html,
    )


def render_popover(post: Post) -> str:
    if not post.html.strip():
        return ""

    date_str = format_date(post.date)
    date_html = POPOVER_DATE_TEMPLATE.format(date=date_str) if date_str else ""
    author_html = (
        POPOVER_AUTHOR_TEMPLATE.format(author=post.author) if post.author else ""
    )

    return POPOVER_TEMPLATE.format(
        post_id=post.id,
        title=post.title,
        stars_html=render_stars(post.rating),
        author_html=author_html,
        date_html=date_html,
        body_html=rewrite_asset_urls(post.html),
    )


# ----- poems section (special) -----


def json_to_svg(words: list[dict]) -> str:
    tiles = []
    for w in words:
        # Approximate width: ~9px per char + 20px padding
        text_width = len(w["text"]) * 9 + 20
        tiles.append(
            SVG_WORD_TEMPLATE.format(
                x=w["x"],
                y=w["y"],
                rotation=w["rotation"],
                text_width=text_width,
                text_x=text_width / 2,
                text=html.escape(w["text"]),
            )
        )
    return SVG_TEMPLATE.format(
        width=POEM_CANVAS_WIDTH,
        height=POEM_CANVAS_HEIGHT,
        tiles="".join(tiles),
    )


def render_poem_tile(data: dict) -> str:
    name, website = data.get("name"), data.get("website")
    if name and website:
        credit = POEM_CREDIT_LINK_TEMPLATE.format(href=html.escape(website), label=html.escape(name))
    elif name:
        credit = POEM_CREDIT_TEMPLATE.format(label=html.escape(name))
    else:
        credit = ""
    return POEM_JSON_TILE_TEMPLATE.format(svg=json_to_svg(data.get("words", [])), credit=credit)


# ----- per-section renderers -----


def render_feed_page() -> tuple[str, str]:
    items = []
    for post in load_section("feed"):
        date_str = format_date(post.date)
        date_html = FEED_DATE_TEMPLATE.format(date=date_str) if date_str else ""
        items.append(FEED_ITEM_TEMPLATE.format(
            body=rewrite_asset_urls(post.html),
            date_html=date_html,
        ))
    content = FEED_PAGE_TEMPLATE.format(items="".join(items))
    return content, ""


def render_grid_page(section: GridSectionName) -> tuple[str, str]:
    """Render a simple grid section."""
    posts = load_section(section)
    cards = "\n".join(render_card(p) for p in posts)
    popovers = "\n".join(render_popover(p) for p in posts)
    content = GRID_PAGE_TEMPLATE.format(section=section, grid=cards)
    return content, popovers


def render_barter_page() -> tuple[str, str]:
    offering = load_section("barter/offering")
    looking_for = load_section("barter/looking-for")
    offering_cards = "\n".join(render_card(p) for p in offering)
    looking_for_cards = "\n".join(render_card(p) for p in looking_for)
    popovers = "\n".join(render_popover(p) for p in offering + looking_for)
    content = BARTER_PAGE_TEMPLATE.format(offering=offering_cards, looking_for=looking_for_cards)
    return content, popovers


def render_poems_page() -> tuple[str, str]:
    by_month: dict[tuple[int, int], list[tuple[datetime, dict]]] = defaultdict(list)
    for path in (CONTENT_DIR / "poems").glob("*.json"):
        data = json.loads(path.read_text())
        date = datetime.fromisoformat(data.get("date", "1970-01-01"))
        by_month[(date.year, date.month)].append((date, data))

    months = []
    for key in sorted(by_month, reverse=True):
        year, month = key
        poems = sorted(by_month[key], key=lambda x: x[0], reverse=True)
        tiles = "\n".join(render_poem_tile(data) for _, data in poems)
        label = datetime(year, month, 1).strftime("%B %Y")
        months.append(POEM_MONTH_TEMPLATE.format(label=label, tiles=tiles))

    content = POEMS_PAGE_TEMPLATE.format(months="\n".join(months))
    return content, ""


def render_guestbook_page() -> tuple[str, str]:
    return GUESTBOOK_PAGE_TEMPLATE, ""


# ----- dispatch table -----

SECTIONS: dict[SectionName, Section] = {
    "feed": Section(title="feed", render=render_feed_page),
    "journal": Section(title="journal", render=partial(render_grid_page, "journal")),
    "books": Section(title="books", render=partial(render_grid_page, "books")),
    "movies": Section(title="movies", render=partial(render_grid_page, "movies")),
    "barter": Section(title="barter", render=render_barter_page),
    "poems": Section(title="your poems", render=render_poems_page),
    "guestbook": Section(title="guestbook", render=render_guestbook_page),
}


# ----- top-level build -----


def build() -> None:
    posts_output = PUBLIC_DIR / "posts"
    shutil.rmtree(posts_output, ignore_errors=True)
    copy_files(CONTENT_DIR / "assets", posts_output)

    template = (ROOT / "template.html").read_text()
    for slug, section in SECTIONS.items():
        content, popovers = section.render()
        rendered = (
            template.replace("{{ title }}", section.title)
            .replace("{{ content }}", content)
            .replace("{{ popovers }}", popovers)
        )
        section_dir = PUBLIC_DIR / slug
        section_dir.mkdir(parents=True, exist_ok=True)
        (section_dir / "index.html").write_text(rendered)

    print(f"Built {len(SECTIONS)} sections")


if __name__ == "__main__":
    build()
