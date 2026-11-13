#!/usr/bin/env python3
"""Weekly digest for AI Escape Log — appends a "## Week of YYYY-MM-DD" section
to DIGEST.md summarizing: new incidents, candidates by source, hot signals,
queue/archive sizes. Idempotent: re-running for the same week replaces that
week's section instead of duplicating it. Committed by auto_publish.sh.
"""
import datetime
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIGEST = os.path.join(ROOT, "DIGEST.md")
HOTLIST = os.path.join(ROOT, "HOTLIST.md")


def load(path, key=None):
    try:
        d = json.load(open(path))
    except (OSError, ValueError):
        return []
    return d if isinstance(d, list) else d.get(key or "candidates", [])


def parse_date(s):
    """Candidate dates are messy ('2026-10-08', 'Wed, 28 Oc'). Best effort."""
    if not s:
        return None
    m = re.match(r"(\d{4}-\d{2}-\d{2})", str(s))
    if m:
        try:
            return datetime.date.fromisoformat(m.group(1))
        except ValueError:
            return None
    import email.utils
    try:
        return email.utils.parsedate_to_datetime(str(s)).date()
    except (TypeError, ValueError):
        return None


def main():
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())  # Monday
    heading = f"## Week of {week_start.isoformat()}"

    if os.path.exists(DIGEST):
        existing = open(DIGEST).read()
        if heading in existing:  # already written this week — replace below
            existing = re.sub(re.escape(heading) + r"\n.*?(?=\n## |\Z)",
                              "", existing, flags=re.S).rstrip() + "\n\n"
        else:
            existing = existing.rstrip() + "\n\n"
    else:
        existing = "# AI Escape Log — Weekly Digest\n\n"

    incs = load(os.path.join(ROOT, "data", "incidents.json"), "incidents")
    cands = load(os.path.join(ROOT, "data", "candidates.json"))
    archive = load(os.path.join(ROOT, "data", "ingested_archive.json"))

    new_incidents = [i for i in incs
                     if (d := parse_date(i.get("date"))) and week_start <= d <= today]
    fresh = [c for c in cands if (d := parse_date(c.get("date"))) and d >= week_start]
    by_source = {}
    for c in fresh:
        by_source[c.get("source", "?")] = by_source.get(c.get("source", "?"), 0) + 1

    hot = []
    if os.path.exists(HOTLIST):
        for block in open(HOTLIST).read().split("\n## ")[1:]:
            lines = block.strip().splitlines()
            if not lines:
                continue
            try:
                ts = datetime.datetime.strptime(lines[0].strip(), "%F %T")
            except ValueError:
                continue
            if ts.date() >= week_start:
                hot += [l.strip() for l in lines[1:] if l.strip().startswith("- [")]

    lines = [heading,
             f"- New verified incidents: {len(new_incidents)}"
             + (f" ({', '.join(i.get('id', '?') for i in new_incidents)})"
                if new_incidents else ""),
             f"- Queue: {len(cands)} live candidates ({len(fresh)} added this week)"
             f" | Archive: {len(archive)}",
             f"- Hot signals this week: {len(hot)}"]
    for src, n in sorted(by_source.items(), key=lambda kv: -kv[1])[:5]:
        lines.append(f"  - {src}: {n}")
    for h in hot[:5]:
        lines.append(f"  - {h}")
    lines.append(f"- _Generated {datetime.datetime.now():%Y-%m-%d %H:%M %Z}_")

    with open(DIGEST, "w") as f:
        f.write(existing + "\n".join(lines) + "\n")
    print(f"[digest] wrote week of {week_start.isoformat()}: "
          f"{len(new_incidents)} incidents, {len(fresh)} fresh candidates, {len(hot)} hot")


if __name__ == "__main__":
    main()
