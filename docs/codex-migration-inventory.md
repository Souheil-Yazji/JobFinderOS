# Codex migration inventory

Phase 1 of the JobFinderOS Codex port. Inspected baseline: `77853cdb91f36037d84db5bd2273cf381b579b10` (2026-09-14). This document inventories the existing implementation and proposes subsequent changes; it does not change runtime behavior or claim Codex parity.

## System and source of truth

JobFinderOS consists of three Markdown personas, 25 Markdown commands, shared recruiter doctrine, private candidate configuration, an Obsidian vault, and local automation. The model performs research and judgment; Python and shell handle scheduling and maintenance.

```text
launchd: com.jobfinderos.scheduler
  -> scripts/scheduler_tick.py
     -> scripts/JobFinderOS_run_skill.sh <label> <skill>
        -> claude -p /<skill>
     -> scripts/jobfinderos_priority_watch.py
        -> scripts/JobFinderOS_run_skill.sh priority-watch jobs-priority-watch

CLAUDE.md + .claude/agents/ + .claude/commands/
  -> config/ + config/recruiter_playbook.md
  -> vault/
```

The scheduler executes `mark-weekly` when weekly is due, otherwise `jobs-daily` when daily is due, then the priority-watch guard. A successful weekly run suppresses daily on that calendar day. Despite the scheduler module's “Mark+Jobs” wording, **the weekly skill does not run the daily workflow**.

Repository state is already sufficient for interactive status retrieval: read candidate configuration, Dashboard, Strategy, company records, tracking queues, and recent dated reports. Do not substitute conversation memory. Scheduler state and ATS deduplication also live outside the repository in `~/.jobfinderos/`; retain that existing operational state.

## Inspection coverage

Reviewed the tracked project instructions, all three agent definitions and all 25 commands, seven candidate templates and the ATS example, scheduler configuration, all shell/Python automation and three launchd templates, vault skeleton and automation notes, README, and retrospective. Assets and LICENSE do not affect execution. There is no tracked CI workflow, test suite, package for an LLM SDK, MCP server configuration, or Codex runtime configuration. `requirements.txt` contains only `PyYAML>=6.0`.

The local action-plan file supplies the migration requirements. It is untracked and is not part of this documentation PR. No private candidate configuration or generated vault content is needed in a migration commit.

## Claude-specific dependencies

