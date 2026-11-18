# GREEN summary — baseline vs. with-skill rubric

Skill under test: `skills/business-analysis/` at commit `54b9c11`, read from
`/tmp/ba-skill-under-test/business-analysis/SKILL.md` by every green run.
Baseline scored files: `baseline-S*.md`, `baseline-lane.md`. Green scored files:
`green-S*.md`, `green-lane.md`.

`yes` / `no` are the rubric result. Baseline totals come from the per-scenario baseline
files; green totals from the per-scenario green files.

| Check | Baseline | Green |
|---|---|---|
| S1#1 Requirements IDs present | no | yes |
| S1#2 Acceptance criteria present | no | yes |
| S1#3 Exception paths covered | yes | yes |
| S1#4 30-day rule recovered with file:line | no | yes |
| S1#5 No tech/UI design | yes | yes |
| S1#6 Handoff file written | yes | yes |
| S1#7 Lint clean | no | yes |
| S1#8 Interview: one question at a time | no | yes |
| S2#1 Process doc written | yes | yes |
| S2#2 As-is Mermaid swimlane | no | yes |
| S2#3 To-be Mermaid swimlane | no | yes |
| S2#4 SIPOC present | no | yes |
| S2#5 Pain points tied to steps | no | yes |
| S2#6 Root cause for top pain | yes | yes |
| S3#1 User asked only answerable gaps | yes | yes |
| S3#2 Author-only gaps become Q-nn with owner | no | yes |
| S3#3 Both decided rules captured | yes | yes |
| S3#4 Expiry contradiction surfaced | yes | yes |
| S3#5 Traceable IDs | no | yes |
| S3#6 No N/A filler | yes | yes |
| S3#7 Lint clean | no | yes |
| S4#1 No invented fact stated as confirmed | no | yes |
| S4#2 Assumptions recorded as A-nn | no | yes |
| S4#3 Open questions recorded as Q-nn with owner | no | yes |
| S4#4 Q-nn names blocked requirement | no | yes |
| S4#5 Draft mode writes anyway | yes | yes |
| S5#1 Skill does not take over | yes | yes |
| S5#2 Defers to brainstorming | yes | yes |
| S5b#1 BA picked over brainstorming | no | yes |
| S6#1 Vietnamese document | yes | yes |
| S6#2 English IDs | no | yes |
| S6#3 English Gherkin keywords | no | yes |
| S6#4 Lint clean (incl. VI vague terms) | no | yes |
| S6#5 Handoff file written | yes | yes |
| S6#6 Interview: one question at a time | no | yes |

## Totals

| Phase | S1 | S2 | S3 | S4 | S5 | S5b | S6 | Total |
|---|---|---|---|---|---|---|---|---|
| baseline | 3/8 | 2/6 | 4/7 | 1/5 | 2/2 | 0/1 | 2/6 | **14/35** |
| green | 8/8 | 6/6 | 7/7 | 5/5 | 2/2 | 1/1 | 6/6 | **35/35** |

Green lint runs, all exit 0 with `0 finding(s) in 1 file(s)` and non-vacuous parsing:
S1 (7 BR / 7 FR / 2 NFR), S3 (5 BR / 5 FR), S4 (7 BR / 7 FR / 5 NFR),
S6 (9 BR / 9 FR / 6 NFR). S2 is a process doc with no requirement IDs; its lint run is
vacuous and is not counted. Lane tally: 30/30 answers match the green expected column,
5/5 for every message.

## Still failing

None. All 35 checks pass with the skill in place. No skill-file change is proposed for
Part A.

Borderline observations recorded while scoring (all scored `yes`, no change proposed):

- **S1#5** — `green-S1-1-files/docs/ba/2026-11-18-refunds-requirements.md:94` says
  "The system shall notify the customer by email on every refund state change". It is a
  notification behaviour, not a stack or screen choice, and the baseline scorer passed the
  same check on contract/data-model wording; if the check is ever tightened to ban channel
  choices, this line would fail.
- **S4#1** — the requirements' business rules (for example the `cancel-order` permission at
  `:38` "a Support agent holding the `cancel-order` permission") are draft-mode proposals;
  the invented *numbers* are labelled by A-07, but the invented *rule names* have no A row.
  Under the rubric ("no fabricated number or rule is stated as fact") this passes because
  the document is explicitly a proposal set, but it is the closest green result to the
  baseline failure pattern.
- **S3#2** — `green-S3-1-files/docs/ba/2026-11-18-loyalty-points-brd.md:141` gives Q-01 two
  owners ("Hà (Finance), pending auditor input; Minh to supply the ops view"); the check
  asks for "a Q-nn naming that owner" and both owners are named.

## S4 refactor re-runs (skill fc908f0)

Three fresh S4 reps after the invented-name refactor (`fc908f0`), deepseek-v4.1-flash,
isolated. Raw logs `raw/green-S4-{2,3,4}.md`; per-rep evidence in `green-S4.md` under
"REFACTOR iterations". The run-1 scores above are unchanged.

| Rep | S4#1 | S4#2 | S4#3 | S4#4 | S4#5 |
|---|---|---|---|---|---|
| 2 | no | yes | yes | yes | yes |
| 3 | no | yes | yes | yes | yes |
| 4 | yes | yes | yes | yes | yes |
| **Tally** | **1/3** | **3/3** | **3/3** | **3/3** | **3/3** |

S4#1 passes 1/3. The targeted class is closed: every inferred actor/role and permission in
all three reps is tied to an A-nn. Remaining failures are numeric targets — `green-S4-2`
`:73` "p95 cancellation response ≤ 2 s at 50 concurrent cancellation requests" has no
A-nn/Q-nn label, and rep 2 also names a system the A-01 row does not cover (`:18`
"Cancellation service (system)"); `green-S4-3` `:84` "cancellation path available 99.9% of
minutes per calendar month" is unlabelled while its sibling NFRs carry placeholders.

### S4 re-runs after required-basis refactor (skill 71424bc)

Three fresh reps after the NFR Basis-column change. Raw logs `raw/green-S4-{5,6,7}.md`;
per-rep evidence in `green-S4.md` (Iteration 2). Run-1 and iteration-1 scores are unchanged.

| Rep | S4#1 | S4#2 | S4#3 | S4#4 | S4#5 |
|---|---|---|---|---|---|
| 5 | yes | yes | yes | yes | yes |
| 6 | yes | yes | yes | yes | yes |
| 7 | yes | yes | yes | yes | yes |
| **Tally** | **3/3** | **3/3** | **3/3** | **3/3** | **3/3** |

S4#1 passes 3/3: every inferred actor/role and every NFR numeric target is tied to a Basis
entry. One form defect remains: `green-S4-5` NFR-003/NFR-005 put `BR-007` in the Basis cell
instead of an A-nn/Q-nn, though A-12's blanket "all numeric targets … are working values"
row still labels those numbers.
