#!/usr/bin/env python3
"""Link-rot guard for AI Escape Log.

HEAD-checks every incident source URL in data/incidents.json, with a GET
fallback, one retry, and bot-wall awareness (403/429/503 = blocked, not dead).
Writes data/link_health.json (committed by auto_publish.sh) so the dataset's
own health is tracked like the data itself.

Exit code is always 0 — a dead link is data, not a failure.
"""
import datetime
import json
import os
import ssl
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INC = os.path.join(ROOT, "data", "incidents.json")
OUT = os.path.join(ROOT, "data", "link_health.json")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 ai-escape-log-linkcheck/1.0"}
TIMEOUT = 20
CTX = ssl.create_default_context()


def check(url):
    """Return (state, code). States: ok | blocked | dead | unreachable."""
    for attempt in (1, 2):
        for method in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(url, headers=UA, method=method)
                with urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX) as r:
                    return "ok", r.status
            except urllib.error.HTTPError as e:
                if e.code in (403, 429, 503, 999):
                    return "blocked", e.code      # bot wall / rate limit, not rot
                if e.code in (404, 410):
                    return "dead", e.code
                if e.code < 500 and attempt == 2:
                    return "ok", e.code           # odd 4xx but server is alive
                err = e.code
            except (urllib.error.URLError, TimeoutError, OSError, ssl.SSLError) as e:
                err = str(e)[:80]
            time.sleep(1)
        if attempt == 1:
            time.sleep(3)  # brief pause before the GET retry pass
    return "unreachable", err


def main():
    data = json.load(open(INC))
    incs = data if isinstance(data, list) else data.get("incidents", [])
    now = datetime.datetime.now().strftime("%F %T")
    results = []
    for it in incs:
        url = it.get("url", "")
        if not url:
            continue
        state, code = check(url)
        results.append({"id": it.get("id", ""), "url": url,
                        "state": state, "code": code, "checked_at": now})
        if state in ("dead", "unreachable"):
            print(f"  [{state} {code}] {it.get('id', '?')}: {url}")
        time.sleep(0.5)  # be polite

    tallies = {}
    for r in results:
        tallies[r["state"]] = tallies.get(r["state"], 0) + 1
    json.dump({"checked_at": now, "counts": tallies, "results": results},
              open(OUT, "w"), indent=2)
    print(f"[linkcheck] {now}: {len(results)} URLs — "
          + ", ".join(f"{k}={v}" for k, v in sorted(tallies.items())))


if __name__ == "__main__":
    main()
