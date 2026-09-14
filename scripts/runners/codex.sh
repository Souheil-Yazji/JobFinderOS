#!/usr/bin/env bash
# Adapter receives the prompt on stdin; orchestration/logging belong to the runner.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
BIN="${CODEX_BIN:-$(command -v codex || true)}"
[[ -n "$BIN" && -x "$BIN" ]] || { echo 'Codex CLI missing; set CODEX_BIN.' >&2; exit 127; }
opts=(-C "$ROOT" -c 'web_search="live"' -c 'sandbox_workspace_write.network_access=true')
[[ -z "${JOBFINDEROS_CODEX_MODEL:-}" ]] || opts+=(-m "$JOBFINDEROS_CODEX_MODEL")
if [[ "${JOBFINDEROS_INTERACTIVE:-0}" == 1 ]]; then
  prompt="$(cat)"
  exec "$BIN" "${opts[@]}" --sandbox workspace-write "$prompt" < /dev/tty
fi
exec "$BIN" exec "${opts[@]}" -c 'approval_policy="never"' --sandbox workspace-write --ephemeral --json \
  --output-schema "$ROOT/config/agent_result.schema.json" \
  --output-last-message "${JOBFINDEROS_RESULT_FILE:?runner must supply result path}" -
