#!/bin/bash
# Auto-publish: rebuild derived data and push to GitHub Pages if anything changed.
# Runs daily via cron. Does NOT verify or log new incidents (that stays manual -
# the anti-misinformation gate needs judgment); it only publishes what is already
# in data/incidents.json plus the latest candidate queue.
set -u
# Location-independent: works locally AND in GitHub Actions CI
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1
LOG="${AI_ESCAPE_LOG:-/Users/tony/Library/Logs/ai_escape_monitor.log}"
mkdir -p "$(dirname "$LOG")" 2>/dev/null || LOG=/tmp/ai_escape_monitor.log
{
  echo "[$(date '+%F %T')] [auto_publish] start"
  git pull --ff-only origin main >/dev/null 2>&1 || echo "[auto_publish] pull skipped/failed (continuing)"
  python3 build_csv.py || exit 1
  python3 db.py || exit 1
  python3 monitor/incident_report.py || exit 1
  python3 monitor/build_feed.py || exit 1
  # git add fails fatally on a missing pathspec and stalls on gitignored files,
  # so stage only files that actually exist (spotlight/human_decisions are
  # optional review.html exports; feed.xml/link_health.json come from Lane D).
  for f in data/incidents.json data/incidents.csv data/candidates.json \
           data/ingested_archive.json data/spotlight.json data/human_decisions.json \
           REPORT.md seen_urls.json HOTLIST.md feed.xml DIGEST.md \
           data/link_health.json; do
    [ -f "$f" ] && git add -- "$f"
  done
  if git diff --cached --quiet; then
    echo "[auto_publish] no changes to publish"
  else
    git commit -m "auto-publish: refresh derived data + candidate queue [cron]" >/dev/null
    pushed=0
    for attempt in 1 2 3; do
      if git push origin main >/dev/null 2>&1; then pushed=1; break; fi
      sleep 5
    done
    if [ "$pushed" -eq 1 ]; then
      echo "[auto_publish] pushed to origin/main (Pages will rebuild)"
    else
      echo "[auto_publish] push FAILED (after 3 attempts)"
    fi
  fi
  echo "[auto_publish] done"
} >> "$LOG" 2>&1
