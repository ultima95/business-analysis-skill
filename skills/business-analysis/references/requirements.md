# Requirements — IDs, stories, Gherkin, edge cases

Loaded for job 1 (feed dev work) and whenever job 3 writes a BRD. This reference defines
how a requirement is written so that it is traceable, testable, and lint-clean.

## ID scheme

| Kind | ID form | One entry is |
|---|---|---|
| Business rule | `BR-001` | one testable condition with its threshold or scope |
| Functional requirement | `FR-001` | one user story or one system behavior |
| Non-functional requirement | `NFR-001` | one measurable quality target |
| Acceptance criterion | `FR-001.AC1`, `NFR-001.AC2` | one Gherkin scenario for its parent |

- Three digits or more, in order of appearance, never reused: `BR-001`, `FR-012`, `NFR-003`.
- An acceptance criterion always carries its parent ID plus `.ACn`.
- IDs exist only in requirements-bearing documents (handoff, BRD). Every other file cites
  them by ID and never redefines them.
- A process doc numbers its steps `P1`, `P2`… in plain prose; a step gets a `BR-nnn` only
  when job 2 → 1 turns that rule into a requirement.

## Canonical definition forms

Use exactly these shapes. The lint script parses a line whose first token (after list,
table, or bold markup) is the ID followed by `:` or `|`.

| Element | Definition line |
|---|---|
| Business rule | `- **BR-001**: <rule with its threshold or scope>.` |
| Functional requirement | `- **FR-001**: As a <role>, I want <capability>, so that <outcome>. Fulfils [BR-001]. Priority: Must.` |
| Non-user-facing FR | `- **FR-002**: The system shall <behavior>. Fulfils [BR-002]. Priority: Must.` |
| Acceptance criterion | `- **FR-001.AC1**: Given <context>, When <action>, Then <observable outcome>.` |
| Non-functional requirement | `\| NFR-001 \| Must \| <measurable target with a number> \| <basis: input quote, A-nn, or Q-nn> \|` |
| NFR acceptance criterion | `- **NFR-001.AC1**: Given <load or condition>, When <action>, Then <metric> is <number>.` |
| Assumption | `\| A-01 \| <assumption> \| <basis in input, or impact if false> \|` |
| Open question | `\| Q-01 \| <question> \| <owner> \| blocks FR-00x \|` |

The NFR table has four columns: ID, MoSCoW priority, target, basis. The target cell carries
the number the lint script requires; the basis cell says where that number came from — a
short verbatim quote from the input or user answers, an `A-nn`, or a `Q-nn` with its owner.

## One story = one functional requirement

Each `FR-nnn` is exactly one story. The statement is the story itself — there is no
separate `US-nnn` namespace.

- User-facing: **As a `<role>`, I want `<capability>`, so that `<outcome>`.**
- Not user-facing (system rule, integration, batch job): **The system shall `<behavior>`.**

One story per FR keeps the acceptance criteria as that story's done-condition and the ID
stable from requirements through tests. A second capability means a second FR.

## INVEST check

Run every story against the six tests before it earns an ID.

| Letter | Question the statement must answer |
|---|---|
| Independent | Can it ship without waiting on another FR? If not, the dependency is an A-nn. |
| Negotiable | Does it state the need rather than a chosen solution? Technology, screens, and schemas belong to brainstorming. |
| Valuable | Does it name the outcome for a role, not an internal step? |
| Estimable | Does the team know when it is done from the statement and its ACs? |
| Small | Can one delivery cover it? Split into two FRs when not. |
| Testable | Can every AC be observed without reading the code? |

A story that fails Independent-, Negotiable-, or Testable is rewritten, not annotated.

## Acceptance criteria — Gherkin

Every `FR-nnn` and `NFR-nnn` gets at least one `FR-nnn.ACn` or `NFR-nnn.ACn`.

- `AC1` — the happy path, in the story's words.
- `AC2…ACn` — one scenario per exception path the gap-finder found: failure, skip, late
  input, limit, permission, duplicate, and already-processed case.
- NFR criteria state the measurement condition and the number.

Shape: `Given <precondition>, When <action>, Then <observable, checkable outcome>.`

- One behavior per scenario; a scenario that needs two `Then` clauses is two ACs.
- The outcome is observable by the actor or by the audit record — no internal state.
- No vague word in a definition or AC line; the lint script rejects the EN and VI lists.

