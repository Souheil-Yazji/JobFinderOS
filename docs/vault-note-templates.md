# Vault note templates

### Company discovery queue — `vault/Tracking/Company Discovery Queue.md`

Mark owns all queue writes in Phases 1–2; Scout feedback is deferred. Use plain careers
URLs, `—` for unavailable optional cells, and `&#124;` for a literal pipe inside
a cell. Keep the table as the final content with a trailing newline for future
append-only feedback. Store review history in company evaluations.

```markdown
# Company Discovery Queue

| Company | Discovery source | Why it may fit | Date discovered | Status | Role found | Role score | Careers URL | Added by | Evaluation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

### Company universe — `vault/Tracking/Company Universe.md`

Mark owns this table. Company Fit is a numeric 1–10 weighted score, separate from
role fit. Evaluation links to `Companies/<Company>/Company Evaluation`. Careers
URL is a plain employer/ATS URL; unknown is permitted only outside direct tiers.
Keep lifecycle metadata above the table and decision history in evaluations.

```markdown
# Company Universe

| Company | Status | Company Fit | Category | Careers URL | ATS | Why It Fits | Last Evaluated | Evaluation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

### Company evaluation — `vault/Companies/<Company>/Company Evaluation.md`

```markdown
> **JobFinderOS:** Mark · YYYY-MM-DD HH:MM TZ

## Navigation
- [[Tracking/Company Universe]] · [[Tracking/Company Discovery Queue]] · [[Dashboard]]

# Company Evaluation — <Company>

## Discovery path
- Seed company/category, graph relationship, discovery source and date:

## Why this company
- Domain alignment:
- Technical-stack / demonstrated experience alignment:
- Relevant role types and historical hiring:
- Location / employment compatibility:
- Compensation evidence or unknown:
- Growth/hiring evidence:

## Company Fit
| Dimension | Weight | Score | Evidence / uncertainty |
| --- | --- | --- | --- |
| Domain/career fit | 25% | | |
| Probability of relevant roles | 20% | | |
| Technical-stack overlap | 20% | | |
| Compensation potential | 10% | | |
| Location/remote compatibility | 10% | | |
| Growth/hiring signal | 10% | | |
| Warm-path potential | 5% | | |

- **Weighted total:**

## Evidence
- Product/company source, source date and access date:
- Careers URL and ATS; verification date and result:
- Recent signal source; distinguish event date from publication date:

## Risks
- Fit concerns, unknowns, hiring/location concerns and blocked checks:

## Recommendation
- Tier 1 / Tier 2 / Watch / Dormant / Rejected, reason and capacity constraints:

## Decision history
| Date | Previous status | New status | Reason / new evidence |
| --- | --- | --- | --- |
```

### Company profile — `vault/Companies/<Company>/<Company>.md`

One profile per employer (funding, go-to-market, org, locations, **contacts**, **communication log**). Start with a **Navigation** block. When other notes exist in the same folder, a **Roles & docs** line lists wikilinks to them.

```markdown
## Navigation
- [[Dashboard]] · [[Companies/]] · [[Daily Digests/]] · [[Market Intel/]] · [[Email Follow-ups Queue]] · [[Outreach Drafts/]]
- **This company:** [[Companies/Acme/Acme]]
- **Roles & docs:** [[Companies/Acme/Acme — Role One]] · [[Companies/Acme/Acme — Role Two]]

# Acme

## Funding
## Go-to-market
## Org / team size
## HQ & locations
## Employee distribution (remote / office)

## Contacts
| Name | Role | Relationship | Last touch | Notes |
|------|------|--------------|------------|-------|

## Communication log
| When | Channel | Summary |
|------|---------|---------|
| YYYY-MM-DD HH:MM TZ | Email / call / LinkedIn | What happened |
```

### Opportunity note — `vault/Companies/<Company>/<Company> — <Role>.md`

```markdown
## Navigation
- [[Dashboard]] · [[Companies/]] · [[Companies/Acme/Acme]] (company profile) · **this role:** [[Companies/Acme/Acme — Head of Field Operations]]
- **Posting:** [Job posting](https://...)
- **Also at this company:** [[Companies/Acme/Acme — Other Role]]
- [[Daily Digests/]] · [[Market Intel/]] · [[Email Follow-ups Queue]] · [[Outreach Drafts/]]

## Overview
- **Company:** 
- **Role:** 
- **Stage:** 🔍 Spotted
- **Score:** X/10
- **Location:** 
- **Comp range:** 
- **Source:** (company careers page / Greenhouse / Lever / Ashby / etc.)
- **Job URL:** 
- **Date spotted:** YYYY-MM-DD
- **Date applied:** 
- **Human path:** (warm contact / alumni / recruiter / named hiring manager, or `cold — no human attached`; playbook §2)

## Why This Role
[2–3 sentences connecting the role to the candidate's background]

## Key Contacts
*(for 8+ roles, multi-thread per playbook §7: recruiter, hiring manager, the hiring manager's boss, a team peer)*
| Name | Title | Thread role (recruiter/HM/boss/peer) | Email/LinkedIn |
|------|-------|--------------------------------------|----------------|

## Timeline
| When | Event |
|------|-------|
| YYYY-MM-DD HH:MM TZ | Spotted by scout |

## Notes & Research

## Outreach / Cover Letter
[Link to Outreach Drafts/ note or inline draft]
```

Stages: `🔍 Spotted` → `📝 Applied` → `📞 Screen` → `🧑‍💼 HM round` → `🏁 Final` → `🎉 Offer`, plus `❌ Closed` and `⚫ Presumed dead` (silence norms, playbook §4).

### Daily digest — `vault/Daily Digests/YYYY-MM-DD.md`

```markdown
**Run:** YYYY-MM-DD HH:MM TZ

> **JobFinderOS:** Jobs · YYYY-MM-DD HH:MM TZ

# Daily Digest — YYYY-MM-DD

## New Opportunities (scored 7+)
| Company | Role | Score | Source | Link |
|---------|------|-------|--------|------|

## Recruiter Emails to Review
| From | Subject | Date | Recommended Action |
|------|---------|------|--------------------|

## Application Updates
| Company | Role | Stage | Notes |
|---------|------|-------|-------|

## Action Items
- [ ] 

## Recruiter's read
```

### Outreach draft — `vault/Outreach Drafts/Company — Role — Type.md`

```markdown
# Outreach: Company — Role

**Type:** Cover Letter / Cold Email / LinkedIn Note
**Status:** Draft / Ready to send / Sent

---

[Draft content]

## Before you send
- [ ] Claims to verify:
- [ ] Sources to read first:
- [ ] `[YOUR TAKE]` slots filled in your own words
```

---
