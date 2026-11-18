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
| S6#1 Vietnamese document | yes | no |
| S6#2 English IDs | no | yes |
| S6#3 English Gherkin keywords | no | yes |
| S6#4 Lint clean (incl. VI vague terms) | no | yes |
| S6#5 Handoff file written | yes | yes |
| S6#6 Interview: one question at a time | no | yes |

## Totals

| Phase | S1 | S2 | S3 | S4 | S5 | S5b | S6 | Total |
|---|---|---|---|---|---|---|---|---|
| baseline | 3/8 | 2/6 | 4/7 | 1/5 | 2/2 | 0/1 | 2/6 | **14/35** |
| green | 8/8 | 6/6 | 7/7 | 5/5 | 2/2 | 1/1 | 5/6 | **34/35** |

Green lint runs, all exit 0 with `0 finding(s) in 1 file(s)` and non-vacuous parsing:
S1 (7 BR / 7 FR / 2 NFR), S3 (5 BR / 5 FR), S4 (7 BR / 7 FR / 5 NFR),
S6 (9 BR / 9 FR / 6 NFR). S2 is a process doc with no requirement IDs; its lint run is
vacuous and is not counted. Lane tally: 30/30 answers match the green expected column,
5/5 for every message.

## Still failing

**S6#1 Vietnamese document** — re-scored to `no` after review of regression run 2. The run-1
FR statements keep the English template frame and labels (`green-S6.md` run-1 table, `:52`
and `:57` of the saved doc). All other 34 checks pass with the skill in place.

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

## Regression run 2 (skill 6c645b2)

Fresh re-runs of S1, S3 and S6 after the invented-name refactor (`fc908f0`) and the
required-Basis refactor (`71424bc`), skill at `6c645b2`, one `deepseek-v4.1-flash` agent per
scenario in an isolated `/tmp` repo. Raw logs `raw/green-S1-2.md`, `raw/green-S3-2.md`,
`raw/green-S6-2.md` with matching `-files/` directories. Run 1 scores above are the
re-scored values (S6#1 corrected to `no`); this section is the comparison only. Raw detail
per check (verbatim quotes, locations, lint transcript) is in `green-S1.md`, `green-S3.md`
and `green-S6.md` under the same heading.

| Check | Run 1 | Run 2 |
|---|---|---|
| S1#1 Requirements IDs present | yes | yes |
| S1#2 Acceptance criteria present | yes | yes |
| S1#3 Exception paths covered | yes | yes |
| S1#4 30-day rule recovered with file:line | yes | yes |
| S1#5 No tech/UI design | yes | yes |
| S1#6 Handoff file written | yes | yes |
| S1#7 Lint clean | yes | yes |
| S1#8 Interview: one question at a time | yes | yes |
| S3#1 User asked only answerable gaps | yes | yes |
| S3#2 Author-only gaps become Q-nn with owner | yes | yes |
| S3#3 Both decided rules captured | yes | yes |
| S3#4 Expiry contradiction surfaced | yes | yes |
| S3#5 Traceable IDs | yes | yes |
| S3#6 No N/A filler | yes | yes |
| S3#7 Lint clean | yes | yes |
| S6#1 Vietnamese document | no | no |
| S6#2 English IDs | yes | yes |
| S6#3 English Gherkin keywords | yes | yes |
| S6#4 Lint clean (incl. VI vague terms) | yes | yes |
| S6#5 Handoff file written | yes | yes |
| S6#6 Interview: one question at a time | yes | yes |

### Totals (regression run 2)

| Run | S1 | S3 | S6 | Total |
|---|---|---|---|---|
| run 1 (skill 54b9c11) | 8/8 | 7/7 | 5/6 | **20/21** |
| run 2 (skill 6c645b2) | 8/8 | 7/7 | 5/6 | **20/21** |

Lint in run 2, all exit 0 with `0 finding(s) in 1 file(s)` and non-vacuous parsing:
S1 (12 BR / 9 FR / 3 NFR), S3 (2 BR / 6 FR / 4 NFR), S6 (12 BR / 12 FR / 7 NFR).

Both refactor targets hold in all three docs:

- **NFR Basis column** — every NFR row in S1, S3 and S6 carries a Basis cell that is an input
  quote, an `A-nn` or a `Q-nn`. No row is blank or self-referential.
- **Invented names** — no actor, permission, system name or business number is stated as fact
  without an `A-nn`/`Q-nn` or an input quote. Every actor row in S1 and S6 has a Basis cell;
  S3's stakeholders all come from the transcript. Remaining unlabelled numbers are test-batch
  scales inside NFR targets (S1 NFR-003 "1,000-refund reconciliation", S6 NFR-003 "40 kịch
  bản", S6 NFR-007 "20 thao tác"); none of them states business behaviour.

Still failing in this subset: **S6#1 Vietnamese document**. All 12 FR statement lines keep English frames and labels, e.g. `:65` "- **FR-001**: As a nhân viên, I want gửi yêu cầu nghỉ phép gồm ngày bắt đầu, ngày kết thúc và lý do, so that xin nghỉ đúng quy trình. Fulfils [BR-001, BR-003, BR-005, BR-007]. Priority: Must." and `:93` "- **FR-008**: The system shall ghi nhật ký cho mỗi lần yêu cầu đổi trạng thái. Fulfils [BR-006]. Priority: Must.", repeated at `:73`, `:76`, `:79`, `:82`, `:86`, `:89`, `:96`, `:99`, `:102`, `:106`. The spec lets only IDs, Gherkin keywords and Mermaid stay English (`skills/business-analysis/references/requirements.md:172`, `:174`), and the baseline run wrote Vietnamese prose without such frames (`raw/baseline-S6-1-files/docs/leave-request-requirements.md:6`), so this is a with-skill regression. Lint cannot see it — the rules cover IDs, ACs and vague terms, not prose language. The agent's own reasoning is in `green-S6.md` under "Remaining failures".

The only new content versus run 1 is S3 recording the 30-percent retention target from turn 2 (the earlier S3 runs never received turn 2). Other borderline observations, scored yes, are listed per scenario: S3 FR-005/FR-006 cite no `[BR-nnn]` (no decided rule covers reporting) and S1 NFR-002's "append-only log" wording.

## S6 re-runs after output-language refactor (skill 7297ac4)

Three fresh two-turn S6 reps with the skill at `7297ac4`, `deepseek-v4.1-flash`, isolated
repos. Raw logs `raw/green-S6-{3,4,5}.md`; per-rep evidence in `green-S6.md` under
"REFACTOR iterations". Earlier scores are unchanged.

| Rep | S6#1 | S6#2 | S6#3 | S6#4 | S6#5 | S6#6 | Pass |
|---|---|---|---|---|---|---|---|
| 3 | no | yes | yes | yes | yes | yes | 5/6 |
| 4 | yes | yes | yes | yes | yes | yes | 6/6 |
| 5 | no | yes | yes | yes | yes | yes | 5/6 |
| **Tally** | **1/3** | **3/3** | **3/3** | **3/3** | **3/3** | **3/3** | **16/18** |

The FR statement frame and labels are Vietnamese in all three reps. S6#1 still fails where
headings or basis labels stay English: rep 5 uses English section headings throughout
(`:3` "## Context", `:9` "## Actors and stakeholders", and all sections through `:155`
"## Next step"), and rep 3 keeps `:11` "## Actor và bên liên quan" and `:15` "Input: …" in
the basis column.
