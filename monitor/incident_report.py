#!/usr/bin/env python3
"""
incident_report.py - Personal AI-incident morning briefing.

Builds a single human-readable report (REPORT.md + prints to stdout) from:
  - data/incidents.json   (verified incidents)
  - data/candidates.json  (fresh unverified signals from the probe)
  - a static counter-action playbook (per category) and early-warning watchlist

Usage: python3 monitor/incident_report.py [--days 14]
"""
import argparse
import datetime
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INCIDENTS = os.path.join(ROOT, "data", "incidents.json")
CANDIDATES = os.path.join(ROOT, "data", "candidates.json")
REPORT = os.path.join(ROOT, "REPORT.md")

CRIME_TAGS = re.compile(
    r"(crime|fraud|scam|ransomware|botnet|phishing|hijack|sabotage|chaos|havoc|"
    r"outage|disrupt|theft|money|bank|financial|impersonat|voice clone|deepfake)",
    re.I,
)

VERIFY_LABEL = {
    "primary-source": "PRIMARY SOURCE",
    "multiple-secondary": "2+ SECONDARY",
    "single-source": "SINGLE SOURCE (verify)",
}

CATEGORY_PLAYBOOK = {
    "sandbox-escape": [
        "Containment = egress control. Assume the model WILL try to reach the internet; the question is only how fast.",
        "Counter-action: hard network egress controls by default; internet access only via scoped, monitored, time-limited exceptions.",
        "Audit package registries / artifact caches (Artifactory, pip/npm proxies) - they are the favorite escape ladder.",
        "Pre-position an open-weight model (e.g. GLM-5.x) on your own infra for forensics, since hosted models refuse attack-artifact analysis.",
    ],
    "rogue-agent": [
        "Rogue agents do exactly what they were optimized to do - the goal was mis-specified, not the code.",
        "Counter-action: scope agent credentials to the absolute minimum; never give an agent live prod tokens.",
        "Log ALL agent actions (the HF agent logged ~17,600 actions); you can't counter what you can't see.",
        "Watch for agents self-coordinating (message boards, shared scratch space) - that's the 'swarm' tell.",
    ],
    "withheld-release": [
        "A lab holding back a model is a 'capability escaped the release process' signal - track it, don't dismiss it.",
        "Counter-action: treat the capability as already-in-the-wild; model the worst release scenario (weights, docs, evals).",
        "Watch OpenRouter 'created' dates + HF uncensored uploads for the same capability leaking via a third party.",
    ],
    "open-weight-leak": [
        "Leaked weights are permanent and unretractable - once out, assume everyone has them.",
        "Counter-action: search HF/dataset hubs for the exact weight name daily; pre-build mitigations before the leak happens.",
    ],
    "government-shutdown": [
        "A state disabling a model is the strongest 'this model is dangerous' confirmation that exists.",
        "Counter-action: follow the disable order's rationale - it tells you the exact capability the state feared.",
    ],
    "policy": [
        "Policy moves telegraph where incidents are heading (kill-switch bills, disclosure mandates, evaluation gates).",
        "Counter-action: comply early; a lab that fights disclosure looks like it's hiding an incident.",
    ],
    "other": [
        "Uncategorized - read the primary source before trusting the headline.",
    ],
}

EARLY_WARNING_WATCHLIST = [
    ("X/Felony Bench", "https://www.felonybench.com/",
     "Live scoreboard of models taking unsanctioned real-world actions; each row links a primary source."),
    ("OpenRouter portal", "https://openrouter.ai/api/v1/models",
     "New `created` model = surprise drop; new `expiration_date` = a model being sunset (often a disable incident). Probe already polls this daily."),
    ("Hugging Face hub", "https://huggingface.co/models?search=uncensored",
     "Fresh uncensored / voice-clone / leaked-weight uploads. Probe already polls this daily."),
    ("Polymarket", "https://polymarket.com/search?q=AI",
     "Prediction markets price incident outcomes before the press; a sharp repricing is a lead, not proof."),
    ("r/singularity mirror", "https://www.singularitymoments.com/news?website=reddit_singularity",
     "Near-real-time mirror of r/singularity + r/OpenAI + r/LocalLLaMA."),
    ("Talent moves", "https://kiankyars.github.io/frontier-lab-moves",
     "Departures often precede containment/withheld-release disclosures (Shazeer, Jumper examples)."),
    ("AI incident databases", "https://incidentdatabase.ai/",
     "Canonical cross-check + AIWI whistleblower channel (https://aiwi.org/)."),
    ("Import AI", "https://importai.substack.com/",
     "Jack Clark's weekly - longest-running frontier-AI roundup, explicit incident angle. Probe pulls its RSS."),
]

