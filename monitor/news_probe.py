#!/usr/bin/env python3
"""
news_probe.py - News + social-media probe for the AI Escape Log.

Pulls recent AI-safety incident chatter from key-free sources:
  - Hacker News (Algolia API) - keyword search
  - Reddit (JSON) - r/artificial, r/singularity, r/LocalLLaMA
  - Tech news RSS: The Register, Ars Technica, The Verge

Filters against the "escape / lost control" signal, dedups against
seen_urls.json + existing candidates, appends NEW candidates to
data/candidates.json, and prints a compact digest to stdout (cron-injectable).

Usage: python3 monitor/news_probe.py [--limit N]
"""
import argparse
import datetime
import json
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEEN = os.path.join(ROOT, "seen_urls.json")
CAND = os.path.join(ROOT, "data", "candidates.json")

SIGNAL = re.compile(
    r"(escap(ed|e)|rogue|went rogue|lost control|broke out|exfiltrat|sandbox|"
    r"containment|unprecedented|shut off|disabled|guardrail|bypass|autonomous "
    r"attack|out of control|leaked weights|uncensored|runaway)",
    re.I,
)

HN_QUERIES = [
    "AI escaped sandbox",
    "AI model containment break",
    "AI rogue agent",
    "AI went rogue",
    "AI sandbox escape",
    "guardrail bypass AI",
]

REDDITS = ["artificial", "singularity", "LocalLLaMA"]
REDDIT_QUERY = "AI escaped sandbox OR rogue OR containment"

FEEDS = [
    ("The Register", "https://www.theregister.com/headlines.atom"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
]

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AiEscapeLogMonitor/1.0"

# --- helpers ----------------------------------------------------------------


def load_json(p, default):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(p, data):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def fetch(url, timeout=15):
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/json,text/xml,*/*"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# --- sources ----------------------------------------------------------------


def hn_search(limit):
    out = []
    for q in HN_QUERIES[:3]:  # keep probe light
        url = ("https://hn.algolia.com/api/v1/search_by_date"
               f"?query={urllib.parse.quote(q)}&tags=story&hitsPerPage={limit}")
        try:
            d = json.loads(fetch(url))
            for h in d.get("hits", []):
                out.append({
                    "title": h.get("title") or "",
                    "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                    "source": "Hacker News",
                    "date": (h.get("created_at") or "")[:10],
                    "snippet": (h.get("story_text") or "")[:300],
                })
        except Exception as e:
            print(f"[warn] HN '{q}' failed: {e}")
    return out


def reddit_search(limit):
    out = []
    for sub in REDDITS:
        url = (f"https://www.reddit.com/r/{sub}/search.json"
               f"?q={urllib.parse.quote(REDDIT_QUERY)}&sort=new&limit={limit}")
        try:
            d = json.loads(fetch(url))
            for c in d.get("data", {}).get("children", []):
                p = c.get("data", {})
                out.append({
                    "title": p.get("title", ""),
                    "url": f"https://www.reddit.com{p.get('permalink', '')}",
                    "source": f"Reddit r/{sub}",
                    "date": datetime.datetime.fromtimestamp(p.get("created_utc", 0)).strftime("%Y-%m-%d"),
                    "snippet": (p.get("selftext") or "")[:300],
                })
        except Exception as e:
            print(f"[warn] reddit r/{sub} failed: {e}")
    return out


def feed_search():
    out = []
    for name, url in FEEDS:
        try:
            raw = fetch(url)
            root = ET.fromstring(raw)
            entries = root.findall("{http://www.w3.org/2005/Atom}entry")
            if not entries:  # RSS 2.0 fallback
                entries = root.findall("channel/item")
            for e in entries[:15]:
                if e.tag.endswith("entry"):
                    t = e.findtext("{http://www.w3.org/2005/Atom}title", "") or ""
                    link_el = e.find("{http://www.w3.org/2005/Atom}link")
                    link = link_el.get("href") if link_el is not None else ""
                    summ = (e.findtext("{http://www.w3.org/2005/Atom}summary", "")
                            or e.findtext("{http://www.w3.org/2005/Atom}content", "")
                            or "")
                    date = e.findtext("{http://www.w3.org/2005/Atom}updated", "")[:10]
                else:
                    t = e.findtext("title", "") or ""
                    link_el = e.find("link")
                    link = link_el.get("href") if link_el is not None else ""
                    summ = e.findtext("description", "") or ""
                    date = e.findtext("pubDate", "")[:10]
                blob = f"{t} {summ}"
                if not SIGNAL.search(blob):
                    continue
                out.append({"title": t, "url": link, "source": name,
                            "date": date, "snippet": summ[:300]})
        except Exception as ex:
            print(f"[warn] feed {name} failed: {ex}")
    return out


# --- main -------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(description="News/social probe for AI Escape Log")
    ap.add_argument("--limit", type=int, default=5)
    args = ap.parse_args()

    seen = set(load_json(SEEN, []))
    candidates = load_json(CAND, [])
    known = {c["url"] for c in candidates}

    today = datetime.date.today().isoformat()
    found = []
    collector = hn_search(args.limit) + reddit_search(args.limit) + feed_search()
    for item in collector:
        blob = f"{item['title']} {item['snippet']}"
        if not SIGNAL.search(blob):
            continue
        if item["url"] in seen or item["url"] in known:
            continue
        item["first_seen"] = today
        found.append(item)

    # dedupe by url, keep first
    uniq = {}
    for it in found:
        uniq.setdefault(it["url"], it)
    found = list(uniq.values())[: args.limit]

    if found:
        candidates.extend(found)
        save_json(CAND, candidates)
    print(f"[news_probe] {len(found)} new candidate(s) -> data/candidates.json"
          f" (total queued: {len(candidates)})")
    for it in found:
        print(f"  - {it['source']} | {it['date']} | {it['title']}")
        print(f"    {it['url']}")


if __name__ == "__main__":
    main()