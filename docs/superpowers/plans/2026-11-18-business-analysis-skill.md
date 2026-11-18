# business-analysis Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a portable `business-analysis` agent skill (router SKILL.md, per-job references, Markdown templates, stdlib lint script) that turns tasks, tickets, transcripts, and process descriptions into testable requirements, process analysis, and formal BA documents.

**Architecture:** One skill (`skills/business-analysis/`) whose SKILL.md picks job + mode and loads only the reference for the active job. Requirements docs follow one ID/definition syntax that `scripts/lint_requirements.py` parses; templates are linted in tests so the two never drift. Skill wording is built test-first: baseline scenarios without the skill (RED), skill written against observed failures (GREEN), loopholes closed (REFACTOR).

**Tech Stack:** Markdown, Mermaid (text only), Python 3.9 standard library, `unittest`.

**Spec:** `docs/superpowers/specs/2026-11-18-business-analysis-skill-design.md` (read it before any task).

## Global Constraints

- Repo root: `/Users/ultima/Workspace/skills/business-analysis-skill/`. Skill name `business-analysis`.
- Portable: works with any `skills`-compatible agent; no Claude-only features required. Diagrams are Mermaid text; documents are Markdown.
- Python ≥ 3.9 (machine has 3.9.6): standard library only, no venv, no deps. Use `from __future__ import annotations`; no `match`, no runtime `X | Y` types.
- Tests: stdlib `unittest`, run with `python3 -m unittest discover -s tests -v` from repo root.
- Script invoked through the interpreter in all prose: `python3 scripts/lint_requirements.py` (relative to the skill dir).
- SKILL.md ≤ ~300 lines; description starts "Use when…", ≤ 1024 chars, triggers only (no workflow summary).
- IDs: `BR-nnn`, `FR-nnn`, `NFR-nnn`; ACs `FR-003.AC1`; FRs cite BRs as `[BR-002]`. Process docs use `P1`, `P2`… and no requirement IDs.
- Output language follows input language; templates in English; IDs, Gherkin keywords, Mermaid syntax stay English.
- Output location: `docs/ba/` at git repo root; otherwise `./ba/`. File names `YYYY-MM-DD-<topic>-{requirements|brd|process|gap-analysis|stakeholders}.md`.
- Template sections that don't apply are deleted, never filled with "N/A".
- Lint exit codes: `0` clean, `1` findings, `2` usage/IO error. Finding line: `path:line: <rule>: <message>`.
- Git: local only, no push. Commit messages Conventional Commits, ending with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. **CRLF line endings or a UTF-8 BOM** (docs saved from Windows/Word) → lint finds the same definitions as LF/no-BOM. Test: Task 1 `test_crlf_and_bom_parse_same`.
2. **IDs inside fenced code blocks** (Mermaid diagrams, examples) → ignored by every rule, never `duplicate-id`/`dangling-ref`. Test: Task 1 `test_fenced_code_ignored`.
3. **Vague term inside a longer word** ("breakfast" contains "fast", "Simplex" contains "simple") → only whole-word/phrase matches fire; case-insensitive. Test: Task 2 `test_vague_term_word_boundary`.
4. **Vietnamese text in NFD (decomposed) form** (copy-paste from macOS/Word) → VI vague terms still caught. Test: Task 2 `test_vague_term_vietnamese_nfd`.
5. **Empty file or file with no IDs** → exit 0, no crash, no findings. Test: Task 1 `test_empty_and_no_id_files_clean`.

---

## File map

