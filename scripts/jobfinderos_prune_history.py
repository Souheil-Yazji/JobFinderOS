#!/usr/bin/env python3
"""
JobFinderOS - vault history retention pruner.
================================================================================
Deletes historical vault notes past their retention window to keep search
results current. Backups are managed separately by the candidate; ignored
notes are not recoverable from Git unless explicitly backed up beforehand.

Policy:
  30 days : Daily Digests/, Archive/Daily Jobs Watch/, Archive/Daily Marketing
            Brief/, Market Intel/"Daily Marketing Brief*", Market Intel/"Market Pulse*"
  90 days : Market Intel/"Weekly Brief*", Market Intel/"Mark Follow-up*"

Safety rails:
  * Only files whose name matches the rule's prefix AND contains a parseable
    YYYY-MM-DD date are candidates. Jobs Handoff.json / ATS Inbox.md etc. are
    untouchable by construction.
  * The NEWEST file in each rule group is always kept, however old - the skills
    read "the most recent" digest/pulse, and a stalled pipeline must not lose
    its only copy.
  * Changes stay local. This helper never invokes Git.
  * --dry-run prints retention decisions without deleting notes.

Flags:
  --dry-run   print what would be deleted, change nothing
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUN_LOG = ROOT / "vault" / "Automation" / "JobFinderOS — Schedule & Run Log.md"
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

# (directory relative to ROOT, filename glob, retention days)
RULES = [
    ("vault/Daily Digests",                 "*",                        30),
    ("vault/Archive/Daily Jobs Watch",      "*",                        30),
    ("vault/Archive/Daily Marketing Brief", "*",                        30),
    ("vault/Market Intel",                  "Daily Marketing Brief*",   30),
    ("vault/Market Intel",                  "Market Pulse*",            30),
    ("vault/Market Intel",                  "Weekly Brief*",            90),
    ("vault/Market Intel",                  "Mark Follow-up*",          90),
]


def now():
    return datetime.now().astimezone()


def log(msg: str) -> None:
    line = f"[{now():%Y-%m-%d %H:%M:%S %Z}] {msg}"
    print(line, flush=True)
    try:
        logp = ROOT / "logs" / "prune.log"
        logp.parent.mkdir(parents=True, exist_ok=True)
        with open(logp, "a") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


def file_date(name: str):
    m = DATE_RE.search(name)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None


def collect(today) -> list[Path]:
    """All files past retention, honoring the keep-newest-per-rule rail."""
    doomed: list[Path] = []
    for rel_dir, pattern, days in RULES:
        d = ROOT / rel_dir
        if not d.is_dir():
            continue
        cutoff = today - timedelta(days=days)
        dated = []
        for p in sorted(d.iterdir()):
            if not p.is_file() or not fnmatch.fnmatch(p.name, pattern):
                continue
            fd = file_date(p.name)
            if fd is not None:
                dated.append((fd, p))
        if not dated:
            continue
        newest = max(dated)[1]  # always kept
        for fd, p in dated:
            if p != newest and fd < cutoff:
                doomed.append(p)
                log(f"  prune ({days}d): {p.relative_to(ROOT)}  [{fd}]")
    return doomed


def append_run_log(n: int) -> None:
    try:
        with open(RUN_LOG, "a") as fh:
            fh.write(f"| {now():%Y-%m-%d %H:%M %Z} | prune-history | "
                     f"Pruned {n} vault history file(s) past retention "
                     f"(30d digests/watch/pulse, 90d weekly). Backups are managed separately. |\n")
    except Exception as exc:
        log(f"WARN: run-log append failed: {exc}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    today = now().date()
    log(f"retention sweep (today {today}, dry_run={args.dry_run})")
    doomed = collect(today)
    if not doomed:
        log("nothing past retention")
        return 0
    if args.dry_run:
        log(f"DRY RUN - {len(doomed)} file(s) would be deleted")
        return 0

    for p in doomed:
        try:
            p.unlink()
        except Exception as exc:
            log(f"WARN: could not delete {p.name}: {exc}")
    append_run_log(len(doomed))

    log(f"pruned {len(doomed)} file(s) locally")
    return 0


if __name__ == "__main__":
    sys.exit(main())
