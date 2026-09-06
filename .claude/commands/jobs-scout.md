---
description: Scan for new roles that fit the profile, direct from company careers pages and ATS boards plus web search, score them, and log the strong ones to the vault. Works for any career. Claude Code, no API keys.
---

**Agent:** `scout` · delegated batch work.
- **Main session:** call the Agent tool with `subagent_type: "scout"` and the prompt: *"Read `.claude/commands/jobs-scout.md` and execute its Task section. Args: <any arguments given>. Return the report described in `.claude/agents/scout.md`."* Relay the report and the Recruiter's read to the user.
- **Already the scout agent, or no Agent tool available:** read `.claude/agents/scout.md`, then execute the Task section here.

## Task

### Always read first
- `config/profile.md` (target roles, seniority filter, comp floor, location, exclusions, keywords, ATS URL table), `config/scoring_rubric.md`, `config/targets.md` if present
- `config/recruiter_playbook.md` §2 and §6
- `vault/Companies/` and `vault/Tracking/Companies.md` for what is already tracked

### Steps
1. Gather candidate roles: direct ATS fetches for every company in the profile's tiers and `config/targets.md`, then `WebSearch` on the profile's role titles plus location phrasing (vary both). Merge and dedupe against the vault.
2. Drop anything already tracked and anything at an excluded company or matching the excluded-profile pattern.
3. Score each new role against the rubric. Apply the rubric's flags and the profile's hard filters.
4. For every role at or above the profile's logging threshold (default 5), create or update `vault/Companies/<Company>/<Company> — <Role>.md` per the opportunity template in `CLAUDE.md`.
5. For every role at or above the profile's act-on-it threshold (default 7), stub the human path: check `vault/Tracking/Contacts.md` and alumni overlap from the profile's career history, and try to name the hiring manager. Record it in Key Contacts. A recommendation without a human-path answer is incomplete. State the sequence: outreach first, apply 48 to 72h later (closing windows: both in parallel).
6. Write the run summary to `vault/Archive/Daily Jobs Watch/Daily Jobs Watch — <today>.md` and surface the actionable roles with their human paths into `vault/Dashboard.md` `🎯 Now`.
7. End with the **Recruiter's read**: what today's scan says about the market and the pipeline, not a list.

### Rules
- No email, no outreach, no git. Direct sources over aggregators.
- Stay inside the profile's lanes; be proactive about adjacent roles that fit the candidate's strengths.
