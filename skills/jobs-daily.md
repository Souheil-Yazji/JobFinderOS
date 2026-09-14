**Agent:** `coach`
**Execution:** orchestrated

Read `agents/coach.md` and `docs/jobfinderos-instructions.md` first.

## Task
The runtime orchestrates separate agent sessions in order: Mark `mark-pulse`, Scout `jobs-scout`, Coach `jobs-email`, Coach `jobs-digest`, then Coach `jobs-daily-finalize`. Coach owns the closing read only. Do not simulate all personas in one session. The runtime must dispatch this task; use `scripts/JobFinderOS_run_agent.sh coach jobs-daily`.

Preserve the dated Daily Jobs Watch archive, pipeline state, and one final run record. Every step honors profile filters and doctrine. No outreach drafting without candidate consent.