| Category | Source | Current dependency | Minimum migration treatment |
|---|---|---|---|
| Agent definition | `.claude/agents/coach.md` | Claude project-subagent discovery; YAML `name`, `description`, `model: inherit`; tools inherited from session | Copy persona to `agents/coach.md`; keep responsibilities and consent rules; replace runtime-specific metadata/instructions |
| Agent definition | `.claude/agents/scout.md`, `.claude/agents/mark.md` | `model: sonnet`; explicit Claude tool names; “Claude Code native tools only”; subagent report contract | Copy into `agents/`; use semantic capabilities and exclusions; choose models in the runtime, not doctrine |
| Skill/command format | All `.claude/commands/*.md` | Claude slash-command discovery, description frontmatter, prose argument placeholders, `.claude/agents/` paths | Copy task bodies into `skills/<name>.md`; make agent ownership explicit; pass argument text through the new runner |
| Orchestration | Ten delegated commands listed below | `Agent` tool, `subagent_type`, main-session relay, inline fallback | Execute the named persona in a separate CLI invocation; remove delegation boilerplate from canonical task files |
| Orchestration | `.claude/commands/jobs-daily.md` | Parallel Mark/Scout, Coach email/digest, closing session; fallback simulates all personas inline | Deterministic external orchestration; no generic-session fallback for the Codex daily workflow |
| Orchestration | `mark-weekly.md`, `jobs-prep.md`, `jobs-email.md`, `whats-next.md` and skill follow-ons | Commands call or recommend other commands by slash name; weekly reads the pulse Task directly | Preserve same-agent reuse; route cross-agent prerequisites through the correct runner; distinguish recommendations from immediate execution |
| CLI/runtime | `scripts/JobFinderOS_run_skill.sh` | `.claude/commands` existence check, `CLAUDE_BIN`, `claude -p`, `--allowedTools`, `--dangerously-skip-permissions`, stdin `/dev/null` | Add explicit agent/skill runner and small Codex adapter; retain a Claude compatibility path |
| CLI/runtime | `scripts/JobFinderOS_check_local_runner.sh` | Claude binary/version/auth check, three Claude command-file checks, old runner executable check | Runtime-aware preflight after manual Codex execution is validated |
| Scheduler | `scheduler_tick.py`; all three `jobfinderos_*_guard.py` files; `JobFinderOS_run_daily.sh`, `JobFinderOS_run_weekly.sh` | Invoke old runner with label and skill, not agent and skill | Resolve deterministic ownership without changing time/state/lock rules |
| Scheduler/documentation | `JobFinderOS_install_launchd.sh` | Installs executable old entrypoints, generates a Claude-specific automation header | Update execution prerequisites and generated text when switching runtime; keep one master scheduler |
| Tool access | Agent files and research tasks | `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`, `WebFetch`, `WebSearch` names | Describe repository reads/writes and live primary-source research; verify actual Codex capabilities |
| Tool access | Coach; email/digest/day-of-card and optional thread-reading tasks | claude.ai Gmail MCP; `search_threads`, `get_thread`; no checked-in connector configuration | Configure and verify read access separately for Codex; never assume Claude auth/connector transfers |
| Tool access | Drafting and voice tasks | macOS `pbcopy`/`pbpaste` | Keep optional clipboard behavior and vault output; this is OS-specific, not Claude-specific |
| Documentation | `CLAUDE.md` | Implicit project loading, directives, note templates, runtime description and skill catalog in one file | Extract shared instructions/templates and explicitly route Codex to them; retain Claude entrypoint |
| Documentation | `AGENTS.md`, `README.md`, both `vault/Automation/` notes, `vault/Companies/README.md` | Claude setup, paths, authentication, command invocation and troubleshooting | Update with the relevant implementation PR; distinguish job-search agents from coding contributors |
| Documentation | `RETROSPECTIVE.md`, mascot assets | Historical Claude implementation/branding | Keep historical material; no execution dependency |
| State/privacy | `.gitignore`, `.claude/commands/voice-check.md` | Ignored `.claude/settings.local.json` and worktrees; voice-check suggests `feedback_*` memory | Preserve ignores; put learned candidate preferences in private `config/voice.md` instead of vendor memory |

## Complete skill ownership and execution map

All source files below are `.claude/commands/<skill>.md`. “Delegated” means the existing command explicitly invokes Claude's Agent tool, with an inline fallback. “In session” includes both single-pass work and conversations; it does not imply suitability for unattended execution.

| Skill | Existing owner | Existing execution | Proposed owner / migration consideration |
|---|---|---|---|
| `checkin` | coach | In session, pauses | coach; retain candidate input and stage updates |
| `day-of-card` | coach | In session | coach; optional calendar/logistics thread reads |
| `draft-message` | coach | In session | coach; explicit drafting consent, vault/clipboard only |
| `email-watch` | coach | Delegated | coach; read-only inbox briefing plus clear pipeline updates |
| `jobs-cover` | coach | In session | coach; preserve permitted company/role research for the letter |
| `jobs-daily` | orchestrator, coach closes | Multi-agent | coach owns finalization; runtime owns dispatch |
| `jobs-digest` | coach | Delegated | coach; scoped Dashboard refresh, no Strategy edits |
| `jobs-email` | coach | Delegated | coach; rejection sweep, auto-prep, due replies, inbound roles |
| `jobs-prep` | coach | In session | coach; missing company research is a Mark prerequisite |
| `jobs-priority-watch` | scout | Delegated | scout; no content writes when nothing new |
| `jobs-research` | mark | Delegated | mark; company profile and research |
| `jobs-scout` | scout | Delegated | scout; score, deduplicate, filter, write opportunity records |
| `mark-profiler` | mark | Delegated | mark; deep company evaluation |
| `mark-pulse` | mark | Delegated | mark; pulse, brief, handoff, named human plays |
| `mark-weekly` | mark | Delegated | mark; includes pulse Task and Strategy pass, not daily |
| `mock-interview` | coach | In session, conversation | coach; do not fabricate candidate answers in batch mode |
| `network-outreach` | coach | In session | coach; targeted invocation authorizes drafting, never sending |
| `onboard` | none, setup guide | In session, interview | Proposed coach-owned setup exception; reads all personas to collect inputs, does not execute their jobs |
| `postmortem` | coach | In session | coach; objection log and optional email evidence |
| `profile` | coach | In session, interview | coach; private wins/voice updates |
| `story` | coach | In session, modes | coach; preserve list/add/find/update arguments and conversations |
| `title-audit` | mark | In session, candidate homework | mark; `quick` omits homework; profile changes require candidate yes |
| `voice-check` | coach | In session | coach; rewrite only on `fix`/yes; private preference storage |
| `warm-path` | coach | In session | coach; audit or company mode, no drafting |
| `whats-next` | coach | In session, loop | coach; route chosen work to its actual owner |

