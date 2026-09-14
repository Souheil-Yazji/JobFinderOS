#!/usr/bin/env bash
# Compatibility interface: <log-label> <skill> [runner options] [-- arguments...]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LABEL="${1:?log label required}"
SKILL="${2:?skill required}"
shift 2
exec "$ROOT/scripts/JobFinderOS_run_agent.sh" auto "$SKILL" --label "$LABEL" "$@"
