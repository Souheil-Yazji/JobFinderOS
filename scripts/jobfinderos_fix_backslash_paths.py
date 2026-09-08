#!/usr/bin/env python3
"""Repair literal-backslash vault paths left by skill runs.

Fallback `claude -p` runs have occasionally written files to literally named
directories like `vault/Market\\ Intel/` (backslash-space in the dir name)
instead of `vault/Market Intel/` — an over-escaped shell heredoc inside the
agent's Bash calls. This script finds any entry under vault/ whose name
contains a backslash, strips the backslashes, and merges it into the intended
path. Runs after every skill run via JobFinderOS_run_skill.sh; safe to run
any time (no-op when the vault is clean).

Rules:
  - `foo\\ bar` -> `foo bar` (backslashes removed from every path segment)
  - If the repaired file path doesn't exist: move.
  - If it exists: keep the LARGER file at the repaired path and save the other
    alongside it as `<name>.conflict-<date>.md` — never silently discard.
  - Emptied bad directories are removed.
"""
from __future__ import annotations

import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"


def repaired_name(name: str) -> str:
    return name.replace("\\", "")


def repair(dry_run: bool = False) -> int:
    if not VAULT.is_dir():
        print(f"fix_backslash_paths: no vault at {VAULT}", file=sys.stderr)
        return 0

    # Deepest first so files move before their parent dirs are considered.
    bad = sorted(
        (p for p in VAULT.rglob("*") if "\\" in p.name),
        key=lambda p: len(p.parts),
        reverse=True,
    )
    fixed = 0
    for src in bad:
        dst = src.with_name(repaired_name(src.name))
        if src.is_dir():
            # Files inside were already handled (deepest first); merge dir.
            if not any(src.iterdir()):
                print(f"rmdir  {src.relative_to(ROOT)}")
                if not dry_run:
                    src.rmdir()
                fixed += 1
                continue
            if not dry_run:
                dst.mkdir(parents=True, exist_ok=True)
                for child in src.iterdir():
                    move_file(child, dst / repaired_name(child.name), dry_run)
                if not any(src.iterdir()):
                    src.rmdir()
            print(f"merge  {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
            fixed += 1
        else:
            move_file(src, dst, dry_run)
            fixed += 1
    if fixed:
        print(f"fix_backslash_paths: repaired {fixed} entr{'y' if fixed == 1 else 'ies'}")
    return 0


def move_file(src: Path, dst: Path, dry_run: bool) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        # Keep the larger file at the canonical path; preserve the other.
        keep, other = (dst, src) if dst.stat().st_size >= src.stat().st_size else (src, dst)
        conflict = dst.with_name(f"{dst.stem}.conflict-{date.today()}{dst.suffix}")
        print(f"conflict {src.relative_to(ROOT)} vs existing -> keeping larger, saving other as {conflict.name}")
        if not dry_run:
            if keep is src:
                shutil.move(str(dst), str(conflict))
                shutil.move(str(src), str(dst))
            else:
                shutil.move(str(src), str(conflict))
    else:
        print(f"move   {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
        if not dry_run:
            shutil.move(str(src), str(dst))


if __name__ == "__main__":
    sys.exit(repair(dry_run="--dry-run" in sys.argv))
