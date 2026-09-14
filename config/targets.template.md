# Target Employers — TEMPLATE (optional)

> Copy to `config/targets.md` (gitignored) if you have specific employers in mind.
> This is OPTIONAL. The scout first fetches each target company's own careers/ATS
page using `config/profile.md`, then broadens with web search to discover additional
primary sources. This file extends the direct target list. Aggregators are not a
primary source of record.

## How the scout uses this
1. Fetch each employer's direct careers/ATS page below and in the profile.
2. Broaden using the profile's role/location keywords; verify findings at their
   original employer/ATS source, merge, score, and deduplicate against the vault.

## Direct careers / ATS list
Add employers you want watched directly. The ATS column helps the scout fetch the right
page (common systems: Greenhouse, Lever, Ashby, Workday, iCIMS, the employer's own site).

| Employer | Careers / ATS URL | ATS | Notes |
|----------|-------------------|-----|-------|
| <Name> | <https://…> | <Greenhouse/Lever/Ashby/Workday/site> | <why it's a target> |

> Tip: many ATSs expose a clean JSON feed — e.g. Greenhouse at
> `https://boards-api.greenhouse.io/v1/boards/<org>/jobs` and Ashby at
> `https://api.ashbyhq.com/posting-api/job-board/<org>`. The scout prefers these when
> available because they render reliably.