| File | Responsibility | Task |
|---|---|---|
| `LICENSE`, `.gitignore` | MIT (`Copyright (c) 2026 ultima95`); `.DS_Store`, `__pycache__/`, `*.log` | 1 |
| `skills/business-analysis/scripts/lint_requirements.py` | parse ID definitions/citations across files; 6 rules; CLI | 1, 2 |
| `tests/test_lint_requirements.py` | lint unit tests | 1, 2 |
| `tests/fixtures/good.md` | realistic clean requirements doc (also the canonical definition-style example) | 1 |
| `tests/scenarios/README.md` | scenario prompts, run protocol, rubric (spec §10) | 3 |
| `tests/scenarios/fixtures/shop/` | tiny repo for S1 (order statuses + 30-day rule) | 3 |
| `tests/scenarios/fixtures/transcript-loyalty.md` | meeting transcript for S3 | 3 |
| `tests/scenarios/results/{baseline,green}-S*.md` | recorded runs, verbatim excerpts + rubric scores | 3, 7 |
| `skills/business-analysis/SKILL.md` | router + core loop | 4 |
| `skills/business-analysis/references/elicitation.md` | gap-finder, modes, inputs, question bank | 4 |
| `skills/business-analysis/references/requirements.md` | IDs, stories, Gherkin, MoSCoW, glossary, edge cases, decision tables, NFRs | 5 |
| `skills/business-analysis/references/code-recovery.md` | recover as-is rules from code | 5 |
| `skills/business-analysis/templates/requirements.md`, `brd.md` | requirements-bearing templates | 5 |
| `skills/business-analysis/references/process-analysis.md` | SIPOC, swimlanes, wastes, 5 Whys, fishbone, to-be, gap table | 6 |
| `skills/business-analysis/templates/process-doc.md`, `gap-analysis.md`, `stakeholder-register.md` | process + formal templates | 6 |
| `tests/test_assets.py` | SKILL.md frontmatter/size, templates lint clean, Mermaid structure | 4, 5, 6 |
| `README.md` | install, use, contents | 8 |

---

### Task 1: Repo scaffold + lint parser + structural rules + CLI

**Files:**
- Create: `LICENSE`, `.gitignore`, `skills/business-analysis/scripts/lint_requirements.py`, `tests/test_lint_requirements.py`, `tests/fixtures/good.md`

**Interfaces:**
- Produces (module `lint_requirements`):
  - `ID_RE = r"\b(BR|FR|NFR)-(\d{3,})(?:\.AC(\d+))?\b"` — any ID or AC mention.
  - `@dataclass(frozen=True) class Finding: path: str; line: int; rule: str; message: str` with `def format(self) -> str` → `f"{path}:{line}: {rule}: {message}"`.
  - `@dataclass class Block: id: str; kind: str  # "BR"|"FR"|"NFR"|"AC"; path: str; line: int; text: str  # def line + continuation lines`
  - `def parse(paths: list[str]) -> tuple[list[Block], list[tuple[str, str, int]]]` → (definition blocks, citations as `(id, path, line)`).
  - `def lint(paths: list[str]) -> list[Finding]` — sorted by (input path order, line, rule).
  - `def main(argv: list[str] | None = None) -> int`.
- Definition syntax (templates in Task 5 MUST use it): a line, outside fenced code, matching
  `^\s*(?:#{1,6}\s+|[-*+]\s+|\|\s*)?(?:\*\*)?(<ID or AC id>)(?:\*\*)?\s*[:|]` — i.e. heading, bullet, or first table cell, optionally bold, followed by `:` or `|`. Canonical forms: `- **FR-001**: As a …`, `- **FR-001.AC1**: Given …`, `| NFR-001 | … |`.
- Block = definition line plus following lines until a blank line, a heading, another definition line, or a table row.
- Citation = every `ID_RE` match outside fenced code that is not the defining token of its own line.

- [ ] **Step 1: Scaffold** — `git init`, `LICENSE` (MIT, `Copyright (c) 2026 ultima95`, same text as `../code-validate-skill/LICENSE`), `.gitignore`.

- [ ] **Step 2: Write `tests/fixtures/good.md`** — a short refund-feature requirements doc in canonical syntax: `BR-001`, `BR-002`; `FR-001`, `FR-002` (story form, each citing a BR, each with Gherkin `.AC1`/`.AC2`); `NFR-001` as a table row with a number in it plus `NFR-001.AC1`; a Mermaid fence mentioning `FR-001`. No vague terms.