Counts: ten delegated commands, thirteen named-agent in-session commands, one setup guide, one orchestrator. Scheduled mapping: `jobs-daily -> coach` (orchestrated), `mark-weekly -> mark`, `jobs-priority-watch -> scout`. These names are hardcoded in the Python/shell callers; `scheduler.yaml` stores windows, not a job/skill registry.

The proposed `config/skill_agents.yaml` must cover all 25 names, including an explicit decision for onboarding and an orchestration marker for daily. Add Coach-owned `jobs-daily-finalize` when implementing daily orchestration. Never accept arbitrary agent/skill combinations simply because both files exist.

## Preserve actual agent boundaries

The personas are distinct, but their legitimate output areas overlap. A blanket “Mark only writes Market Intel” policy would break existing behavior:

- Scout creates opportunity notes, archives scans, and updates Dashboard `🎯 Now`; it does not draft outreach, read Gmail, or own strategy.
- Mark writes market notes, company profiles, the handoff, Dashboard human-play recommendations, and the weekly Strategy pass. Title-audit can update profile terms with consent. Mark must not mutate application stages or draft outreach.
- Coach owns pipeline judgment, email, prep, drafts, stories, and losses. `jobs-email` explicitly permits recording inbound opportunities; `checkin` permits a user-provided role stub. These are existing exceptions to Scout's discovery ownership. Research for a letter/interview is also explicitly allowed; it must not expand into an independent market/scouting run.
- `jobs-digest` expressly forbids Strategy changes, although other Coach skills permit them. Restrictions must account for the skill as well as the persona.

Claude's tool lists are not equivalent to per-directory write enforcement: Scout and Mark have Bash and Write/Edit. The runner's default allowlist contains no named Gmail tools; actual unattended connector availability is unverified. Carry semantic restrictions into every canonical agent and use runtime controls where available, while describing their limits honestly. Tests can detect prohibited changes; they do not by themselves prevent external tool side effects.

## Daily orchestration and handoffs

The current daily command calls Mark pulse and Scout scan in parallel, then Coach email, then Coach digest, then consolidates the archive and appends a run row. Every pass has its own persona/report instructions, but its inline fallback abandons process separation.

For Codex, implement separate processes in this initial order:

```text
mark / mark-pulse
scout / jobs-scout
coach / jobs-email
coach / jobs-digest
coach / jobs-daily-finalize
```

Start sequentially. Mark and Scout both edit Dashboard; Scout, email, digest, and finalization share the dated Daily Jobs Watch archive. Parallelism needs an explicit shared-write strategy and can wait. Preserve the Scout scan before consolidation and give finalization fresh, dated inputs and per-pass status. It should summarize completed research, not perform another scan.

