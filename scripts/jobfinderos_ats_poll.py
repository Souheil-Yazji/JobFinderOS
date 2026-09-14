#!/usr/bin/env python3
"""
JobFinderOS - local direct-ATS poller.
================================================================================
Finds NEW matching reqs by hitting each target company's ATS JSON API directly.
Deterministic: HTTP + filter + diff. No LLM, no API keys. Every filter below is
read from the `filters:` block of config/ats_boards.yaml (see the example file).

Pipeline:
    boards (config/ats_boards.yaml)
      -> fetch each board's job list
      -> TITLE gate (seniority token if leadership_only, AND a target-function term)
      -> LOCATION gate (remote / home region / country-wide = clean;
                        hub-city-only at a tier-1 = surface with a relocation flag;
                        everything else dropped). US-centric vocabulary; edit the
                        region regexes below for other countries.
      -> COMP gate (parsed range midpoint must clear filters.min_comp; unparseable =
                    surface as "comp unverified" - fails OPEN toward surfacing)
      -> diff against the seen-set (~/.jobfinderos/ats_seen.json)
      -> append survivors to vault/Market Intel/ATS Inbox.md (unscored)
      -> desktop-notify only the clean-location ones (tight match)

Scoring is deliberately NOT done here - the /jobs-daily digest reads the
inbox and applies config/scoring_rubric.md. This script only decides what is
worth showing a human.

Flags:
    --seed       mark everything currently live as already-seen, write the inbox
                 scaffold, notify nothing, commit nothing. Run this ONCE at
                 install so the first real run surfaces only genuinely new reqs.
    --dry-run    fetch + decide + print. Touches no state, no vault, no git.
    --status     print seen-set size and last-run info, then exit.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

# ---------------------------------------------------------------- paths / config

ROOT = Path(__file__).resolve().parent.parent
BOARDS_FILE = ROOT / "config" / "ats_boards.yaml"
if not BOARDS_FILE.exists():
    BOARDS_FILE = ROOT / "config" / "ats_boards.example.yaml"
INBOX = ROOT / "vault" / "Market Intel" / "ATS Inbox.md"
STATE_DIR = Path.home() / ".jobfinderos"
STATE_FILE = STATE_DIR / "ats_seen.json"
LOG_FILE = ROOT / "logs" / "ats-poll.log"

DEFAULT_FILTERS = {
    "timezone": "",                       # IANA name; empty = system local time
    "min_comp": 0,                        # total-comp floor in local currency units; 0 = no floor
    "leadership_only": True,              # require a seniority token in the title
    "seniority_terms": r"head\s+of|head|vp|svp|evp|vice\s+president|chief|director|dir\.?|manager|mgr\.?|general\s+manager|gm",
    "function_terms": "",                 # regex alternatives; a title must match one. Empty = any function
    "priority_function_terms": "",        # subset that counts as the priority lane (Lane A)
    "ic_override_terms": r"staff|principal|individual\s+contributor",
    "home_region_terms": "",              # regex alternatives for your home city/state; empty = none
    "home_region_label": "home region",
    "lane_labels": {"A": "Priority function", "B": "Secondary function"},
    "user_agent": "JobFinderOS-ATS-Poller/1.0 (personal job search)",
}


def _load_cfg() -> dict:
    try:
        return yaml.safe_load(BOARDS_FILE.read_text()) or {}
    except FileNotFoundError:
        sys.exit(f"no board registry: copy config/ats_boards.example.yaml to {BOARDS_FILE}")


_CFG = _load_cfg()
FILTERS = {**DEFAULT_FILTERS, **(_CFG.get("filters") or {})}

TZ = ZoneInfo(FILTERS["timezone"]) if (FILTERS["timezone"] and ZoneInfo) else None
MIN_COMP = int(FILTERS["min_comp"] or 0)
HTTP_TIMEOUT = 25
UA = FILTERS["user_agent"]

# ---------------------------------------------------------------- filter rules

# Seniority token required in the title when filters.leadership_only is true,
# e.g. "Manager, Widget Design". "Senior Widget Designer" has none -> IC -> dropped.
LEADERSHIP_RE = re.compile(r"\b(" + FILTERS["seniority_terms"] + r")\b", re.I)

# ...and the title must name one of the target functions (filters.function_terms).
FUNCTION_RE = re.compile("(" + FILTERS["function_terms"] + ")", re.I) if FILTERS["function_terms"] else None

# Lane A = the priority-function subset (filters.priority_function_terms).
LANE_A_RE = re.compile("(" + FILTERS["priority_function_terms"] + ")", re.I) if FILTERS["priority_function_terms"] else None

# Explicit IC markers that override a stray seniority word in a long title.
IC_OVERRIDE_RE = re.compile(r"\b(" + FILTERS["ic_override_terms"] + r")\b", re.I) if FILTERS["ic_override_terms"] else None

REMOTE_US_RE = re.compile(
    r"(remote\s*[-,/]?\s*(us|u\.s\.|usa|united\s+states|america|anywhere\s+in\s+the\s+us)"
    r"|(us|u\.s\.|usa|united\s+states)[\s,()-]*remote"
    r"|remote\s*[-,/]?\s*(north\s+america|nam)"
    r"|^remote$|\(remote\)|remote\s+-\s+[a-z\s]*(california|colorado|oregon|washington|"
    r"texas|new\s+york|illinois|georgia|utah|massachusetts|florida|arizona|virginia|"
    r"north\s+carolina|d\.?c\.?))",
    re.I,
)

US_GENERIC_RE = re.compile(r"^\s*(united\s+states|usa|u\.s\.a?\.?|us)\s*$", re.I)
HOME_REGION_RE = re.compile(r"\b(" + FILTERS["home_region_terms"] + r")\b", re.I) if FILTERS["home_region_terms"] else None

US_HUB_RE = re.compile(
    r"\b(san\s+francisco|sf\b|new\s+york|nyc\b|brooklyn|seattle|bellevue|boston|"
    r"cambridge|palo\s+alto|mountain\s+view|menlo\s+park|sunnyvale|santa\s+clara|"
    r"los\s+angeles|san\s+jose|chicago|denver|washington|d\.?c\.?|atlanta|miami|"
    r"chapel\s+hill|redwood\s+city|foster\s+city|san\s+mateo)\b",
    re.I,
)

NON_US_RE = re.compile(
    r"\b(london|uk|united\s+kingdom|england|scotland|ireland|dublin|paris|france|"
    r"berlin|munich|germany|amsterdam|netherlands|zurich|geneva|switzerland|"
    r"stockholm|sweden|oslo|norway|copenhagen|denmark|helsinki|finland|iceland|"
    r"brussels|belgium|vienna|austria|prague|czech|warsaw|poland|budapest|hungary|"
    r"bucharest|romania|athens|greece|istanbul|turkey|lisbon|portugal|madrid|"
    r"barcelona|spain|milan|rome|italy|luxembourg|estonia|latvia|lithuania|"
    r"tokyo|japan|singapore|seoul|korea|china|shanghai|beijing|hong\s+kong|taiwan|"
    r"sydney|melbourne|australia|auckland|new\s+zealand|manila|philippines|"
    r"hanoi|vietnam|bangkok|thailand|jakarta|indonesia|kuala\s+lumpur|malaysia|"
    r"toronto|canada|vancouver|montreal|ottawa|"
    r"bangalore|bengaluru|india|mumbai|delhi|hyderabad|chennai|pune|"
    r"thiruvananthapuram|pakistan|bangladesh|"
    r"tel\s+aviv|israel|dubai|uae|abu\s+dhabi|qatar|doha|riyadh|saudi|kuwait|"
    r"bahrain|oman|jordan|lebanon|egypt|cairo|morocco|tunisia|nigeria|kenya|"
    r"ghana|south\s+africa|africa|mena|"
    r"sao\s+paulo|brazil|mexico|argentina|buenos\s+aires|chile|santiago|colombia|"
    r"bogota|peru|lima|uruguay|costa\s+rica|panama|"
    r"apac|emea|latam|anz|noram|international)\b",
    re.I,
)

# A leading "Remote" ("Remote - California") is the company declaring the role
# remote-first. A trailing "(Remote)" bolted onto a city ("Foster City, CA (Remote)")
# is ambiguous - it is often a hub-based seat wearing a remote label.
LEADING_REMOTE_RE = re.compile(r"^\s*(fully\s+)?remote\b", re.I)
REMOTE_WORD_RE = re.compile(r"\bremote\b", re.I)

MONEY_RE = re.compile(r"\$\s?([\d][\d,\.]*)\s?([kK])?\b")
# "$500 million in funding" must never be read as a $500,000 salary.
SCALE_WORD_RE = re.compile(r"^\s*(million|billion|bn\b|mm\b|m\b|b\b)", re.I)

# ---------------------------------------------------------------- data model


@dataclass
class Req:
    company: str
    tier: object
    ats: str
    req_id: str          # globally unique: "<slug>:<ats id>"
    title: str
    location: str
    url: str
    comp_text: str = ""
    # decision fields
    location_class: str = ""   # clean | hub_flag | drop
    comp_status: str = ""      # clear | unverified | under
    comp_range: str = ""
    lane: str = ""
    reason: str = ""
    notes: list = field(default_factory=list)


# ---------------------------------------------------------------- utilities


def now():
    return datetime.now(TZ) if TZ else datetime.now()


def log(msg: str) -> None:
    stamp = now().strftime("%Y-%m-%d %H:%M:%S %Z")
    line = f"[{stamp}] {msg}"
    print(line)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


def http_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def http_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        return resp.read().decode("utf-8", "replace")


def strip_html(raw: str) -> str:
    import html as _html

    txt = re.sub(r"<[^>]+>", " ", raw or "")
    return _html.unescape(txt)


# ---------------------------------------------------------------- fetchers


def fetch_greenhouse(board) -> list[Req]:
    slug = board["slug"]
    data = http_json(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
    out = []
    for j in data.get("jobs", []):
        out.append(
            Req(
                company=board["company"],
                tier=board.get("tier"),
                ats="greenhouse",
                req_id=f"{slug}:{j.get('id')}",
                title=(j.get("title") or "").strip(),
                location=((j.get("location") or {}).get("name") or "").strip(),
                url=j.get("absolute_url") or f"https://boards.greenhouse.io/{slug}/jobs/{j.get('id')}",
            )
        )
    return out


def fetch_ashby(board) -> list[Req]:
    slug = board["slug"]
    data = http_json(
        f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true"
    )
    out = []
    for j in data.get("jobs", []):
        comp = ""
        c = j.get("compensation") or {}
        if isinstance(c, dict):
            comp = c.get("compensationTierSummary") or ""
            if not comp:
                # fall back to any summary component we can find
                tiers = c.get("summaryComponents") or []
                if isinstance(tiers, list) and tiers:
                    comp = " ".join(str(t.get("summary", "")) for t in tiers if isinstance(t, dict))
        loc = j.get("location") or ""
        if j.get("isRemote") and "remote" not in loc.lower():
            loc = f"{loc} (Remote)".strip()
        out.append(
            Req(
                company=board["company"],
                tier=board.get("tier"),
                ats="ashby",
                req_id=f"{slug}:{j.get('id') or j.get('jobId') or j.get('title')}",
                title=(j.get("title") or "").strip(),
                location=loc.strip(),
                url=j.get("jobUrl") or j.get("applyUrl") or f"https://jobs.ashbyhq.com/{slug}",
                comp_text=comp or "",
            )
        )
    return out


def fetch_lever(board) -> list[Req]:
    slug = board["slug"]
    data = http_json(f"https://api.lever.co/v0/postings/{slug}?mode=json")
    out = []
    for j in data if isinstance(data, list) else []:
        cats = j.get("categories") or {}
        out.append(
            Req(
                company=board["company"],
                tier=board.get("tier"),
                ats="lever",
                req_id=f"{slug}:{j.get('id')}",
                title=(j.get("text") or "").strip(),
                location=(cats.get("location") or "").strip(),
                url=j.get("hostedUrl") or "",
                comp_text=(j.get("descriptionPlain") or "")[:6000],
            )
        )
    return out


FETCHERS = {"greenhouse": fetch_greenhouse, "ashby": fetch_ashby, "lever": fetch_lever}


def fetch_comp_detail(r: Req) -> str:
    """Second-pass JD fetch, only for reqs that already passed title+location."""
    try:
        if r.ats == "greenhouse":
            slug, jid = r.req_id.split(":", 1)
            j = http_json(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs/{jid}")
            return strip_html(j.get("content") or "")
        if r.ats == "lever":
            return r.comp_text
    except Exception as exc:
        r.notes.append(f"comp fetch failed: {exc}")
    return r.comp_text


# ---------------------------------------------------------------- gates


def passes_leadership(title: str) -> tuple[bool, str]:
    if not title:
        return False, ""
    if FILTERS["leadership_only"] and not LEADERSHIP_RE.search(title):
        return False, ""
    if FUNCTION_RE and not FUNCTION_RE.search(title):
        return False, ""
    if FILTERS["leadership_only"] and IC_OVERRIDE_RE and IC_OVERRIDE_RE.search(title) and not re.search(
        r"\b(head|vp|vice\s+president|director|chief)\b", title, re.I
    ):
        return False, ""
    lane = "A" if (LANE_A_RE and LANE_A_RE.search(title)) else "B"
    return True, lane


def classify_location(loc: str, tier) -> tuple[str, str]:
    """-> (clean | hub_flag | drop, human reason)"""
    if not loc:
        # No location given: treat as US-ambiguous, surface with a flag rather than drop.
        return "hub_flag", "no location listed - verify"

    parts = [p.strip() for p in re.split(r"[;|/]|\s+or\s+", loc) if p.strip()]
    blob = " ; ".join(parts)

    has_home = bool(HOME_REGION_RE.search(blob)) if HOME_REGION_RE else False
    has_us_generic = any(US_GENERIC_RE.match(p) for p in parts) or bool(
        re.search(r"united\s+states", blob, re.I)
    )
    has_hub = bool(US_HUB_RE.search(blob))
    has_non_us = bool(NON_US_RE.search(blob))
    has_remote_word = bool(REMOTE_WORD_RE.search(blob))
    leading_remote = bool(LEADING_REMOTE_RE.match(blob))

    # 1. A non-US location dominates. A bare "(Remote)" on "Munich, Germany" does
    #    not make it US-eligible - that was the bug that let 7 EMEA/APAC reqs through.
    if has_non_us and not (has_home or has_us_generic or has_hub):
        return "drop", "international only"
    # 2. Home region listed anywhere - hybrid there is fine.
    if has_home:
        return "clean", f"{FILTERS['home_region_label']} listed"
    # 3. Company declared it remote-first.
    if leading_remote:
        return "clean", "remote-first listing"
    if REMOTE_US_RE.search(blob) and not has_hub:
        return "clean", "remote-US"
    # 4. US with no city constraint.
    if has_us_generic and not has_hub:
        return "clean", "US, no city constraint"
    # 5. A named US hub city.
    if has_hub:
        if has_remote_word:
            # Ambiguous: ATS says remote but anchors a hub. Surface to verify, never alert.
            return "hub_flag", "remote flag on a hub city - verify remote scope"
        if str(tier) == "1":
            return "hub_flag", "hub-based at a Tier-1 - relocation, deprioritized"
        return "drop", "hub-only at a non-Tier-1"
    if has_us_generic:
        return "clean", "US-listed"
    if has_remote_word:
        return "hub_flag", "remote but region unclear - verify"
    return "hub_flag", "location unclear - verify"


def parse_comp(text: str) -> tuple[str, str]:
    """-> (clear | under | unverified, human range). Fails OPEN to 'unverified'."""
    if not text:
        return "unverified", ""
    vals = []
    for m in MONEY_RE.finditer(text):
        amt, k = m.group(1), m.group(2)
        # Skip funding/valuation figures: "$500 million in funding", "$8.3B valuation".
        if SCALE_WORD_RE.match(text[m.end(): m.end() + 12]):
            continue
        try:
            v = float(amt.replace(",", "").rstrip("."))
        except ValueError:
            continue
        if k:
            v *= 1000
        # No bare-number upscaling: "$500" stays 500 and falls out of the salary
        # band below, rather than becoming a phantom $500K.
        if 50_000 <= v <= 2_000_000:
            vals.append(v)
    if not vals:
        return "unverified", ""

    vals = sorted(set(vals))
    if len(vals) >= 2:
        lo, hi = vals[0], vals[-1]
        mid = (lo + hi) / 2
        rng = f"${lo:,.0f}-${hi:,.0f} (mid ${mid:,.0f})"
        return ("clear" if mid >= MIN_COMP else "under"), rng
    # single figure: too ambiguous to reject on - fail open unless it clearly clears
    v = vals[0]
    return ("clear" if v >= MIN_COMP else "unverified"), f"${v:,.0f}"


# ---------------------------------------------------------------- state


def load_seen() -> set[str]:
    if not STATE_FILE.exists():
        return set()
    try:
        return set(json.loads(STATE_FILE.read_text()).get("seen", []))
    except Exception as exc:
        log(f"WARN: could not read seen-set ({exc}); starting empty")
        return set()


def save_seen(seen: set[str], note: str = "") -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "seen": sorted(seen),
                "count": len(seen),
                "last_run": now().isoformat(),
                "note": note,
            },
            indent=2,
        )
    )


# ---------------------------------------------------------------- collection


def collect(boards) -> tuple[list[Req], list[str]]:
    """Fetch every enabled board and apply the title+location gates."""
    survivors, problems = [], []
    for b in boards:
        if b.get("enabled") is False:
            continue
        fn = FETCHERS.get(b.get("ats"))
        if not fn:
            problems.append(f"{b['company']}: no fetcher for ats={b.get('ats')}")
            continue
        try:
            reqs = fn(b)
        except Exception as exc:  # a bad board never kills the run
            problems.append(f"{b['company']}: fetch failed ({exc})")
            continue

        kept = 0
        for r in reqs:
            ok, lane = passes_leadership(r.title)
            if not ok:
                continue
            lclass, lreason = classify_location(r.location, r.tier)
            if lclass == "drop":
                continue
            r.lane, r.location_class, r.reason = lane, lclass, lreason
            survivors.append(r)
            kept += 1
        log(f"  {b['company']:<14} {len(reqs):>4} reqs -> {kept} title+location match")
    return survivors, problems


def apply_comp_gate(reqs: Iterable[Req]) -> list[Req]:
    out = []
    for r in reqs:
        text = r.comp_text or ""
        if not text or r.ats == "greenhouse":
            text = fetch_comp_detail(r) or text
        status, rng = parse_comp(text)
        r.comp_status, r.comp_range = status, rng
        if status == "under":
            continue  # below the floor, midpoint rule
        out.append(r)
    return out


# ---------------------------------------------------------------- output


def render_entry(r: Req) -> str:
    loc_note = "clean" if r.location_class == "clean" else f"⚠️ {r.reason}"
    comp = r.comp_range if r.comp_range else "not posted"
    if r.comp_status == "unverified":
        comp += " — **comp unverified**"
    labels = FILTERS.get("lane_labels") or {}
    lane = f"Lane {r.lane} ({labels.get(r.lane, '')})"
    return (
        f"### {r.company} — {r.title}\n"
        f"- **Status:** unscored\n"
        f"- **Location:** {r.location or '(none listed)'} — {loc_note}\n"
        f"- **Comp:** {comp}\n"
        f"- **Lane:** {lane}\n"
        f"- **ATS:** {r.ats} · req `{r.req_id}`\n"
        f"- **Posting:** {r.url}\n"
        f"- **Found:** {now().strftime('%Y-%m-%d %H:%M %Z')}\n\n"
    )


INBOX_HEADER = """> **JobFinderOS:** ATS Poller · local direct-ATS sweep · [[Dashboard]] · [[Strategy]]

