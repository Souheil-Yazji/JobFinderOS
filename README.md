<p align="center">
  <img src="assets/hero.svg" width="352" alt="Clawd, the Claude Code mascot, in a prospector's hat with a pickaxe and a gold nugget">
</p>

<h1 align="center">JobFinderOS</h1>

<p align="center"><b>Find your next job with local AI agents. No coffee breaks, no doomscrolling, no sleep till you're hired!</b></p>

This project capitalizes on one simple fact:  a career search is a numbers game. More real contacts lead to more listings you hear about early, more of those become applications with a person attached, and more of those become interviews. A single human running that chain alone has limited hours in the week. Agents do not. JobFinderOS is a local agent project that puts agents to work on your search, profiling markets, following companies, crawling job postings, identifying new strategic contacts and preparing you for every interview. Each stage of the job search funnel gets more nurturing than you could feed it yourself, and the judgment stays with you.

This manual covers four things:

1. [What it is](#1-what-it-is)
2. [Getting up and running](#2-getting-up-and-running)
3. [Using it](#3-using-it)
4. [The methodology: how agentic job search works here](#4-the-methodology)

Plus a short [reference](#5-reference) and a note on [contributing](#contributing) at the end.

---

## 1. What it is

JobFinderOS is a set of agent personas and skills that run through Codex CLI (with Claude compatibility) and work for you to identify career opportunities based on your criteria. They watch the market, find roles, keep your pipeline up to date and honest, and get you ready for every interview. They write everything to a folder of Markdown notes, which you can open in [Obsidian](https://obsidian.md) or any text editor.

**Three agents, each with one job.**

<p align="center">
  <img src="assets/coach.png" width="114" alt="Coach: Clawd in a ball cap holding a clipboard">&nbsp;&nbsp;&nbsp;
  <img src="assets/scout.png" width="114" alt="Scout: Clawd in a bucket hat with binoculars">&nbsp;&nbsp;&nbsp;
  <img src="assets/mark.png" width="114" alt="Mark: Clawd in a green eyeshade reading ticker tape">
  <br>
  <sub><b>Coach</b>, the recruiter &nbsp;·&nbsp; <b>Scout</b>, the crawler &nbsp;·&nbsp; <b>Mark</b>, the market analyst</sub>
</p>

| Agent | What it does | What it can touch |
|---|---|---|
| **Coach** | The recruiter brain. Judges the pipeline, preps you for interviews, runs mock interviews, keeps your career stories, drafts outreach and cover letters in your voice, checks drafts for AI tells, writes a postmortem on every loss, and produces the morning digest. | Everything, including reading your Gmail. Never sends. |
| **Scout** | The crawler. Scans your target companies' own careers pages, scores each role against your rubric, and logs the good ones as opportunity notes. | Web and the vault. No email. |
| **Mark** | The market analyst. Tracks funding, leadership moves, new team build-outs, and job-title renames at the companies you care about, and tells Scout and Coach where to look next. | Web and the vault. No email. |

> [!IMPORTANT]
> **🔒 Privacy by Design**
>
> Candidate records live in local `config/` and `vault/`. Private configuration, generated notes and logs are gitignored. Some shipped vault skeletons (Dashboard, Strategy, tracking tables and automation notes) remain tracked; keep filled-in versions out of commits. The selected CLI/model service processes the information a session reads. Job-search automation never commits, pushes, sends messages, or creates Gmail drafts.

**Skills are the tasks you run.** Each is a short Markdown prompt in `skills/`, with an owner listed in `config/skill_agents.yaml`. There are 25 user-facing tasks plus an internal daily finalizer. Run them with `./scripts/JobFinderOS_run_agent.sh <agent> <skill>`. Section 3 uses `/skill` as shorthand for task names; those remain native slash commands only in the retained Claude compatibility files.

**Your config is what they read first.** `config/profile.md` says who you are and what you want. `config/scoring_rubric.md` says how to score a role. `config/recruiter_playbook.md` says how the agents behave. Section 4 explains that playbook in plain English.

**The vault is where everything lands.** `vault/Dashboard.md` is the daily read. `vault/Strategy.md` is the weekly one. Every company gets a folder under `vault/Companies/` with a profile and one note per role. Digests, market briefs, outreach drafts, and interview prep all have their own folders.

**What it never does.** It never sends an email or a message. Drafts go to your clipboard and the vault, and you send them from your own client. It never mass-applies. It never sits in the interview.

**What it needs.** An installed, authenticated Codex CLI and Python with the dependencies in `requirements.txt`. The runner uses saved CLI authentication; no direct LLM API integration is required.

---

## 2. Getting up and running

Four steps, starting in your terminal. Onboarding opens an interactive session.

### Step 1. Get Codex CLI

Install Codex CLI and authenticate it. [Official CLI documentation](https://developers.openai.com/codex/cli).

```bash
codex login
```

### Step 2. Clone and install

Paste this block as one piece:

```bash
git clone https://github.com/Souheil-Yazji/JobFinderOS.git
cd JobFinderOS
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Use Python 3.11 or newer as recommended by the project. Python runs the agent entrypoint, scheduler and deterministic helpers.

### Step 3. Teach it who you are

From the repository root:

```bash
./scripts/JobFinderOS_run_agent.sh coach onboard --interactive
```

This is a 15-minute conversation. It asks about your current role, what you want next, your salary floor, where you will and will not work, companies to avoid, the exact job titles recruiters use for your target, and two or three real wins with numbers. Any career works. It does not assume you are technical.

When it finishes you have four private files, all gitignored:

| File | What it holds |
|---|---|
| `config/profile.md` | Who you are, targets, comp floor, location rules, exclusions, target companies with their careers-page URLs |
| `config/scoring_rubric.md` | How to score a role from 1 to 10, weighted by what you said matters |
| `config/wins.md` | Your wins in situation-task-action-result form, used in prep and cover letters |
| `config/voice.md` | How you write, so drafts sound like you |

### Step 4. Run the first scan

```bash
./scripts/JobFinderOS_run_agent.sh scout jobs-scout
```

Scout reads your target companies' careers pages, scores what it finds, and writes an opportunity note for anything that clears your bar. Open `vault/` and read `Dashboard.md`. You are running.

### Optional extras

Each of these is independent. Add them when you want them.

- **Obsidian.** Open `vault/` as a vault in [Obsidian](https://obsidian.md) to read the notes with working links. Any text editor works too.
- **Gmail.** Configure a Gmail read connector in your selected CLI runtime; Claude connector setup does not transfer automatically to Codex. Coach can then triage recruiter email, spot interview invitations, and detect rejections. It is instructed to read only; Section 5 explains what that rests on.
- **A schedule (macOS only).** Drafts are copied to the clipboard with `pbcopy` and the scheduler uses launchd, so this part is Mac-specific. Elsewhere, drafts still land in the vault and you run the skills by hand.

  ```bash
  bash scripts/JobFinderOS_install_launchd.sh
  ```

  One LaunchAgent ticks every 30 minutes. When a window in `config/scheduler.yaml` comes due it runs `/jobs-daily` (every day), `/mark-weekly` (once a week), and a narrow weekday watch on your priority function. Your Mac has to be awake. A missed run catches up on the next tick. Runs are logged to `logs/` and mirrored to `vault/Automation/`.

  Check it is working:

  ```bash
  python3 scripts/scheduler_tick.py --dry-run
  bash scripts/verify_local_automation.sh
  ```

---

## 3. Using it

Every skill run ends with a **Recruiter's read**: two to five sentences of candid advice about what today's state means and what you are avoiding. It is never a recap. Read it.

### Every day

<img src="assets/coach.png" width="40" alt="Coach"> **Coach** runs these. `/jobs-daily` runs Mark, Scout, Coach email, Coach digest, then Coach finalization in separate sequential sessions. Each step reads the completed inputs recorded by the runner.

```
/jobs-daily     Separate Mark and Scout runs, then Coach email, digest, and finalization.
/checkin        Tick boxes on the Dashboard, tell it what happened, it ages every thread.
/whats-next     "What should we do next?" It sweeps the pipeline and offers the 3 to 5 best moves.
```

If you run one thing a day, run `/whats-next`. It is a conversation: pick a move, do it together, the vault updates, the list re-ranks.

### Before you apply

<img src="assets/coach.png" width="40" alt="Coach"> **Coach** runs these.

```
/warm-path <Company>       Who do you know, or can reach, there? Returns a verdict and dates.
/network-outreach <Co>     Finds 2 or 3 peer-level people and drafts a research-backed note.
/draft-message             A reply, nudge, thank-you, or cold note. Copies to clipboard.
/voice-check               Scans any draft for AI tells. PASS, REWRITE, or DO NOT SEND.
```

The rule behind this is in Section 4.2. Short version: find a human first, apply two or three days later.

### Researching a company

<img src="assets/mark.png" width="40" alt="Mark"> **Mark** runs these.

```
/jobs-research <Company>   Business, funding, leadership, product, how they sell, open roles, an angle.
/mark-profiler <Company>   A deeper evaluation for a real decision. Scored, with a verdict.
/title-audit               Reads live postings and tells you what your job is called right now.
```

### When interviews start

<img src="assets/coach.png" width="40" alt="Coach"> **Coach** runs these.

```
/jobs-prep <Company> <Role> <Stage>    Full prep brief: company, round, and every person in the room.
/mock-interview <Company> <Round>      Plays the interviewer in character. Scores each answer.
/day-of-card <Company> <Round>         One page to have open: beats, lead stories, questions, traps.
/jobs-cover <Company> <Role>           A cover letter built from research, in your voice.
/story add | find | update             Your career story library. Prep and covers draw from it.
```

### After a loss

<img src="assets/coach.png" width="40" alt="Coach"> **Coach** runs these.

```
/postmortem <Company>      Classifies the objection, logs it in Strategy.md, names the fix.
/profile                   Deepens your wins and voice files over time.
```

### The rest

`/mark-pulse`, `/jobs-scout`, `/jobs-email`, and `/jobs-digest` are the pieces `/jobs-daily` is made of. Run them alone when you want one piece. `/mark-weekly` is the weekly brief and Strategy pass, `/email-watch` is a read-only inbox briefing, and `/jobs-priority-watch` is the narrow weekday scan the scheduler runs.

### Reading the vault

| Note | When to read it |
|---|---|
| `vault/Dashboard.md` | Every morning. Funnel pulse, plays for today, live threads, aging applications. |
| `vault/Strategy.md` | Weekly. Positioning, the objection log, funnel history, proof assets, deadline math. |
| `vault/Daily Digests/` | The morning briefing for each day. |
| `vault/Companies/<Company>/` | One profile per company plus one note per role, with contacts and a timeline. |
| `vault/Tracking/` | Contacts, the email follow-up queue, the company index. |
| `vault/Outreach Drafts/` | Every draft the coach has written. Nothing here has been sent. |
| `vault/Market Intel/` | Weekly briefs, the market pulse, and the handoff file Mark writes for Scout. |

---

## 4. The methodology

This is the operating doctrine the agents follow, written for a person. The source is `config/recruiter_playbook.md`. Everything here came out of running one real search for five months and studying what worked.

### 4.1 Act like a recruiter, not a clerk

A job board shows you listings. A recruiter tells you what your pipeline means, which thread is dying, which play you are avoiding, and when a pattern has formed. That is the coach's job. The Recruiter's read at the end of every run is the mechanism. If it is uncomfortable, it is working.

### 4.2 Attach a human before you apply

An application with no human attached is the last resort, not the default. Before anything is queued, the agents walk a ladder: people you already know at the company, former colleagues who moved there, the hiring manager and their boss by name, a named recruiter. Outreach goes first. The application follows 48 to 72 hours later, so a mention inside the company lands before your resume hits the pile.

When the ladder comes up empty, the application is logged as cold. The system tracks the ratio and aims for 70 percent warm. In the search this was built on, every single rejection was a cold application. Not most. All.

### 4.3 Never sound like a machine

Everyone on the hiring side reads AI-written messages all day and is pattern-matching for them. One detected template can quietly end a conversation, and the people in your field talk to each other. So:

- **Low volume by design.** At most 3 new people a day, 10 a week. At most 2 follow-ups per thread, then park it for 30 days. Never two similar messages to two people at one company.
- **The two-fact rule.** Every outbound message carries one fact that took real work to find, with the source cited so you can read it first, and one thing only you could say. Missing either, it does not go. Silence beats generic.
- **You send everything.** Drafts land on your clipboard with a "before you send" checklist and slots you have to fill in your own words. The agents never send, never schedule, never create a Gmail draft.
- **The voice gate.** Nothing drafted for you may read as AI-written. No em dashes, no "I hope this finds you well," no perfectly balanced three-part sentences, no flattery openers. `/voice-check` enforces it.

### 4.4 Silence is data

Every thread is aged against a table of norms. An application at a small company with no reply after 14 days is presumed dead. After a recruiter screen, 7 days of silence means you are the backup candidate, so open a second thread at a comparable company now. A warm contact who has not answered in a week is busy, not hostile, so one bump with a new angle, then park. Presumed-dead threads stop getting your energy. If one revives, that is a bonus, not a plan.

### 4.5 Every loss becomes intelligence

After any rejection, withdrawal, or 30-day ghost, `/postmortem` classifies the objection, both what they said and what they probably meant: domain-proof gap, level mismatch, location, comp, slate, culture, unknown. It goes into the objection log in `Strategy.md`. Three of the same objection is a positioning problem, not bad luck, and the fix becomes a strategy action. Nine postmortems in the original search surfaced the pattern that changed its whole back half.

### 4.6 Check what your job is called now

Job titles move, and postings are the trailing indicator. Mark watches for renames at your target companies. `/title-audit` reads their live postings, tallies the vocabulary, and hands you the exact terms to put in your profile and saved searches. In the original search the target role had been renamed at the companies that mattered. The winning listing arrived three weeks after the search terms changed, under the new name. The crawler never found it. The rename did.

### 4.7 Spend AI on depth, not volume

Mass-applying stopped working for everyone at about the same time, because everyone can do it now. The edge moved to the rooms. AI makes serious preparation cheap: a research brief per round, a profile on every interviewer, mock interviews, cover letters that start from research, a story library you know cold. That is where the time saved by the agents should go.

### 4.8 Run the pipeline like a funnel

Stages are Applied, Screen, Hiring-manager round, Final, Offer, tracked separately for warm and cold. The weekly Strategy pass does the math out loud. If cold applications are not converting to screens, more cold applications are not the answer. If screens are not converting to hiring-manager rounds, the leak is your narrative. Two more rules from the same section: every serious opportunity gets multi-threaded (recruiter, hiring manager, their boss, a peer) so one silence cannot kill it, and when any process reaches the hiring-manager stage, accelerate the two best comparable ones so offers land in the same ten days. Never bluff an offer that does not exist.

### 4.9 Work backward from a date

Set a deadline for having an offer in hand. Finals two weeks before that, hiring-manager rounds a month before, screens six weeks before, warm plays now. Every weekly read says in plain terms whether the current pace hits the date and what would change it.

---

## 5. Reference

### Layout

```
agents/              coach.md · scout.md · mark.md         canonical personas
skills/              25 tasks + daily finalizer             canonical tasks
.claude/             retained Claude compatibility
config/skill_agents.yaml                                 explicit ownership
config/              profile, rubric, wins, voice, targets  your copies are gitignored; templates ship
config/recruiter_playbook.md                               the doctrine in Section 4, in full
scripts/             scheduler, guards, ATS poller, pruner
vault/               the Obsidian vault
AGENTS.md            repository routing and contributor rules
docs/                shared task instructions and vault templates
CLAUDE.md            retained Claude project instructions
```

### Email safety

No code in this repository calls a send or draft API. Coach can use configured email read tools; Scout and Mark must not access email. The agent definitions and shared doctrine prohibit sending, forwarding, replying through APIs, and creating Gmail drafts. Output auditing detects prohibited file changes, but is not a tool-level email access lock. A missing connector must be reported as blocked; it is never interpreted as an empty inbox.

### Privacy

Your profile, rubric, wins, stories, voice notes, and vault contents are gitignored. Nothing about you ships in this repo, and nothing the agents write goes anywhere you did not put it. If a company you are applying to has guidance on AI use in applications, follow it: you draft first, the coach refines.

### Retention

Daily digests, run summaries, and daily briefs keep 30 days. Weekly briefs keep 90. A weekly launchd job prunes the rest. The vault is gitignored here, so if you want a permanent archive, back it up to a private repository of your own. Anything worth keeping lives in `Strategy.md`, `Tracking/`, or `Companies/`, never in an old digest.

### Manual runs and logs

```bash
python3 scripts/scheduler_tick.py --dry-run             # what would run right now
bash scripts/JobFinderOS_run_skill.sh jobs-daily jobs-daily   # run one skill the way the scheduler does
bash scripts/JobFinderOS_check_local_runner.sh          # check the selected runtime and authentication
tail -f logs/launchd-runs.log                            # watch runs
```

### Credits

The pixel character is Clawd, the Claude Code mascot. He belongs to Anthropic and is redrawn here in work clothes, with affection and no affiliation.

The three agents are the same character in different gear. Coach wears the ball cap and carries the clipboard. Scout has the bucket hat and binoculars. Mark wears the green eyeshade and reads the ticker tape. The drawings live in `assets/` as SVG sources; the three agent icons also ship as PNGs because GitHub collapses SVGs inside Markdown tables.

### Writing your own skill

Copy a task from `skills/`, retain its Agent and Execution headers, and add its owner to `config/skill_agents.yaml`. Keep persona doctrine in `agents/`. Validate with `bash scripts/verify_local_automation.sh --static`.

---

## Contributing

Issues and pull requests are welcome. Bug reports, wording fixes, and "this claim does not match the code" are all useful.

The most valuable contribution is a new skill. Each canonical file in `skills/` is a short Markdown prompt with **Agent** and **Execution** headers and a Task section. If you have built one that helped your own search, open a pull request with it. A few things to keep in mind:

- **Keep it career-neutral.** Skills read `config/profile.md` for everything about the candidate. Nothing about a specific person, industry, or company belongs in a skill.
- **Follow the playbook.** Warm path first, low outreach volume, a human in the loop on every message, and a Recruiter's read at the end. `config/recruiter_playbook.md` is the doctrine; a skill that fights it will not be merged.
- **Never send.** Drafts go to the clipboard and the vault. No skill may send email, create Gmail drafts, or post anywhere on the candidate's behalf.
- **Scrub before you push.** Check the diff for your own profile, wins, contacts, or vault notes. The `.gitignore` covers the usual paths, but a copied example can slip through.

Say in the pull request what the skill is for, which agent runs it, and what it wrote to the vault when you ran it. MIT licensed, so contributions are too.

## Runtime reference

Runtime-neutral personas are in `agents/`, tasks in `skills/`, and ownership in
`config/skill_agents.yaml`. Shared directives and note templates are in
`docs/jobfinderos-instructions.md` and `docs/vault-note-templates.md`.
Claude commands remain available under `.claude/`. Use `./scripts/JobFinderOS_run_agent.sh scout jobs-scout --dry-run` to inspect a
task, then omit `--dry-run` to execute it with Codex. Copying these Markdown
files does not register native Codex skills. Scheduling now uses the canonical runner and defaults to Codex. Candidate state stays in `config/`
and `vault/`, and learned preferences stay in `config/voice.md`.

Manual Codex execution needs an authenticated Codex CLI on PATH (or `CODEX_BIN`)
and the existing Python dependency (`pip install -r requirements.txt`). The runner
reads repository files and uses `codex exec --sandbox workspace-write`; it never
calls an LLM API directly. Optional `JOBFINDEROS_CODEX_MODEL` selects a model.

```bash
./scripts/JobFinderOS_run_agent.sh coach onboard --interactive
./scripts/JobFinderOS_run_agent.sh scout jobs-scout
./scripts/JobFinderOS_run_agent.sh mark mark-pulse
./scripts/JobFinderOS_run_agent.sh coach jobs-prep -- "Acme" "Widget Lead" "Screen"
```

Conversation skills require `--interactive`. Arguments follow `--` and retain
spaces. `JOBFINDEROS_SKILL_TIMEOUT_SEC` defaults to 1800. Logs and completion
records are under ignored `logs/agent-runs/`; lifecycle events use the existing
run log and vault mirror. The runner detects prohibited output changes and returns
failure; it leaves those changes for inspection. This is detection, not a
per-directory sandbox or a tool-level Gmail lock. Research needs live web access;
Coach email work needs a separately configured read connector. Missing required
inputs or tools must be reported as blocked. No inbox access is assumed.

`JOBFINDEROS_RUNTIME=claude` selects the optional Claude adapter using the same
canonical tasks. Original `.claude/` slash commands remain available unchanged
for direct Claude sessions. Claude model parity is not yet established; retain
those definitions until representative comparisons pass. The adapter uses normal
CLI permissions and never bypasses them.

Daily execution is sequential because Mark and Scout both update Dashboard.
`logs/daily-runs/<id>/run.json` records the current run's children, results and final
status. Failed or blocked children stop the sequence and do not advance scheduler
success state. Missing company research for `jobs-prep` runs Mark first.

```bash
./scripts/JobFinderOS_run_agent.sh coach jobs-daily
JOBFINDEROS_RUNTIME=claude ./scripts/JobFinderOS_run_agent.sh scout jobs-scout
bash scripts/verify_local_automation.sh --static
.venv/bin/python -m unittest discover -s tests -v
```

The scheduler dry-run reads state without creating locks or logs. The default
`verify_local_automation.sh` remains an operational check: it requires today's
digest, so a fresh checkout or weekly-only day can fail it. Use `--static` to check
configuration without a model or candidate data. The existing master scheduler
uses system-local time; its priority guard honors `scheduler.yaml`'s timezone.
This migration preserves that existing distinction.

The [validation report](docs/codex-validation.md) distinguishes automated regression
from real fictional persona runs and lists the remaining live Gmail/Claude parity
gates. `tests/live_smoke.py` prepares an isolated fictional repository; add
`--execute` to run the optional real-CLI smoke test.
