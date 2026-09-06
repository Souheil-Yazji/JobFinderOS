#!/usr/bin/env bash
# Install the optional launchd helpers from scripts/launchd/*.plist.template:
#   com.jobscoutos.latest  — rewrites the dated pointer notes at the vault root (WatchPaths)
#   com.jobscoutos.prune   — weekly retention sweep of digests/pulses/watches
#   com.jobscoutos.atspoll — deterministic direct-ATS poller (needs config/ats_boards.yaml)
# Usage: bash scripts/JobScoutOS_install_helpers.sh [latest|prune|atspoll ...]   (default: all three)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${JOBSCOUTOS_PYTHON:-$ROOT/.venv/bin/python}"
[[ -x "$PY" ]] || PY="$(command -v python3)"
STATE_DIR="${HOME}/.jobscoutos"
AGENT_DIR="${HOME}/Library/LaunchAgents"
mkdir -p "$STATE_DIR/logs" "$AGENT_DIR"
DOMAIN="gui/$(id -u)"

jobs=("$@"); [[ ${#jobs[@]} -eq 0 ]] && jobs=(latest prune atspoll)
for j in "${jobs[@]}"; do
  tpl="$ROOT/scripts/launchd/com.jobscoutos.$j.plist.template"
  [[ -f "$tpl" ]] || { echo "no template for $j" >&2; exit 2; }
  out="$AGENT_DIR/com.jobscoutos.$j.plist"
  sed -e "s|__PYTHON__|$PY|g" -e "s|__REPO__|$ROOT|g" -e "s|__STATE_DIR__|$STATE_DIR|g" "$tpl" > "$out"
  launchctl bootout "$DOMAIN" "$out" 2>/dev/null || true
  launchctl bootstrap "$DOMAIN" "$out"
  echo "installed com.jobscoutos.$j → $out"
done
echo "State/logs: $STATE_DIR   (to remove: launchctl bootout $DOMAIN/com.jobscoutos.<name>; rm the plist)"
