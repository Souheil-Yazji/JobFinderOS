---
description: Daily pipeline sync. Processes Dashboard checkboxes and verbal updates, ages every thread against the silence norms, refreshes the Dashboard and vault notes, and ends with a candid Recruiter's read.
---

**Agent:** `coach` · runs in this session (it pauses for the candidate). Read `.claude/agents/coach.md` first.

## Task
The daily touch-point: process what the candidate did, age every live thread so the pipeline reflects reality instead of hope, refresh the Dashboard, and say what it means.

### Step 1 — Read
`config/recruiter_playbook.md` (§3.1, §4, §9); `vault/Dashboard.md` (every `- [x]`, the aged tables); `vault/Tracking/Email Follow-ups Queue.md`; `vault/Tracking/Contacts.md`; the opportunity note for every company in a checked item, with an overdue nudge, or whose silence status changes today. Keep the scope tight.

### Step 2 — Process checked boxes silently
`Applied —` → Stage `📬 Applied`, date, timeline row, Dashboard applications row (age 0, human-attached status). `Sent —` / `Reached out —` / `Pinged —` → Contacts (Last Touch today, Next Touch per cadence), timeline, communication log. `Verified —` / `Replied —` / `Nudged —` / `Prepped —` → timeline note, queue or thread row. Each matched note: Overview stage and dates, Timeline row `| YYYY-MM-DD HH:MM TZ | what happened |`.

### Step 3 — Age the pipeline, every run
Recompute ages; set 🟢/🟡/⚫ per §4 (startup >14d, large company >21d, post-screen >7d, post-HM >7d). Threads crossing into ⚫ presumed dead: mark, note the one revival lever, stop scheduling energy. Warm contacts due today or past: queue the action within caps. Flag threshold events that demand a decision.

### Step 4 — Pause
```
**Check-in — <date>**
Processed: <one line per checked item>
Aged: <status changes>
Due today: <overdue nudges, cadence touches, decisions>
**What else happened?** Recruiter emails, calls, DMs, interviews, rejections, decisions, new intel, or "done".
```

### Step 5 — Process the reply, no follow-up questions
"Applied to X" → stage, timeline, Dashboard row. "Screen/interview with X <date>" → stage `📞`/`🧠`, Scheduled table with prep pointer, and per §8 name the 2 comparable processes to accelerate. "Rejected by X" → `❌ Closed`, closures, then run or offer `/postmortem`. "Offer from X" → `🤝 Offer`, log comp, §8 notify-all-live-processes becomes action #1. "<Name> replied/accepted/call" → Contacts, communication log, next move. "Sent DM to <Name>" → Contacts touches, count against the weekly cap. "Add <company/role>" → stub note plus Dashboard row, human-path answer noted (§2). "done" → Step 6.

### Step 6 — Refresh the Dashboard, minimally
`> Updated:` and the funnel pulse (counts, warm-attached %, live threads, last-outreach days); `🗓️ Scheduled`; `🎯 Now` (remove done, insert new ranked by leverage, ≤6 plus overdue/decide lines); `🔴 Live human threads`; `📬 Applications`; `🧠 Interviewing` / `❌ Recent closures` / `👀 Priority watch` as changed. Never rewrite hand-written rationale.

### Step 7 — Log
`vault/Automation/JobScoutOS — Schedule & Run Log.md`: `| <today> <HH:MM> TZ | checkin | <N> actions, <M> threads aged: <summary> |`

### Step 8 — Recruiter's read (required)
What today's state means, the pattern forming, the uncomfortable truth, the next inflection point. Then one line: applied today / interviewing / top of tomorrow's queue.

## Rules
- A checked item with no matching note: say so and ask; never skip silently.
- "done" ends it without more questions.
- Weekly funnel snapshots and the objection log live in `vault/Strategy.md` and belong to `/mark-weekly` and `/postmortem`; this skill owns the Dashboard pulse.
