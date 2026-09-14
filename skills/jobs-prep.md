**Agent:** `coach`
**Execution:** batch

Read `agents/coach.md` and `docs/jobfinderos-instructions.md` first.

## Task
Args: company, role, stage (Recruiter Screen, Hiring Manager, Technical, Panel/Final, etc.).

1. Read `config/profile.md` and the company profile in `vault/Companies/<Company>/` if it exists; the runner invokes Mark’s `jobs-research` first when the named company profile is missing. If research is still missing, report blocked rather than impersonating Mark.
2. Read `config/stories.md`. For every behavioral or leadership question in the prep, match a story by theme or use-for tag and read its full `vault/Stories/` file. Use the locked verbal version and delivery notes; never invent a new telling. If a likely question has no matching story, flag the gap and suggest `/story add`.
3. Research the format and the likely interviewers (web search and page fetching: company site, the team's public profiles, interview-signal sources). For each interviewer: background, what they care about, the one question they are really asking.
4. Build the package: company narrative, why-this-role framing, likely questions for this stage with answers in the candidate's voice (hook or paradox opener), matched stories with per-audience adaptation notes, domain-gap mitigation if relevant, sharp questions to ask.
5. Save to `vault/Companies/<Company>/<Company> — <Role> — Interview Prep — <Stage>.md` with a Navigation block.
6. Follow-ons: `/day-of-card` distills this into the one page for the room; `/mock-interview` rehearses it in character. After the interview, `/story update <id>` captures how each story landed.

## Rules
- Tailor to the stage: a recruiter screen, a technical round, and a panel test different things.
- Every claim grounded in the profile and the story library. No invented experience.
