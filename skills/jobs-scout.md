**Agent:** `scout`
**Execution:** batch

Read `agents/scout.md` and `docs/jobfinderos-instructions.md` first.

## Task

### Always read first
- `config/profile.md` (target roles, seniority filter, comp floor, location, exclusions, keywords, ATS URL table), `config/scoring_rubric.md`, `config/targets.md` if present
- `config/recruiter_playbook.md` §2 and §6
- `vault/Companies/` and `vault/Tracking/Companies.md` for what is already tracked

### Steps
First read `vault/Market Intel/ATS Inbox.md` if present. Treat entries marked
`**Status:** unscored` as candidate leads, verify against the supplied source,
apply the profile filters/rubric and normal deduplication, and promote eligible
roles through the steps below. Mark each processed entry `scored` with its score
or exclusion reason; retain source details. Do not resurface already scored leads.

1. Gather candidate roles: direct ATS fetches for every company in the profile's tiers and `config/targets.md`, then web search on the profile's role titles plus location phrasing (vary both). Merge and dedupe against the vault.
2. Drop excluded companies and excluded-profile matches. Do not re-alert already tracked roles; retain existing provisional/held roles for verification and update their notes in place.
3. Score each new role against the rubric. Apply the rubric's flags and the profile's hard filters.
4. For every role at or above the profile's logging threshold (default 5), create or update `vault/Companies/<Company>/<Company> — <Role>.md` per the opportunity template in `docs/vault-note-templates.md`.
5. For roles in the profile/rubric's daily priority bands (default 7 only when neither defines a threshold), stub the human path: check `vault/Tracking/Contacts.md` and alumni overlap from the profile's career history, and try to name the hiring manager. Record it in Key Contacts. A recommendation without a human-path answer is incomplete. State the sequence: outreach first, apply 48 to 72h later (closing windows: both in parallel).
6. Merge the run summary into `vault/Archive/Daily Jobs Watch/Daily Jobs Watch — <today>.md` and update the Dashboard using Scout's output discipline. Revisit existing provisional/held leads on retries; preserve history and unrelated tasks. Complete Scout's evidence and output checks before returning.
7. End with the **Recruiter's read**: what today's scan says about the market and the pipeline, not a list.

### Rules
- No email, no outreach, no git. Direct sources over aggregators.
- Stay inside the profile's lanes; be proactive about adjacent roles that fit the candidate's strengths.