## Priority — MoSCoW

Every FR and NFR carries exactly one label:

| Label | Meaning |
|---|---|
| Must | without it the release does not solve the problem |
| Should | painful to omit, but the release still works |
| Could | wanted, and dropped first under pressure |
| Won't | explicitly out of this release, recorded so it is not re-litigated |

Write it inline on an FR (`Priority: Must.`) and in the priority column of the NFR table.

## Non-functional requirements

Every NFR target needs a number, and its Basis says where the number came from: a quote from
the input, an `A-nn` for a working value you set, or a `Q-nn` owned by the person who can set
the target. Check every category:

| Category | What to measure |
|---|---|
| Performance | response time, throughput, batch window |
| Availability | uptime per period, recovery time, recovery point |
| Security | authentication, authorization, rate limits |
| Privacy / compliance | data retention, consent, access scope, regulation |
| Usability | task completion, step count, error rate |
| Accessibility | contrast, keyboard path, screen-reader coverage |
| Auditability | what is logged, for how long, who can read it |

An NFR with no number in its definition and its ACs is `unmeasurable-nfr`. If only the
business can supply the number, record a Q-nn with its owner and the requirement it blocks.

## Edge-case matrix

Generate cases by crossing **roles × entity states × create/read/update/delete**, then keep
the cells that reveal a rule or an exception path.

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| <role> | <state> | <expected result> | <expected result> | <expected result> | <expected result> |

Each non-obvious cell becomes a `BR-nnn`, an exception AC, or a Q-nn. The matrix is complete
when every role × state intersection has been considered, even if the answer is "not
allowed".

## Decision tables

A rule with three or more interacting conditions becomes a decision table instead of prose.

| Condition / action | R1 | R2 | R3 |
|---|---|---|---|
| <condition 1> | Y | Y | N |
| <condition 2> | Y | N | – |
| <action> | <outcome> | <outcome> | <outcome> |

Each column is one testable combination. Give the table one `BR-nnn` and cite it from the
FRs it drives.

## Glossary

| Term | Meaning |
|---|---|
| <domain term> | <one sentence a new team member understands> |

Define every domain noun, status name, and role once here, then use that word everywhere.
A synonym in prose is a contradiction; align it to the glossary entry.

## Assumptions and open questions

The formats, ownership rules, and stop conditions live in `elicitation.md`. Use them exactly
as written; do not invent a parallel register.

- An assumption is a value you filled to keep writing: row `A-01` in the assumption table.
- An open question is a gap only someone else can answer: row `Q-01` with its owner and the
  requirement it blocks.
- A prose list titled "assumptions to validate" is not a register and does not satisfy
  either slot.

## Traceability

- Each FR cites the BRs it enforces inline: `Fulfils [BR-001].`
- Each AC carries its parent ID: `FR-001.AC1`.
- Each Q-nn names the requirement it blocks.
- Never write a traceability table whose first cell is an ID. The lint script parses an ID
  in the first cell as a new definition and reports `duplicate-id`. Link by citation, not
  by table.

## Language

Output follows the input's language; IDs and Gherkin keywords stay English.

- Headings and prose: the input language.
- IDs: `BR-001`, `FR-001`, `NFR-001` — never translated.
- Gherkin keywords: `Given`, `When`, `Then` — never translated; only the prose after each
  keyword is.

Canonical Vietnamese line (English keywords, Vietnamese prose):

- **FR-001.AC1**: Given nhân viên còn 12 ngày phép, When gửi đơn nghỉ 3 ngày, Then hệ thống ghi nhận còn 9 ngày phép.

## Lint

Run `python3 scripts/lint_requirements.py <files…>` on every requirements-bearing document,
with all files of one analysis in a single call — they share one ID namespace. A clean exit
on a document that defines no IDs is vacuous, not clean.

| Rule | Fix |
|---|---|
| `vague-term` | replace the word with a measurable criterion |
| `missing-ac` | add `FR-nnn.ACn` / `NFR-nnn.ACn` |
| `dangling-ref` | define the cited ID or correct the citation |
| `duplicate-id` | keep one definition and cite it elsewhere |
| `unmeasurable-nfr` | add a number to the target or its AC |
| `orphan-br` | cite the BR from the FR it drives, or delete it |