Reuse `logs/launchd-runs.log` and the existing best-effort vault mirror for lifecycle events. Distinguish child invocation records from the **one final daily run record**; do not let both orchestration code and a skill append duplicate final records. Add agent, skill, runtime, duration and exit code, and a changed-file list when reliably detectable. Git diff alone misses ignored vault/config outputs; snapshots should report paths without publishing candidate contents.

On child failure, propagate a nonzero result and leave daily success state unset. Specify how missing Gmail is reported: an unavailable inbox is not an empty inbox, and an incomplete required email pass must not be represented as full behavioral parity. Interactive skills must remain interactive or explicitly report missing inputs; stdin EOF is not consent.

## Automation inventory and baseline discrepancies

| Files | Existing behavior to preserve or explicitly account for |
|---|---|
| `scripts/scheduler_tick.py` | `fcntl` lock at `~/.jobfinderos/scheduler.lock`; atomic JSON state replacement; daily local dates; ISO-week catch-up; weekly precedence; success-only state updates; watch after the main job. Watch subprocess failure is not propagated. |
| `config/scheduler.yaml` | Daily 07:00, Monday weekly 08:00, weekday watch 09:00; 1800-second interval; optional IANA timezone. Master tick uses system-local `datetime.now().astimezone()` and **does not read the configured timezone**. Guards do. Do not accidentally change this during adapter work; any fix deserves explicit tests and scope. |
| `scripts/jobfinderos_priority_watch.py` | Reads watch hour/minute and timezone; weekday gate, PID-file lock, daily `.last-success`; prints JSON on failure but returns normally, so process status remains zero. |
| `scripts/jobfinderos_daily_guard.py`, `scripts/jobfinderos_weekly_guard.py` | Alternate legacy/manual guards with separate locks/markers and hardcoded 07:15 weekday / Monday 08:30 windows. Not called by the current master tick. Do not install them as overlapping scheduled jobs. |
| `scripts/JobFinderOS_run_daily.sh`, `scripts/JobFinderOS_run_weekly.sh` | Thin shell entrypoints to the old runner; preserve compatibility. |
| `scripts/JobFinderOS_run_skill.sh` | Runs from root; uses `CLAUDE_BIN`; 1800-second default timeout only if external `timeout` exists; logs start/completed/failure; preserves CLI failure; runs path repair after success. No per-invocation transcript, duration, agent identity, or changed-file tracking. CLI discovery precedes adding `~/.local/bin` to PATH. |
| `scripts/JobFinderOS_log_run.sh` | Appends timestamp/label/phase to repo logs; mirrors to tracked automation note if writable. |
| `scripts/JobFinderOS_install_launchd.sh` | Generates scheduler YAML, external launcher and plist; removes two legacy launch agents; preserves existing run-log tail while replacing header. Relies on project `.venv/bin/python`; generated PATH adds only the venv. Runtime binary visibility in launchd must be tested. |
| `scripts/JobFinderOS_test_launchd.sh` | Kickstarts the real scheduler with `-k`; operational action, not an isolated test. Do not run for inventory validation. |
| `scripts/verify_local_automation.sh` | Prints markers/log tail and exits zero only if today's digest exists. This is an operational health check, not a static migration test. A fresh checkout fails; a successful weekly-only day can also lack a daily digest. |
| `scripts/JobFinderOS_install_helpers.sh`, `scripts/launchd/*.plist.template` | Optional latest/prune/ATS jobs; helper logs under `~/.jobfinderos/logs`. Existing schedule triggers are independent of the main YAML. Preserve integrations without installing them during development. |
| `scripts/jobfinderos_update_latest.py` | Derived dated pointer notes, stable Dashboard/Strategy links, superseded pointer cleanup; provider independent. |
| `scripts/jobfinderos_fix_backslash_paths.py` | Repairs escaped vault paths and preserves conflicts; invoked after successful skills; provider independent despite Claude-specific comment. Its `move_file` creates parent directories even in dry-run mode. |
| `scripts/jobfinderos_ats_poll.py` | Direct Greenhouse/Ashby/Lever HTTP, private YAML filters, seen-set in `~/.jobfinderos/ats_seen.json`, unscored ATS Inbox, desktop notifications. `--dry-run` still fetches and writes logs. Default execution stays local, but `--push` invokes Git pull/add/commit/push. |
| `scripts/jobfinderos_prune_history.py` | 30/90-day retention, newest file retained per group. **Default non-dry execution pulls, stages, commits and pushes**; `--no-push` still commits. Dry-run writes logs. |

