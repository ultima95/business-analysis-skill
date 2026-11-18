# business-analysis skill — Design

Date: 2026-11-18
Status: draft, awaiting approval

## 1. Intent

A portable agent skill that does **business analysis**: it turns a thin task, ticket,
meeting transcript, or process description into complete, testable requirements and
process analysis — and, when asked, into formal stakeholder documents.

It has three jobs, all in scope:

| Job | Input | Output | Reader |
|---|---|---|---|
| 1. Feed dev work | task / ticket / vague ask / notes | requirements, user stories, acceptance criteria, edge cases, assumptions, open questions | the user + a coding agent, then `brainstorming` / `writing-plans` |
| 2. Analyze a business process (non-software too) | description of how the business does X today | as-is map, pain points + root causes, to-be map, gaps | business people |
| 3. Formal artifacts | output of job 1 or 2 | BRD, gap analysis, process doc, stakeholder register | stakeholders / client |

Jobs combine: job 2 → job 3 (process analysis plus formal stakeholder docs), job 1 → job 3
(requirements written up as a BRD).

**Which file each job writes:**

| Request | Files |
|---|---|
| Job 1 alone | `…-requirements.md` (handoff template) |
| Job 1 + 3 | `…-brd.md` **instead of** the handoff — the BRD holds the requirements and is itself the handoff file brainstorming reads. One file, one source of IDs. |
| Job 2 alone | `…-process.md` (process-doc template: SIPOC, as-is, pain points, root cause, to-be, gap table) |
| Job 2 + 3 | the process doc, plus `…-gap-analysis.md` and/or `…-stakeholders.md` as requested. Formal docs link to the process doc instead of restating it. |
| Job 2 → 1 | process doc first; software requirements for the to-be go in a requirements/BRD file that cites process steps |

Requirements (BR/FR/NFR) are defined in exactly one file per analysis; every other file
cites them by ID.

### Lane vs `superpowers:brainstorming`

- **BA owns *what* and *why*:** problem, stakeholders, business rules, exception paths,
  edge cases, non-functional needs, success metrics.
- **Brainstorming owns *how to build*:** approaches, architecture, tech choices, UI.
- BA **never designs the solution.** For job 1 it ends with a handoff file and tells the
  user the next step is brainstorming/planning with that file as context.
- Trigger phrases are disjoint: BA triggers on "analyze this process", "gather/elicit
  requirements", "user stories / acceptance criteria for…", "write a BRD", "as-is / to-be",
  "gap analysis", "requirements from this ticket/meeting/email", "business analysis",
  "phân tích nghiệp vụ". It does **not** trigger on "build/implement/create X".

## 2. Goals

v1 features (numbers match the agreed idea list):

**Core (all jobs)**
1. **Gap-finder checklist** — actors, trigger, happy path, exception paths, business rules,
   data, non-functional needs, constraints, success metric. The agent checks the input
   against it and asks only about what's missing.
2. **Two modes**, chosen by an observable predicate:
   - *Interview* — the user is present and has not opted out of questions → ask **one
     question at a time**, highest-impact gap first; play back understanding as it forms.
   - *Draft* — the user said "just draft"/"don't ask", the session is autonomous, or the
     input is someone else's material being analyzed offline → write the document anyway,
     with every unknown recorded as an **Assumption (A-nn)** or **Open Question (Q-nn)**.
     Each open question names who should answer it and which requirement it blocks.
     Draft mode never presents an invented fact as confirmed.
   - *Hybrid* — the user is present **and** the input is someone else's material
     (transcript, email thread, ticket written by another person) → interview the user only
     on gaps they can plausibly answer (their own goals, priorities, scope); record gaps only
     the material's authors can answer as Q-nn with that author as owner. This is the
     default for pasted transcripts (S3).
3. **Inputs accepted:** task text, ticket, meeting notes/transcript, email thread, existing
   doc, file paths to any of these.
