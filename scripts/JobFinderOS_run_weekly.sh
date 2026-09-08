#!/usr/bin/env bash
# Weekly Mark brief via local Claude Code skill.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$ROOT/scripts/JobFinderOS_run_skill.sh" mark-weekly mark-weekly
