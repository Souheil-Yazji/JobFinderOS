# JobFinderOS — Local Runbook

> **JobFinderOS:** system · local-first automation (macOS launchd + Codex CLI; optional Claude adapter)

Scheduled work runs **on your Mac**, writes directly to **`vault/`** on disk (Obsidian). No cloud routines, no API keys, no `git push` required for automation to work.

---

## Architecture

```
launchd (com.jobfinderos.scheduler)
  → scheduler_tick.py (every ~30 min while awake)
    → JobFinderOS_run_agent.sh (explicit persona/task when due)
    → jobfinderos_priority_watch.py (each tick)
      → selected CLI → vault/
```

Logs: `logs/launchd-runs.log`, `logs/scheduler-cron/*.last-success`, mirror in [[JobFinderOS — Schedule & Run Log]] when allowed.

## Scheduled jobs

| Job | Entrypoint | Skill | Window (timezone in `config/scheduler.yaml`) |
|-----|------------|-------|----------------------------------------------|
| Daily Jobs | `scheduler_tick` → `JobFinderOS_run_agent.sh` | `/jobs-daily` | After `daily.hour` (default 7:00) |
| Weekly Mark | `scheduler_tick` → `JobFinderOS_run_agent.sh` | `/mark-weekly` | `weekly.weekday` after `weekly.hour` (default Monday 8:00). Weekly wins: daily is skipped that day |
| Priority watch | `jobfinderos_priority_watch.py` each tick | `/jobs-priority-watch` | Weekdays after `watch.hour` (default 9:00) |

Install or refresh:

```bash
bash scripts/JobFinderOS_install_launchd.sh
JOBS_DAILY_HOUR=7 MARK_WEEKLY_WEEKDAY=1 WATCH_HOUR=9 JOBFINDEROS_TZ=America/New_York bash scripts/JobFinderOS_install_launchd.sh
```

## Optional helpers

`bash scripts/JobFinderOS_install_helpers.sh [latest|prune|atspoll]` renders `scripts/launchd/*.plist.template` and installs:

| Label | What | Cadence |
|-------|------|---------|
| `com.jobfinderos.latest` | `jobfinderos_update_latest.py`: rewrites the dated pointer notes at the vault root | On any write to the digest folders |
| `com.jobfinderos.prune` | `jobfinderos_prune_history.py`: 30-day retention for digests/pulses/watches, 90 for weekly briefs | Weekly |
| `com.jobfinderos.atspoll` | `jobfinderos_ats_poll.py`: deterministic direct-ATS sweep → `Market Intel/ATS Inbox.md` | Per the template's calendar interval |

The poller needs `config/ats_boards.yaml` (copy the example, edit `filters:`, run `--seed` once). Its stdout/stderr go to `~/.jobfinderos/logs/`, not the repo, because launchd cannot write under `~/Documents` without Full Disk Access.

## Prerequisites

1. Codex CLI on PATH and logged in (`codex login`), or `JOBFINDEROS_RUNTIME=claude` for the optional adapter
2. A Gmail read connector configured in the selected runtime for email tasks. Without it, the required email pass reports blocked and daily does not record success.
3. The Mac awake during the windows
4. PyYAML in the project venv (`pip install -r requirements.txt`)

## Manual commands

```bash
bash scripts/JobFinderOS_check_local_runner.sh
bash scripts/JobFinderOS_run_skill.sh jobs-daily jobs-daily
python3 scripts/scheduler_tick.py --dry-run
python3 scripts/scheduler_tick.py
bash scripts/verify_local_automation.sh
bash scripts/JobFinderOS_test_launchd.sh
python3 scripts/jobfinderos_priority_watch.py     # standalone guard; JSON on stdout
python3 scripts/jobfinderos_ats_poll.py --dry-run
```

## Failure triage

| Symptom | Check |
|---------|-------|
| No digest on disk | `tail logs/launchd-runs.log`; run the skill manually |
| CLI missing | Install the selected CLI; set `CODEX_BIN` or `CLAUDE_BIN` |
| Auth errors | `codex login` (or `claude auth login`) |
| Guard always `skip` | Window not reached, weekend, or marker already set; see the JSON `reason` |
| Stuck lock | Remove `logs/scheduler-cron/*.lock` only after confirming no agent process is running |
| launchd `Operation not permitted` | The repo is under `~/Documents`/`Desktop`/`Downloads`. Move it (e.g. `~/Developer/`) or grant Full Disk Access to the venv Python |
| Session limit from the CLI | Wait for the reset; the tick logs `failed (exit 1)` without updating markers |

## Backup (optional, by hand)

Automation never commits or pushes. The vault is gitignored in this repo. If you want it backed up, keep it in a **private** repository of your own.

## Canonical runtime

```bash
./scripts/JobFinderOS_run_agent.sh scout jobs-scout --dry-run
./scripts/JobFinderOS_run_agent.sh coach jobs-daily
./scripts/JobFinderOS_run_agent.sh coach jobs-prep -- "Acme" "Widget Lead" "Screen"
bash scripts/verify_local_automation.sh --static
```

Daily runs separate Mark pulse, Scout scan, Coach email, Coach digest and Coach
finalization processes in sequence. They share a manifest under
`logs/daily-runs/<id>/run.json`; each invocation writes results and audit metadata
under `logs/agent-runs/<id>/`. There is one final daily lifecycle record. Any failed
or blocked child stops the remaining sequence and preserves the scheduler's
previous success state. Candidate replies/drafts are never inferred from silence.

The installer captures `JOBFINDEROS_RUNTIME`, `CODEX_BIN` and `CLAUDE_BIN` into its
launcher and adds common CLI locations to PATH. Re-run installation after changing
runtime selection. Installation is a separate operational action; testing does
not install or kickstart launchd. Original `.claude/` commands remain intact.

Static verification needs no private profile or CLI invocation. Operational
verification still requires today's digest and can fail on a fresh checkout or a
weekly-only day. Scheduler dry-run is read-only. The existing timezone distinction
is retained: master daily/weekly use system-local time, while the priority guard
uses the configured timezone. Optional helpers retain their existing triggers.
