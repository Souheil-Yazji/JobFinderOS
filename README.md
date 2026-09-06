# JobScoutOS

An agentic job search that runs on [Claude Code](https://claude.com/claude-code). Three agents work for one candidate: a **recruiter** who exercises judgment and gets you ready for every room, a **crawler** who scans employers' own careers pages, and a **market analyst** who reads the signals that precede job postings. Everything they produce lands in an [Obsidian](https://obsidian.md) vault you own.

It was built and used for one real search, then scrubbed and generalized. It works for any career: the agents learn who you are from an interview, not from a hardcoded profile.

## What makes it different

- **It behaves like a recruiter, not a job board.** Every run ends with a candid "Recruiter's read": what the pipeline means, what pattern is forming, what you are avoiding. Losses get a postmortem and feed an objection log.
- **Warm-path-first.** An application without a human attached is the last resort. The agents name who you know or can reach before anything is queued, and sequence outreach before the application.
- **Anti-AI-spam by design.** Low outreach volume, a two-fact rule for every message, and a hard gate that nothing drafted in your voice may read as AI-written. The agents never send anything; drafts go to your clipboard and you send them from your own client.
- **No API keys.** Reasoning is your Claude Code subscription. Email is the Gmail MCP connector (read only). Scheduling is macOS launchd. The vault is a folder on disk.
- **Private by default.** Your profile, rubric, wins, stories, and vault are gitignored. Nothing about you is in this repo, and nothing the agents write goes anywhere you did not put it.

## Requirements

- macOS (scheduling uses launchd; the skills themselves run anywhere Claude Code runs)
- [Claude Code](https://claude.com/claude-code) installed and logged in (`claude auth login`)
- Python 3.11+ with PyYAML (`pip install -r requirements.txt`) for the scheduler and helper scripts
- [Obsidian](https://obsidian.md) to read the vault (optional; it is plain Markdown)
- Gmail connected as an MCP connector in claude.ai, if you want the inbox triage

## Quick start

```bash
git clone <this repo> JobScoutOS && cd JobScoutOS
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
claude
```

Then, inside Claude Code:

```
/onboard          # 15-minute interview → config/profile.md, scoring_rubric.md, wins.md, voice.md
/jobs-scout       # first scan of your target companies' careers pages
/jobs-daily       # the everyday routine: market pulse + scout → email → digest → Recruiter's read
/whats-next       # "what should we do next?" — the highest-leverage actions, done together
```

Open `vault/` in Obsidian. `Dashboard.md` is the daily read, `Strategy.md` the weekly one.

## How it is put together

```
.claude/agents/      coach.md · scout.md · mark.md     ← the personas (Claude Code subagents)
.claude/commands/    25 skills                         ← thin task prompts; each names its agent
config/              templates + the recruiter playbook ← your private copies are gitignored
scripts/             launchd scheduler, guards, ATS poller, retention pruner
vault/               the Obsidian vault (skeleton only in git)
CLAUDE.md            project instructions the agents read every run
```

| Agent | Job | Tools |
|-------|-----|-------|
| `coach` | Pipeline judgment, prep, mock interviews, drafting, voice checks, postmortems, inbox triage, the digest | All tools incl. Gmail (read only) |
| `scout` | ATS-direct scanning, scoring, opportunity notes, the weekday watch | Web + vault |
| `mark` | Funding, leadership moves, renames, weekly briefs, company deep-dives | Web + vault |

The doctrine they share is `config/recruiter_playbook.md`: the Recruiter's read, the warm-path gate, the authenticity rules, silence norms, funnel math, multi-threading, offer orchestration, the objection log, deadline math. Read it once; it is the reason the system works.

### Skills

| Skill | What it does |
|-------|--------------|
| `/onboard` | First run. Interviews you and generates your private config. Career-neutral. |
| `/jobs-daily` | The everyday driver: pulse + scout in parallel, then email, then digest, then one Recruiter's read |
| `/jobs-scout` · `/jobs-priority-watch` | Scan employers' own careers pages and ATS boards; the watch is a narrow weekday check on your priority function |
| `/jobs-email` · `/email-watch` | Gmail triage, rejection sweep, interview detection with auto-prep; flags replies due, drafts only on yes |
| `/jobs-digest` | The morning briefing, a scoped Dashboard refresh, a warm-path coverage check |
| `/mark-pulse` · `/mark-weekly` · `/mark-profiler` · `/jobs-research` | Market signals, the weekly brief and Strategy pass, company deep-dives |
| `/whats-next` · `/checkin` | The two conversational drivers: choose the next move, or sync the pipeline |
| `/warm-path` · `/network-outreach` · `/draft-message` · `/voice-check` | Attach a human, find peers, draft in your voice, gate every draft for AI tells |
| `/jobs-prep` · `/mock-interview` · `/day-of-card` · `/story` | Interview prep grounded in your story library, a simulated round, the one page for the room |
| `/jobs-cover` · `/postmortem` · `/title-audit` · `/profile` | Cover letters, loss analysis, search-vocabulary audits, progressive profiling |

Every skill is a short Markdown file in `.claude/commands/`. Read one to see the pattern, then write your own.

## Scheduling

```bash
bash scripts/JobScoutOS_install_launchd.sh          # one launchd job; ticks every 30 min while the Mac is awake
JOBS_DAILY_HOUR=7 MARK_WEEKLY_WEEKDAY=1 JOBSCOUTOS_TZ=America/New_York bash scripts/JobScoutOS_install_launchd.sh
python3 scripts/scheduler_tick.py --dry-run          # what would run now
bash scripts/JobScoutOS_install_helpers.sh           # optional: ATS poller, retention pruner, pointer notes
```

The tick runs `/jobs-daily` once a day, `/mark-weekly` once a week, and the priority watch on weekdays, all through `claude -p`. Times and timezone live in `config/scheduler.yaml`. Details and failure triage: `vault/Automation/JobScoutOS — Local Runbook.md`.

The optional **ATS poller** (`scripts/jobscoutos_ats_poll.py`) is deterministic: it hits Greenhouse, Ashby, and Lever JSON APIs for the boards in `config/ats_boards.yaml`, applies your title, location, and comp filters, and appends only genuinely new reqs to `vault/Market Intel/ATS Inbox.md` for the digest to score. Copy `config/ats_boards.example.yaml`, edit the `filters:` block, run `--seed` once, then `--dry-run`.

## Privacy and safety

- `config/profile.md`, `scoring_rubric.md`, `wins.md`, `voice.md`, `targets.md`, `stories.md`, `ats_boards.yaml`, and all vault content are gitignored. If you want your vault backed up, do it in a private repository and remove those rules yourself.
- Agents never commit, never push, never send email, never create Gmail drafts. There is no code path to a send API.
- Gmail access is the claude.ai MCP connector, so credentials never touch this repo.

## Known limits

- The ATS poller's location classifier speaks US geography (remote-US, hub cities, a home region). The vocabulary is a handful of regexes at the top of the script; edit them for another country.
- launchd is macOS only. On Linux, point cron at `scripts/scheduler_tick.py` instead.
- The Gmail skills assume the Gmail MCP connector. Without it, `/jobs-email` and `/email-watch` are no-ops and everything else still works.
- Skills are prompts, not code. They are only as good as the profile `/onboard` writes; spend the 15 minutes.

## License

MIT. See `LICENSE`.
