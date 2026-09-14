**Agent:** `coach`
**Execution:** interactive

Read `agents/coach.md` and `docs/jobfinderos-instructions.md` first.

Setup exception: the profile and rubric need not exist. Read `agents/scout.md` and `agents/mark.md` to understand input needs, without performing their tasks.

## Task
Interview a new user and turn the answers into their private configuration. Any career: teacher, nurse, marketer, electrician, engineer. Do not assume a technical field.

### Where things go (gitignored, private)
`config/profile.md` ← `config/profile.template.md` · `config/scoring_rubric.md` ← its template · `config/wins.md` ← its template · `config/voice.md` ← its template · `config/targets.md` ← its template (only if they name employers) · `vault/` created if missing. Personal answers go nowhere else. Never commit.

### The interview, one topic at a time, conversational
1. **Who you are:** current or most recent role, years, the through-line, what you're known for, in their words. Full name and the name they go by (outreach is signed with the short name).
2. **What you want next:** role families ranked; IC vs management; seniority; honest about stretch.
3. **Money:** minimum total comp; dealbreakers. Offer to research typical ranges if they don't know.
4. **Location and arrangement:** remote, hybrid, onsite; exceptions.
5. **Industries and exclusions:** wanted domains, profiles to avoid, employers never to surface (former employers usually belong here).
5b. **Target employers and timing:** any specific companies they want (Tier 1 = the few they most want, Tier 2, a watch list), the one function the weekday watch should check for, and the date they want an offer in hand. Offer to look up each Tier 1 company's careers page for the ATS URL table.
6. **Keywords:** the exact titles recruiters use for their targets now, plus field vocabulary. Suggest, let them refine. Mention that `/title-audit` will keep this current.
7. **Two or three real wins:** the most important part. STAR detail with numbers. These seed the Wins Library.
8. **Voice:** how they want to sound; hard rules; a short paragraph they wrote and like, if they have one.

### Generate
Fill each template. `profile.md` complete and in their voice, with a Contact block including the goes-by name, the seniority filter, the priority function, the target date, and the Target Companies section with its ATS URL table (empty rows are fine). `scoring_rubric.md` with weights matching what they said matters and concrete 10/6/2 anchors. `wins.md` with the wins in STAR form, metrics, tags, theme index. `voice.md`. `targets.md` if named. Confirm `.gitignore` covers every personal path.

### Finish
Summarize what was captured, then: `/jobs-scout` (find roles), `/jobs-daily` (the routine), `/profile` and `/story add` (deepen over time), `/title-audit` (check what your job is called now).

## Rules
- Career-neutral. Private data to gitignored paths only. Never commit, never send email.
- A thin profile is a working start; `/profile` deepens it later.
