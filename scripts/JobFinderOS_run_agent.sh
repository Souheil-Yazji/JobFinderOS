#!/usr/bin/env bash
# Canonical interface: <agent> <skill> [--dry-run] [--interactive] [-- arguments...]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${JOBFINDEROS_PYTHON:-$ROOT/.venv/bin/python}"
[[ -x "$PY" ]] || PY=python3
exec "$PY" "$ROOT/scripts/jobfinderos_agent_runner.py" "$@"
