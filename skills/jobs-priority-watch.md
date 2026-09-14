**Agent:** `scout`
**Execution:** batch

Read `agents/scout.md` and `docs/jobfinderos-instructions.md` first.

## Task

A narrow, fast watch for the function the profile marks as priority, at the companies the profile marks as priority. It runs every weekday tick, so it must be quiet when there is nothing to say.

### Always read first
- `config/profile.md`: the priority function and its title vocabulary, the seniority filter, the **priority companies** section, the **watch companies** section, the most-wanted product category if one is named, comp floor, location rules, exclusions, and the direct ATS URL table
- `config/scoring_rubric.md`
- `vault/Companies/` so nothing is re-alerted

### Steps
1. page fetching each priority and watch company's own careers page or ATS from the profile's URL table. No aggregators.
2. Look only for roles that match the priority function's vocabulary **and** pass the seniority filter. If the profile says leadership only, IC titles do not surface (log and skip); a founding or team-build mandate counts as leadership even at a Manager title.
3. Score new roles with the rubric (the priority function scores top marks on role fit; apply the comp, location, and any flagged-company rules).
4. **Nothing new:** stop. Write no files, no summary.
5. **New roles:** create or update opportunity notes per the template in `docs/vault-note-templates.md` (Stage `🔍 Spotted`, score, flags). For roles at or above the act-on-it threshold, stub the human path in Key Contacts (Contacts.md check, likely hiring manager). Append a line to `vault/Archive/Daily Jobs Watch/Daily Jobs Watch — <today>.md` and surface any top-scoring find into `vault/Dashboard.md` `🎯 Now`.

### Rules
- No email, no outreach, no git. Honor every exclusion.
