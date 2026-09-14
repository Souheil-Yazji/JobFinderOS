**Agent:** `coach`
**Execution:** batch

Read `agents/coach.md` and `docs/jobfinderos-instructions.md` first.

## Task
Args: company, role, optional job URL. Invoking this skill with a target is the candidate's yes to draft.

1. Read `config/profile.md` (background, strengths, current employer) and `config/voice.md` if present. Scan `config/stories.md`; if a story's themes match the role, read its full `vault/Stories/` file and use its cover-letter hook and key lines as the proof material. Never re-invent a locked telling.
2. Research the company first, direct from its own site and the posting: product, funding, GTM, and the specific role.
3. Write the letter connecting the candidate's background to concrete, specific things about this company and this role. Present tense for the current employer. No generic flattery, no bullet structure, no filler that could apply to any company. One specific, verifiable detail per paragraph that proves the homework.
4. Run the `/voice-check` scan on it before saving.
5. Save to `vault/Outreach Drafts/<Company> — <Role> — Cover Letter.md` using the Outreach draft template in `docs/vault-note-templates.md`, with a "Before you send" list of anything to verify.
