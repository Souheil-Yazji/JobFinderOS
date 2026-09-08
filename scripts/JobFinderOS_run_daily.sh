#!/usr/bin/env bash
# Full Jobs daily routine via local Claude Code skill (scout + email + digest).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$ROOT/scripts/JobFinderOS_run_skill.sh" jobs-daily jobs-daily