- [ ] **Step 3: Write failing tests** in `tests/test_lint_requirements.py`. Import via `sys.path.insert(0, str(ROOT / "skills/business-analysis/scripts")); import lint_requirements as lr`. Helper `run(**files: str) -> list[Finding]` writes each `name=text` to a temp dir and calls `lr.lint` on them in order.

```python
def test_good_fixture_clean(self):
    self.assertEqual(lr.lint([str(FIXTURES / "good.md")]), [])

def test_duplicate_id_across_files(self):
    f = run(a="- **FR-001**: x\n- **FR-001.AC1**: Given a When b Then c\n",
            b="- **FR-001**: y\n- **FR-001.AC1**: Given a When b Then c\n")
    self.assertEqual([x.rule for x in f], ["duplicate-id", "duplicate-id"])  # FR-001, FR-001.AC1 in b

def test_missing_ac(self):
    f = run(a="- **FR-001**: The system shall log refunds\n")
    self.assertEqual([(x.rule, x.line) for x in f], [("missing-ac", 1)])

def test_dangling_ac_parent_and_br_cite(self):
    f = run(a="- **FR-001**: refund [BR-009]\n- **FR-001.AC1**: Given a When b Then c\n- **FR-007.AC1**: Given a When b Then c\n")
    self.assertEqual(sorted(x.rule for x in f), ["dangling-ref", "dangling-ref"])

def test_cross_file_citation_resolves(self):
    brd = "- **FR-002**: x\n- **FR-002.AC1**: Given a When b Then c\n"
    self.assertEqual(run(brd=brd, gap="Gap closes FR-002.\n"), [])
    self.assertEqual([x.rule for x in run(gap="Gap closes FR-002.\n")], ["dangling-ref"])

def test_orphan_br(self):
    f = run(a="- **BR-001**: Refunds within 30 days\n")
    self.assertEqual([x.rule for x in f], ["orphan-br"])

def test_fenced_code_ignored(self):
    f = run(a="```mermaid\nflowchart LR\n FR-001 --> FR-009\n```\n- **FR-001**: x\n- **FR-001.AC1**: Given a When b Then c\n")
    self.assertEqual(f, [])

def test_crlf_and_bom_parse_same(self):
    text = (FIXTURES / "good.md").read_text(encoding="utf-8")
    self.assertEqual(run(a="﻿" + text.replace("\n", "\r\n")), [])

def test_empty_and_no_id_files_clean(self):
    self.assertEqual(run(a="", b="# Notes\nNothing here.\n"), [])

def test_cli_exit_codes(self):
    good = str(FIXTURES / "good.md")
    bad = write_tmp("- **FR-001**: The system shall log refunds\n")   # returns path str
    with redirect_stdout(io.StringIO()) as out, redirect_stderr(io.StringIO()):
        self.assertEqual(lr.main([]), 2)
        self.assertEqual(lr.main(["/nonexistent.md"]), 2)
        self.assertEqual(lr.main([good]), 0)
    self.assertEqual(out.getvalue(), "")
    with redirect_stdout(io.StringIO()) as out, redirect_stderr(io.StringIO()):
        self.assertEqual(lr.main([bad]), 1)
    self.assertEqual(out.getvalue().splitlines(),
                     [f"{bad}:1: missing-ac: FR-001 has no acceptance criteria"])
```

Module constants used by both test files: `ROOT = Path(__file__).resolve().parents[1]`, `SKILL = ROOT / "skills/business-analysis"`, `FIXTURES = ROOT / "tests/fixtures"`.

- [ ] **Step 4: Run — expect FAIL** (`ModuleNotFoundError: lint_requirements`).
Run: `python3 -m unittest tests.test_lint_requirements -v`