Two findings need isolated correction before calling the port compliant with repository rules:

1. **Automated Git writes exist.** Remove pruner Git operations and ATS `--push` behavior in a focused prerequisite fix, retaining local retention and polling. Both helpers call an unscoped `git commit` after staging paths, potentially including already-staged unrelated files. Do not execute either write path during validation. The pruner's promise that deleted history remains in Git is false for ignored, never-committed vault notes.
2. **The whole vault is not ignored.** `.gitignore` deliberately re-includes tracked skeleton files, including Dashboard, Strategy, tracking tables, and the automation run log. Filled-in versions remain trackable; ignore rules do not protect changes to tracked files. Preserve compatibility in this port and inspect exact staged paths for every PR. A fully private skeleton redesign is separate work.

Additional source inconsistencies to capture in regression expectations:

- The ATS Inbox header assigns scoring/promotion to the daily digest, but `jobs-digest` does not explicitly read the Inbox or implement that status transition. Make Scout's handling of unscored ATS entries explicit in a scoped integration change; do not give Coach unrestricted discovery work.
- `config/targets.template.md` promotes aggregators, contrary to current direct-source doctrine. The rubric template says high scores generate outreach, while the playbook requires consent. Ported instructions should resolve these in favor of doctrine.
- `checkin` uses stage emoji variants and claims no Strategy write; the playbook describes checkin funnel refreshes. Preserve established record structure and test explicit stage meanings instead of assuming every source uses identical symbols.

## Already portable components

The core personas and task bodies are ordinary text; the scoring rubric, consent rules, recruiter doctrine, filenames, Obsidian navigation, and persistent record structure need no provider-specific data conversion. Python scheduling, filesystem logs, ATS HTTP parsing, retention selection, path repair, and pointer generation do not call an LLM API. Keep that separation.

