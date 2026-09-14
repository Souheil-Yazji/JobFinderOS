#!/usr/bin/env bash
# Preflight the selected local runtime and canonical scheduled tasks.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
runtime="${JOBFINDEROS_RUNTIME:-codex}"
case "$runtime" in
  codex) bin="${CODEX_BIN:-$(command -v codex || true)}" ;;
  claude) bin="${CLAUDE_BIN:-$(command -v claude || true)}" ;;
  *) echo "Unsupported runtime: $runtime" >&2; exit 2 ;;
esac
[[ -n "$bin" && -x "$bin" ]] || { echo "Missing $runtime CLI" >&2; exit 127; }
"$bin" --version
for skill in jobs-daily mark-weekly jobs-priority-watch; do
  "$ROOT/scripts/JobFinderOS_run_agent.sh" auto "$skill" --dry-run
 done
[[ -d "$ROOT/vault" ]] || { echo 'Missing vault'; exit 1; }
if [[ "$runtime" == codex ]]; then
  "$bin" login status
else
  "$bin" auth status
fi
echo "Runtime preflight passed. Web and Coach read-only email access must be validated in the selected runtime."
