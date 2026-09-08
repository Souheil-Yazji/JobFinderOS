---
description: Full daily routine. Runs the market pulse and the scout in parallel, then email triage, then the digest, and writes one consolidated run record and Recruiter's read. The everyday driver. Claude Code, no API keys.
---

**Agent:** orchestrator · runs in this session as `coach` for the closing read. Read `.claude/agents/coach.md` first.

## Task

Four passes. Delegate each to its agent via the Agent tool; if the Agent tool is unavailable, read the named agent file and run the pass inline in this order: pulse, scout, email, digest.

1. **In parallel:**
   - **Market Pulse** → `subagent_type: "mark"`: *"Read `.claude/commands/mark-pulse.md` and execute its Task section. Return the report."*
   - **Scout** → `subagent_type: "scout"`: *"Read `.claude/commands/jobs-scout.md` and execute its Task section. Return the report."*
2. **Email** → `subagent_type: "coach"`: *"Read `.claude/commands/jobs-email.md` and execute its Task section. Return the report, including every reply that is due."*
3. **Digest** → `subagent_type: "coach"`: *"Read `.claude/commands/jobs-digest.md` and execute its Task section. Today's Market Pulse and scout results are already in the vault. Return the report."*

Then, in this session:
4. Consolidate into `vault/Archive/Daily Jobs Watch/Daily Jobs Watch — <today>.md`: market signals, new roles with human paths, pipeline changes, replies due, prep actions.
5. Append a run row to `vault/Automation/JobFinderOS — Schedule & Run Log.md`.
6. One consolidated **Recruiter's read** covering market, pipeline, and the single most important move today. If replies are due, list them and offer to draft; write nothing until the candidate says yes.

## Rules
- Honor every filter in `config/profile.md`. Direct sources, never aggregators.
- The vault root stays `Dashboard.md` + `Strategy.md`.
