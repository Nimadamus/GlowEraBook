"""
Rebuild the in-article cluster navigation block for every page in a topic cluster.

Reads cluster/<id>.json and rewrites the block between
<!-- cluster-nav:<id> --> and <!-- /cluster-nav:<id> --> inside each published
page of that cluster. Only pages marked "published": true become links, so the
cluster never ships dead internal links. Flip "published" to true when an
article goes live, rerun this, and every sibling page links to it automatically.

Usage:
  python build_cluster_nav.py                 # all clusters
  python build_cluster_nav.py sleep-heart-health
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BLOG_DIR = ROOT / "blog"
CLUSTER_DIR = ROOT / "cluster"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def nav_html(cluster, current_slug):
    live = [p for p in cluster["pages"] if p.get("published")]
    items = []
    for p in live:
        if p["slug"] == current_slug:
            items.append(
                f'          <li class="cluster-nav-current"><span>{esc(p["title"])}</span>'
                f'<em>You are here</em></li>'
            )
        else:
            items.append(
                f'          <li><a href="{p["slug"]}.html">{esc(p["title"])}</a></li>'
            )
    return (
        f'      <nav class="cluster-nav" aria-label="{esc(cluster["name"])} series">\n'
        f'        <p class="cluster-nav-label">{esc(cluster["navHeading"])}</p>\n'
        f'        <p class="cluster-nav-intro">{esc(cluster["navIntro"])}</p>\n'
        f'        <ul>\n' + "\n".join(items) + "\n"
        f'        </ul>\n'
        f'      </nav>'
    )


INLINE_RE = re.compile(
    r'<(?:a|span)\b[^>]*class="cluster-link"[^>]*data-slug="([a-z0-9\-]+)"[^>]*>(.*?)</(?:a|span)>',
    re.S,
)


def linkify_inline(html, published_slugs):
    """Turn in-body cluster references into real links once the target is live.

    Unpublished targets stay as plain <span> text so the cluster never ships a
    dead internal link. Idempotent in both directions.
    """
    def repl(m):
        slug, text = m.group(1), m.group(2)
        if slug in published_slugs:
            return (f'<a class="cluster-link" data-slug="{slug}" '
                    f'href="{slug}.html">{text}</a>')
        return f'<span class="cluster-link" data-slug="{slug}">{text}</span>'
    return INLINE_RE.sub(repl, html)


def apply_cluster(cluster):
    cid = cluster["id"]
    open_mark = f"<!-- cluster-nav:{cid} -->"
    close_mark = f"<!-- /cluster-nav:{cid} -->"
    pattern = re.compile(
        re.escape(open_mark) + r".*?" + re.escape(close_mark), re.S
    )
    published = {q["slug"] for q in cluster["pages"] if q.get("published")}
    n = 0
    for p in cluster["pages"]:
        if not p.get("published"):
            continue
        path = BLOG_DIR / f"{p['slug']}.html"
        if not path.exists():
            print(f"  MISSING page marked published: {path.name}")
            continue
        html = path.read_text(encoding="utf-8")
        new = linkify_inline(html, published)
        if open_mark not in new:
            if new != html:
                path.write_text(new, encoding="utf-8")
                print(f"  inline links updated: {path.name}")
            else:
                print(f"  skip (no cluster-nav marker): {path.name}")
            continue
        block = f"{open_mark}\n{nav_html(cluster, p['slug'])}\n      {close_mark}"
        new = pattern.sub(lambda _m: block, new, count=1)
        if new != html:
            path.write_text(new, encoding="utf-8")
            print(f"  updated: {path.name}")
            n += 1
    print(f"[{cid}] rebuilt nav on {n} page(s).")


def main():
    wanted = sys.argv[1:] or None
    files = sorted(CLUSTER_DIR.glob("*.json"))
    if not files:
        print("No cluster manifests found in cluster/")
        return
    for f in files:
        cluster = json.loads(f.read_text(encoding="utf-8"))
        if wanted and cluster["id"] not in wanted:
            continue
        apply_cluster(cluster)


if __name__ == "__main__":
    main()
