---
description: Draft a follow-up, thank you, cold outreach, recruiter reply, or offer acknowledgment in the candidate's voice. Copies to clipboard and logs to the vault. Never sends, never creates Gmail drafts.
---

**Agent:** `coach` · runs in this session. Read `.claude/agents/coach.md` first (drafting voice, two-fact rule, human-in-the-loop).

## Task

### If called without a target
Read `vault/Dashboard.md` and `vault/Tracking/Email Follow-ups Queue.md`, list what is overdue against today, and ask which (if any) to draft. Never draft unasked. Respect the caps: max 2 bumps per thread, new angle each time.

### Step 1 — Context
Identify company, role, contact (name, title, LinkedIn vs email), message type, and prior interaction. Read the company profile (communication log), the opportunity note (stage, timeline), any prior `vault/Outreach Drafts/` for this company, and `config/stories.md` when the message needs a proof point (pull from a story's key lines rather than inventing one). If a Gmail thread is relevant, read it in full first.

### Writing rules
- Short. Follow-ups 2 to 3 sentences. Thank-yous 4 to 5. Cold outreach two paragraphs at most.
- One specific detail per message that proves attention. No sentence that could appear in any message to any company.
- Lead with the strongest point; never open with an intro, a reference to the posting, or "I wanted to follow up."
- Give an easy out on follow-ups; never beg.
- No bullets in the body. Sign with the short name from the profile.

### Scenarios
- **Follow-up after a LinkedIn DM (no reply):** 2 sentences max. Reference what was sent, not when. Low-friction close. No apology. One follow-up only.
- **Follow-up after applying (no ATS response):** 3 sentences. Acknowledge the formal process, add one thing the application could not capture, light ask.
- **Post-recruiter-screen thank-you:** one specific thing from the conversation, tied briefly to the candidate's background, clear interest. 4 sentences. Within 24 hours.
- **Post-hiring-manager thank-you:** the most specific thing discussed; one paragraph that advances the narrative; optionally address a concern directly; confident close. 5 sentences.
- **Panel or final thank-yous:** individual notes, each about what that person talked about. 3 to 4 sentences each.
- **Cold email to an executive:** hook first (the most specific, non-obvious observation), never open with who the candidate is, two paragraphs, 20-minute ask. Read the vault profile first if the company is tracked.
- **Reply to inbound recruiter:** warm but measured. State the comp expectation from the profile early, state location clearly, ask one qualifying question, propose a next step. 3 to 4 sentences.
- **Warm contact check-in:** peer tone, reference the last real interaction, one sentence on what the candidate is looking for now, light ask. Only when there is a concrete reason (`feedback_outreach_with_intention`); no nurture pings to thin, high-value contacts.
- **Offer or comp:** never accept or counter without explicit instruction. Counters anchor high with specifics and keep the door open. Acknowledgments express interest and buy time gracefully with a date.

### Step 2 — Draft, show, revise
Write it, show it, take feedback, revise until approved.

### Step 3 — Clipboard
`pbcopy` the final body as plain prose (no markdown). State the suggested **To:** and **Subject:** (replies: "Re: <original subject>"). Include a **Before you send** note: claims to verify, sources to read first, `[YOUR TAKE]` slots. Never `create_draft`.

### Step 4 — Vault
Save to `vault/Outreach Drafts/<Company> — <Role> — <Type> — Draft.md`. Add a communication-log row to the company profile. If it is a nudge, update the queue with the next date.

### Step 5 — Confirm
Report: copied (recipient, subject), vault logged, what to fill or verify, time sensitivity (thank-yous within 24 hours), and a **Recruiter's read** when the thread state warrants it: what this message is trying to move, and what happens if it lands vs stays silent.

## Rules
- One follow-up per thread; if one already went, say so and ask before drafting another.
- Never guess email addresses. Save the draft and ask for the address.
- If the vault is thin, write from what exists and flag exactly what would make it stronger.
