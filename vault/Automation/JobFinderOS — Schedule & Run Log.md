> **JobFinderOS:** system

# JobFinderOS automation

The canonical runner defaults to Codex; `JOBFINDEROS_RUNTIME=claude` selects the optional adapter. Daily runs five separate persona/task sessions and records one final outcome.

Run `bash scripts/JobFinderOS_install_launchd.sh` to (re)generate this header and install the scheduler.

## Run log

Each scheduled run appends **start** / **completed** / **failed** lines to `logs/launchd-runs.log` in the project root (gitignored). The same lines are mirrored below when macOS allows background jobs to write here.

_Newest entries at the bottom._
