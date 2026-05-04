"""HTML + SVG templates used by build.py. All interpolated via str.format()."""

# ----- card + popover (grid sections) -----

STARS_TEMPLATE = '<span class="card-rating">{filled}{empty}</span>'

CARD_TEMPLATE = """
        <div class="card{clickable}"{data_attr}>
          {thumb_html}
          <div class="card-info">
            <span class="card-title">{title}</span>
            {stars_html}
            {author_html}
            {date_html}
          </div>
        </div>"""

CARD_THUMB_TEMPLATE = '<img class="card-thumb" src="/posts/{thumbnail}" alt="" />'
CARD_THUMB_PLACEHOLDER = '<div class="card-thumb card-thumb-placeholder"></div>'
CARD_DATE_TEMPLATE = '<span class="card-date">{date}</span>'
CARD_AUTHOR_TEMPLATE = '<span class="card-date">{author}</span>'

POPOVER_TEMPLATE = """
    <div class="popover-data" id="popover-{post_id}" style="display: none;">
      <h2>{title}</h2>
      {stars_html}
      {author_html}
      {date_html}
      <div class="popover-body">{body_html}</div>
    </div>"""

POPOVER_DATE_TEMPLATE = '<p class="popover-date">{date}</p>'
POPOVER_AUTHOR_TEMPLATE = '<p class="popover-date">{author}</p>'


# ----- poems + SVG -----

SVG_TEMPLATE = (
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    'viewBox="0 0 {width} {height}" preserveAspectRatio="xMidYMid meet">'
    '<image href="/assets/refrigerator-texture.jpg" '
    'width="{width}" height="{height}" preserveAspectRatio="xMidYMid slice"/>'
    "{tiles}"
    "</svg>"
)

SVG_WORD_TEMPLATE = (
    '<g transform="translate({x},{y}) rotate({rotation})">'
    '<rect width="{text_width}" height="24" fill="#faf7ef" stroke="black" stroke-width="1.5"/>'
    '<text x="{text_x}" y="16" text-anchor="middle" '
    'font-family="serif" font-size="14" fill="black">{text}</text>'
    "</g>"
)

POEM_JSON_TILE_TEMPLATE = '<div class="poem-tile"><div class="poem-image">{svg}</div>{credit}</div>'
POEM_CREDIT_LINK_TEMPLATE = '<p class="poem-credit"><a href="{href}" target="_blank">{label}</a></p>'
POEM_CREDIT_TEMPLATE = '<p class="poem-credit">{label}</p>'


# ----- per-section page wrappers -----

FEED_PAGE_TEMPLATE = """
    <section id="feed" class="section">
      <div class="feed">
        {items}
      </div>
    </section>"""

FEED_ITEM_TEMPLATE = """
        <div class="feed-item">
          <div class="feed-text">{body}</div>
          {date_html}
        </div>"""

FEED_DATE_TEMPLATE = '<span class="feed-date">{date}</span>'

GRID_PAGE_TEMPLATE = """
    <section id="{section}" class="section">
      <div class="grid">
        {grid}
      </div>
    </section>"""

BARTER_PAGE_TEMPLATE = """
    <section id="barter" class="section">
      <div class="barter-columns">
        <div class="barter-column">
          <h2>I can offer...</h2>
          <div class="grid">
            {offering}
          </div>
        </div>
        <div class="barter-column">
          <h2>I am looking for...</h2>
          <div class="grid">
            {looking_for}
          </div>
        </div>
      </div>
    </section>"""

POEMS_PAGE_TEMPLATE = """
    <section id="poems" class="section">
      <p class="poems-preface">i'll try my best to check my mail and update this page promptly</p>
      {months}
    </section>"""

POEM_MONTH_TEMPLATE = """
      <div class="poem-month">
        <h3 class="poem-month-header">{label}</h3>
        <div class="poems-grid">
          {tiles}
        </div>
      </div>"""

GUESTBOOK_PAGE_TEMPLATE = """
    <section id="guestbook" class="section">
      <iframe src="https://webmar27.atabook.org" class="guestbook-frame"></iframe>
    </section>"""
