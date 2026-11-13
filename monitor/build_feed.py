#!/usr/bin/env python3
"""Build the Atom feed (feed.xml) for AI Escape Log from data/incidents.json.

Newest 50 incidents. Called by auto_publish.sh after the derived-data rebuild,
so the feed always ships in the same commit as the data it reflects.
"""
import datetime
import json
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INC = os.path.join(ROOT, "data", "incidents.json")
OUT = os.path.join(ROOT, "feed.xml")
SITE = "https://00eva.github.io/ai-escape-log"
MAX_ENTRIES = 50


def rfc3339(date_str):
    try:
        return f"{date_str}T12:00:00Z"  # date-only granularity, noon UTC
    except (TypeError, ValueError):
        return None


def entry(it):
    eid = escape(str(it.get("id", "")))
    title = escape(it.get("title") or it.get("incident_type") or "Untitled incident")
    url = escape(it.get("url") or SITE)
    updated = rfc3339(it.get("date")) or f"{datetime.date.today()}T12:00:00Z"
    summary = escape((it.get("summary") or "")[:500])
    cat = escape(it.get("category") or "other")
    return f"""  <entry>
    <id>tag:00eva.github.io,2026:/ai-escape-log/{eid}</id>
    <title>{title}</title>
    <link href="{url}"/>
    <updated>{updated}</updated>
    <summary>{summary}</summary>
    <category term="{cat}"/>
  </entry>"""


def main():
    data = json.load(open(INC))
    incs = data if isinstance(data, list) else data.get("incidents", [])
    incs = sorted(incs, key=lambda i: i.get("date", ""), reverse=True)[:MAX_ENTRIES]
    updated = max((rfc3339(i.get("date")) or "" for i in incs), default="") \
        or f"{datetime.date.today()}T12:00:00Z"
    body = "\n".join(entry(i) for i in incs)
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>AI Escape Log</title>
  <subtitle>A public, machine-readable tracker of frontier AI models escaping the lab.</subtitle>
  <link href="{SITE}/"/>
  <link rel="self" href="{SITE}/feed.xml"/>
  <id>tag:00eva.github.io,2026:/ai-escape-log</id>
  <updated>{updated}</updated>
{body}
</feed>
"""
    with open(OUT, "w") as f:
        f.write(xml)
    print(f"[feed] wrote feed.xml ({len(incs)} entries, updated {updated})")


if __name__ == "__main__":
    main()
