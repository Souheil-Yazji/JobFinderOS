---
description: Company research brief. Business model, funding, leadership, product, GTM motion, culture, open reqs in the candidate's lanes, interview signals, and a recommended angle. Saves to the vault. Claude Code, no API keys.
---

**Agent:** `mark` · delegated batch work.
- **Main session:** call the Agent tool with `subagent_type: "mark"` and the prompt: *"Read `.claude/commands/jobs-research.md` and execute its Task section for <Company>. Return the summary, contacts found, the recommended angle, and the file written."*
- **Already the mark agent, or no Agent tool available:** read `.claude/agents/mark.md`, then execute the Task section here.

## Task
Arg: company.

1. Read `config/profile.md` and `config/scoring_rubric.md` for what matters to the candidate.
2. Research via primary sources (company site, the careers/ATS page from the profile's URL table, funding announcements, leadership pages, recent press): business model, funding and stage, leadership (especially revenue and field leadership), product, GTM motion, culture, interview signals.
3. Note open reqs in the candidate's lanes and whether a new revenue leader was hired recently (field hiring follows in 60 to 90 days).
4. Write or update `vault/Companies/<Company>/<Company>.md` using the company profile template in `CLAUDE.md`. Surface contacts into the Contacts table and a recommended angle for the candidate.
5. Cite URLs. Flag if the company brushes the excluded-profile pattern.
