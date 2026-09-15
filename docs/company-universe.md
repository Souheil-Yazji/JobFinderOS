# Durable company discovery

Mark discovers and qualifies employers. Scout discovers and qualifies roles.
Coach decides candidate attention, outreach and applications. A company promotion
authorizes future research, not an application or a message.

## Current scope: Phases 1–2

Only manual Mark company discovery/evaluation is enabled. The queue and universe
persist, but they do not yet change Scout's scan set. Scout feedback, weekly
integration and monthly audits are later phases. Existing target inputs and
scheduling remain unchanged. Invoke discovery through
`./scripts/JobFinderOS_run_agent.sh mark company-discovery`.

## Records and ownership

- `vault/Tracking/Company Discovery Queue.md`: Mark owns all writes in this phase.
  Role-evidence columns reserve space for the future Scout feedback loop.
- `vault/Tracking/Company Universe.md`: Mark owns company scores, tiers and review
  dates. This is the persistent source of truth for discovered companies.
- `vault/Companies/<Company>/Company Evaluation.md`: Mark's evidence, dimension
  scores, risks, recommendation and dated decision history. This company score is
  separate from Scout's role score and does not replace other company notes.
- `vault/Market Intel/Jobs Handoff.json`: existing market handoff. Discovery does
  not update it in this phase; later optional changes must not replace the universe.

Create absent tracking notes from `docs/vault-note-templates.md`; absence on the
first run is empty state, not a missing research dependency. Keep filled records
private; templates ship in docs. Do not repurpose `Tracking/Companies.md`, which
tracks the opportunity pipeline.

## Discovery and evidence

Read the profile, role rubric, wins if present, Strategy and prior evaluations.
Derive and evolve discovery categories from the candidate's actual lanes and
proven strengths. No fixed industry or technology list belongs in the code.
For each Tier 1 seed, explore competitors, partners, adjacent categories, major
customers/integrations, related investor portfolios, open-source peers and stack
neighbors. Record seed, relationship, source URL and date so findings accumulate
into a market graph. Rotate seeds/categories to avoid repeated coverage.

Review queued companies before discovering roughly 10–20 new companies per discovery
cycle. This is a research budget, not a quota: fewer supported evaluations and zero
promotions are valid. Never invent companies, sources or signals to fill a list.
Normalize case/spacing and verified aliases for deduplication; check both tracking
notes, profile targets, existing company notes and prior rejected evaluations.
Do not merge distinct employers merely because their names resemble each other.

Use primary product/company, careers, leadership and dated market sources. Read
postings only to establish company hiring patterns; do not score or recommend
vacancies as Mark. Historical relevant teams count without current openings.
Record source dates and distinguish historical hiring from live availability.
A careers landing page does not verify a live role.

Each evaluation needs domain fit, stack/experience overlap, relevant role families,
location evidence, compensation evidence or unknown, growth/hiring evidence, risks,
unknowns, source URLs and access dates, a verified careers URL and ATS type (or
`Company site` / `Unknown`). Do not guess ATS slugs. No direct-tier promotion without
adequate fit evidence and a verified employer careers/ATS URL. Failed source access
remains pending with a specific blocker; it is not a rejection.

## Company rubric

Score each dimension from 1 to 10; weighted scores sum to a 1–10 company fit.
Interpret anchors using the candidate's profile and role rubric. Candidate hard
filters take precedence. Never silently relax location constraints.

| Dimension | Weight | High / medium / low anchors |
|---|---:|---|
| Domain/career fit | 25% | 10 core business matches top lanes; 8 strong adjacency; 6 relevant teams; 4 weak alignment; 2 little connection |
| Probability of relevant roles | 20% | 10 repeated relevant hiring/established function; 6 credible team with limited history; 2 little evidence of the function |
| Technical-stack overlap | 20% | 10 immediate credibility from proven skills; 6 transferable experience with gaps; 2 major retraining |
| Compensation potential | 10% | 10 evidenced strong relevant bands; 6 unknown or plausible; 2 evidenced incompatibility with the profile |
| Location/remote compatibility | 10% | 10 evidenced preferred employment arrangement; 6 uncertain, flag; 2 incompatible unless the profile permits an exception |
| Growth/hiring signal | 10% | 10 current relevant expansion; 6 stable/unknown; 2 freeze, distress or shrinking relevant teams |
| Warm-path potential | 5% | 10 documented usable relationship; 6 evidenced reachable functional lead; 2 no established route |

Unknown compensation scores 6 and never causes rejection on its own. A public name
is not a relationship. Missing evidence lowers confidence, not invents facts. Write
each component, weighted total and justification in the evaluation. Apply thresholds
to the unrounded total and display two decimals.

