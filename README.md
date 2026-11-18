# business-analysis

A **business analysis skill** for AI coding agents. It turns a thin task, ticket, meeting transcript, or process description into complete, testable requirements and process analysis — and, when asked, into formal stakeholder documents. It handles three jobs: feeding development work (requirements, user stories, acceptance criteria, edge cases, assumptions, open questions), analyzing a business process (as-is and to-be maps, pain points, root causes, gaps), and producing formal artifacts (BRD, gap analysis, process doc, stakeholder register). The core principle: it owns **what** and **why** — problem, actors, business rules, exception paths, non-functional needs, success metrics — and never designs the solution; it hands off to `brainstorming` with the requirements file as context.

Works with any [`skills`](https://github.com/vercel-labs/skills)-compatible agent (Claude Code, Cursor, GitHub Copilot, Cline, and 18+ others).

## Install

```bash
npx skills add ultima95/business-analysis-skill
```

Install just this skill from the repo:

```bash
npx skills add ultima95/business-analysis-skill --skill business-analysis
```

Preview before installing:

```bash
npx skills add ultima95/business-analysis-skill --list
```

Or symlink it manually for Claude Code:

```bash
ln -s "$PWD/skills/business-analysis" ~/.claude/skills/business-analysis
```

There are no dependencies beyond Python 3.9+ for the lint script, which uses the standard library only.

## Use

Ask your agent in plain language. Examples:

```
Add refunds to our shop. Read the existing order code first, then work out the
full refund behavior: rules, exception cases, and anything still open.
```

```
Map our invoice approval process — today it runs on email and a shared Excel
sheet across three roles — and show how it could work better.
```

```
Here are the notes from our loyalty-points meeting. Turn them into requirements
and write them up as a formal document for stakeholders.
```

```
Phân tích nghiệp vụ quy trình nghỉ phép và viết yêu cầu đầy đủ trước khi code.
```

When you are available it interviews you one question at a time, highest-impact gap first — for someone else's material, only on gaps you can answer, with author-only gaps recorded as open questions for their owner. In draft mode (you say "just draft", or the session is autonomous) it writes the document anyway and records every unknown as a labelled assumption or open question.

The skill does not take over build requests ("build me a todo app" stays with `brainstorming`), and it does not design technology, architecture, schemas, or UI.

## What it produces

Output goes to `docs/ba/` at the git repo root (or `./ba/` outside a repo; a user preference overrides both). File names are `YYYY-MM-DD-<topic>-<kind>.md`.

| Request | File written |
|---|---|
| Requirements for dev work (job 1) | `<topic>-requirements.md` — the handoff file `brainstorming` reads |
| Requirements written up formally (job 1 + 3) | `<topic>-brd.md` — replaces the handoff; the BRD holds the requirements and is itself the handoff |
| Process analysis (job 2) | `<topic>-process.md` — SIPOC, as-is and to-be Mermaid swimlanes, pain points, root cause, gap table |
| Process analysis plus formal docs (job 2 + 3) | the process doc, plus `<topic>-gap-analysis.md` and/or `<topic>-stakeholders.md` |

Requirements are defined in exactly one file per analysis; every other file cites them by ID (`BR-nnn`, `FR-nnn`, `NFR-nnn`, acceptance criteria as `FR-nnn.ACn`).

## Lint

The skill lints every document that contains requirement IDs. Run it yourself from the repo root:

```bash
python3 skills/business-analysis/scripts/lint_requirements.py FILE.md [FILE.md ...]
```

Exit codes: `0` clean, `1` findings, `2` usage or IO error. Files passed in one call share one ID namespace, so cross-file citations resolve and duplicate IDs across the set are caught.

| Rule | Fires when |
|---|---|
| `vague-term` | a requirement or acceptance-criterion line contains a vague word from the English/Vietnamese list (fast, quickly, easy, user-friendly, simple, flexible, robust, efficient, etc., and/or, as appropriate, TBD, normally / nhanh, dễ dàng, thân thiện, linh hoạt, v.v., phù hợp, hợp lý) |
| `missing-ac` | an `FR-nnn` or `NFR-nnn` is defined but has no `<ID>.ACn` |
| `dangling-ref` | an acceptance criterion or `[BR-nnn]` citation points to an ID that is never defined |
| `duplicate-id` | the same ID is defined twice |
| `unmeasurable-nfr` | an NFR definition and its acceptance criteria contain no number |
| `orphan-br` | a `BR-nnn` is defined but never cited by any FR or acceptance criterion |

## How it was tested

`tests/scenarios/` runs a baseline-versus-with-skill harness: every scenario is executed by a fresh agent without the skill, then with it, against a rubric. Latest scored runs: S1 8/8, S2 6/6, S3 7/7, S4 5/5 on each of 3 reps, S6 6/6 on each of 3 reps (18/18), and lane routing 30/30 answers. The rubric totals table records 14/35 at baseline against 34/35 with the skill; S2 and the lane test are the latest evidence from an earlier skill commit, not fresh re-runs. Full evidence, raw outputs, and borderline notes are in [`tests/scenarios/results/green-summary.md`](tests/scenarios/results/green-summary.md). The lint script and skill assets are covered by 23 stdlib `unittest` tests: `python3 -m unittest discover -s tests`.

## What's in this repo

```
README.md                          # this file
LICENSE                            # MIT
.gitignore                         # .DS_Store, __pycache__/, *.log, .superpowers/
docs/superpowers/specs/            # design spec
docs/superpowers/plans/            # implementation plan
skills/business-analysis/
  SKILL.md                         # router and core loop (loaded by the agent)
  references/                      # elicitation, requirements, code recovery, process analysis
  templates/                       # requirements, BRD, gap analysis, process doc, stakeholder register
  scripts/lint_requirements.py     # requirement-ID lint, Python stdlib only
tests/
  test_lint_requirements.py        # per-rule, multi-file, exit-code, Vietnamese tests
  test_assets.py                   # skill frontmatter, links, size, template lint checks
  fixtures/good.md                 # clean requirements fixture
  scenarios/                       # baseline vs with-skill scenarios, rubrics, recorded results
```

## License

MIT — see [LICENSE](LICENSE).
