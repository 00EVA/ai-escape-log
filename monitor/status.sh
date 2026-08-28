#!/bin/bash
# status.sh - at-a-glance health of the 2-hour pipeline:
#   probe :00 -> ingest :15 -> publish :30 (even hours UTC-local)
# Usage: bash monitor/status.sh
set -u
cd "$(dirname "$0")/.." || exit 1
LOG="$HOME/Library/Logs/ai_escape_monitor.log"
NOW=$(date +%s)

last_run() {  # $1 = log marker; lines look like "[YYYY-MM-DD HH:MM:SS] [marker] ..."
    grep -aE "^\[?[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\]? .*$1" "$LOG" 2>/dev/null | tail -1
}

age_min() {   # $1 = "YYYY-MM-DD HH:MM:SS"
    [ -z "$1" ] && { echo "?"; return; }
    echo $(( (NOW - $(date -j -f "%Y-%m-%d %H:%M:%S" "$1" +%s 2>/dev/null) ) / 60 ))
}

echo "=== AI Escape Log pipeline status  ($(date '+%F %T')) ==="

echo "--- schedule (crontab) ---"
(crontab -l < /dev/null 2>/dev/null | grep AIincidents) || echo "  (crontab read failed - entries may still exist)"

echo "--- last runs ---"
for stage in "news_probe" "ingest" "auto_publish"; do
    line=$(last_run "\[$stage\]")
    ts=$(echo "$line" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}' | head -1)
    mins=$(age_min "$ts")
    printf "  %-15s %s  (%s min ago)\n" "[$stage]" "${ts:-NEVER}" "${mins:-?}"
done

echo "--- publish agent (launchd) ---"
launchctl print gui/$(id -u)/com.tony.aiincidents.autopublish 2>/dev/null | grep -m1 "state =" | sed 's/^/  /' || echo "  NOT LOADED"

echo "--- last push to GitHub ---"
git log origin/main --format='  %h %ad %s' --date=format:'%F %H:%M' -1

echo "--- queue ---"
python3 -c "
import json
c=json.load(open('data/candidates.json'))
print(f'  candidates queued: {len(c)}')" 2>/dev/null

echo "--- source warnings (last probe run) ---"
tail -40 "$LOG" | grep -a "\[warn\]" | tail -3 || true
