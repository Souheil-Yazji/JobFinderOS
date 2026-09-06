#!/usr/bin/env python3
"""
JobScoutOS - "Latest ..." pointer notes at the vault root.
================================================================================
Keeps one pointer note per digest family at the top level of the vault, each
embedding (transcluding) the newest dated note in its family, so you can
open "Latest Daily Digest" in Obsidian and always see today's content.

Mechanics:
  * A launchd job (com.jobscoutos.latest) runs this via WatchPaths on the
    digest directories - any write there (local skill run,
    retention prune) re-points the notes within seconds. RunAtLoad trues it
    up at login. Idempotent: rewrites a pointer only when the target changes.
  * Pointer files are generated + gitignored ("/vault/Latest *.md") - they are
    derived state, not content. The digests themselves stay the record.

Flags:
  --dry-run   print decisions, write nothing
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

# family title -> list of (dir, glob) to scan for the newest dated note.
# Pointer note at the vault root is named "<title> — <date>.md" (archive-folder
# style); the previous pointer is removed when the date
# rolls forward.
FAMILIES = {
    "Daily Digest": [("vault/Daily Digests", "*.md")],
    "Market Pulse": [("vault/Market Intel", "Market Pulse*.md")],
    "Weekly Brief": [("vault/Market Intel", "Weekly Brief*.md")],
    "Daily Marketing Brief": [
        ("vault/Market Intel", "Daily Marketing Brief*.md"),
        ("vault/Archive/Daily Marketing Brief", "*.md"),
    ],
}

# Canonical root notes (stable filenames every skill/wikilink depends on) that
# get a dated pointer companion showing when they last changed. Date comes from
# the note's own "> Updated: ..." header line, falling back to file mtime.
CANONICAL = {
    "Dashboard": "vault/Dashboard.md",
    "Strategy": "vault/Strategy.md",
}


def newest(scans) -> tuple[str, Path] | None:
    """(date, path) of the newest dated file across the family's dirs."""
    best = None
    for rel_dir, pattern in scans:
        d = ROOT / rel_dir
        if not d.is_dir():
            continue
        for p in d.glob(pattern):
            m = DATE_RE.search(p.name)
            if not p.is_file() or not m:
                continue
            key = (m.group(1), p)
            if best is None or key[0] > best[0]:
                best = key
    return best


def pointer_body(title: str, target: Path, date: str) -> str:
    # Obsidian wikilinks resolve by path-from-vault-root without extension.
    link = str(target.relative_to(VAULT).with_suffix(""))
    return (
        f"> **JobScoutOS:** auto-generated pointer — do not edit "
        f"(rewritten by `scripts/jobscoutos_update_latest.py` whenever a newer "
        f"{title} lands). [[{link}|Open the note →]]\n"
        f"\n"
        f"# {title} — {date}\n"
        f"\n"
        f"![[{link}]]\n"
    )


def canonical_date(path: Path) -> str:
    """YYYY-MM-DD a canonical note last changed: its 'Updated:' header, else mtime."""
    try:
        for line in path.read_text().splitlines()[:8]:
            if "Updated:" in line:
                m = DATE_RE.search(line)
                if m:
                    return m.group(1)
    except Exception:
        pass
    return datetime.fromtimestamp(path.stat().st_mtime).astimezone().strftime("%Y-%m-%d")


def main() -> int:
    dry = "--dry-run" in sys.argv
    changed = 0
    targets = [(title, newest(scans)) for title, scans in FAMILIES.items()]
    targets += [
        (title, (canonical_date(ROOT / rel), ROOT / rel))
        for title, rel in CANONICAL.items()
        if (ROOT / rel).is_file()
    ]
    for title, found in targets:
        if found is None:
            print(f"{title}: no dated notes found; leaving as-is")
            continue
        date, target = found
        pointer = VAULT / f"{title} — {date}.md"
        # Retire superseded pointers: older dates of this family at the root,
        # plus the legacy "Latest <title>.md" naming.
        for stale in [*VAULT.glob(f"{title} — *.md"), VAULT / f"Latest {title}.md"]:
            if stale.is_file() and stale != pointer:
                print(f"  retire: {stale.name}" + ("  (dry-run)" if dry else ""))
                if not dry:
                    stale.unlink()
        body = pointer_body(title, target, date)
        current = pointer.read_text() if pointer.is_file() else ""
        if current == body:
            continue
        print(f"{pointer.name} -> {target.relative_to(ROOT)}"
              + ("  (dry-run)" if dry else ""))
        if not dry:
            pointer.write_text(body)
            changed += 1
    print(f"{datetime.now().astimezone():%F %T} updated {changed} pointer note(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