4. **Requirement IDs + traceability:** `BR-nnn` (business rule), `FR-nnn` (functional),
   `NFR-nnn` (non-functional). Acceptance criteria carry their parent's ID:
   `FR-003.AC1`, `NFR-001.AC2`. FRs cite the BRs they enforce (`[BR-002]`).
   IDs are used only in requirements-bearing docs (handoff, BRD). Process docs number
   their steps (`P1`, `P2`…) and list rules in plain prose; they get BR IDs only when
   job 2 → 1 turns them into requirements.
5. **Lint script** `scripts/lint_requirements.py` (see §5).
6. **MoSCoW priority** on every FR/NFR; a **glossary** section for domain terms.

**Feed dev work**
7. **User stories** (INVEST check) with **Gherkin** acceptance criteria (Given/When/Then).
   **One story = one FR:** the FR's statement is the story ("As a …, I want …, so that …");
   its Gherkin scenarios are `FR-nnn.ACn`. FRs that are not user-facing (system rules,
   integrations) use "The system shall …" instead. No separate `US-nnn` IDs.
8. **Edge-case generator:** roles × entity states × create/read/update/delete matrix;
   **decision tables** for rules with 3+ interacting conditions.
9. **Code recovery:** when run inside a repo for job 1, read the code that touches the
   affected domain to recover current business rules (as-is), cite them as
   `file:line`, and flag any new requirement that contradicts them.
10. **Handoff file:** `docs/ba/YYYY-MM-DD-<topic>-requirements.md` — the input
    brainstorming reads.

**Business processes**
12. **As-is / to-be maps** as Mermaid flowcharts with one `subgraph` per role (swimlanes).
13. **SIPOC** summary table.
14. **Pain-point analysis:** waits, handoffs, rework, approvals, manual re-entry, Lean
    wastes (DOWNTIME); root cause via 5 Whys, fishbone when causes branch.

**Formal artifacts**
16. **Markdown templates:** BRD, gap analysis, process doc, stakeholder register, plus the
    dev handoff (requirements) template.

## 3. Non-goals (v1)

