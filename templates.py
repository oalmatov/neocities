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
    <section id="barter" class="barter-page">
      <p class="barter-preface">bartering is the exchange of goods or services directly for other goods or services without using money. It is one of the oldest forms of commerce, allowing individuals to trade what they have for what they need.</p>
      <div class="barter-columns">
        <div class="barter-column">
          <h3 class="barter-heading">i can offer</h3>
          <ul class="barter-list" data-side="offering">
            {offering}
          </ul>
        </div>
        <div class="barter-column">
          <h3 class="barter-heading">i am looking for</h3>
          <ul class="barter-list" data-side="looking_for">
            {looking_for}
          </ul>
        </div>
      </div>

      <div class="barter-form">
        <p class="barter-hint">also feel free to send any other offer or add any additional information</p>
        <textarea id="barter-message" rows="12"></textarea>
        <button id="barter-send" type="button">send offer</button>
      </div>
    </section>
    <script>
      (function () {{
        const textarea = document.getElementById('barter-message');
        const sendBtn = document.getElementById('barter-send');
        const email = 'omar.almatov@gmail.com';

        function selected(side) {{
          return Array.from(
            document.querySelectorAll('.barter-list[data-side="' + side + '"] input[type=checkbox]:checked')
          ).map(i => i.dataset.title);
        }}

        function bullets(items) {{
          return items.length ? items.map(t => '- ' + t).join('\\n') : '- ';
        }}

        function rebuild() {{
          const offering = selected('offering');
          const wanting = selected('looking_for');
          textarea.value =
            "i can give u this:\\n" +
            bullets(wanting) +
            "\\n\\nfor this:\\n" +
            bullets(offering);
        }}

        document.querySelectorAll('.barter-list input[type=checkbox]').forEach(cb => {{
          cb.addEventListener('change', rebuild);
        }});

        sendBtn.addEventListener('click', () => {{
          const subject = 'barter offer';
          const body = textarea.value;
          window.location.href =
            'mailto:' + email +
            '?subject=' + encodeURIComponent(subject) +
            '&body=' + encodeURIComponent(body);
        }});

        rebuild();
      }})();
    </script>"""

BARTER_ITEM_TEMPLATE = """
            <li class="barter-item">
              <label>
                <input type="checkbox" data-title="{title}" />
                {thumb_html}
                <div class="barter-item-info">
                  <span class="barter-item-title">{title}</span>
                  {body_html}
                </div>
              </label>
            </li>"""

BARTER_ITEM_THUMB_TEMPLATE = '<img class="barter-item-thumb" src="/posts/{thumbnail}" alt="" />'

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


# ----- journal -----

JOURNAL_PAGE_TEMPLATE = """
    <section id="journal" class="journal-layout">
      <aside class="journal-sidebar">
        <div class="journal-sidebar-list">
          {sidebar}
        </div>
        <a class="journal-sitemap-link" href="/sitemap/">keep perceiving</a>
      </aside>
      <main class="journal-content">
        {entries}
      </main>
    </section>
    <script>
      (function () {{
        function setActive(slug) {{
          document.querySelectorAll('.journal-entry').forEach(el => el.classList.remove('active'));
          document.querySelectorAll('.journal-link').forEach(el => el.classList.remove('active'));
          const entry = document.getElementById('entry-' + slug);
          const link = document.querySelector('.journal-link[data-slug="' + slug + '"]');
          if (entry) entry.classList.add('active');
          if (link) link.classList.add('active');
        }}
        function fromHash() {{
          const m = location.hash.match(/^#entry-(.+)$/);
          if (m) return m[1];
          const first = document.querySelector('.journal-entry');
          return first ? first.id.replace(/^entry-/, '') : null;
        }}
        window.addEventListener('hashchange', () => setActive(fromHash()));
        const slug = fromHash();
        if (slug) setActive(slug);
      }})();
    </script>"""

JOURNAL_YEAR_TEMPLATE = """
        <div class="journal-year">
          <h3>{year}</h3>
          {months}
        </div>"""

JOURNAL_MONTH_TEMPLATE = """
          <div class="journal-month">
            <h4>{month}</h4>
            <ul>
              {links}
            </ul>
          </div>"""

JOURNAL_LINK_TEMPLATE = '<li><a class="journal-link" data-slug="{slug}" href="#entry-{slug}">{title}</a></li>'

JOURNAL_ENTRY_TEMPLATE = """
        <article id="entry-{slug}" class="journal-entry">
          <h2>{title}</h2>
          {date_html}
          <div class="journal-body">{body_html}</div>
        </article>"""

JOURNAL_DATE_TEMPLATE = '<p class="journal-date">{date}</p>'
