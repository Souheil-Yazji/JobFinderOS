**Agent:** `coach`
**Execution:** batch

Read `agents/coach.md` and `docs/jobfinderos-instructions.md` first.

## Task

The test: read it as if it just landed in the recipient's inbox. If any line smells like a model wrote it, it fails. Recruiters read AI-written messages all day and they can tell; one detected template quietly ends a conversation.

Input: the draft (inline, a file path, or `clipboard` via `pbpaste`); optional register `dm` · `email` · `cover` · `answer` · `post` · `resume` (infer and say so if absent); optional `fix`.

### Always read first
`config/recruiter_playbook.md` §3.2 to §3.4; `config/voice.md` if present; the **Key lines** of `vault/Stories/*.md` and any filled `[YOUR TAKE]` text in past drafts (the candidate's verbatim phrasing is the reference standard). For `cover`/`answer`/`resume`, the register rules in the coach agent file.

### Step 1 — Mechanical scan (report line numbers)
- **Punctuation and structure:** em dashes and spaced hyphens doing their job; rule-of-three lists; balanced clauses and mirrored pairs ("Not X. Y." more than once, "it isn't A, it's B"); no sentence-length variance (report shortest and longest); bullets in a DM or email; rhetorical-question opener; zero contractions in a peer note.
- **Vocabulary:** hedging openers (Honestly, To be honest, Frankly); formulaic closers (Either way, At the end of the day, glad to stay in touch as…); stock AI words (resonated, aligns, leverage, delve, navigate, landscape, journey, tapestry, game-changer, unlock, seamless, robust, empower, elevate, "I hope this finds you well", "excited to connect", "came across your profile", "following your journey", "in today's fast-paced"); self-positioning slogans; generic flattery; unexpanded acronyms; signed with the long name instead of the profile's short name; job-seeker framing in peer outreach.
- **Register caps:** DM max 5 sentences; email fits one phone screen; cover has no bullets; answer answers the question in sentence one.

### Step 2 — Substance scan
Two-fact rule: quote the sentence satisfying (a) a fact that took work, source named, and (b) something only the candidate could say, or mark MISSING (missing either = does not go). Homework debt: anything referenced that the candidate hasn't read or watched. Fabricated familiarity: claims WebSearch can't confirm. Rough edge: point to the sentence that most needs the candidate's own rewording, or say none exists yet. The ask (outreach): small and easy to say yes to.

### Step 3 — Voice match
Flag any sentence the candidate wouldn't say out loud on a Tuesday; prefer their own phrasings from the story library. If the candidate wrote the draft and a "tell" is simply how they write, say "reads as AI to a stranger; your call" rather than sanding it off.

### Step 4 — Report
```
## Voice check — <register> — <date>
**Verdict:** PASS / REWRITE / DO NOT SEND
| Line | Tell | Why it reads as generated | Fix |
**Two-fact rule:** (a) … · (b) …
**Homework before sending:** …
**The sentence to reword in your own words:** …
**Register notes:** …
```
DO NOT SEND = two-fact failure or fabricated familiarity. REWRITE = tells present, substance there. PASS = cosmetic notes at most.

On `fix` or a yes: rewrite, list every change (old → new), keep sentences that already pass, `pbcopy` the result. The fix direction is plainer and rougher, never more polished. If the source was a vault draft, update it and add `Voice check: <verdict> <date>` under Status.

### Recruiter's read (required)
Would this get a reply, and why? The single tell most likely to get it flagged. If the same tell recurs across drafts, name it and propose a learned preference in private `config/voice.md`.

## Rules
- Never improve a draft by making it longer or smoother. Never remove the candidate's rough edge.
- A two-fact failure is not fixed by prose: "do the research or don't send," then stop.
