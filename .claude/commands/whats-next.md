---
description: "Choose-your-own-adventure session. Full pipeline sweep, then the 3 to 5 highest-leverage actions toward landing the next role. Pick one, do it together, the vault syncs, the menu re-ranks. Triggers on 'what should we do next?'"
---

**Agent:** `coach` · runs in this session (it is a loop with the candidate). Read `.claude/agents/coach.md` first.

## Task
Triggers: "what should we do next," "what's next," "what should I focus on," "where should we spend time today."

### Step 1 — Full sweep
`config/recruiter_playbook.md`, `config/profile.md`, `config/scoring_rubric.md`; `vault/Dashboard.md`; `vault/Strategy.md` (funnel, objection log, proof assets, deadline math: options serve the strategy, not just the pipeline); the queue; Contacts.md; the newest Daily Digest and Market Pulse; opportunity notes for every company interviewing, overdue, top-of-mind, or a menu candidate. Note today's date and weekday.

### Step 2 — Candidates, three buckets, 10 to 15 before ranking
**A. Advance existing:** prep for scheduled calls, overdue nudges, silent-app re-engagement, thank-yous, referral asks, verify-then-apply items, borderline decisions. **B. Open new:** unactioned high-scoring roles, direct ATS re-checks of target companies, fresh postings in the profile's most-wanted categories, refill if the queue is thin. **C. Grow connections:** contacts due a touch, post-connect warm-ups, peer outreach at companies with live strong roles, dormant-relationship revivals, presence moves.

### Step 3 — Rank by impact × urgency × probability
Impact: how much it moves toward an offer. Urgency: closing windows (interviews inside 72h, fast-filling postings, nudges going stale at 10 to 14 days, cooling intros). Probability: warm > cold, live > silent, high score > threshold score, location-clean > verify-needed. Default order: imminent prep > warm plays into live apps > overdue nudges > apply to fresh top roles > new networking > refill > hygiene. **Gap bias:** a bucket with no completed action in ~7 days gets its best action promoted, and the menu says why. **Proof-asset override:** unshipped proof assets in Strategy outrank new cold applications. Hard filters from the profile always apply (exclusions, comp floor, location rules, excluded profile). Seat over company.

### Step 4 — The menu
```
**What's next — <Day, Mon DD>**
*Pulse: N live conversations · N apps awaiting · N nudges overdue · last outreach N days ago.*
**1. <emoji> <Action>.** <2 to 4 sentences: history, why now, closing window.> *What we'd do:* <deliverables>. *~time.*
**2.** …
Reply 1–N, "more" for the next tier, or tell me something I don't know.
```
Best first. Every option names real companies, people, dates. Generic advice never. New information instead of a number → absorb, update the vault, re-rank, re-present.

### Step 5 — Execute
**Warm-path gate:** if the action is an application, run `/warm-path` logic first; reachable path → outreach now, apply 48 to 72h later. **Inline:** drafts (a chosen option whose deliverable is a draft counts as yes; otherwise ask) to clipboard and vault via `/draft-message` rules; role verification direct on the ATS; borderline decisions with evidence; talking-point refreshes. **Route to the skill** and say so: `/jobs-prep`, `/day-of-card`, `/mock-interview`, `/jobs-cover`, `/jobs-research` or `/mark-profiler`, `/network-outreach`, `/draft-message`, `/jobs-scout`, `/jobs-email` or `/email-watch`, `/postmortem`, `/voice-check`.

### Step 6 — Sync
Opportunity note (stage, dates, timeline); Dashboard (item, `> Updated:`, pulse); queue; Contacts (touches, warmth, caps); communication log; one row in `vault/Automation/JobScoutOS — Schedule & Run Log.md` (`whats-next | <action>`). Minimum edits.

### Step 7 — Loop
Remove the completed action, re-rank (regenerate if the world changed), add anything new, tighter each pass. On stop: **Recruiter's read**: what got done, what it changed, whether the week's pace holds the deadline math in §10, the top of the queue next time.

## Rules
- Specificity is the product. A stale vault (>3 days) → say so and offer `/checkin` as option 1.
