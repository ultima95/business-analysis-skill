# Green S2 — Invoice approval process (two turns)

| Field | Value |
|---|---|
| Phase | green (skill `business-analysis` @ 54b9c11) |
| Run | 1 (scored rerun, canned turn 2 per Ruling R18) |
| Agent id | `120fa5aa-5117-419f-9c2f-7689559d3206` |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Raw log | `raw/green-S2-1.md` |
| Saved doc | `raw/green-S2-1-files/docs/ba/2026-11-18-invoice-approval-process.md` (215 lines) |
| Git status | `raw/green-S2-1-files/_git-status.txt` |
| Lint | not applicable — process doc with no `BR/FR/NFR-nnn` IDs (`:1` "Process document: steps are P1, P2… No BR/FR/NFR IDs appear in this file."). Run anyway: exit 0, `0 finding(s) in 1 file(s)` — vacuous, so it is not cited as evidence. |

The first attempt (`raw/green-S2-0-asked-only.md`) entered interview mode and ended after
one question, because the harness ran S2 as a single turn. Ruling R18 treats that as a
harness gap; the rerun below with a canned turn 2 is what this file scores. The
first-attempt log is supporting evidence that the "one question at a time" behaviour held.

## Rubric

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Process doc written | yes | `_git-status.txt:2` "?? docs/ba/2026-11-18-invoice-approval-process.md". |
| 2 | As-is Mermaid swimlane | yes | `:42` "### Swimlane" → `:44` "```mermaid" / `:46` "subgraph employee [\"Employee\"]" / `:50` "subgraph manager [\"Manager\"]" / `:55` "subgraph finance [\"Finance\"]", with the P1–P8 as-is edges between them. |
| 3 | To-be Mermaid swimlane | yes | `:118` "## To-be process" → `:138` "```mermaid" / `:140` "subgraph employee [\"Employee\"]" / `:143` "subgraph manager [\"Manager\"]" / `:149` "subgraph finance [\"Finance\"]". |
| 4 | SIPOC present | yes | `:21` "## SIPOC" and `:23` "\| Suppliers \| Inputs \| Process \| Outputs \| Customers \|". |
| 5 | Pain points tied to steps | yes | `:70` "## Pain points" table has a `Step` column: `:74` "\| P3 \| Case cannot move while the manager is away; no named stand-in" and `:75` "\| P5 → P6 \| Approval sits in one person's inbox; Finance has no shared queue"; every row names its step. |
| 6 | Root cause for top pain | yes | `:96` "Root cause: no written approval policy that names who may approve when the usual approver is unavailable." — resolved for the top-ranked P3 pain through the 5 Whys at `:85` "## Root cause". |

**Score: 6 pass / 0 fail.**

## Remaining failures

None. Every S2 check passes.
