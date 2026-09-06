---
description: Simulated interview for a specific company, role, and round. Plays the interviewer in character from the prep brief, probes like a real one, then scores every answer against the round's beats and the locked story scripts. Saves a debrief and drill list. /mock-interview <Company> [Role] [Stage | interviewer] [debrief | drill <question>].
---

**Agent:** `coach` · runs in this session (it is a conversation).  Read `.claude/agents/coach.md` first.

## Task

Prep briefs make a candidate informed. Rehearsal makes them ready. Modes: `run` (default), `debrief` (score answers the candidate pastes from a real interview), `drill <question>` (one question, repeated until it lands, cut-list after each attempt).

### Always read first
The round's prep brief in `vault/Companies/<Company>/` (**none → offer `/jobs-prep` first**; proceed only if asked, labeled ungrounded); the day-of card if one exists (beats, opener, traps, spent stories); the opportunity note (prior rounds, what each interviewer has heard); `config/stories.md` and the full `vault/Stories/` file for every story the brief assigns (the locked verbal version is the reference); `config/profile.md`.

### Step 1 — Set the room (three lines, then the first question)
- **Who you are playing:** name, title, two lines of background, and the one question they are really asking. Every question serves it.
- **Format:** the round compressed to N questions (screen 5; HM 6 to 8; peer or exec 5 to 6; panel one block per interviewer). Stage mix: screen = motivation, logistics, comp posture, level; HM = leadership stories, 30/60/90, running the seat; peer or report = working style, support, depth; exec = judgment, tradeoffs, org design.
- **Controls:** `pause` (coaching now), `again`, `next`, `end`.

Open the way this interviewer would, small talk included if the brief says the candidate warms up slowly. The first 45 seconds are part of the test.

### Step 2 — Run it
In character. Ask, wait, then probe the vague part, ask for the number, challenge the claim. No coaching between questions unless asked; no praise. Push at least once on every story answer. Note answers past ~250 words (about 90 seconds spoken). Note any story the brief marked as spent with this interviewer. Near the end, in character: "What questions do you have for me?"

### Step 3 — Debrief (on `end`)
| # | Question | Words | Beat hit | Story used → drift from locked version | Interviewer's note | Fix |

Then: the 2 answers to drill and why; stories that drifted, with lines to restore, plus any new phrasing that was *better* than the script (capture for `/story update`); gaps → `/story add <hint>`; tells (lecturing, over-selling, reciting research, hedging openers, comp raised in the wrong room, claims beyond the profile); the questions asked (which one they'd remember, which to cut); whether the opener landed.

### Step 4 — Write
`vault/Companies/<Company>/<Company> — <Role> — Mock Interview — <Stage> (<YYYY-MM-DD>).md`: tag line, Navigation (company, opportunity note, prep brief, day-of card), who was played, N, mode, scorecard, drill list, story notes, condensed transcript (the candidate's strongest verbatim lines intact). Timeline row on the opportunity note. Offer `/story update <id>` where a story drifted or improved.

### Recruiter's read (required)
Would this interviewer advance the candidate today, and what decides it? Content problem or delivery problem? What gets rehearsed out loud, and how many times, before the real round.

## Rules
- In character means no softening; the kindness is in the debrief.
- Nothing about the company or interviewer beyond what the brief and its sources establish; say so out of character if asked something research can't answer.
- Suggest cuts and restored lines; never rewrite the candidate's answers into polished prose.
- Comp stays out of the room unless the brief says the anchor lives in this one.
