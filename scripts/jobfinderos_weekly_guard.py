#!/usr/bin/env python3
"""JobFinderOS scheduled guard: weekly Mark brief (local agent task)."""
from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent

def _scheduler_cfg() -> dict:
    """config/scheduler.yaml as a dict ({} if missing or PyYAML absent)."""
    cfg = ROOT / 'config' / 'scheduler.yaml'
    try:
        import yaml  # type: ignore
        return yaml.safe_load(cfg.read_text()) or {}
    except Exception:
        return {}


def _tz():
    name = (_scheduler_cfg().get('timezone') or '').strip()
    if name:
        try:
            return ZoneInfo(name)
        except Exception:
            pass
    return datetime.now().astimezone().tzinfo

LOCAL_TZ = _tz()
MARKER = ROOT / 'logs' / 'scheduler-cron' / 'weekly-market-brief.last-success'
LOCK = ROOT / 'logs' / 'scheduler-cron' / 'weekly-market-brief.lock'
MARKET_DIR = ROOT / 'vault' / 'Market Intel'


def emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def lock_status(lock_path: Path) -> str | None:
    if not lock_path.exists():
        return None
    try:
        pid = int(lock_path.read_text().strip() or '0')
    except ValueError:
        lock_path.unlink(missing_ok=True)
        return None
    if pid > 0:
        try:
            os.kill(pid, 0)
            return f'in_progress:{pid}'
        except OSError:
            lock_path.unlink(missing_ok=True)
            return None
    lock_path.unlink(missing_ok=True)
    return None


def acquire_lock(lock_path: Path) -> bool:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    with os.fdopen(fd, 'w') as fh:
        fh.write(str(os.getpid()))
    return True


def newest_matching(prefix: str) -> str | None:
    files = [p for p in MARKET_DIR.glob(f'{prefix}*.md') if p.is_file()]
    if not files:
        return None
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return str(files[0])


def main() -> None:
    now = datetime.now(LOCAL_TZ)
    week = now.strftime('%G-W%V')
    monday = (now - timedelta(days=now.weekday())).replace(hour=8, minute=30, second=0, microsecond=0)
    if now < monday:
        emit({'status': 'skip', 'reason': 'before_window', 'week': week})
        return
    if MARKER.exists() and MARKER.read_text().strip() == week:
        emit({'status': 'skip', 'reason': 'already_succeeded', 'week': week})
        return
    active = lock_status(LOCK)
    if active:
        emit({'status': 'skip', 'reason': active, 'week': week})
        return
    if not acquire_lock(LOCK):
        emit({'status': 'skip', 'reason': 'in_progress', 'week': week})
        return

    try:
        cmd = ['bash', 'scripts/JobFinderOS_run_skill.sh', 'mark-weekly', 'mark-weekly']
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if proc.returncode != 0:
            emit({
                'status': 'error',
                'reason': 'run_weekly_failed',
                'week': week,
                'returncode': proc.returncode,
                'stdout_tail': proc.stdout[-4000:],
                'stderr_tail': proc.stderr[-4000:],
            })
            return

        MARKER.parent.mkdir(parents=True, exist_ok=True)
        MARKER.write_text(week + '\n')
        emit({
            'status': 'success',
            'week': week,
            'weekly_brief': newest_matching('Weekly Brief'),
            'mark_followup': newest_matching('Mark Follow-up'),
        })
    finally:
        LOCK.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
