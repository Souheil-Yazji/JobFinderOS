---
description: Deep company evaluation for a career decision. Scored dimensions, the real day-to-day role, 12 to 24 month trajectory, honest verdict. Saves to the vault. Claude Code, no API keys.
---

**Agent:** `mark` · delegated batch work.
- **Main session:** call the Agent tool with `subagent_type: "mark"` and the prompt: *"Read `.claude/commands/mark-profiler.md` and execute its Task section for <Company>. Return the verdict, the file written, and the Recruiter's read."*
- **Already the mark agent, or no Agent tool available:** read `.claude/agents/mark.md`, then execute the Task section here.

## Task
Arg: company. Prefer truth and career leverage over politeness.

1. Read `config/profile.md` (lanes, comp floor, location rules, what the candidate values) and `config/scoring_rubric.md`.
2. Research deeply via primary sources: funding and runway, leadership quality, GTM maturity, product moat, culture, hiring signals, and what the candidate would *really* do there day to day.
3. Produce the deep-dive: scored dimensions, the real role on offer (which of the profile's lanes it fits), the 12 to 24 month trajectory, the honest risks, and a clear verdict: pursue, and as what.
4. Save to `vault/Companies/<Company>/Company Profiler.md` alongside the company profile, with a Navigation block linking both.
5. End with the **Recruiter's read**.
