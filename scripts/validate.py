#!/usr/bin/env python3
"""Validate metadata.json and article pages. Exit 1 on any error.

Usage: python3 scripts/validate.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STAGES = ["planning", "tool_call", "retrieval", "execute", "verify", "output"]
REQUIRED = ["id", "slug", "title", "hook", "path", "date", "status", "type", "tags",
            "reading_time_minutes", "pinned"]
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

errors = []


def err(msg):
    errors.append(msg)


def main():
    try:
        data = json.loads((ROOT / "metadata.json").read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f"metadata.json: {e}")
        return 1

    articles = data.get("articles", [])
    seen = {"id": {}, "slug": {}, "coined_term": {}}
    listed = set()
    for a in articles:
        label = a.get("slug", "<no slug>")
        for k in REQUIRED:
            if k not in a:
                err(f"{label}: missing field '{k}'")
        if "format" in a:
            err(f"{label}: use 'type', not 'format'")
        if a.get("type") not in ("diagnostic", "guide"):
            err(f"{label}: type must be 'diagnostic' or 'guide'")
        if not re.fullmatch(r"\d{4}", str(a.get("id", ""))):
            err(f"{label}: id must be a 4-digit string")
        if not DATE.match(str(a.get("date", ""))):
            err(f"{label}: date must be YYYY-MM-DD")
        rw = a.get("research_window")
        if rw is not None and not (isinstance(rw, list) and len(rw) == 2 and all(DATE.match(x) for x in rw)):
            err(f"{label}: research_window must be [YYYY-MM-DD, YYYY-MM-DD]")
        for k in ("root_cause_stage", "symptom_stage"):
            if k in a and a[k] not in STAGES:
                err(f"{label}: {k} must be one of {STAGES}")
        if a.get("type") == "diagnostic" and "root_cause_stage" not in a:
            err(f"{label}: diagnostics need root_cause_stage")
        for k in seen:
            v = a.get(k)
            if v is None:
                continue
            v = str(v).lower()
            if v in seen[k]:
                err(f"{label}: duplicate {k} '{v}' (also {seen[k][v]})")
            seen[k][v] = label
        path = ROOT / a.get("path", "")
        listed.add(a.get("path"))
        if not path.is_file():
            err(f"{label}: path {a.get('path')} does not exist")
            continue
        html = path.read_text(errors="replace")
        title = re.search(r"<title>([^<]*)</title>", html)
        if not title or "Agentic Engineering" not in title.group(1):
            err(f"{a['path']}: <title> should end with 'Agentic Engineering'")
        if "../index.html" not in html and "iggym.github.io/agentic-engineering/\"" not in html:
            err(f"{a['path']}: no link back to the homepage")
        for href in re.findall(r'href="([^"#:]+\.html)"', html):
            if not (path.parent / href).resolve().is_file():
                err(f"{a['path']}: broken internal link {href}")

    for f in sorted((ROOT / "articles").glob("*.html")):
        rel = f"articles/{f.name}"
        if rel not in listed:
            err(f"{rel}: not listed in metadata.json")

    for e in errors:
        print("ERROR", e)
    print(f"{len(articles)} articles checked, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
