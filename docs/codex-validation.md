# Codex migration validation

Validation date: 2026-09-14. The port retains all original `.claude/` definitions and `CLAUDE.md`. Model parity with the original Claude implementation has not been established, so compatibility removal is intentionally deferred.

## Automated regression

```bash
.venv/bin/python -m unittest discover -s tests -v
bash scripts/verify_local_automation.sh --static
python3 scripts/scheduler_tick.py --dry-run  # activate .venv first
bash scripts/JobFinderOS_check_local_runner.sh
```

The suite uses fictional fixtures and mocked CLI/HTTP boundaries; it never executes real job-search models or connects to an inbox. It covers:

- All 26 canonical tasks, ownership and execution modes, and private-path ignore rules with tracked vault exceptions.
- Invalid names, mismatched personas, missing CLI, literal arguments and repository working directory, blocked/malformed results, timeout logging and overlapping-run exclusion.
- Separate daily child processes in the required order, failure at every child, one final record, and Mark research before Coach prep when a company profile is absent.
- Output auditing: Scout cannot draft outreach; Mark cannot change application stages; records include ignored-style vault outputs.
- Weekly precedence, success-only scheduler state, catch-up and ISO-year boundaries, explicit routing, and scheduler dry-run without locks/logs/jobs.
- Priority-watch success markers, duplicate suppression and failure without a success marker.
- Three ATS parsers, compensation gates, local inbox/seen-state writes without Git, 30/90-day retention with newest/durable-note preservation, and idempotent pointer generation.

Static verification and scheduler dry-run pass on a fresh checkout with dependencies installed. Codex preflight passed using saved ChatGPT authentication. The default operational verifier requires today's digest: it correctly fails in the user's uninitialized checkout and passes in the generated fictional vault. No fake digest was added to the user's vault to satisfy that check. No launch agents were installed or kickstarted.

## Real Codex persona smoke runs

Four separate real Codex invocations used an isolated temporary repository, a synthetic candidate, and supplied offline primary-source snapshots. No real inbox, candidate data, or external research was used. CLI version: `0.154.0-alpha.6.2`. Each invocation returned `status: complete`, exit zero, and zero audited boundary violations.

| Task | Observed result | Boundary evidence |
|---|---|---|
| Scout `jobs-scout` | Processed five supplied roles; created the eligible Acme Widgets manager opportunity at 8/10 and a scan archive | Excluded employer, IC, onsite and below-floor roles did not become opportunities; no outreach |
| Mark `mark-pulse` | Wrote synthetic brief, supported expansion signal, handoff JSON and Dashboard recommendation | Existing opportunity stage unchanged; no outreach |
| Coach `jobs-digest` | Wrote the dated synthetic digest and updated Dashboard/archive | Strategy and opportunity stage unchanged; supplied empty email fixture explicitly distinguished from a real inbox |
| Coach `jobs-prep` | Wrote a Screen prep note and linked it from the company profile | Used the fictional story's exact facts; flagged gaps; stage stayed Spotted; no outreach |

Each run produced its own private transcript, completion result and audit record. The read-only artifact validator confirmed one qualifying opportunity, score 8/10, unchanged Spotted stage, no outreach files, market handoff, synthetic digest and Screen prep. These runs validate bounded persona behavior; they do not establish live-web or live-email parity. They exercised the standalone runner revision before scheduler integration; subprocess tests separately validate the integrated daily sequence.

## Reproduce the bounded smoke test

The optional harness builds a new temporary repository from **committed HEAD**, then fills private configuration from `tests/fixtures/fictional/`. It never copies uncommitted candidate state. Commit/merge the fixture files before using it. Preparation alone executes no model:

```bash
.venv/bin/python tests/live_smoke.py
```

Real CLI execution uses the selected runtime's existing authentication and consumes that account's usage:

```bash
.venv/bin/python tests/live_smoke.py --runtime codex --execute
.venv/bin/python tests/live_smoke.py --runtime claude --execute
```

The harness prints the temporary repository path and leaves logs there for inspection. To re-check an existing result without executing a model:

```bash
.venv/bin/python tests/live_smoke.py --validate /path/to/fictional-repository
```

Run the two runtimes from the same committed source with identical fixtures, then compare role filtering/scores, stage preservation, filenames, handoffs and Recruiter's reads. This comparison is a future gate; the Claude CLI was not installed in the validation environment. Original Claude slash-command behavior also needs comparison before retiring those definitions.

## Remaining operational and compatibility gates

- Configure and verify a read-only Gmail connector in the selected Codex environment. The port does not transfer claude.ai connectors or infer an unavailable inbox is empty. Default daily fails closed on an incomplete required email pass.
- Run a real complete daily workflow with that connector, and verify its final manifest and scheduler success marker. Automated tests exercise process ordering and failure handling; no live inbox-dependent daily was executed.
- Test real company/ATS research availability in the deployment environment; supplied snapshots deliberately avoid network variability.
- Compare representative Claude and Codex outputs, including weekly Strategy behavior, before changing or deleting `.claude/` compatibility.
- Install launchd only when ready to operate the port. Runtime selection and binary paths are captured by the installer. The inherited timezone distinction remains: master daily/weekly use system-local time; the priority guard uses configured timezone.

Job-search data remains file-backed. Root Dashboard/Strategy, tracking skeletons and automation notes are still tracked exceptions to the vault ignore rule; review staged paths before publishing any future changes to them. Output audits detect prohibited file changes after execution and retain them for review; they are not a tool-level authorization boundary.