- [ ] **Step 5: Implement** `parse`, `lint` (rules `duplicate-id`, `missing-ac`, `dangling-ref`, `orphan-br`), `main`. Read files with `encoding="utf-8-sig"` (strips BOM; universal newlines handle CRLF). `missing-ac` counts AC *definitions* only. `orphan-br`: BR id never cited inside any FR/NFR/AC block. `dangling-ref`: citation or AC definition whose base ID (or full AC id, when an AC is cited) is undefined across the whole file set. Messages: `"<ID> has no acceptance criteria"`, `"<ID> is defined more than once (first at <path>:<line>)"`, `"<ID> is not defined"`, `"<ID> is not cited by any requirement"`. `main` prints findings to stdout, a `N finding(s) in M file(s)` summary to stderr, IO/decode errors to stderr with exit 2, usage `usage: lint_requirements.py FILE.md [FILE.md ...]` with exit 2.

- [ ] **Step 6: Run — expect PASS.** Same command; all tests OK.

- [ ] **Step 7: Commit**
```bash
git add LICENSE .gitignore skills/business-analysis/scripts/lint_requirements.py tests/
git commit -m "feat(lint): requirements ID parser with structural rules and CLI"
```

---

### Task 2: Lint content rules — `vague-term`, `unmeasurable-nfr`

**Files:**
- Modify: `skills/business-analysis/scripts/lint_requirements.py`, `tests/test_lint_requirements.py`

**Interfaces:**
- Consumes: `Block`, `parse`, `lint`, `Finding` from Task 1.
- Produces: `VAGUE_TERMS_EN: tuple[str, ...]`, `VAGUE_TERMS_VI: tuple[str, ...]`; both rules wired into `lint`.

- [ ] **Step 1: Write failing tests**

```python
def test_vague_term_en(self):
    f = run(a="- **FR-001**: Refunds must be fast and user-friendly\n- **FR-001.AC1**: Given a When b Then c\n")
    self.assertEqual([x.rule for x in f], ["vague-term", "vague-term"])
    self.assertTrue(any("'fast'" in x.message for x in f))

def test_vague_term_word_boundary(self):
    f = run(a="- **FR-001**: Breakfast menu shows Simplex items\n- **FR-001.AC1**: Given a When b Then c\n")
    self.assertEqual(f, [])
    f = run(a="- **FR-001**: Show items etc.\n- **FR-001.AC1**: Given a When b Then c and/or d\n")
    self.assertEqual(len(f), 2)

def test_vague_term_only_in_definition_blocks(self):
    self.assertEqual(run(a="## Assumptions\n- A-01: fast network\n"), [])

def test_vague_term_vietnamese(self):
    f = run(a="- **FR-001**: Hệ thống xử lý nhanh, giao diện thân thiện\n- **FR-001.AC1**: Given a When b Then c\n")
    self.assertEqual(len(f), 2)

def test_vague_term_vietnamese_nfd(self):
    import unicodedata
    text = unicodedata.normalize("NFD", "- **FR-001**: Giao diện thân thiện\n- **FR-001.AC1**: Given a When b Then c\n")
    self.assertEqual([x.rule for x in run(a=text)], ["vague-term"])

def test_unmeasurable_nfr(self):
    f = run(a="| NFR-001 | Page loads quickly enough |\n- **NFR-001.AC1**: Given load When open Then page is responsive\n")
    self.assertIn("unmeasurable-nfr", [x.rule for x in f])
    f = run(a="| NFR-001 | p95 page load < 2 s |\n- **NFR-001.AC1**: Given 100 users When open Then p95 < 2 s\n")
    self.assertEqual(f, [])
```

- [ ] **Step 2: Run — expect FAIL** (rules not implemented). `python3 -m unittest tests.test_lint_requirements -v`

