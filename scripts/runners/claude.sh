#!/usr/bin/env bash
# Optional Claude adapter using the same canonical prompt and completion contract.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
BIN="${CLAUDE_BIN:-$(command -v claude || true)}"
[[ -n "$BIN" && -x "$BIN" ]] || { echo 'Claude CLI missing; set CLAUDE_BIN.' >&2; exit 127; }
prompt="$(cat)"
if [[ "${JOBFINDEROS_INTERACTIVE:-0}" == 1 ]]; then
  exec "$BIN" "$prompt" < /dev/tty
fi
# Keep the CLI's normal permission checks. No permission/sandbox bypass.
"$BIN" -p "$prompt" > "${JOBFINDEROS_RESULT_FILE:?runner must supply result path}" < /dev/null
cat "$JOBFINDEROS_RESULT_FILE"
