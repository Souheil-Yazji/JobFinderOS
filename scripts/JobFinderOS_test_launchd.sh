#!/usr/bin/env bash
# Manually trigger JobFinderOS launchd scheduler and show recent log output.
# Usage: bash scripts/JobFinderOS_test_launchd.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOMAIN="gui/$(id -u)"
LABEL="com.jobfinderos.scheduler"

echo "JobFinderOS launchd test — $(date)"
echo "ROOT=$ROOT"
echo ""

echo "→ kickstart $LABEL"
launchctl kickstart -k "$DOMAIN/$LABEL" 2>&1 || true

sleep 2

log="$ROOT/logs/launchd-${LABEL}.log"
err="$ROOT/logs/launchd-${LABEL}.err"
echo ""
echo "=== $LABEL stderr (last 20 lines) ==="
if [[ -f "$err" ]]; then tail -20 "$err"; else echo "(no err file)"; fi
echo ""
echo "=== $LABEL stdout (last 15 lines) ==="
if [[ -f "$log" ]]; then tail -15 "$log"; else echo "(no log file)"; fi

echo ""
RUNS="$ROOT/logs/launchd-runs.log"
echo "=== launchd-runs.log (last 20 lines) ==="
if [[ -f "$RUNS" ]]; then tail -20 "$RUNS"; else echo "(no file yet — runs after next tick)"; fi
echo ""

LEGACY_ERR="$ROOT/logs/launchd-com.jobfinderos.jobs-daily.err"
if [[ -f "$LEGACY_ERR" ]] && grep -q "Operation not permitted" "$LEGACY_ERR" 2>/dev/null; then
  echo "NOTE: legacy 'Operation not permitted' in jobs-daily.err — old agent; current scheduler is ${LABEL}."
fi
