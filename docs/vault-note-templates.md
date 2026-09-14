# Vault note templates

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
