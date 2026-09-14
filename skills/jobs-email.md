**Agent:** `coach`
**Execution:** batch

Read `agents/coach.md` and `docs/jobfinderos-instructions.md` first.

## Task

### Always read first
- `config/recruiter_playbook.md` (§1, §3, §4), `config/profile.md`
- `vault/Dashboard.md`, `vault/Tracking/Email Follow-ups Queue.md`

### Steps
1. Search Gmail (`search_threads`) for inbound recruiter mail, pipeline updates, interview invites, and stale threads. Read full history with `get_thread` before acting.
2. **Rejection and status-change sweep, every run.** Do not only look for good news. Search explicitly for closed language: `"not to move forward"`, `"other candidates"`, `"after careful consideration"`, `"decided not to"`, `"recently hired"`, `"position has been filled"`, `"not be moving forward"`, `"unable to move forward"`. For every hit, set the correct stage (❌ Closed) in the queue, the Dashboard, and the opportunity note, and reconcile any row mis-logged as silent that was really a rejection. The record must match reality.
3. **Interview detected → auto-prep, every run.** If a screen, interview, or hiring-manager round is scheduled (invite, coordinator email, "availability", "next step"), log date, time, and interviewer to the queue and the opportunity note, then generate or update a stage-specific prep brief in `vault/Companies/<Company>/` per `/jobs-prep`. Surface the top prep actions. Do not wait to be asked.
4. **Reconcile the queue** against today. Apply silence norms §4 rather than re-dating: a startup application silent past 14 days or a large company past 21 days is ⚫ presumed dead (note the one revival lever if a warm contact exists); post-screen or post-HM silence past 7 days triggers the backup-candidate play (one nudge, accelerate comparables). Caps: max 2 bumps then park 30 days, each bump with a new angle.
5. **Flag replies that are due.** For each, say who, why, and by when. Do not compose. On the candidate's yes, `/draft-message` composes to clipboard and vault with a "Before you send" note, and the queue gets a nudge date.
6. Surface new opportunities into `vault/Companies/<Company>/`.
7. Update `vault/Archive/Daily Jobs Watch/Daily Jobs Watch — <today>.md` and reflect anything actionable in `vault/Dashboard.md`. If a rejection was logged, prompt for `/postmortem <Company>`.
8. End with the **Recruiter's read**: what the inbox is saying about momentum, silence patterns, which threads deserve energy this week and which to release.

### Rules
- Steps 2 and 3 are never optional.
- Keep nudging in vault notes until the candidate pauses the row or removes it.
