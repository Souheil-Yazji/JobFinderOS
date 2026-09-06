# JobScoutOS — Local Runbook

> **JobScoutOS:** system · local-first automation (macOS launchd + Claude Code CLI)

Scheduled work runs **on your Mac**, writes directly to **`vault/`** on disk (Obsidian). No cloud routines, no API keys, no `git push` required for automation to work.

---

## Architecture

```
launchd (com.jobscoutos.scheduler)
  → scheduler_tick.py (every ~30 min while awake)
    → JobScoutOS_run_skill.sh (daily / weekly when due)
    → jobscoutos_priority_watch.py (each tick)
      → claude -p /skill → vault/
```

Logs: `logs/launchd-runs.log`, `logs/scheduler-cron/*.last-success`, mirror in [[JobScoutOS — Schedule & Run Log]] when allowed.

## Scheduled jobs

| Job | Entrypoint | Skill | Window (timezone in `config/scheduler.yaml`) |
|-----|------------|-------|----------------------------------------------|
| Daily Jobs | `scheduler_tick` → `JobScoutOS_run_skill.sh` | `/jobs-daily` | After `daily.hour` (default 7:00) |
| Weekly Mark | `scheduler_tick` → `JobScoutOS_run_skill.sh` | `/mark-weekly` | `weekly.weekday` after `weekly.hour` (default Monday 8:00). Weekly wins: daily is skipped that day |
| Priority watch | `jobscoutos_priority_watch.py` each tick | `/jobs-priority-watch` | Weekdays after `watch.hour` (default 9:00) |

Install or refresh:

```bash
bash scripts/JobScoutOS_install_launchd.sh
JOBS_DAILY_HOUR=7 MARK_WEEKLY_WEEKDAY=1 WATCH_HOUR=9 JOBSCOUTOS_TZ=America/New_York bash scripts/JobScoutOS_install_launchd.sh
```

## Optional helpers

`bash scripts/JobScoutOS_install_helpers.sh [latest|prune|atspoll]` renders `scripts/launchd/*.plist.template` and installs:

| Label | What | Cadence |
|-------|------|---------|
| `com.jobscoutos.latest` | `jobscoutos_update_latest.py`: rewrites the dated pointer notes at the vault root | On any write to the digest folders |
| `com.jobscoutos.prune` | `jobscoutos_prune_history.py`: 30-day retention for digests/pulses/watches, 90 for weekly briefs | Weekly |
| `com.jobscoutos.atspoll` | `jobscoutos_ats_poll.py`: deterministic direct-ATS sweep → `Market Intel/ATS Inbox.md` | Per the template's calendar interval |

The poller needs `config/ats_boards.yaml` (copy the example, edit `filters:`, run `--seed` once). Its stdout/stderr go to `~/.jobscoutos/logs/`, not the repo, because launchd cannot write under `~/Documents` without Full Disk Access.

## Prerequisites

1. Claude Code CLI on PATH and logged in (`claude auth login`)
2. Gmail MCP connected in claude.ai (for the email pass; everything else works without it)
3. The Mac awake during the windows
4. PyYAML in the project venv (`pip install -r requirements.txt`)

## Manual commands

```bash
bash scripts/JobScoutOS_check_local_runner.sh
bash scripts/JobScoutOS_run_skill.sh jobs-daily jobs-daily
python3 scripts/scheduler_tick.py --dry-run
python3 scripts/scheduler_tick.py
bash scripts/verify_local_automation.sh
bash scripts/JobScoutOS_test_launchd.sh
python3 scripts/jobscoutos_priority_watch.py     # standalone guard; JSON on stdout
python3 scripts/jobscoutos_ats_poll.py --dry-run
```

## Failure triage

| Symptom | Check |
|---------|-------|
| No digest on disk | `tail logs/launchd-runs.log`; run the skill manually |
| `claude: command not found` | Install Claude Code CLI; set `CLAUDE_BIN` |
| Auth errors | `claude auth login` |
| Guard always `skip` | Window not reached, weekend, or marker already set; see the JSON `reason` |
| Stuck lock | Remove `logs/scheduler-cron/*.lock` if no claude process is running |
| launchd `Operation not permitted` | The repo is under `~/Documents`/`Desktop`/`Downloads`. Move it (e.g. `~/Developer/`) or grant Full Disk Access to the venv Python |
| Session limit from the CLI | Wait for the reset; the tick logs `failed (exit 1)` without updating markers |

## Backup (optional, by hand)

Automation never commits or pushes. The vault is gitignored in this repo. If you want it backed up, keep it in a **private** repository of your own.