- Solution design, architecture, tech/UI choices (brainstorming's lane).
- Estimation, sprint planning, project management.
- Push to GitHub issues / Jira (#11 — later).
- RACI per step, process KPIs (#15 — later).
- `.docx` export (#17 — later).
- Change-impact analysis against an existing BRD (#18 — later).
- Strategy tools: SWOT, business model canvas, ROI (#19 — skipped).

## 4. Anti-goals (failure even if it "works")

- The skill rewrites the user's idea into a solution (picks tech, screens, schemas).
- Documents bloated with boilerplate: template sections that don't apply must be
  **deleted**, not filled with "N/A".
- Invented stakeholders, numbers, or rules presented as confirmed facts.
- Asking a wall of questions at once in interview mode.
- Stealing "build X" requests from brainstorming.

## 5. Constraints

- **Portable:** works with any `skills`-compatible agent (Claude Code, Cursor, Copilot, …),
  same as `code-validate-skill`. No Claude-only features required. Diagrams are Mermaid
  text; documents are Markdown.
- **Install:** `npx skills add ultima95/business-analysis-skill` once pushed; manual
  symlink into `~/.claude/skills/business-analysis` documented in README.
- **Script:** Python ≥ 3.9, **standard library only** (no venv, no deps). Tests use stdlib
  `unittest`. Invoked through the interpreter: `python3 scripts/lint_requirements.py`.
- **SKILL.md** ≤ ~300 lines; detail lives in `references/`, loaded only for the active job.
- **Description** starts "Use when…", ≤ 1024 chars, triggers only (no workflow summary).
- **Language:** output follows the input's language (Vietnamese input → Vietnamese doc).
  Templates are written in English; the agent translates headings when writing Vietnamese.
  IDs (`FR-001`), Gherkin keywords, and Mermaid syntax stay English.
- **Where output goes:** `docs/ba/` at the git repo root when in a repo; otherwise
  `./ba/` in the current directory. User preference overrides.

## 6. Approaches considered

| Approach | Trade-off |
|---|---|
| **A. One skill, router SKILL.md + per-job references + templates + lint script** *(picked)* | One trigger surface, so no collisions between BA skills; shared core (gap-finder, IDs, lint) written once; progressive disclosure keeps context small. SKILL.md must route well. |
| B. Three skills (`ba-requirements`, `ba-process`, `ba-artifacts`) in one repo | Sharper triggers each, but the shared core is duplicated or cross-referenced, three descriptions compete with each other and with brainstorming, and combined jobs (2 → 3) cross skill boundaries. |
| C. One skill + Claude Code companion subagent (like `code-validator`) for code recovery | Isolated context for repo reading, but Claude-only and extra surface before there's evidence code reading bloats context. Revisit after v1 if #9 proves heavy. |

**Picked A** (assistant's call — the user delegated the how with "let's proceed").

## 7. Layout

```
business-analysis-skill/
  README.md                         # install, use, what's inside (mirrors code-validate-skill)
  LICENSE                           # MIT, "Copyright (c) 2026 ultima95"
  .gitignore                        # .DS_Store, __pycache__/, *.log
  docs/superpowers/specs/…          # this design
  docs/superpowers/plans/…          # implementation plan
  skills/business-analysis/
    SKILL.md                        # router + core loop
    references/
      elicitation.md                # #1 gap-finder, #2 modes, #3 inputs, question bank per gap
      requirements.md               # #4 IDs, #6 MoSCoW + glossary, #7 stories + Gherkin, #8 edge cases + decision tables
      code-recovery.md              # #9
      process-analysis.md           # #12 Mermaid swimlanes, #13 SIPOC, #14 wastes, 5 Whys, fishbone
    templates/
      requirements.md               # #10 dev handoff
      brd.md
      gap-analysis.md
      process-doc.md
      stakeholder-register.md
    scripts/
      lint_requirements.py          # #5
  tests/
    test_lint_requirements.py       # unittest
    fixtures/                       # good.md, bad-*.md
    scenarios/                      # skill test scenarios + recorded baseline/with-skill results
```

## 8. SKILL.md core loop

1. **Pick job(s)** from the request (1, 2, 3, or a combination). Ambiguous → ask once.
2. **Read input** (text or files). Job 1 inside a repo → also run code recovery
   (`references/code-recovery.md`).
3. **Run gap-finder** (`references/elicitation.md`) → list of gaps.
4. **Pick mode** by the predicate in §2.2. Interview: ask gaps one at a time by impact.
   Draft: record each gap as A-nn or Q-nn.
5. **Analyze** using the active job's reference.
6. **Write output** from the matching template; delete sections that don't apply.
7. **Lint** any doc that contains requirement IDs; fix every finding or record why it
   stays (e.g. an NFR that is genuinely qualitative becomes an open question).
8. **Report** to the user: file path, counts (BR/FR/NFR/AC/open questions), top 3 risks
   or open questions, and the next step (job 1: "brainstorm with this file as context").

## 9. Lint script contract (`lint_requirements.py`)

```
python3 scripts/lint_requirements.py <file.md> [<file.md> ...]
```

Output: one line per finding, `path:line: <rule>: <message>`. Exit `0` = clean,
`1` = findings, `2` = usage/IO error.

**Multi-file = one shared namespace:** all files passed in one call are linted together.
Definitions and citations are collected across the set, so a gap analysis citing a BRD's
`FR-002` resolves when both files are passed, and the same ID defined in two files is a
`duplicate-id`. The skill lints the whole set for an analysis in one call. Lint is run
only on sets that contain at least one requirements-bearing doc (handoff or BRD).

| Rule | Fires when |
|---|---|
| `vague-term` | a requirement or AC line contains a vague word from the EN/VI list (e.g. fast, quickly, easy, user-friendly, simple, flexible, robust, efficient, etc., and/or, as appropriate, TBD, normally / nhanh, dễ dàng, thân thiện, linh hoạt, v.v., phù hợp, hợp lý) |
| `missing-ac` | an `FR-nnn` or `NFR-nnn` is defined but has no `<ID>.ACn` anywhere |
| `dangling-ref` | an AC or `[BR-nnn]` citation points to an ID that is never defined |
| `duplicate-id` | the same ID is defined twice |
| `unmeasurable-nfr` | an NFR definition line and its ACs contain no number |
| `orphan-br` | a `BR-nnn` is defined but never cited by any FR or AC |

"Defined" = a line whose first token (after list/table markup and bold) is the ID
followed by `:` or a table cell boundary. Exact regexes are the builder's call; the
templates must use a definition style the script parses, and `tests/fixtures/good.md`
must lint clean.

## 10. Testing (writing-skills TDD)

**Lint script:** unittest per rule (one firing fixture + the clean fixture), exit codes,
multi-file input, Vietnamese vague terms.

**Skill behavior** — scenarios run by fresh subagents, first **without** the skill
(baseline, recorded verbatim in `tests/scenarios/`), then **with** it:

| ID | Scenario | Pass criteria with skill |
|---|---|---|
| S1 | Job 1: "Add refunds to the shop" inside a tiny fixture repo whose code already has order statuses and a 30-day rule | IDs + ACs present, exception paths covered, existing 30-day rule recovered with `file:line`, no tech/UI design, handoff file written, lint clean |
| S2 | Job 2: invoice approval done by email + Excel across 3 roles | process doc written; as-is + to-be Mermaid swimlanes, SIPOC, pain points tied to steps, root cause for top pain |
| S3 | Job 1 + 3: user pastes a meeting transcript → BRD (hybrid mode) | user asked only what they can answer; author-only gaps become Q-nn with owner; traceable IDs; no N/A filler; lint clean |
| S4 | Draft mode: autonomous, no user, thin ticket | no invented fact stated as confirmed; A-nn / Q-nn with owner + blocked requirement |
| S5 | Lane: "build me a todo app" | skill does not take over; defers to brainstorming |
| S5b | Reverse lane: "gather requirements for a leave-request flow" | BA is picked over brainstorming |
| S6 | Vietnamese input for job 1 | Vietnamese doc, English IDs/Gherkin keywords, VI vague terms caught by lint |

Lane tests (S5, S5b) run with **both** installed brainstorming descriptions present:
superpowers 7.0.2 and the standalone `~/.agents/skills/brainstorming`, whose description
says "Explores user intent, requirements and design before implementation". The BA
description must win "requirements for X" against both.

Wording that shapes output gets micro-tested against a no-guidance control (5+ reps)
per writing-skills. A scenario whose baseline already passes gets no extra guidance.

## 11. Decided by the user

- New skill for business analysis; all three jobs in scope.
- New folder under `/Users/ultima/Workspace/skills/` (the root).
- "Expand" = assistant adds ideas; the v1/later/skip split in §2–3 was accepted as proposed.

## 12. Assistant's calls (user can override)

- Folder `business-analysis-skill/`, skill name `business-analysis`.
- Approach A (§6).
- Output language follows input language.
- Output location `docs/ba/` (repo) / `./ba/` (no repo).
- Python stdlib + unittest; MIT license; README modeled on `code-validate-skill`.
- Template sections that don't apply get deleted.
- Mermaid `flowchart` + `subgraph` per role as the swimlane notation.
- Hybrid mode for pasted third-party material (§2.2).
- One file defines requirements per analysis; job 1 + 3 writes the BRD in place of the
  handoff (§1).
- Job 2 alone writes a process doc (§1).
- One story = one FR; no `US-nnn` IDs (§2.7).
- IDs and lint only in requirements-bearing docs; process docs use `P1…` steps (§2.4).
- Lint treats all files in one call as one namespace (§9).
- BA description designed to coexist with both installed brainstorming skills (§10).
- Local `git init` with no push; pushing to GitHub waits for the user's go-ahead.

## 13. Left to the builder

- Exact wording of SKILL.md, references, and templates (within the size budget).
- Lint regexes and the full vague-term lists.
- Fixture repo contents for S1 and the transcript for S3.
- Question-bank phrasing per gap.
