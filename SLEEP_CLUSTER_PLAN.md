# Sleep and Heart Health, topic cluster plan

Site: glowerabook.com (Glow Era). Cluster id: `sleep-heart-health`.
Manifest: `cluster/sleep-heart-health.json`. Nav builder: `build_cluster_nav.py`.

## URL map

| # | Page | URL | Status |
|---|------|-----|--------|
| 0 | **Pillar / hub**: Sleep and Heart Health: Why 7 to 9 Hours of Rest Is Your Heart's Best Ally | `/blog/sleep-and-heart-health.html` | LIVE |
| 1 | The Silent Killer: How Lack of Sleep Raises Your Risk of Stroke (existing, URL unchanged) | `/blog/the-silent-killer-how-lack-of-sleep-raises-your-risk-of-stroke.html` | LIVE |
| 2 | Can Lack of Sleep Cause a Stroke? What the Research Shows | `/blog/can-lack-of-sleep-cause-a-stroke.html` | planned |
| 3 | How Many Hours of Sleep Help Reduce Stroke Risk? | `/blog/how-many-hours-of-sleep-reduce-stroke-risk.html` | planned |
| 4 | Sleep Deprivation and High Blood Pressure: The Hidden Connection | `/blog/sleep-deprivation-and-high-blood-pressure.html` | planned |
| 5 | Can Poor Sleep Cause a Heart Attack? | `/blog/can-poor-sleep-cause-a-heart-attack.html` | planned |
| 6 | Sleep Apnea and Stroke Risk: Symptoms You Should Not Ignore | `/blog/sleep-apnea-and-stroke-risk.html` | planned |
| 7 | Why Waking Up Throughout the Night May Affect Your Heart | `/blog/waking-up-throughout-the-night-and-heart-health.html` | planned |
| 8 | Irregular Sleep Schedules and Heart Health | `/blog/irregular-sleep-schedules-and-heart-health.html` | planned |
| 9 | What Happens to Your Body After 24 Hours Without Sleep? | `/blog/24-hours-without-sleep-effects-on-the-body.html` | planned |
| 10 | Signs You Are Not Getting Enough Quality Sleep | `/blog/signs-you-are-not-getting-enough-quality-sleep.html` | planned |
| 11 | How to Improve Sleep for Better Heart Health | `/blog/how-to-improve-sleep-for-better-heart-health.html` | planned |

The existing stroke article keeps its URL. No redirect, no rename, no removal, no `noindex` anywhere in the cluster.

## Hub

The pillar page is the hub. It carries the full series navigation plus a contextual in-body link into every supporting article, so no separate thin category page is created. The blog index at `/blog/` already lists every post automatically from `blog/posts-data.js`.

## Internal linking model

Two mechanisms, both generated so they can never go stale or dangle:

1. **Series nav block** (`<!-- cluster-nav:sleep-heart-health -->` … `<!-- /cluster-nav:... -->`)
   Every cluster page carries the markers. `build_cluster_nav.py` rewrites the block on all published pages from the manifest, marking the current page "You are here". This creates the hub-and-spoke plus spoke-to-spoke mesh.

2. **Contextual in-body links** (`<span class="cluster-link" data-slug="...">descriptive anchor</span>`)
   Written into the prose with descriptive, keyword-relevant anchor text, never "click here". The builder converts a span to a real `<a href="slug.html">` the moment that slug is marked published, and leaves it as plain text until then. Result: no dead internal links while the cluster is still being written.

Link rules per page:
- Every supporting article links **up** to the pillar in its opening section, anchor: "sleep and heart health" or a natural variant.
- The pillar links **down** to all 11 supporting pages from the topically relevant section, not a link dump.
- Supporting articles link **sideways** to 2 to 4 close siblings only where it genuinely helps the reader (for example, blood pressure ↔ heart attack ↔ sleep apnea).
- The existing stroke article links up to the pillar and carries the series nav.

Anchor text is defined per page in the manifest `anchor` field, so anchors stay varied and descriptive across the cluster.

## Publishing a supporting article

```
cp templates/cluster-article-template.html blog/<SLUG>.html   # fill placeholders
# add hero image to blog/images/, reference as images/<file>
# add entry to blog/posts-data.js
# flip "published": true for that slug in cluster/sleep-heart-health.json
python build_cluster_nav.py
python build_sitemap.py
git add -A && git commit -m "Add: <title>" && git push
```

`enrich_blog_seo.py` is idempotent and skips pages that already carry the `<!-- seo-enrich -->`, `<!-- author-box -->` marks, so hand-authored heads and author boxes are preserved.

## Content and E-E-A-T standards for this cluster

- One unique H1, unique title tag, unique meta description per page. No duplicated boilerplate intro across pages.
- Every medical claim is worded as association, not causation, unless the source states causation, and is traceable to CDC, NIH (NHLBI), or the American Heart Association. Approved source URLs are listed in each page's Sources section.
- No unattributed statistics. If a precise percentage cannot be traced to a named source, state the direction of the finding instead.
- Visible "Updated <date>" line, author box, and the standard medical disclaimer on every page.
- No thin, duplicate, placeholder, or filler pages. A slug stays `"published": false` until a real article exists behind it.

## Core sources for the cluster

- American Heart Association, Life's Essential 8: https://www.heart.org/en/healthy-living/healthy-lifestyle/lifes-essential-8
- American Heart Association, Sleep and heart health: https://www.heart.org/en/healthy-living/healthy-lifestyle/sleep
- CDC, About Sleep: https://www.cdc.gov/sleep/about/index.html
- NIH NHLBI, Sleep Deprivation and Deficiency: https://www.nhlbi.nih.gov/health/sleep-deprivation
- NIH NHLBI, Sleep Apnea: https://www.nhlbi.nih.gov/health/sleep-apnea