Codex can receive a file-reading task through `codex exec`, run with an explicit working directory and workspace-write sandbox, and emit a final response or JSONL events. Saved CLI authentication is reused; no separate LLM API integration is required. The local CLI reports `0.154.0-alpha.6.2`; its `exec --help` confirms `--cd`, `--sandbox`, `--json`, `--output-last-message`, and stdin prompts. No actual model task was executed for this inventory. [Official non-interactive execution documentation](https://learn.chatgpt.com/docs/non-interactive-mode).

Codex discovers `AGENTS.md` as project instructions. Canonical `agents/*.md` and `skills/*.md` should be explicitly read through the runner; copying files there does not itself register native Codex personas or skills. Keep `AGENTS.md` short and link shared doctrine/templates, preserving its coding-contributor rules. [Official AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Minimum-diff PR sequence

Each PR should target the fork, use explicit file staging, and state its dependency. Later branches may stack on earlier branches in the same fork to keep diffs reviewable; do not merge or activate launchd as part of preparation.

1. **Inventory (this PR):** only this document. Runtime unchanged.
2. **Local-only helper correction:** remove automated Git writes and stale backup claims from ATS/pruner; test local outputs/retention with fictional fixtures and a Git spy.
3. **Vendor-neutral layout (Phase 2):** copy all personas/tasks, extract shared guidance/templates, define ownership, retain `.claude/`. Static path/ownership checks; no scheduler/runtime switch.
4. **Explicit Codex runner (Phases 3–4):** add canonical runner and adapter; validate arguments and agent/skill pairing; preserve labels/logging/exit codes; add dry-run, argument forwarding and timeout behavior. Test Scout, pulse, digest and prep independently before orchestration.
5. **Daily orchestration and scheduler integration (Phases 5–6):** implement separate-process daily and finalization before enabling Codex as the scheduler default. Preserve due/lock/state behavior and compatibility callers; update preflight, installer-generated text, README and runbook. This ordering avoids a scheduled daily invocation that is routed to Coach before orchestration exists.
6. **Regression/parity (Phase 7):** fictional fixtures for weekly/watch/daily, ATS consumption, retention, logs, Dashboard and Strategy; compare representative Claude and Codex runs from the same state. Keep mock-runtime verification distinct from live model parity.
7. **Compatibility decision (Phase 8):** only after evidence of parity; retain `.claude/` until then. Do not assume deletion is the desired outcome.

## Proposed Phase 2 file changes

| Action | Files | Scope |
|---|---|---|
| Add | `agents/coach.md`, `agents/scout.md`, `agents/mark.md` | Preserve personas and boundaries; remove Claude model/tool metadata; reference shared instructions and templates |
| Add | `skills/<skill>.md` for each of the 25 names in the ownership table | Preserve Task bodies; name owner first; update paths and tool terminology; remove Claude delegation/fallback boilerplate; mark daily as orchestration contract, not a single-persona task |
| Add | `config/skill_agents.yaml` | Explicit complete mapping; Coach-owned onboarding exception and daily orchestration marker |
| Add | `docs/jobfinderos-instructions.md` | Shared directives and read-first/state rules extracted from `CLAUDE.md`; no copied persona doctrine |
| Add | `docs/vault-note-templates.md` | Company, opportunity, digest and outreach templates extracted without changing note structure |
| Update | `AGENTS.md` | Concise canonical routing plus existing contributor/privacy/verification rules; describe runner as planned until implemented |
| Update | `README.md` | Explain new canonical layout and retained Claude compatibility; do not advertise an executable Codex runner prematurely |
| Add | `tests/test_canonical_definitions.py` | Static mapping/file/path/agent checks; report the existing tracked-skeleton privacy exceptions explicitly |

Keep `.claude/`, `CLAUDE.md`, scheduler, launchd installers, runtime scripts and vault content unchanged in Phase 2. Copied canonical instructions must not depend on `CLAUDE.md`; the shared extraction above is necessary to achieve that. Temporary duplication with the retained Claude definitions is explicit; compare the task bodies and track deliberate differences until parity permits compatibility wrappers.

## Validation evidence and remaining gates

Inventory checks on the unmodified baseline:

- Exactly three tracked agent definitions and 25 commands; every current named-agent reference resolves. `onboard` and daily require the explicit special handling above.
- `git check-ignore --no-index` confirms all seven private config paths, representative generated company notes, and logs are ignored. Dashboard and the automation run log correctly report **not ignored**, matching the skeleton exceptions.
- `python3 scripts/scheduler_tick.py --dry-run`: exits 1 because this checkout's Python lacks PyYAML. No jobs executed. Once dependencies exist, the baseline dry-run still creates/opens the home state directory/lock and appends an evaluation log; its watch “invoked” field is descriptive, as the return occurs before the guard runs.
- `bash scripts/verify_local_automation.sh`: exits 1 because today's digest is absent; no run markers/logs existed. Do not create a fake digest to make this check pass.
- Local `codex --version` and `codex exec --help` succeeded, with a sandbox warning about creating PATH aliases. This confirms available CLI syntax, not authentication, research access, Gmail access, or behavior.

Before switching scheduling, add tests for invalid/path-traversal names, wrong persona pairing, working directory, arguments with spaces, missing CLI, propagated failure/timeout, dry-run without model execution or state writes, and complete logs. Test weekly/daily precedence, catch-up, year/week boundaries, lock contention and success-state updates using controlled dates and temporary state. Test daily child ordering and failure at each stage; one final record on full success, no success marker on failure.

Behavioral smoke fixtures must contain only fictional candidates and deterministic source material. Assert Scout filters/scores/deduplicates without outreach; Mark writes market intelligence without stage changes; Coach preserves existing records and consent; daily uses separate personas and consolidates fresh outputs. Compare actual Claude/Codex runs separately before claiming parity or removing compatibility.
