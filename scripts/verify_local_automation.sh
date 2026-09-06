#!/usr/bin/env bash
# Verify local-first automation health (disk vault, not origin/main).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TODAY="$(date +%Y-%m-%d)"
CRON_DIR="$ROOT/logs/scheduler-cron"
RUN_LOG="$ROOT/logs/launchd-runs.log"
DIGEST="$ROOT/vault/Daily Digests/${TODAY}.md"

echo "=== JobScoutOS local automation verification ==="
echo "Date: $TODAY"
echo

if [[ -d "$CRON_DIR" ]]; then
  echo "--- scheduler-cron markers ---"
  for f in "$CRON_DIR"/*.last-success; do
    [[ -f "$f" ]] || continue
    echo "$(basename "$f"): $(tr -d '\n' < "$f")"
  done
else
  echo "WARN: $CRON_DIR not found (no scheduled runs yet)"
fi

echo
if [[ -f "$DIGEST" ]]; then
  echo "OK: today's digest on disk — $DIGEST"
else
  echo "MISSING: $DIGEST"
fi

echo
if [[ -f "$RUN_LOG" ]]; then
  echo "--- last 10 run log lines ---"
  tail -10 "$RUN_LOG"
else
  echo "WARN: $RUN_LOG not found"
fi

echo
if [[ -f "$DIGEST" ]]; then
  exit 0
fi
exit 1
