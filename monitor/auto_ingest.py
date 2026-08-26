#!/usr/bin/env python3
"""Auto-ingestion pipeline for AI Escape Log.

Priority order:
  1. HUMAN DECISIONS (data/human_decisions.json, exported from review.html):
       accept  -> promote to incident regardless of gate (human override)
       decline -> archive (kept forever, never deleted)
       star    -> promote (if needed) + add to data/spotlight.json (index page pins it)
  2. AUTO gate (only without a human decision):
       official-domain source (openai.com, cisa.gov, ...) AND hot_score >= 3
  3. Everything else STAYS in the queue for human review; items older than
     PRUNE_DAYS with score < 3 are archived as "expired" (still on disk).

Nothing is ever deleted: candidates.go → data/ingested_archive.json with a reason.
Run --dry-run to preview. Commits + pushes only when something changed (Pages refresh).
"""
import argparse
import datetime
import email.utils
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CAND = os.path.join(ROOT, "data", "candidates.json")
INC = os.path.join(ROOT, "data", "incidents.json")
ARCHIVE = os.path.join(ROOT, "data", "ingested_archive.json")
DECS = os.path.join(ROOT, "data", "human_decisions.json")
SPOTLIGHT = os.path.join(ROOT, "data", "spotlight.json")

AI_SPECIFIC = re.compile(
    r"(AI|agent|LLM|GPT|chatgpt|copilot|gemini|claude|llama|deepseek|mistral|"
    r"chatbot|model server|inference|vLLM|ollama|mlflow|pytorch|tensorflow|"
    r"GPU|vector database|RAG|openweight|open-weight|voice clone|deepfake)",
    re.I,
)

CATEGORY_RULES = [
    ("government-shutdown", r"(ban|bans|blocked|shut(?:s|down)? order|disables|"
                            r"government (?:orders|forces)|country (?:blocks|pulls))"),
    ("open-weight-leak", r"(leak|weights (?:escaped|published)|uncensored|"
                         r"weights (?:appeared|released) without)"),
    ("withheld-release", r"(withheld|stealth|unreleased|quietly (?:shipped|deployed)|"
                         r"undisclosed model|halt|pause(s|d)? (?:training|development))"),
    ("sandbox-escape", r"(sandbox|escaped? (?:the|its)|containment|guardrail|"
                       r"exfiltrat|bypass)"),
    ("rogue-agent", r"(rogue|went rogue|unauthorized|unsanctioned|deceiv|"
                    r"sabotage|self[- ]cop|agent.{0,30}(?:attack|hid|tamper))"),
    ("policy", r"(regulat|policy|executive order|ai act|lawsuit|senate|"
               r"congress|fda|subpoena|probe into|attorney general|investigation into)"),
    ("crime-fraud", r"(fraud|scam|phish|deepfake|ransom|theft|impersonat|"
                    r"market manipulation|botnet|hijack|arrest|charged)"),
]

OFFICIAL = re.compile(
    r"(openai\.com|anthropic\.com|deepmind\.google|ai\.googleblog|blog\.google|"
    r"meta\.com|nvidia\.com|huggingface\.co|cisa\.gov|nvd\.nist\.gov|microsoft\.com|"
    r"metr\.org|waymo\.com|tesla\.com|openrouter\.ai)",
    re.I,
)

PRUNE_DAYS = 30


def load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def parse_date(s):
    s = (s or "").strip()
    if re.match(r"\d{4}-\d{2}-\d{2}", s):
        return s[:10]
    try:
        return email.utils.parsedate_to_datetime(s).date().isoformat()
    except Exception:
        return datetime.date.today().isoformat()


def norm_title(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())[:80]


def cve_ids(text):
    return set(re.findall(r"CVE-\d{4}-\d{4,7}", (text or "").upper()))


def classify(item, all_candidates):
    blob = f"{item['title']} {item.get('snippet') or ''} {item.get('url') or ''}"
    cat = "other"
    for name, pat in CATEGORY_RULES:
        if re.search(pat, blob, re.I):
            cat = name
            break
    # corroboration: same normalized title from 2+ distinct sources
    tn = norm_title(item["title"])
    outlets = {c["source"] for c in all_candidates if norm_title(c["title"]) == tn}
    if OFFICIAL.search(item.get("url") or ""):
        ver = "primary-source"
    elif len(outlets) >= 2:
        ver = "multiple-secondary"
    else:
        ver = "single-source"
    return cat, ver