# ATS Inbox

Newly-discovered reqs found by the local direct-ATS poller
(`scripts/jobfinderos_ats_poll.py`), pending scoring by the daily digest.

**How this works:** the poller is deterministic — it only filters (leadership title,
location, comp floor) and diffs against a seen-set. It does **not** score. The daily
digest reads every entry marked `**Status:** unscored`, scores it against
`config/scoring_rubric.md`, promotes 7+ to an opportunity note, and flips the status
to `scored`.

Location flags: `clean` = remote / home region / country-wide. `⚠️` = hub-city-only at a
tier-1 (relocation) or unclear, verify.

---

"""


def write_inbox(new_reqs: list[Req]) -> None:
    INBOX.parent.mkdir(parents=True, exist_ok=True)
    if not INBOX.exists():
        INBOX.write_text(INBOX_HEADER, encoding="utf-8")
    if not new_reqs:
        return
    body = f"## {now().strftime('%Y-%m-%d')} — {len(new_reqs)} new\n\n"
    body += "".join(render_entry(r) for r in new_reqs)
    with INBOX.open("a", encoding="utf-8") as fh:
        fh.write(body)


def notify(tight: list[Req]) -> None:
    if not tight:
        return
    head = tight[0]
    title = f"{len(tight)} new matching req" + ("s" if len(tight) > 1 else "")
    msg = f"{head.company} — {head.title}"
    if len(tight) > 1:
        msg += f"  (+{len(tight) - 1} more)"
    try:
        subprocess.run(
            [
                "osascript",
                "-e",
                f'display notification {json.dumps(msg)} with title {json.dumps(title)} '
                f'subtitle "JobFinderOS · ATS Inbox"',
            ],
            check=False,
            timeout=10,
        )
    except Exception as exc:
        log(f"WARN: notification failed ({exc})")


# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description="JobFinderOS local direct-ATS poller")
    ap.add_argument("--seed", action="store_true", help="mark all current reqs seen; write nothing else")
    ap.add_argument("--dry-run", action="store_true", help="print decisions, change nothing")
    ap.add_argument("--status", action="store_true", help="print state and exit")
    args = ap.parse_args()

    if args.status:
        if STATE_FILE.exists():
            st = json.loads(STATE_FILE.read_text())
            print(f"seen reqs : {st.get('count', 0)}")
            print(f"last run  : {st.get('last_run', 'never')}")
            print(f"note      : {st.get('note', '')}")
        else:
            print("no state yet - run with --seed first")
        print(f"inbox     : {INBOX} ({'exists' if INBOX.exists() else 'not created'})")
        return 0

    boards = _CFG.get("boards") or []
    active = [b for b in boards if b.get("enabled") is not False]
    log(f"sweeping {len(active)} boards "
        f"({len(boards) - len(active)} phase-2 boards skipped: no clean JSON API)")

    survivors, problems = collect(boards)
    log(f"{len(survivors)} reqs passed title+location; applying comp gate")
    survivors = apply_comp_gate(survivors)
    log(f"{len(survivors)} reqs passed the comp floor")

    for p in problems:
        log(f"PROBLEM: {p}")

    seen = load_seen()
    fresh = [r for r in survivors if r.req_id not in seen]

    if args.seed:
        seen.update(r.req_id for r in survivors)
        if not args.dry_run:
            INBOX.parent.mkdir(parents=True, exist_ok=True)
            if not INBOX.exists():
                INBOX.write_text(INBOX_HEADER, encoding="utf-8")
            save_seen(seen, note="seeded from live boards at install")
        log(f"SEEDED: {len(survivors)} currently-live reqs marked as seen. "
            f"Only reqs posted after now will surface.")
        return 0

    if args.dry_run:
        log(f"DRY RUN - {len(fresh)} would be NEW (of {len(survivors)} matching)")
        for r in survivors:
            tag = "NEW " if r.req_id in {f.req_id for f in fresh} else "seen"
            alert = "🔔" if (r.location_class == "clean" and r.req_id in
                             {f.req_id for f in fresh}) else "  "
            print(f"  [{tag}]{alert} {r.company:<13} {r.title[:58]:<58} "
                  f"| {r.location[:34]:<34} | {r.location_class:<8} | "
                  f"{r.comp_status:<10} {r.comp_range}")
        return 0

    if not fresh:
        log("no new reqs")
        save_seen(seen, note="no new reqs")
        return 0

    tight = [r for r in fresh if r.location_class == "clean"]
    log(f"{len(fresh)} NEW req(s); {len(tight)} tight-match (clean location) -> notifying")
    for r in fresh:
        log(f"  NEW: {r.company} - {r.title} [{r.location_class}] "
            f"{r.comp_status} {r.comp_range}")

    write_inbox(fresh)
    seen.update(r.req_id for r in fresh)
    save_seen(seen, note=f"{len(fresh)} new on {now().strftime('%Y-%m-%d')}")
    notify(tight)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
