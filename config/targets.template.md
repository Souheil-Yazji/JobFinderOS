# Target Employers — TEMPLATE (optional)

> Copy to `config/targets.md` (gitignored) if you have specific employers in mind.
> This is OPTIONAL. The scout's primary engine is multi-source web search across job
> boards and company sites driven by your profile keywords, so you do NOT need to know
> your targets up front. This file just lets you ALSO watch specific employers directly
> (their careers page / applicant-tracking system), which catches roles that aggregators
> miss or lag on.

## How the scout uses this
1. **Primary:** web search for your role + location + keywords across job boards
   (Google Jobs, Indeed, etc.) and company career pages.
2. **Enrichment:** for each employer listed below, fetch its careers/ATS page directly
   and merge any matching roles, de-duplicated against the web-search results.

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
