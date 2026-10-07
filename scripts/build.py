#!/usr/bin/env python3
"""Generate sitemap.xml, feed.xml and the homepage <noscript> article list from metadata.json.

Usage: python3 scripts/build.py
"""
import html
import json
import pathlib
import re
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    data = json.loads((ROOT / "metadata.json").read_text())
    site = data["site"]
    base = site["base_url"].rstrip("/") + "/"
    articles = [a for a in data["articles"] if a.get("status") == "published"]
    pinned = [a for a in articles if a.get("pinned")]
    rest = sorted((a for a in articles if not a.get("pinned")), key=lambda a: a["date"], reverse=True)
    ordered = pinned + rest

    # sitemap.xml
    urls = [f"  <url><loc>{base}</loc></url>"]
    urls += [f"  <url><loc>{base}{a['path']}</loc><lastmod>{a['date']}</lastmod></url>" for a in ordered]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")

    # feed.xml (Atom)
    def ts(d):
        return f"{d}T00:00:00Z"
    updated = max((a["date"] for a in ordered), default=datetime.now(timezone.utc).date().isoformat())
    entries = []
    for a in rest:
        entries.append(
            "  <entry>\n"
            f"    <title>{html.escape(a['title'])}</title>\n"
            f"    <link href=\"{base}{a['path']}\"/>\n"
            f"    <id>{base}{a['path']}</id>\n"
            f"    <updated>{ts(a['date'])}</updated>\n"
            f"    <summary>{html.escape(a['hook'])}</summary>\n"
            + "".join(f"    <category term=\"{html.escape(t)}\"/>\n" for t in a.get("tags", []))
            + "  </entry>")
    (ROOT / "feed.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        f"  <title>{html.escape(site['title'])}</title>\n"
        f"  <subtitle>{html.escape(site['tagline'])}</subtitle>\n"
        f"  <link href=\"{base}\"/>\n  <link rel=\"self\" href=\"{base}feed.xml\"/>\n"
        f"  <id>{base}</id>\n  <updated>{ts(updated)}</updated>\n"
        f"  <author><name>{html.escape(site['title'])}</name></author>\n"
        + "\n".join(entries) + "\n</feed>\n")

    # static fallback list in index.html, between markers
    items = "\n".join(
        f'      <li><a href="{a["path"]}">{html.escape(a["title"])}</a> — {html.escape(a["hook"])}</li>'
        for a in ordered)
    block = (f"<!-- build:noscript -->\n  <noscript>\n    <ul class=\"noscript-list\">\n{items}\n"
             "    </ul>\n  </noscript>\n  <!-- /build:noscript -->")
    index = ROOT / "index.html"
    s = index.read_text()
    s, n = re.subn(r"<!-- build:noscript -->.*?<!-- /build:noscript -->", lambda m: block, s, flags=re.S)
    if n != 1:
        raise SystemExit("index.html: build:noscript markers not found")
    index.write_text(s)
    print(f"built sitemap.xml, feed.xml and noscript list for {len(ordered)} articles")


if __name__ == "__main__":
    main()
