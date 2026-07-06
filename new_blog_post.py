"""
Create and publish a new Glow Era blog post in one step.

Usage:
  python new_blog_post.py "Post Title" "One-sentence excerpt for the card" "Category" body.txt
  python new_blog_post.py "Post Title" "Excerpt" "Category" body.txt --no-push

Body file format (plain text):
  - Blank line = new paragraph
  - Line starting with "## " = <h2> subheading
  - Line starting with "> " = blockquote
"""
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
BLOG_DIR = ROOT / "blog"
POSTS_DATA = BLOG_DIR / "posts-data.js"
SITEMAP = ROOT / "sitemap.xml"
SITE_URL = "https://glowerabook.com"


def slugify(title):
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def render_body(text):
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    html = []
    for b in blocks:
        if b.startswith("## "):
            html.append(f"      <h2>{b[3:].strip()}</h2>")
        elif b.startswith("> "):
            html.append(f"      <blockquote>{b[2:].strip()}</blockquote>")
        else:
            para = " ".join(line.strip() for line in b.split("\n"))
            html.append(f"      <p>{para}</p>")
    return "\n".join(html)


def read_time(text):
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}, Glow Era Blog | Prudence Neo</title>
<meta name="description" content="{excerpt}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Playfair+Display:wght@500;600;700;800&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
</head>
<body>

<div class="grain-overlay"></div>

<header class="site-header" id="siteHeader">
  <div class="container header-inner">
    <a href="/" class="logo">Glow&nbsp;Era</a>
    <nav class="main-nav">
      <a href="/#about-book">The Book</a>
      <a href="/#who">Who It's For</a>
      <a href="/#author">Author</a>
      <a href="/blog/">Blog</a>
      <a href="/#contact">Contact</a>
    </nav>
    <a href="https://www.amazon.com/dp/B0GZKK3TYL/" class="btn btn-small btn-outline" target="_blank" rel="noopener">Buy the Book</a>
  </div>
</header>

<main>
  <section class="article-hero">
    <div class="container">
      <a href="/blog/" class="article-back">&larr; Back to the Blog</a>
      <div class="article-meta"><span>{category}</span><span>&middot;</span><span>{date_display}</span><span>&middot;</span><span>{read_time}</span></div>
      <h1>{title}</h1>
    </div>
  </section>

  <section class="article-body">
    <div class="container">
{body_html}

      <div class="article-cta">
        <h3>Ready to start your glow era?</h3>
        <p>Grab your copy of Glow Era by Prudence Neo and begin your own journey back to yourself.</p>
        <a href="https://www.amazon.com/dp/B0GZKK3TYL/" class="btn btn-primary" target="_blank" rel="noopener">Read the Book</a>
      </div>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="container footer-inner">
    <span class="logo footer-logo">Glow&nbsp;Era</span>
    <p>&copy; <span id="year"></span> Glow Era by Prudence Neo. All rights reserved.</p>
  </div>
</footer>

<script src="../script.js"></script>
</body>
</html>
"""


def insert_post_entry(slug, title, excerpt, category, date_iso, rtime):
    content = POSTS_DATA.read_text(encoding="utf-8")
    entry = (
        "  {\n"
        f'    slug: "{slug}",\n'
        f'    title: "{title}",\n'
        f'    excerpt: "{excerpt}",\n'
        f'    date: "{date_iso}",\n'
        f'    readTime: "{rtime}",\n'
        f'    category: "{category}"\n'
        "  },\n"
    )
    marker = "const BLOG_POSTS = [\n"
    idx = content.index(marker) + len(marker)
    new_content = content[:idx] + entry + content[idx:]
    POSTS_DATA.write_text(new_content, encoding="utf-8")


def rebuild_sitemap():
    urls = [f"{SITE_URL}/", f"{SITE_URL}/blog/"]
    for f in sorted(BLOG_DIR.glob("*.html")):
        if f.name == "index.html":
            continue
        urls.append(f"{SITE_URL}/blog/{f.name}")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(f"  <url><loc>{u}</loc></url>")
    lines.append("</urlset>")
    SITEMAP.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    no_push = "--no-push" in sys.argv
    if len(args) < 4:
        print(__doc__)
        sys.exit(1)
    title, excerpt, category, body_path = args[0], args[1], args[2], args[3]
    body_text = Path(body_path).read_text(encoding="utf-8")

    slug = slugify(title)
    date_iso = datetime.now().strftime("%Y-%m-%d")
    date_display = datetime.now().strftime("%B %-d, %Y") if sys.platform != "win32" else datetime.now().strftime("%B %#d, %Y")
    rtime = read_time(body_text)
    body_html = render_body(body_text)

    out_path = BLOG_DIR / f"{slug}.html"
    html = ARTICLE_TEMPLATE.format(
        title=title, excerpt=excerpt, category=category,
        date_display=date_display, read_time=rtime, body_html=body_html
    )
    out_path.write_text(html, encoding="utf-8")

    insert_post_entry(slug, title, excerpt, category, date_iso, rtime)
    rebuild_sitemap()

    print(f"Created blog/{slug}.html")
    print(f"Updated blog/posts-data.js and sitemap.xml")

    if not no_push:
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
        subprocess.run(["git", "commit", "-m", f"Add blog post: {title}"], cwd=ROOT, check=True)
        subprocess.run(["git", "push"], cwd=ROOT, check=True)
        print(f"Pushed. Live at {SITE_URL}/blog/{slug}.html (may take ~1 min to build)")
    else:
        print("Skipped git push (--no-push). Run 'git add -A && git commit -m ... && git push' when ready.")


if __name__ == "__main__":
    main()