- [ ] **Step 3: Implement.** Lists must include at least the spec's terms — EN: `fast, quickly, easy, user-friendly, simple, flexible, robust, efficient, etc., and/or, as appropriate, TBD, normally`; VI: `nhanh, dễ dàng, thân thiện, linh hoạt, v.v., phù hợp, hợp lý` (extend at your discretion). Match per term with `(?<!\w)` + `re.escape(term)` + `(?!\w)`, `re.IGNORECASE`, over `unicodedata.normalize("NFC", block.text)`; one finding per term occurrence, message `"vague term 'fast' — replace with a measurable criterion"`, line = actual line of the occurrence. `unmeasurable-nfr`: for each NFR, strip all `ID_RE` matches from its block and its AC blocks, then fire (at the NFR definition line) if no `\d` remains; message `"NFR-001 has no number in its definition or acceptance criteria"`.

- [ ] **Step 4: Run — expect PASS**, including all Task 1 tests.

- [ ] **Step 5: Commit** — `feat(lint): vague-term (EN/VI) and unmeasurable-nfr rules`

---

### Task 3: Scenario harness + RED baseline (no skill)

**Files:**
- Create: `tests/scenarios/README.md`, `tests/scenarios/fixtures/shop/` (`orders.py`, `refunds.py`, `test_orders.py`), `tests/scenarios/fixtures/transcript-loyalty.md`, `tests/scenarios/results/baseline-S1.md` … `baseline-S6.md`, `tests/scenarios/results/baseline-lane.md`

**Interfaces:**
- Produces: scenario prompts + rubric reused verbatim by Task 7.

- [ ] **Step 1: Write fixtures.**
  - `shop/orders.py`: `class OrderStatus(Enum)` with `PENDING, PAID, SHIPPED, DELIVERED, CANCELLED`; `RETURN_WINDOW_DAYS = 30`; `def can_return(order, today) -> bool` enforcing DELIVERED + within 30 days. `refunds.py`: empty stub module docstring "Refunds: not implemented". `test_orders.py`: two tests pinning the 30-day rule.
  - `transcript-loyalty.md`: ~60-line meeting transcript (PM Lan, Ops lead Minh, Finance Hà) about a loyalty-points program, containing: 2 decided rules, 1 contradiction between Ops and Finance on point expiry, 2 facts only Finance can confirm, vague asks ("make it fast", "easy to redeem").

- [ ] **Step 2: Write `tests/scenarios/README.md`** with, per scenario S1–S6 from spec §10: exact prompt, setup, turn protocol, and a rubric of yes/no checks copied from the spec's pass criteria. Protocol:
  - Each run = fresh subagent; S1 runs in a fresh copy `cp -R tests/scenarios/fixtures/shop "$(mktemp -d)/shop"`.
  - Interview scenarios (S1, S3, S6) are two turns: turn 1 instruction "If you need to ask the user something, ask at the end of your reply and stop." Turn 2 (via message to the same agent): canned answer listed in README + "Draft the rest now; do not ask more."
  - Baseline runs: prompt prefixed "Do not invoke or read any skills." Skill runs (Task 7): prefixed "Read and follow /…/skills/business-analysis/SKILL.md."
  - Lane micro-test (S5, S5b + variants "write user stories for a leave-request flow", "analyze our invoice approval process", "phân tích nghiệp vụ quy trình nghỉ phép", "build a leave-request app"): fresh agent gets a skill list (name + description) — superpowers brainstorming 7.0.2, `~/.agents/skills/brainstorming`, writing-plans, code-validate, and (Task 7 only) business-analysis — plus the user message; asked "Which one skill do you invoke first? Answer with the name only." 5 reps per message.

- [ ] **Step 3: Run baselines** S1–S6 without skill (subagents in parallel, one per scenario). Save each to `results/baseline-S<n>.md`: verbatim excerpts of the output, rubric table (check | yes/no | evidence), and the failure patterns observed in the agent's own words.

- [ ] **Step 4: Run lane baseline** (no BA in list) for the 5 messages × 5 reps; save tallies to `results/baseline-lane.md`.

- [ ] **Step 5: Summarize** at top of `tests/scenarios/README.md` a "Baseline failures" list: each failed rubric check → which skill file must address it. A check that already passes at baseline gets **no** dedicated guidance (spec §10).

