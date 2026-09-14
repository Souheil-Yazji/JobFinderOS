**Agent:** `coach`
**Execution:** batch

Read `agents/coach.md` and `docs/jobfinderos-instructions.md` first.

## Task

The funnel truth behind this skill: in this system's history, every documented loss was a cold application with no human attached at apply time, and the wins came once a human was in the loop. No application gets queued without the question answered.

Input: `/warm-path <Company> [Role]` for one opportunity; `/warm-path audit` (or no argument) to sweep every opportunity at Spotted, Queued, or Applied.

### Always read first
`config/recruiter_playbook.md` §2, §3.1, §7; `config/profile.md` (career history = the alumni search key; tiers); `vault/Tracking/Contacts.md`; the company profile; the opportunity note (Human path line, Key Contacts, stage, any closing window).

### Step 1 — Cap check
An unanswered thread at this company stops the outreach half; report the thread's age against §4 and the date a second thread is allowed. If the weekly new-humans cap is hit, the plan gets a banked date instead of a Day 0.

### Step 2 — Walk the ladder, in order, and record every rung checked
1. **Existing contacts** at the company or one intro away (name the intro path).
2. **Alumni overlap.** For each former employer in the profile: web search `"<former employer>" "<target company>" site:linkedin.com/in`. Plus the candidate's two-minute homework you cannot do for them: company LinkedIn page → People → filter by former employers and 1st/2nd degree. Ask them to paste results; list it as homework if they haven't.
3. **Hiring manager and the HM's boss, by name** (required at or above the act-on-it score). Posting text, leadership pages, org announcements, conference bios.
4. **A named recruiter** at the company, ideally the one on the posting.

For each human: name, title, LinkedIn, how the candidate reaches them, why this rung.

### Step 3 — Verdict
`warm — active` (a human is already in conversation about this seat) · `warm — reachable` (named human plus a credible route, not yet worked) · `cold — no human attached` (ladder walked, empty; the application may proceed, logged as cold, with the reminder that cold has converted at zero). "Drafted but unsent" is reachable, not active.

### Step 4 — Sequence, with real dates
| Verdict | Plan |
|---------|------|
| active | Apply now if the human said to; otherwise tell them to expect it and apply within 48h |
| reachable | Day 0 outreach (`/network-outreach` for a peer or HM, `/draft-message` for a recruiter or known contact). Day 2 to 3 apply. Silent at Day 7 to 10: one bump, new angle; apply on Day 10 regardless and log cold |
| cold | Apply, log cold, second ladder pass in 14 days |
| closing window (evidenced: posting age, recruiter statement, referral deadline) | Apply now and work the path in parallel; say why the exception applies |

### Step 5 — Write
Opportunity note: `**Human path:**` line = verdict plus names; Key Contacts rows with thread roles; timeline row `Warm-path gate: <verdict>`. Contacts.md: new humans under Priority — Not Yet Contacted, goal `referral`, next touch = Day 0. Company profile: communication-log row. Dashboard: the Day 0 outreach as a play if reachable. **Do not draft here.** Name what is due, offer, write only on yes.

### Audit mode
Table for every open opportunity: company · role · stage · human path · named HM? · named recruiter? · next action. Then the ratio of applications with a human attached against the 70% target, and the three opportunities where a single-company gate would move it most. Append to `vault/Strategy.md` → Funnel.

### Recruiter's read (required)
Is this seat worth the outreach budget under the caps, or is applying cold and moving on the honest call? Where does the thread fit in the company play? In audit mode: is the ratio moving, and which habit holds it down.

## Rules
- Never fabricate a warm path. "Probably knows someone" is cold.
- The closing-window exception must be evidenced, never assumed.
