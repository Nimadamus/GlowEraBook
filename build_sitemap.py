#!/usr/bin/env python3
"""Rebuild glowerabook.com sitemap.xml from live files, commit + push if changed."""
import glob, os, subprocess, sys

REPO = os.path.dirname(os.path.abspath(__file__))
BASE = "https://glowerabook.com"
os.chdir(REPO)

urls = [f"{BASE}/", f"{BASE}/blog/"]
skip = {"google", "404"}
for f in sorted(glob.glob("blog/*.html")):
    name = os.path.basename(f)
    if name == "index.html" or any(name.startswith(s) for s in skip):
        continue
    urls.append(f"{BASE}/blog/{name}")

body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
body += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
body += "</urlset>\n"

with open("sitemap.xml", "r", encoding="utf-8") as fh:
    old = fh.read()
if old == body:
    print("sitemap unchanged")
    sys.exit(0)

with open("sitemap.xml", "w", encoding="utf-8") as fh:
    fh.write(body)
subprocess.run(["git", "add", "sitemap.xml"], check=True)
subprocess.run(["git", "commit", "-q", "-m", "Auto-update sitemap"], check=True)
subprocess.run(["git", "push", "-q", "origin", "main"], check=True)
print(f"sitemap updated: {len(urls)} urls, pushed")