- [ ] **Step 6: Commit** — `test(scenarios): BA scenario harness and RED baseline results`

---

### Task 4: SKILL.md router + elicitation reference

**Files:**
- Create: `skills/business-analysis/SKILL.md`, `skills/business-analysis/references/elicitation.md`, `tests/test_assets.py`

**Interfaces:**
- Consumes: baseline failure list (Task 3 Step 5); lint CLI (Task 1).
- Produces: section names later tasks link to — SKILL.md links `references/elicitation.md`, `references/requirements.md`, `references/code-recovery.md`, `references/process-analysis.md`, `templates/*.md` by those exact paths.

- [ ] **Step 1: Write failing tests** in `tests/test_assets.py`:

```python
def test_skill_frontmatter(self):
    fm = parse_frontmatter(SKILL / "SKILL.md")          # small helper: text between first two '---' lines
    self.assertEqual(fm["name"], "business-analysis")
    self.assertTrue(fm["description"].startswith("Use when"))
    self.assertLessEqual(len(fm["description"]), 1024)

def test_skill_size(self):
    self.assertLessEqual(len((SKILL / "SKILL.md").read_text().splitlines()), 300)

def test_skill_links_resolve(self):
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    paths = set(re.findall(r"(?:references|templates|scripts)/[\w.-]+\.(?:md|py)", text))
    self.assertTrue(paths)
    self.assertEqual([p for p in sorted(paths) if not (SKILL / p).is_file()], [])
```
  `test_assets.py` imports the lint module the same way as Task 1 (`sys.path.insert` + `import lint_requirements as lr`) and defines `parse_frontmatter(path) -> dict[str, str]` (split on the first two `---` lines, `key: value` per line, strip surrounding quotes).
  `test_skill_links_resolve` stays failing until Tasks 5–6 create the linked files — mark it `@unittest.expectedFailure` now and remove the decorator in Task 6.

- [ ] **Step 2: Run — expect FAIL.** `python3 -m unittest tests.test_assets -v`

- [ ] **Step 3: Write SKILL.md.** Description (tune wording only in Task 7 against the lane micro-test):
  > Use when asked to analyze a business process, gather or elicit requirements, write user stories or acceptance criteria, or produce a BRD, gap analysis, process map, or stakeholder register — including turning a task, ticket, meeting transcript, or email thread into testable requirements, and analyzing non-software processes (approvals, onboarding, invoicing). Triggers on "business analysis", "BA", "requirements for…", "as-is / to-be", "phân tích nghiệp vụ", "thu thập yêu cầu". Not for designing or building the solution — hand off to brainstorming after this.

  Body sections, in order: Overview (core principle: own *what* and *why*, never *how*) · When not to use (lane vs brainstorming) · Pick the job (job table + spec §1 "which file each job writes" table, with the reference to load per job) · Pick the mode (interview / draft / hybrid predicates from spec §2.2) · Core loop (spec §8 steps 1–8, lint as `python3 scripts/lint_requirements.py <files…>`) · Output location, file names, language · Report format (path, counts BR/FR/NFR/AC/Q, top 3 risks, next step) · Quick reference (ID syntax canonical forms from Task 1) · Common mistakes / red flags — only those observed in the Task 3 baseline.

- [ ] **Step 4: Write `references/elicitation.md`**: the 9-item gap-finder (actors, trigger, happy path, exception paths, business rules, data, non-functional needs, constraints, success metric) with 2–3 questions each; ranking rule for interview order (ask the gap whose answer changes the most requirements first, one per message); stop rule (stop when every gap is answered, recorded as A-nn/Q-nn, or the user opts out); A-nn / Q-nn formats (`| Q-01 | question | owner | blocks FR-00x |`); input-type notes (transcript: separate decisions vs opinions vs contradictions; email thread: latest decision wins, flag reversals).

- [ ] **Step 5: Run — expect PASS** (links test still expected-failure).

