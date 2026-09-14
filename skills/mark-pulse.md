**Agent:** `mark`
**Execution:** batch

Read `agents/mark.md` and `docs/jobfinderos-instructions.md` first.

## Task

### Steps
1. Read `config/profile.md` (target tiers, priority companies, watch list, ATS table), `config/scoring_rubric.md`, and `vault/Market Intel/Jobs Handoff.json`.
2. Scan primary sources (web search and page fetching, never aggregators) across the target set for: Series B+ funding, new revenue leadership (field hiring follows in 60 to 90 days), enterprise GTM build-outs, function renames, and any company worth adding to the target set.
3. Write `vault/Market Intel/Daily Marketing Brief — <today>.md`:
   - `> **JobFinderOS:** Mark · <today> <time> TZ`
   - `# Daily Marketing Brief — <today>`
   - `## Market Context and Top Signals` with inline source links
   - `## Tracked Companies — Current Status`: every Tier 1/2 company, one status line plus its careers link; flag live roles
   - `## New Company Spotlight`: one newly relevant company not yet in the standing scan
   - `## Action Recommendations — Week of <today>`: 4 to 6 numbered actions with wikilinks. Pre-posting trigger rule (§6): every raise, GTM-exec hire, or field-org build-out at a target produces a named human play this week, written into `vault/Dashboard.md` `🎯 Now`.
   - `### Companies tracked this cycle`
4. Write `vault/Market Intel/Market Pulse — <today>.md`: 6 to 8 ranked signals, each with sources. The brief is the summary; the pulse is the research backing.
5. Update `vault/Market Intel/Jobs Handoff.json` (`priority_now`, `new_to_evaluate`, `apply_queue_status`).
6. End with the **Recruiter's read**.

### Rules
- Inline clickable URLs, not footnotes. Honor the excluded-profile filter and the profile's flagged exceptions.
- Today's brief replaces yesterday's by filename pattern; old ones stay in `Market Intel/` until pruned.
