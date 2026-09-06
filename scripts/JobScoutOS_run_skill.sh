#!/usr/bin/env bash
# Run a Claude Code skill locally (subscription auth). Writes to local vault/ only.
# Usage: JobScoutOS_run_skill.sh <log-label> <skill-name>
# Example: JobScoutOS_run_skill.sh jobs-daily jobs-daily
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p "$ROOT/logs"

LABEL="${1:?log label required (e.g. jobs-daily)}"
SKILL="${2:?skill name required (e.g. jobs-daily)}"
CMD_FILE="$ROOT/.claude/commands/${SKILL}.md"
if [[ ! -f "$CMD_FILE" ]]; then
  echo "JobScoutOS_run_skill: missing skill file: $CMD_FILE" >&2
  exit 2
fi

CLAUDE_BIN="${CLAUDE_BIN:-$(command -v claude || true)}"
if [[ -z "$CLAUDE_BIN" || ! -x "$CLAUDE_BIN" ]]; then
  echo "JobScoutOS_run_skill: claude CLI not found (set CLAUDE_BIN)" >&2
  exit 127
fi

TIMEOUT_SEC="${JOBSCOUTOS_SKILL_TIMEOUT_SEC:-1800}"
ALLOWED_TOOLS="${JOBSCOUTOS_SKILL_ALLOWED_TOOLS:-Agent,Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch}"

export PATH="${HOME}/.local/bin:${PATH}"

"$ROOT/scripts/JobScoutOS_log_run.sh" "$LABEL" start
set +e
if command -v timeout >/dev/null 2>&1; then
  timeout "$TIMEOUT_SEC" "$CLAUDE_BIN" -p "/${SKILL}" \
    --allowedTools "$ALLOWED_TOOLS" \
    --dangerously-skip-permissions \
    < /dev/null
  ec=$?
  if [[ "$ec" -eq 124 ]]; then
    "$ROOT/scripts/JobScoutOS_log_run.sh" "$LABEL" "failed (timeout ${TIMEOUT_SEC}s)"
    exit "$ec"
  fi
else
  "$CLAUDE_BIN" -p "/${SKILL}" \
    --allowedTools "$ALLOWED_TOOLS" \
    --dangerously-skip-permissions \
    < /dev/null
  ec=$?
fi
set -e

if [[ "$ec" -eq 0 ]]; then
  "$ROOT/scripts/JobScoutOS_log_run.sh" "$LABEL" completed
  PY="${ROOT}/.venv/bin/python"
  [[ -x "$PY" ]] || PY=python3
  # Repair any literal-backslash vault paths a skill run may have written
  "$PY" "$ROOT/scripts/jobscoutos_fix_backslash_paths.py" || true
else
  "$ROOT/scripts/JobScoutOS_log_run.sh" "$LABEL" "failed (exit $ec)"
  exit "$ec"
fi