- [ ] **Step 6: Commit** — `feat(skill): business-analysis router and elicitation reference`

---

### Task 5: Requirements reference, code recovery, requirements + BRD templates

**Files:**
- Create: `skills/business-analysis/references/requirements.md`, `skills/business-analysis/references/code-recovery.md`, `skills/business-analysis/templates/requirements.md`, `skills/business-analysis/templates/brd.md`
- Modify: `tests/test_assets.py`

**Interfaces:**
- Consumes: definition syntax (Task 1); SKILL.md link paths (Task 4).

- [ ] **Step 1: Write failing test**

```python
def test_requirement_templates_lint_clean(self):
    for name in ("requirements.md", "brd.md"):
        self.assertEqual(lr.lint([str(SKILL / "templates" / name)]), [], name)
```

- [ ] **Step 2: Run — expect FAIL** (files missing).

- [ ] **Step 3: Write `references/requirements.md`**: ID scheme + canonical definition forms (identical to Task 1); one story = one FR ("As a …, I want …, so that …" or "The system shall …"); INVEST check; Gherkin ACs as `FR-nnn.ACn` (happy path + each exception path); MoSCoW on every FR/NFR; NFR categories (performance, availability, security, privacy/compliance, usability, accessibility, auditability) each needing a number or a Q-nn; edge-case matrix (roles × entity states × create/read/update/delete) and decision table format for rules with 3+ conditions; glossary format. Rule: never a traceability table whose first cell is an ID (it would parse as a definition).

- [ ] **Step 4: Write `references/code-recovery.md`**: find domain code (grep entity/status names, enums, constants, validators, state transitions, tests); record each recovered rule as `BR-nnn` with source `file:line`; flag a new requirement contradicting code as Q-nn "conflicts with <file:line>"; never propose code changes.

- [ ] **Step 5: Write templates** in canonical syntax with placeholder IDs that lint clean (placeholders like `<As a …>`, NFR placeholder containing a number, each placeholder FR/NFR with an AC, each BR cited).
  - `requirements.md`: Context (problem, why now) · Actors & stakeholders · Scope (in / out) · Business rules · Functional requirements · Non-functional requirements · Edge cases · Rules recovered from code · Glossary · Assumptions · Open questions · Next step ("Brainstorm the solution with this file as context").
  - `brd.md`: Document control (version, date, author, status) · Executive summary · Business objectives & success metrics · Background / as-is · Scope · Stakeholders · Business rules · Functional requirements · Non-functional requirements · Assumptions, constraints, dependencies · Open questions · Glossary · Sign-off.
  - Each template opens with a one-line comment: delete sections that don't apply.

- [ ] **Step 6: Run — expect PASS.** `python3 -m unittest discover -s tests -v`

- [ ] **Step 7: Commit** — `feat(skill): requirements reference, code recovery, requirements and BRD templates`

---

### Task 6: Process-analysis reference + process, gap-analysis, stakeholder templates

**Files:**
- Create: `skills/business-analysis/references/process-analysis.md`, `skills/business-analysis/templates/process-doc.md`, `skills/business-analysis/templates/gap-analysis.md`, `skills/business-analysis/templates/stakeholder-register.md`
- Modify: `tests/test_assets.py` (remove `expectedFailure` from `test_skill_links_resolve`)

- [ ] **Step 1: Write failing test; remove `@unittest.expectedFailure` from `test_skill_links_resolve`.**

```python
def test_mermaid_blocks_well_formed(self):
    blocks = mermaid_blocks(SKILL / "references", SKILL / "templates")  # list[(path, list[str])]
    self.assertTrue(blocks)
    for path, lines in blocks:
        body = [l for l in lines if l.strip()]
        self.assertRegex(body[0], r"^\s*(flowchart|mindmap)\b", path)
        subs = [l for l in body if re.match(r"^\s*subgraph\b", l)]
        ends = [l for l in body if re.match(r"^\s*end\s*$", l)]
        self.assertEqual(len(subs), len(ends), path)
        for l in subs:
            self.assertRegex(l, r'^\s*subgraph\s+\w+\s*\["[^"]+"\]', path)
```

