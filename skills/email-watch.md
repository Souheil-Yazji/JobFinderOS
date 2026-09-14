**Agent:** `coach`
**Execution:** batch

Read `agents/coach.md` and `docs/jobfinderos-instructions.md` first.

## Task

### Step 1 — Pipeline state
`config/recruiter_playbook.md` (§3.1, §4), `config/profile.md` (target companies, exclusions), `vault/Dashboard.md`, `vault/Tracking/Companies.md`, `vault/Tracking/Email Follow-ups Queue.md`.

### Step 2 — Search Gmail
Last 48 hours unless told otherwise. Run all, dedupe:
- `subject:(opportunity OR role OR position OR opening) newer_than:2d`
- `subject:(interview OR screen OR call OR meet) newer_than:2d`
- `subject:(application OR applied OR candidacy OR resume) newer_than:2d`
- `subject:(offer OR compensation OR comp) newer_than:2d`
- `from:(recruiter OR talent OR hiring OR recruit OR people) newer_than:2d`
- The profile's role-title vocabulary, e.g. `(VP OR director OR "head of" OR "<function>") newer_than:2d`
- Every company with a live thread in the queue or Dashboard, by name

Read full threads for every hit that is not obvious noise.

### Step 3 — Classify
**RESPOND TODAY** (interview request, availability ask, offer, direct question) · **RESPOND THIS WEEK** (warm inbound, reply to something sent, scheduling) · **LOG IT** (rejection, confirmation, status; vault update, no reply) · **NEW LEAD** (untracked but qualified) · **STALE WARNING** (sent, no reply, past the nudge date) · **NOISE**.

For STALE WARNING, apply the silence norms: say what the silence means at that stage and what the move is, not just that it is overdue.

### Step 4 — Act on clear pipeline updates
Rejection, interview invite, or offer: update the opportunity note stage and timeline, and the Dashboard.

### Step 5 — Briefing
```
## Inbox Watch — <date, time>
### Act Now
| Thread | From | Ask | Suggested action |
### New Inbound — Not Yet Tracked
| From | Company hint | Signal | Recommended next step |
### Pipeline Updates (auto-logged)
| Company | What changed | Source |
### Stale Threads — Follow-up Overdue
| Company | Last contact | Days since | Nudge due | What the silence means |
### FYI / Noise
```
Close with the **Recruiter's read**: what the inbox says about momentum this week.

### Rules
- Never surface excluded companies. Time-sensitive items at the top. Recommend, do not describe.
- A strong new inbound (estimated score at or above the act-on-it threshold) gets said explicitly, with an offer to log it.
