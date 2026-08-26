#!/usr/bin/env python3
"""Auto-ingestion pipeline for AI Escape Log.

Takes the candidate queue and:
  1. AUTO-INGESTS candidates that pass a strict deterministic gate:
       - URL host is a trusted primary source (vendor/CISA/NVD/lab blog)
       - hot_score >= 3 (strong AI-incident signal)
     Logged with verification="single-source" so the frontend Community-Note
     shows amber "Context needs review" until a human upgrades it.
  2. PRUNES the queue: items older than PRUNE_DAYS that never scored hot,
     keeping the queue reviewable.
  3. REBUILDS derived data (csv/db/REPORT.md) and PUSHES to origin so
     GitHub Pages refreshes. Safe: skips commit when nothing changed.

Manual verification (prompt.md step 3b) remains the gate for upgrading
auto-ingested entries to primary-source status.
"""
import datetime
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

CAND = os.path.join(ROOT, "data", "candidates.json")
INC = os.path.join(ROOT, "data", "incidents.json")
SEEN = os.path.join(ROOT, "seen_urls.json")
LOG = "/Users/tony/Library/Logs/ai_escape_monitor.log"

TRUSTED_HOSTS = (
    "openai.com", "anthropic.com", "huggingface.co", "metr.org",
    "cisa.gov", "nvd.nist.gov", "jeffreyfountaine.github.io",
)
PRUNE_DAYS = 30
MIN_SCORE = 3

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"[auto_ingest] {datetime.datetime.now():%F %T} {msg}\n")

def load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default

def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def host_of(url):
    m = re.match(r"https?://([^/]+)", url or "")
    h = (m.group(1) if m else "").lower()
    return h[4:] if h.startswith("www.") else h

def trusted(url):
    h = host_of(url)
    return any(h == d or h.endswith("." + d) for d in TRUSTED_HOSTS)

def cve_ids(text):
    return set(re.findall(r"CVE-\d{4}-\d{4,7}", (text or "").upper()))

def already_logged(item, incidents):
    """Dedup beyond URL: match CVE IDs (NVD candidate vs CISA-alert incident etc.)."""
    ids = cve_ids(f"{item.get('url','')} {item.get('title','')}")
    if not ids:
        return False
    for inc in incidents:
        blob = f"{inc.get('id','')} {inc.get('url','')} {inc.get('title','')} {inc.get('summary','')}"
        if ids & cve_ids(blob):
            return True
    return False

def slugify(text, n=48):
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s[:n].rstrip("-")

CATEGORY_RULES = [
    ("sandbox-escape", r"sandbox|containment|escape|isolat"),
    ("rogue-agent",    r"rogue|unsanctioned|agent.{0,20}(hack|attack|sabotage)|went rogue"),
    ("withheld-release", r"pause|halt|withhold|pull(s|ed)? (the )?model|delay(s|ed)? release"),
    ("open-weight-leak", r"leak(ed|s)? weights|uncensored upload|weights (leak|published)"),
    ("government-shutdown", r"shut ?down|disable[sd]? (the )?model|order(s|ed)? .{0,30}(removal|disable)"),
    ("policy",         r"subpoena|laws?uit|regulat|senate|congress|bill |act |attorney general|investigation into"),
]

def categorize(text):
    for cat, pat in CATEGORY_RULES:
        if re.search(pat, text, re.I):
            return cat
    return "other"

def main():
    import importlib.util
    spec = importlib.util.spec_from_file_location("np", os.path.join(HERE, "news_probe.py"))
    np = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(np)

    candidates = load(CAND, [])
    incidents = load(INC, [])
    seen = set(load(SEEN, []))
    known_urls = {i.get("url") for i in incidents}

    today = datetime.date.today().isoformat()
    cutoff = (datetime.date.today() - datetime.timedelta(days=PRUNE_DAYS)).isoformat()

    ingested, pruned, kept = [], [], []
    for c in candidates:
        url = c.get("url") or ""
        if not url:
            continue  # malformed candidate
        score = np.hot_score(c)
        if url in known_urls or url in seen or already_logged(c, incidents):
            continue  # already handled; drop silently
        if score >= MIN_SCORE and trusted(url):
            title = c.get("title") or url
            blob = f"{title} {c.get('snippet','')}"
            inc = {
                "id": f"{c.get('first_seen', today)}-{slugify(title) or 'incident'}",
                "date": c.get("first_seen", today),
                "lab": "AUTO-INGEST (unverified publisher)",
                "model": "see source",
                "category": categorize(blob),
                "incident_type": title[:200],
                "title": title,
                "url": url,
                "source": c.get("source", ""),
                "summary": (c.get("snippet") or title)[:400],
                "status": "AUTO-INGESTED - pending human verification",
                "tags": ["auto-ingest", c.get("source", "").lower().replace(" ", "-") or "unknown-source"],
                "verification": "single-source",
            }
            incidents.append(inc)
            seen.add(url)
            ingested.append(inc)
        elif (c.get("first_seen") or today) < cutoff and score < MIN_SCORE:
            seen.add(url)  # expired, never hot -> retire
            pruned.append(c)
        else:
            kept.append(c)

    if ingested or pruned or len(kept) != len(candidates):
        save(CAND, kept)
        save(INC, incidents)
        save(SEEN, sorted(seen))

    log(f"ingested={len(ingested)} pruned={len(pruned)} queue={len(kept)}")
    for i in ingested:
        log(f"  + {i['id']} <- {i['url']}")

    if ingested:
        subprocess.run(["python3", os.path.join(ROOT, "build_csv.py")], check=True,
                       capture_output=True)
        subprocess.run(["python3", os.path.join(ROOT, "db.py")], check=True,
                       capture_output=True)
        subprocess.run(["python3", os.path.join(ROOT, "monitor", "incident_report.py")],
                       check=True, capture_output=True)

    # publish whatever changed (incidents and/or queue refresh) so Pages stays current
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode != 0
    if staged:
        msg = f"auto-ingest: {len(ingested)} incident(s), queue {len(candidates)}->{len(kept)}, pruned {len(pruned)} [cron]"
        subprocess.run(["git", "commit", "-m", msg], cwd=ROOT, check=True, capture_output=True)
        r = subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, capture_output=True)
        log("pushed Pages update" if r.returncode == 0 else f"push FAILED: {r.stderr[:200]}")
    else:
        log("no changes; nothing to publish")

    print(f"[auto_ingest] ingested={len(ingested)} pruned={len(pruned)} queue={len(kept)}"
          + (" -> published" if staged else " -> nothing new"))

if __name__ == "__main__":
    main()