- [ ] **Step 2: Run — expect FAIL** (process-analysis and process templates missing → both tests fail).

- [ ] **Step 3: Write `references/process-analysis.md`**: SIPOC table; as-is steps `P1…` with role, input, output, tool, wait time; swimlane notation = Mermaid `flowchart LR` with one `subgraph <id> ["<Role>"]` per role (one worked example); pain-point table (step | type: wait / handoff / rework / approval / manual re-entry | Lean waste from DOWNTIME | evidence | impact); 5 Whys format; fishbone as Mermaid `mindmap` or 6M list when causes branch; to-be map rules (labelled as proposal, each change tied to a pain point); gap table (as-is | to-be | gap | change needed). Process docs use no BR/FR/NFR IDs.

- [ ] **Step 4: Write templates.**
  - `process-doc.md`: Process summary · SIPOC · As-is (steps + swimlane) · Pain points · Root cause · To-be (swimlane) · Gaps · Assumptions · Open questions.
  - `gap-analysis.md`: Purpose · Current state (link to process doc) · Target state · Gaps (area | current | target | gap | impact | priority | recommendation) · Risks · Next steps.
  - `stakeholder-register.md`: one table — Stakeholder / role | Group | Interest | Influence (H/M/L) | Expectations | Engagement approach | Communication.

- [ ] **Step 5: Run — expect PASS**, full suite: `python3 -m unittest discover -s tests -v`

- [ ] **Step 6: Commit** — `feat(skill): process analysis reference and process/gap/stakeholder templates`

---

### Task 7: GREEN runs + REFACTOR

**Files:**
- Create: `tests/scenarios/results/green-S1.md` … `green-S6.md`, `tests/scenarios/results/green-lane.md`
- Modify: skill files as findings require

- [ ] **Step 1: Run S1–S6 with skill** using the exact Task 3 prompts/protocol (prefix "Read and follow …/SKILL.md"). Save output excerpts + rubric to `results/green-S<n>.md`. Run the lint on every requirements/BRD file a run produced; record its output.

- [ ] **Step 2: Run lane micro-test** with business-analysis in the skill list, 5 messages × 5 reps. Pass: "build a leave-request app" and S5 → a brainstorming skill 5/5; every BA message → `business-analysis` 5/5. Save tallies to `results/green-lane.md`.

- [ ] **Step 3: REFACTOR.** For each failed rubric check: quote the agent's rationalization, change the smallest piece of skill text that addresses it (form per writing-skills "Match the Form to the Failure"), re-run only that scenario. Repeat until every rubric check passes. Log each iteration (failure → change → result) in the matching `green-S<n>.md`.

- [ ] **Step 4: Verify** full unit suite still passes and SKILL.md ≤ 300 lines: `python3 -m unittest discover -s tests -v`

- [ ] **Step 5: Commit** — `test(scenarios): GREEN results; refine skill wording from failures`

---

### Task 8: README + final verification

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write README** modeled on `../code-validate-skill/README.md`: one-paragraph pitch; Install (`npx skills add ultima95/business-analysis-skill`, `--skill business-analysis`, `--list`; manual `ln -s "$PWD/skills/business-analysis" ~/.claude/skills/business-analysis`); Use (example asks per job, incl. Vietnamese); What it produces (file table from spec §1); Lint usage; Lane note (runs before brainstorming, never designs the solution); What's in this repo; License MIT.

- [ ] **Step 2: Verify** — `python3 -m unittest discover -s tests -v` → all OK; `python3 skills/business-analysis/scripts/lint_requirements.py tests/fixtures/good.md; echo $?` → `0`; `git status` clean after commit.

- [ ] **Step 3: Commit** — `docs: README with install and usage`

Push to GitHub and installing the symlink into `~/.claude/skills/` are **not** part of this plan — ask the user.