| Company Fit | Eligible status |
|---|---|
| 8.5–10 | Tier 1 candidate; Tier 2 or Watch if capacity/evidence warrants |
| 7.5–less than 8.5 | Tier 2; Watch if capacity/evidence warrants |
| 6.5–less than 7.5 | Watch |
| Below 6.5 | Rejected, or Dormant for previously relevant companies |

Mark may promote qualified companies automatically within these limits; Coach
still owns attention and application decisions. Keep at most 10 universe Tier 1
and 25 universe Tier 2 rows, with roughly 20–40 Watch companies. Never pad tiers.
The union of explicit targets and automatic direct targets has a budget of 35:
count deduplicated explicit profile/targets companies first and use remaining slots
for the strongest universe targets. Keep overflow in Watch with the capacity reason.
If explicit targets alone exceed 35, honor them, stop automatic expansion and ask
the candidate to narrow the explicit set.

Profile exclusions always win. Mark never rewrites explicit profile/targets choices;
a universe demotion cannot silently remove them from Scout's explicit scan set.
Flag conflicting manual targets for Coach/candidate review. Keep rejected/dormant
records and history. Reevaluate rejected companies only on a materially new signal
or a changed profile; record what changed. An audit date alone is not new evidence.
Hard exclusions cannot be reopened by market news. For current targets, review
available Scout summaries: repeated wrong seniority, geography, compensation or
irrelevant roles can reduce the corresponding company dimensions; repeated strong
roles can increase confidence. Record dates and sources, not an arbitrary score
penalty. Access failures and unscanned companies are unknowns, not negative hiring
evidence. Do not alter Scout to collect this feedback in Phases 1–2.

## State transitions and handoff

Queue: `unreviewed` → `evaluating` → `promoted` or `rejected`. Keep blocked research
`evaluating` with its blocker in the evaluation. `promoted` means an evaluation
entered the universe, including Watch/Dormant; it does not imply a direct scan.
Write the evaluation and universe before marking the queue processed. Retry
incomplete work in place so partial runs cannot lose discoveries.

Universe: `Tier 1`, `Tier 2`, `Watch`, `Dormant`, `Rejected`. Date evaluations and
record old/new status, reason and sources in the evaluation's decision history.

## Deferred integrations and recommended Phase 3

Phase 3 should add the deduplicated union of profile Tier 1/2, explicit
`config/targets.md`, and universe Tier 1/2 to the normal Scout scan. Preserve
exclusions and explicit-target precedence, verify careers URLs, and honor the
35-company budget. Watch/Dormant/Rejected are not automatic direct targets.
Test consumption of promoted employers, missing URLs, duplicate aliases, rejected
companies and backward compatibility of explicit targets with fictional sources.
The narrow weekday watch should not grow implicitly.

Phase 4 adds append-only Scout feedback: company, strong role, role score, source,
careers URL if known and relevance reason. Mark alone evaluates or assigns tiers.
Phase 5 runs discovery within Mark weekly, with no separate scheduler. Optional
handoff arrays `new_companies`, `promoted_companies`, `demoted_companies` should
preserve existing fields and use objects containing company, previous/new status,
reason, careers URL and evaluation link. They supplement the durable universe.

Phase 6 adds a monthly mode inside Mark weekly: review stale targets, category
balance, emerging clusters, title changes and the quality of Scout's outcomes.
Demote low-value targets while retaining decision history; preserve manual targets
and never treat failed source access as an empty market. Timing and completion
markers will be implemented in that phase, not in the current scheduler.

## Verification

Before completion, check unique companies, valid statuses/dates, seven score
components and total, thresholds/capacity, careers/evidence links, queue-to-universe
consistency and preserved history. State coverage and unresolved
evidence gaps. Output auditing enforces ownership and basic table validity; it cannot establish the truth of web evidence.

### Phase 1–2 validation — 2026-09-15

- All 36 automated tests passed with the project virtual environment, including
  company-table validity, ownership, tier limits, privacy and the new task routing.
- Static verification accepted 27 agent/skill pairs; scheduler dry-run passed.
- Two real CLI invocations of `mark/company-discovery` ran in an isolated temporary
  repository using only `tests/fixtures/fictional/company-discovery.md` and the
  fictional profile/rubric. No real candidate records or live research were used.
- The first invocation persisted two evaluations: New Widgets, Tier 1 at 9.80,
  and Paper Forms, Rejected at 2.40. Component arithmetic, evidence URLs, offline
  labels, queue/universe consistency and absence of opportunity notes were checked.
- The repeat invocation changed no files and did not reopen the rejection or
  duplicate either company. Both runs exited zero with no boundary violations.
- Full operational verification remains separate: the local workspace had no
  daily digest for 2026-09-15. These tests do not verify live careers-source access.