def hot_score(item):
    """Same scoring as news_probe (kept in sync; probe module optional)."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "np", os.path.join(HERE, "news_probe.py"))
        np = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(np)
        return np.hot_score(item)
    except Exception:
        blob = f"{item.get('title','')} {item.get('snippet','')}".lower()
        return 2 if re.search(r"(?i)(rogue|escape|breach|post-?mortem)", blob) else 0


def make_incident(c, cat, ver, note=""):
    date = parse_date(c.get("date"))
    slug = re.sub(r"[^a-z0-9]+", "-", (c.get("title") or "").lower())[:48].strip("-")
    return {
        "id": f"{date}-{slug}" or c.get("url"),
        "date": date,
        "lab": "Unattributed",
        "model": "",
        "category": cat,
        "incident_type": c.get("title"),
        "title": c.get("title"),
        "url": c.get("url"),
        "source": c.get("source"),
        "summary": (c.get("snippet") or c.get("title") or "").strip(),
        "status": (note or "auto-ingested"),
        "tags": ["human-accepted"] if note else [],
        "verification": ver,
    }


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cands = load(CAND, [])
    incs = load(INC, [])
    archive = load(ARCHIVE, [])
    decisions = load(DECS, {})
    spotlight = load(SPOTLIGHT, [])
    dec_map = decisions.get("decisions", decisions) if decisions else {}

    known_urls = {i.get("url") for i in incs} | {a.get("url") for a in archive}
    known_titles = {norm_title(i.get("title")) for i in incs}
    known_cves = set()
    for i in incs:
        known_cves |= cve_ids(f"{i.get('id','')} {i.get('url','')} {i.get('title','')} {i.get('summary','')}")

    today = datetime.date.today().isoformat()
    cutoff = (datetime.date.today() - datetime.timedelta(days=PRUNE_DAYS)).isoformat()

    promoted, pruned, starred_new = [], [], []
    remaining = []
    for c in cands:
        url = c.get("url") or ""
        title = c.get("title") or ""
        blob = f"{title} {c.get('snippet') or ''} {url}"
        dec = dec_map.get(url, {})
        score = hot_score(c)
        ids = cve_ids(blob)

        def archive_it(reason):
            archive.append({**c, "reason": reason, "archived_at": today})

        # 1. human decision wins
        if dec.get("decision") == "decline":
            archive_it("human-declined")
            continue
        if url in known_urls or norm_title(title) in known_titles or (ids & known_cves):
            archive_it("duplicate")
            continue
        if dec.get("decision") == "accept":
            cat, ver = classify(c, cands)
            incs.append(make_incident(c, cat, ver, note="human-accepted"))
            known_urls.add(url); known_titles.add(norm_title(title)); known_cves |= ids
            promoted.append(c)
            if dec.get("star"):
                spotlight.append({"url": url, "title": title, "id": incs[-1]["id"]})
                starred_new.append(title)
            continue
        # 2. auto gate
        if score >= 3 and OFFICIAL.search(url):
            if "cisa" in (c.get("source") or "").lower() and not AI_SPECIFIC.search(blob):
                archive_it("not-ai-specific-cve")
                continue
            cat, ver = classify(c, cands)
            incs.append(make_incident(c, cat, ver))
            known_urls.add(url); known_titles.add(norm_title(title)); known_cves |= ids
            promoted.append(c)
            if dec.get("star"):
                spotlight.append({"url": url, "title": title, "id": incs[-1]["id"]})
                starred_new.append(title)
            continue
        # 3. prune stale low-signal
        if (c.get("first_seen") or today) < cutoff and score < 3:
            archive_it("expired")
            pruned.append(c)
            continue
        remaining.append(c)

    if args.dry_run:
        print(f"[ingest:dry] promote {len(promoted)}, prune {len(pruned)}, "
              f"keep {len(remaining)}, archive total {len(archive)}")
        for c in promoted[:10]:
            cat, ver = classify(c, cands)
            print(f"  [{ver}|{cat}] {c['title'][:70]}")
        return

    changed = promoted or pruned or len(remaining) != len(cands) or starred_new
    if not changed:
        print("[ingest] nothing to do")
        return

    json.dump(incs, open(INC, "w"), indent=2, ensure_ascii=False)
    json.dump(archive, open(ARCHIVE, "w"), indent=2, ensure_ascii=False)
    json.dump(remaining, open(CAND, "w"), indent=2, ensure_ascii=False)
    if spotlight:
        json.dump(spotlight, open(SPOTLIGHT, "w"), indent=2, ensure_ascii=False)

    for script in ("build_csv.py", "db.py", os.path.join("monitor", "incident_report.py")):
        subprocess.run([sys.executable, os.path.join(ROOT, script)], capture_output=True)

    msg = (f"[auto-ingest] +{len(promoted)} incidents, -{len(pruned)} expired, "
           f"queue {len(cands)}->{len(remaining)}, archive {len(archive)}\n\n" +
           "\n".join(f"- {c['title']}" for c in promoted[:20]))
    git("add", "data/incidents.json", "data/incidents.csv", "data/incidents.db",
        "data/candidates.json", "data/ingested_archive.json", "data/spotlight.json",
        "data/human_decisions.json", "REPORT.md")
    c = git("commit", "-m", msg)
    if c.returncode == 0:
        git("pull", "--rebase", "-q", "origin", "main")
        p = git("push", "-q", "origin", "main")
        pushed = "pushed" if p.returncode == 0 else f"PUSH FAILED: {p.stderr.strip()}"
    else:
        pushed = f"commit skipped: {c.stderr.strip()[:120]}"
    print(f"[ingest] +{len(promoted)} incidents (-{len(pruned)} expired) "
          f"-> total {len(incs)}, queue {len(remaining)} | {pushed}")
    for c in promoted[:12]:
        cat, ver = classify(c, cands)
        print(f"  + [{ver}|{cat}] {c['title'][:76]}")


if __name__ == "__main__":
    main()
