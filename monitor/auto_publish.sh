#!/bin/bash
# Auto-publish: rebuild derived data and push to GitHub Pages if anything changed.
# Runs daily via cron. Does NOT verify or log new incidents (that stays manual -
# the anti-misinformation gate needs judgment); it only publishes what is already
# in data/incidents.json plus the latest candidate queue.
set -u
cd /Users/tony/AIincidents || exit 1
LOG=/Users/tony/Library/Logs/ai_escape_monitor.log
{
  echo "[$(date '+%F %T')] [auto_publish] start"
  git pull --ff-only origin main >/dev/null 2>&1 || echo "[auto_publish] pull skipped/failed (continuing)"
  python3 build_csv.py || exit 1
  python3 db.py || exit 1
  python3 monitor/incident_report.py || exit 1
  git add data/incidents.json data/incidents.csv data/incidents.db data/candidates.json REPORT.md seen_urls.json 2>/dev/null
  if git diff --cached --quiet; then
    echo "[auto_publish] no changes to publish"
  else
    git commit -m "auto-publish: refresh derived data + candidate queue [cron]" >/dev/null
    if git push origin main >/dev/null 2>&1; then
      echo "[auto_publish] pushed to origin/main (Pages will rebuild)"
    else
      echo "[auto_publish] push FAILED"
    fi
  fi
  echo "[auto_publish] done"
} >> "$LOG" 2>&1
