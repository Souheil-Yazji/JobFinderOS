#!/usr/bin/env bash
# Record a launchd run event to logs/launchd-runs.log and mirror to the vault when allowed.
# Usage: JobScoutOS_log_run.sh <label> <phase>
#   label: jobs-daily | mark-weekly
#   phase: start | completed | failed (exit N) | any short description
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LABEL="${1:-unknown}"
PHASE="${2:-event}"
LOG="$ROOT/logs/launchd-runs.log"
VAULT="$ROOT/vault/Automation/JobScoutOS — Schedule & Run Log.md"
mkdir -p "$ROOT/logs"
LINE="- $(date '+%Y-%m-%d %H:%M:%S %Z') — ${LABEL} — ${PHASE}"
echo "$LINE" >>"$LOG"
# Vault mirror (may fail under TCC when the repo lives under ~/Documents and launchd runs in background)
if ! echo "$LINE" >>"$VAULT" 2>/dev/null; then
  :
fi
