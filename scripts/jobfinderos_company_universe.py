"""Read-only validation of the two durable company tables; no research or scoring."""
from __future__ import annotations

from collections import Counter
from datetime import date
import math
import re
from urllib.parse import urlparse

QUEUE = "vault/Tracking/Company Discovery Queue.md"
UNIVERSE = "vault/Tracking/Company Universe.md"
QUEUE_COLUMNS = ("Company", "Discovery source", "Why it may fit", "Date discovered",
                 "Status", "Role found", "Role score", "Careers URL", "Added by", "Evaluation")
UNIVERSE_COLUMNS = ("Company", "Status", "Company Fit", "Category", "Careers URL",
                    "ATS", "Why It Fits", "Last Evaluated", "Evaluation")


def scaffold(path):
    columns = QUEUE_COLUMNS if path == QUEUE else UNIVERSE_COLUMNS
    title = "Company Discovery Queue" if path == QUEUE else "Company Universe"
    return (f"# {title}\n\n"
            "| " + " | ".join(columns) + " |\n"
            "| " + " | ".join("---" for _ in columns) + " |\n")


def company_key(name):
    return " ".join(name.split()).casefold()


def table(text, columns):
    """One table with a stable schema. Literal cell pipes must use &#124;."""
    lines = text.splitlines()
    cells = lambda line: tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
    headers = [i for i, line in enumerate(lines) if line.startswith("|") and cells(line) == columns]
    if len(headers) != 1:
        raise ValueError("Missing or duplicate company-table header")
    start = headers[0]
    if start + 1 >= len(lines):
        raise ValueError("Missing table separator")
    separator = cells(lines[start + 1])
    if len(separator) != len(columns) or not all(re.fullmatch(r":?-{3,}:?", c) for c in separator):
        raise ValueError("Invalid table separator")
    rows = []
    seen = set()
    for line in lines[start + 2:]:
        if not line.strip():
            continue
        if not line.startswith("|") or not line.rstrip().endswith("|"):
            raise ValueError("Company tables must end with rows; keep history in evaluations")
        values = cells(line)
        if len(values) != len(columns):
            raise ValueError("Invalid company-table row width")
        row = dict(zip(columns, values))
        key = company_key(row["Company"])
        if not key or key in seen:
            raise ValueError("Empty or duplicate company")
        seen.add(key)
        rows.append(row)
    return rows


def score(value):
    number = float(value)
    if not math.isfinite(number) or not 1 <= number <= 10:
        raise ValueError("Score must be finite and between 1 and 10")
    return number


def check_date(value):
    if date.fromisoformat(value).isoformat() != value:
        raise ValueError("Use YYYY-MM-DD dates")


def web_url(value):
    # Careers URL cells contain a plain URL, not a link label or an inferred slug.
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc) and not re.search(r"\s", value)


def validate_queue(text):
    rows = table(text, QUEUE_COLUMNS)
    for row in rows:
        if row["Status"] not in {"unreviewed", "evaluating", "promoted", "rejected"}:
            raise ValueError("Invalid discovery status")
        if row["Added by"] not in {"Mark", "Scout"}:
            raise ValueError("Invalid discovery author")
        check_date(row["Date discovered"])
        if not row["Discovery source"] or not row["Why it may fit"]:
            raise ValueError("Discovery needs source and reason")
        if row["Role score"] not in {"", "—"}:
            score(row["Role score"])
        if row["Careers URL"] not in {"", "—", "Unknown"} and not web_url(row["Careers URL"]):
            raise ValueError("Invalid careers URL")
    return rows


def validate_universe(text):
    rows = table(text, UNIVERSE_COLUMNS)
    for row in rows:
        status = row["Status"]
        if status not in {"Tier 1", "Tier 2", "Watch", "Dormant", "Rejected"}:
            raise ValueError("Invalid universe status")
        fit = score(row["Company Fit"])
        floor = {"Tier 1": 8.5, "Tier 2": 7.5, "Watch": 6.5}.get(status, 1)
        if fit < floor:
            raise ValueError("Company score does not support tier")
        check_date(row["Last Evaluated"])
        if status in {"Tier 1", "Tier 2"} and not web_url(row["Careers URL"]):
            raise ValueError("Direct targets need a careers URL")
        if not all(row[c] and row[c] != "—" for c in ("Category", "ATS", "Why It Fits", "Evaluation")):
            raise ValueError("Company evaluation metadata missing")
    counts = Counter(row["Status"] for row in rows)
    if counts["Tier 1"] > 10 or counts["Tier 2"] > 25:
        raise ValueError("Automatic company tier capacity exceeded")
    return rows
