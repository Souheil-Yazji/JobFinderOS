---
description: Audit the search vocabulary against what the market calls the job right now. Reads real postings at target companies, extracts the live title vocabulary, diffs it against saved searches and profile terms, and hands back the exact terms to paste into LinkedIn preferences. /title-audit [function description | quick]. Claude Code, no API keys.
---

**Agent:** `mark` · runs in this session (Step 4 needs the candidate to paste their LinkedIn preferences). Read `.claude/agents/mark.md` first.

## Task

The principle: the matching layer can only find the candidate if the candidate speaks its current language. Titles drift; saved searches don't. This skill makes the rename check a routine instead of an accident.

Input: an optional plain-English description of the function. If none, derive it from `config/profile.md` → Target Role Types. `quick` skips the LinkedIn homework in Step 4.

### Always read first
`config/profile.md` (Target Role Types, Target Companies with ATS URLs, **Core Keyword Set → Role titles to search**, the vocabulary under audit); `config/recruiter_playbook.md` §6; the two newest `vault/Market Intel/` notes; `vault/Tracking/Companies.md`.

### Step 1 — Describe the function, not the title
Two title-free lines on what the job does. This is the search key; every match below is on responsibilities, never on the title the candidate currently uses.

### Step 2 — Pull 15 to 25 real postings, direct
Careers pages and ATS boards from the profile's URL table, never aggregators: every Tier 1 company with an open req in the function, a sample of Tier 2 and watch companies, and 3 to 5 un-indexed companies visibly hiring in the space (`WebSearch` on responsibility phrases from the profile's keyword set, e.g. `"<duty phrase>" "<duty phrase>" site:jobs.ashbyhq.com`). Capture per posting: exact title · level word · function noun · modifier · company · URL · date · leadership seat or not. Match on the responsibilities paragraph; a posting the candidate would never have searched but whose duties are their job is the point. Flag those. Do not filter the *sample* by the profile's seniority or comp rules (IC postings still tell you what the function is called); filter only the *recommendations*.

### Step 3 — Tally
Term (normalized, level words stripped) · count · companies · first seen (from Market Intel history if known) · trend, only with evidence. Group synonyms; note which modifier is winning. **Threshold: 3 or more distinct companies** before a term is recommended as an add.

### Step 4 — Diff against three surfaces
1. `config/profile.md` → Role titles to search (what the scout searches)
2. LinkedIn job preferences and saved searches: ask the candidate to paste them (Jobs → Preferences → Job titles; saved-search terms). Two-minute homework. Skipped in `quick`; say the diff is partial.
3. The machine-readable profile surface: LinkedIn headline, first line of About, resume headline, if shared.

Classify: **ADD** (market uses it, candidate doesn't) · **KEEP** · **RETIRE** (candidate searches it, market moved on; keep only if it still returns real reqs) · **WATCH** (1 to 2 companies).

### Step 5 — Write `vault/Market Intel/Title Audit — <YYYY-MM-DD>.md`
Tag line, Navigation, function audited, sample size. Sections: What the market calls it (table) · Postings you would have missed (title as posted, company, why it's your job, link) · Diff against your searches (term, scout, LinkedIn prefs, headline, action) · **Paste list** (one exact term per line, leadership forms first) · Saved-search terms (quoted) · Headline note (which terms the headline should carry; a recommendation, no prose drafted) · Recruiter's read · Next audit due (monthly in an active search, or on a Market Intel naming signal).

With the candidate's yes, update `config/profile.md` → Role titles to search (adds and retires) so the scout inherits it. One line in `vault/Strategy.md` → Decision log per change.

### Recruiter's read (required)
Is the function being renamed, and how far along is it? Which surface is the biggest blind spot? Is there a lane the vocabulary reveals that the candidate isn't targeting? The single term to add today.

## Rules
- Recommend changes to the candidate's inputs. Never speculate about how any platform's matching algorithm consumes them; the confirmed mechanism is "preferences changed, listing appeared."
- Excluded companies never appear as recommendations; their postings may still count in the tally.
