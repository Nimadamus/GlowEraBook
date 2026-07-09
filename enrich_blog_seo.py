"""
Idempotent SEO + internal-linking enrichment for every Glow Era blog article.

For each blog/*.html (except index.html) it injects, only if missing:
  - canonical + robots index,follow
  - Open Graph + Twitter Card tags
  - BlogPosting JSON-LD (author = Prudence Nteo, publisher = Glow Era)
  - a visible "Written by Prudence Nteo" author box (E-E-A-T)
  - a static, crawlable "Continue Reading" block with 3 related posts

Safe to run repeatedly. new_blog_post.py calls this before committing.
"""
import re
import json
from pathlib import Path

ROOT = Path(__file__).parent
BLOG_DIR = ROOT / "blog"
POSTS_DATA = BLOG_DIR / "posts-data.js"
SITE_URL = "https://glowerabook.com"
AUTHOR = "Prudence Nteo"

HEAD_MARK = "<!-- seo-enrich -->"
AUTHOR_MARK = "<!-- author-box -->"
RELATED_MARK = "<!-- related-posts -->"


def load_posts():
    txt = POSTS_DATA.read_text(encoding="utf-8")
    posts = []
    for block in re.findall(r"\{(.*?)\}", txt, re.S):
        def g(key):
            m = re.search(rf'{key}:\s*"((?:[^"\\]|\\.)*)"', block)
            return m.group(1) if m else ""
        slug = g("slug")
        if not slug:
            continue
        posts.append({
            "slug": slug, "title": g("title"), "excerpt": g("excerpt"),
            "date": g("date"), "readTime": g("readTime"),
            "category": g("category"), "image": g("image"),
        })
    return posts


def fmt_date(iso):
    from datetime import datetime
    try:
        return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %d, %Y").replace(" 0", " ")
    except ValueError:
        return iso


def head_block(p):
    url = f"{SITE_URL}/blog/{p['slug']}.html"
    title = f"{p['title']}, Glow Era Blog | {AUTHOR}"
    desc = p["excerpt"]
    img_abs = f"{SITE_URL}/blog/{p['image']}" if p["image"] else ""
    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": p["title"],
        "description": desc,
        "datePublished": p["date"],
        "dateModified": p["date"],
        "articleSection": p["category"],
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": {"@type": "Person", "name": AUTHOR, "url": f"{SITE_URL}/#author"},
        "publisher": {"@type": "Organization", "name": "Glow Era", "url": SITE_URL},
    }
    if img_abs:
        ld["image"] = img_abs
    lines = [
        HEAD_MARK,
        f'<link rel="canonical" href="{url}">',
        '<meta name="robots" content="index, follow">',
        '<meta property="og:type" content="article">',
        f'<meta property="og:title" content="{esc(p["title"])}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{url}">',
        '<meta property="og:site_name" content="Glow Era">',
        f'<meta property="article:published_time" content="{p["date"]}">',
        f'<meta property="article:author" content="{AUTHOR}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(p["title"])}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
    ]
    if img_abs:
        lines.insert(7, f'<meta property="og:image" content="{img_abs}">')
        lines.append(f'<meta name="twitter:image" content="{img_abs}">')
    lines.append('<script type="application/ld+json">' + json.dumps(ld) + '</script>')
    return "\n".join(lines) + "\n"


def esc(s):
    return s.replace('"', "&quot;")


def author_box():
    return (
        f'{AUTHOR_MARK}\n'
        '      <div class="article-author">\n'
        '        <p class="article-author-label">Written by</p>\n'
        f'        <h3><a href="/#author">{AUTHOR}</a></h3>\n'
        '        <p>Author of Glow Era, writing on self-care, boundaries, confidence, and the daily practice of coming home to yourself.</p>\n'
        '      </div>\n'
    )


def related_block(current, posts):
    others = [q for q in posts if q["slug"] != current["slug"]]
    idx = next((i for i, q in enumerate(posts) if q["slug"] == current["slug"]), 0)
    ordered = [posts[(idx + k) % len(posts)] for k in range(1, len(posts))]
    picks = [q for q in ordered if q["slug"] != current["slug"]][:3]
    if not picks:
        picks = others[:3]
    cards = []
    for q in picks:
        media = (f'<img src="{q["image"]}" alt="{esc(q["title"])}" loading="lazy">'
                 if q["image"] else '<span>Glow Era</span>')
        cards.append(
            f'        <a class="blog-card" href="{q["slug"]}.html">\n'
            f'          <div class="blog-card-media">{media}</div>\n'
            f'          <div class="blog-card-body">\n'
            f'            <div class="blog-card-meta"><span>{q["category"]}</span><span class="dot">&middot;</span><span>{fmt_date(q["date"])}</span><span class="dot">&middot;</span><span>{q["readTime"]}</span></div>\n'
            f'            <h3>{q["title"]}</h3>\n'
            f'            <p>{q["excerpt"]}</p>\n'
            f'            <span class="blog-card-link">Read the Post</span>\n'
            f'          </div>\n'
            f'        </a>'
        )
    return (
        f'  {RELATED_MARK}\n'
        '  <section class="article-related">\n'
        '    <div class="container">\n'
        '      <h2>Continue Reading</h2>\n'
        '      <div class="blog-grid">\n'
        + "\n".join(cards) + "\n"
        '      </div>\n'
        '    </div>\n'
        '  </section>\n'
    )


def enrich_file(path, post, posts):
    html = path.read_text(encoding="utf-8")
    changed = False

    if HEAD_MARK not in html:
        anchor = '<link rel="stylesheet" href="../style.css">\n'
        if anchor in html:
            html = html.replace(anchor, anchor + head_block(post), 1)
            changed = True

    if AUTHOR_MARK not in html and '<div class="article-cta">' in html:
        html = html.replace('      <div class="article-cta">',
                            author_box() + '\n      <div class="article-cta">', 1)
        changed = True

    if RELATED_MARK not in html and "</main>" in html:
        html = html.replace("</main>", related_block(post, posts) + "</main>", 1)
        changed = True

    if changed:
        path.write_text(html, encoding="utf-8")
    return changed


def main():
    posts = load_posts()
    by_slug = {p["slug"]: p for p in posts}
    n = 0
    for f in BLOG_DIR.glob("*.html"):
        if f.name == "index.html":
            continue
        post = by_slug.get(f.stem)
        if not post:
            print(f"  skip (no posts-data entry): {f.name}")
            continue
        if enrich_file(f, post, posts):
            print(f"  enriched: {f.name}")
            n += 1
    print(f"Enriched {n} article(s).")


if __name__ == "__main__":
    main()
