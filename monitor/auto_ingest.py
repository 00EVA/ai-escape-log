#!/usr/bin/env python3
"""
auto_ingest.py - Automated candidate -> incident ingestion (no human gate).

Replaces the manual verification step with a source-tier verification model:
  primary-source      CISA/NVD, official lab newsroom posts
  multiple-secondary  same story corroborated by 2+ distinct outlets
  single-source       one outlet (kept, visibly labeled)

Non-AI-specific CVE entries (CISA/NVD matches on generic software) are
archived with a reason instead of polluting the incident log.

After ingestion: rebuilds csv/db/REPORT.md, commits and pushes so GitHub
Pages refreshes. Safe to run repeatedly (idempotent by URL + title).

Usage: python3 monitor/auto_ingest.py [--dry-run]
"""
import argparse
import datetime
import email.utils
import json
import os
import re
import subprocess
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CAND = os.path.join(ROOT, "data", "candidates.json")
INC = os.path.join(ROOT, "data", "incidents.json")
ARCHIVE = os.path.join(ROOT, "data", "ingested_archive.json")

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
                         r"undisclosed model)"),
    ("sandbox-escape", r"(sandbox|escaped? (?:the|its)|containment|guardrail|"
                       r"exfiltrat|bypass)"),
    ("rogue-agent", r"(rogue|went rogue|unauthorized|unsanctioned|deceiv|"
                    r"sabotage|self[- ]cop|agent.{0,30}(?:attack|hid|tamper))"),
    ("policy", r"(regulat|policy|executive order|ai act|lawsuit|senate|"
               r"congress|fda|subpoena|probe into)"),
    ("crime-fraud", r"(fraud|scam|phish|deepfake|ransom|theft|impersonat|"
                    r"market manipulation|botnet|hijack|arrest|charged)"),
]

OFFICIAL = re.compile(
    r"(openai\.com|anthropic\.com|deepmind\.google|ai\.googleblog|blog\.google|"
    r"meta\.com|nvidia\.com|huggingface\.co|cisa\.gov|nvd\.nist\.gov|microsoft\.com|"
    r"waymo\.com|tesla\.com|openrouter\.ai)",
    re.I,
)


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


def classify(item, all_candidates):
    blob = f"{item['title']} {item['snippet']}"
    cat = "other"
    for name, pat in CATEGORY_RULES:
        if re.search(pat, blob, re.I):
            cat = name
            break
    # corroboration: same normalized title from 2+ distinct sources
    tn = norm_title(item["title"])
    outlets = {c["source"] for c in all_candidates if norm_title(c["title"]) == tn}
    if OFFICIAL.search(item["url"]):
        ver = "primary-source"
    elif len(outlets) >= 2:
        ver = "multiple-secondary"
    else:
        ver = "single-source"
    return cat, ver


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cands = json.load(open(CAND))
    incs = json.load(open(INC))
    archive = json.load(open(ARCHIVE)) if os.path.exists(ARCHIVE) else []
    known_urls = {i.get("url") for i in incs} | {a.get("url") for a in archive}
    known_titles = {norm_title(i["title"]) for i in incs}

    promoted, skipped = [], 0
    for c in cands:
        blob = f"{c['title']} {c['snippet']} {c['url']}"
        if "cisa" in c["source"].lower() or "NVD" in c["source"]:
            if not AI_SPECIFIC.search(blob):
                archive.append({**c, "reason": "not-ai-specific-cve"})
                skipped += 1
                continue
        if c["url"] in known_urls or norm_title(c["title"]) in known_titles:
            archive.append({**c, "reason": "duplicate"})
            skipped += 1
            continue
        cat, ver = classify(c, cands)
        date = parse_date(c["date"])
        slug = re.sub(r"[^a-z0-9]+", "-", c["title"].lower())[:48].strip("-")
        incs.append({
            "id": f"{date}-{slug}" or c["url"],
            "date": date,
            "lab": "Unattributed",
            "model": "",
            "category": cat,
            "incident_type": c["title"],
            "title": c["title"],
            "url": c["url"],
            "source": c["source"],
            "summary": (c["snippet"] or c["title"]).strip(),
            "status": "auto-ingested",
            "tags": [],
            "verification": ver,
        })
        known_urls.add(c["url"])
        known_titles.add(norm_title(c["title"]))
        promoted.append(c)

    if args.dry_run:
        print(f"[ingest:dry] would promote {len(promoted)}, archive {skipped}")
        for c in promoted[:10]:
            cat, ver = classify(c, cands)
            print(f"  [{ver}|{cat}] {c['title'][:70]}")
        return

    if not promoted and not skipped:
        print("[ingest] queue empty - nothing to do")
        return

    json.dump(incs, open(INC, "w"), indent=2, ensure_ascii=False)
    json.dump(archive, open(ARCHIVE, "w"), indent=2, ensure_ascii=False)
    remaining = [c for c in cands if c not in promoted]
    # keep promoted out of the queue; archive holds them for audit
    json.dump(remaining, open(CAND, "w"), indent=2, ensure_ascii=False)

    for script in ("build_csv.py", "db.py", os.path.join("monitor", "incident_report.py")):
        subprocess.run([sys.executable, os.path.join(ROOT, script)],
                       capture_output=True)

    msg = (f"[auto-ingest] +{len(promoted)} incidents from queue "
           f"({skipped} archived)\n\n" +
           "\n".join(f"- {c['title']}" for c in promoted[:20]))
    git("add", "data/incidents.json", "data/incidents.csv", "data/incidents.db",
        "data/candidates.json", "data/ingested_archive.json", "REPORT.md")
    c = git("commit", "-m", msg)
    if c.returncode == 0:
        git("pull", "--rebase", "-q", "origin", "main")
        p = git("push", "-q", "origin", "main")
        pushed = "pushed" if p.returncode == 0 else f"PUSH FAILED: {p.stderr.strip()}"
    else:
        pushed = f"commit skipped: {c.stderr.strip()[:120]}"
    print(f"[ingest] +{len(promoted)} incidents (archived {skipped}) "
          f"-> total {len(incs)} | {pushed}")
    for c in promoted[:12]:
        cat, ver = classify(c, cands)
        print(f"  + [{ver}|{cat}] {c['title'][:76]}")


if __name__ == "__main__":
    main()
