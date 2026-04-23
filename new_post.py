"""Create a new post in the given section and open it in nvim.

Usage: uv run new_post.py <section>

The filename is the current local datetime so posts are chronologically sortable
and unique. The `date:` frontmatter is set to the same timestamp so sort logic
in build.py keeps working.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

FRONTMATTER_TEMPLATES: dict[str, str] = {
    "feed": "date: {date}\n",
    "journal": "title: \ndate: {date}\n",
    "books": "title: \ndate: {date}\nthumbnail: \nrating: \nauthor: \n",
    "movies": "title: \ndate: {date}\nthumbnail: \nrating: \nauthor: \n",
    "barter/offering": "title: \ndate: {date}\nthumbnail: \n",
    "barter/looking-for": "title: \ndate: {date}\nthumbnail: \n",
}


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in FRONTMATTER_TEMPLATES:
        sections = ", ".join(FRONTMATTER_TEMPLATES)
        sys.exit(f"usage: uv run new_post.py <section>\nsections: {sections}")

    section = sys.argv[1]
    now = datetime.now().replace(microsecond=0)
    stem = now.strftime("%Y-%m-%d_%H%M%S")

    path = Path("content") / section / f"{stem}.md"
    if path.exists():
        sys.exit(f"already exists: {path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = FRONTMATTER_TEMPLATES[section].format(date=now.strftime("%Y-%m-%d %H:%M:%S"))
    path.write_text(f"---\n{frontmatter}---\n\n")

    print(f"created {path}")
    subprocess.run(["nvim", str(path)])


if __name__ == "__main__":
    main()