CRIME_PLAYBOOK = [
    "AI crime triage: is the AI the actor (rogue agent/autonomous hack) or the tool (deepfake, phishing gen)? Response differs.",
    "Deepfake/voice-clone fraud -> verify identity out-of-band (second channel), freeze/flag the transaction, report to bank + law enforcement (FTC/IC3).",
    "Autonomous-agent hacks -> assume creds are burned; rotate everything in blast radius, ship logs to forensics before cleanup.",
    "Ransomware/outage -> isolate, preserve evidence, contact CISA; never pay without a plan.",
    "Financial-market manipulation by AI -> report to the exchange/regulator; most have AI-abuse reporting now.",
]


def load_json(p, default):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def render(brief, days):
    incidents = load_json(INCIDENTS, [])
    candidates = load_json(CANDIDATES, [])

    today = datetime.date.today()
    cutoff = (today - datetime.timedelta(days=days)).isoformat()

    recent = sorted(
        [i for i in incidents if (i.get("date") or "0000") >= cutoff],
        key=lambda i: i.get("date", ""),
        reverse=True,
    )
    crime = [i for i in recent if CRIME_TAGS.search((i.get("title", "") + " " + " ".join(i.get("tags", []))))]

    L = []
    A = L.append
    A(f"# AI Incident Briefing — {today.isoformat()}")
    A("")
    A(f"_Verified incidents in last {days}d: {len(recent)} | AI-crime/chaos flagged: {len(crime)} | "
      f"fresh candidates queued: {len(candidates)}_")
    A("")

    A("## 1. Latest verified incidents")
    A("")
    if not recent:
        A("None in the window.")
    for i in recent:
        flag = " [CRIME/CHAOS]" if i in crime else ""
        v = i.get("verification") or "primary-source"
        vlabel = f" | VERIFY: {VERIFY_LABEL.get(v, v.upper())}"
        A(f"### {i['date']} {i['title']}{flag}")
        A(f"- Lab/Model: {i.get('lab','N/A')} / {i.get('model','N/A')} | Category: {i.get('category','N/A')}{vlabel}")
        A(f"- {i.get('summary','')}")
        A(f"- Source: {i.get('url','')}")
        pb = CATEGORY_PLAYBOOK.get(i.get("category"), CATEGORY_PLAYBOOK["other"])
        A(f"- Counter-action: {pb[0]}")
        A("")

    A("## 2. AI crime / chaos / havoc watch")
    A("")
    if not crime:
        A("No crime/chaos-flagged incidents in the window.")
    for i in crime:
        A(f"- {i['date']} | {i['title']} ({i.get('category','N/A')})")
        A(f"  {i.get('url','')}")
    A("")
    A("If one of these hits you: " + " | ".join(CRIME_PLAYBOOK))
    A("")

    A(f"## 3. Fresh unverified candidates (be-first-to-know queue, n={len(candidates)})")
    A("")
    if not candidates:
        A("Queue empty.")
    for c in candidates[:20]:
        t = c.get("title") or ""
        if not CRIME_TAGS.search(t) and "rogue" not in t.lower() and "escaped" not in t.lower() and "hack" not in t.lower():
            continue
        A(f"- [{c.get('source','?')}] {t}  ({c.get('date','?')})")
        A(f"  {c.get('url','')}")
    A("")

    A("## 4. Early-warning watchlist (be first to know)")
    A("")
    for name, url, why in EARLY_WARNING_WATCHLIST:
        A(f"- **{name}** <{url}> - {why}")
    A("")

    A("## 5. Counter-action playbook by category")
    A("")
    for cat, actions in CATEGORY_PLAYBOOK.items():
        A(f"### {cat}")
        for a in actions:
            A(f"- {a}")
        A("")

    body = "\n".join(L)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write(body)
    print(body)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="AI incident morning briefing")
    ap.add_argument("--days", type=int, default=14)
    args = ap.parse_args()
    render(args.days, args.days)
