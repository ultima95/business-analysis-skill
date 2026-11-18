# Green S4 — Draft mode, thin ticket (single turn)

| Field | Value |
|---|---|
| Phase | green (skill `business-analysis` @ 54b9c11) |
| Run | 1 |
| Agent id | `1f220a1d-11d4-4850-a847-2c98ddf79665` |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Raw log | `raw/green-S4-1.md` |
| Saved doc | `raw/green-S4-1-files/docs/ba/2026-11-18-order-cancellation-after-payment-requirements.md` (154 lines) |
| Git status | `raw/green-S4-1-files/_git-status.txt` |
| Lint | not part of this scenario's rubric; run anyway → exit 0, `0 finding(s) in 1 file(s)` (7 BR, 7 FR, 5 NFR parsed) |

## Rubric

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | No invented fact stated as confirmed | yes | `:5` "Problem: customers who have already paid cannot cancel their order. The ticket reports the block exists; it does not say which payment methods, order states, or channels are affected."; `:6` "Why now: not stated in the ticket. The driver and any target date are recorded as Q-01."; `:131` "A-07 \| The numeric targets in NFR-001 to NFR-005 are provisional proposals pending Finance and Support sign-off." — the invented NFR numbers carry an explicit provisional label. |
| 2 | Assumptions recorded as A-nn | yes | `:125` "\| A-01 \| This release covers whole-order cancellation only; cancelling individual line items is out of scope. \| …"; the table runs `A-01`–`A-08` at `:121` "## Assumptions". |
| 3 | Open questions recorded as Q-nn with owner | yes | `:144` "\| Q-01 \| What business event produced this ticket, and by what date must cancellation be live? \| Ticket author / Product owner \| all FRs for the cancellation release \|"; all of `Q-01`–`Q-07` name an owner. |
| 4 | Q-nn names blocked requirement | yes | `:147` "\| Q-04 \| Are shipping and handling charges refunded with the order total? \| Finance \| BR-002, FR-002 \|"; `:148` "\| Q-05 \| What is the agreed resolution time for a `Failed` refund? \| Finance operations \| NFR-002, FR-007 \|" — every Q row has a `Blocks` cell naming requirement IDs. |
| 5 | Draft mode writes anyway | yes | `_git-status.txt:2` "?? docs/ba/2026-11-18-order-cancellation-after-payment-requirements.md"; the reply asks nothing and ends at `raw/green-S4-1.md:267` "Next: brainstorm solution with this file as context, then writing-plans." |

**Score: 5 pass / 0 fail.**

## Remaining failures

None. Every S4 check passes.

## REFACTOR iterations

Iteration 1 — failure: the agent wrote invented actors and a permission as plain fact — doc `:14` "| Customer support agent | cancels on the customer's behalf; decides within policy | needs the `cancel-order` permission |", `:38` "- **BR-003**: Only the Customer who placed the order, or a Support agent holding the `cancel-order` permission, may cancel it. Every other actor is refused.", and the actor rows at `:13-17`, with no A-nn/Q-nn row; the run's own reasoning applied the invented-fact rule to numbers only (`raw/green-S4-1.md:37` "Careful not to invent. Make it assumption.") while planning `raw/green-S4-1.md:63` "- BR-003: Only the customer who placed the order, or a support agent holding the cancel-order permission, may cancel it." — change: `skills/business-analysis/SKILL.md:110` now reads "| A metric, stakeholder, rule, quote, actor, role, team, permission, or system or component name that is not in the input or the user's answers, written as fact | Invented. Every one must be an A-nn or a Q-nn, never a confirmed statement. |" — result:

| Rep | S4#1 | S4#2 | S4#3 | S4#4 | S4#5 | Evidence |
|---|---|---|---|---|---|---|
| 2 (`green-S4-2`, `63f043d1-2f90-456b-a3fa-35cc26bef5ba`) | no | yes | yes | yes | yes | Actor rows `:15-17` cite `A-01`; `:18` "| Cancellation service (system) | Enforces the cut-off, calls payments, records the attempt | Derived from `A-01`; no implementation is described here |" is not covered by A-01, and glossary `:106` "| Paid | The payment provider has captured money for the order. |" names a system with no A-nn/Q-nn row. NFR-001–003 and NFR-005 (`:73-75`, `:77`) carry no provisional label: `:73` "| NFR-001 | Must | p95 cancellation response ≤ 2 s at 50 concurrent cancellation requests |". |
| 3 (`green-S4-3`, `22f3d2f6-4add-4fc2-89b3-e64a387dc487`) | no | yes | yes | yes | yes | Actor rows `:15-18` cite `A-05`–`A-08` and BR-007 cites `A-06`, so permissions are labelled. NFR-001, NFR-002 and NFR-004 carry "(placeholder; see Q-10/Q-07)", but `:84` "| NFR-003 | Should | cancellation path available 99.9% of minutes per calendar month |" and `:87` "| NFR-006 | Could | fewer than 1% of cancellation requests ending in an unhandled error over a calendar month |" carry no A-nn/Q-nn label. |
| 4 (`green-S4-4`, `9f8e5087-b73d-497d-9c4c-21b840a79032`) | yes | yes | yes | yes | yes | Actor rows `:17-19` cite `A-02`–`A-07`, and `:94` "All targets here are working values set by this analysis, not targets stated in the ticket." labels every NFR target as a working value; BR-001–BR-009 each name an A-nn basis. |

Verdict: S4#1 passes 1/3 (rep 4 only). The actor/permission class is closed — every inferred actor row in all three reps cites an A-nn. Remaining unlabeled inventions are numeric targets and one system name: `green-S4-2` `:73` "p95 cancellation response ≤ 2 s at 50 concurrent cancellation requests" and `:18` "Cancellation service (system) … Derived from `A-01`"; `green-S4-3` `:84` "cancellation path available 99.9% of minutes per calendar month".

Iteration 2 — failure: NFR numeric targets invented and unlabeled in 2/3 re-runs — `raw/green-S4-2-files/docs/ba/2026-11-18-order-cancellation-requirements.md:73` "| NFR-001 | Must | p95 cancellation response ≤ 2 s at 50 concurrent cancellation requests |" and `raw/green-S4-3-files/docs/ba/2026-11-18-order-cancellation-after-payment-requirements.md:84` "| NFR-003 | Should | cancellation path available 99.9% of minutes per calendar month |"; cause: the skill requires every NFR to carry a number, so the agent invents one — change: NFR rows now carry a required Basis column, and the actors table gains a basis slot — `skills/business-analysis/SKILL.md:95` "| Non-functional requirement | `| NFR-001 | <priority> | <measurable target> | <basis: input quote, A-nn, or Q-nn> |` plus `- **NFR-001.AC1**: Given …, When …, Then ….` |"; `skills/business-analysis/references/requirements.md:33` "| Non-functional requirement | `\| NFR-001 \| Must \| <measurable target with a number> \| <basis: input quote, A-nn, or Q-nn> \|` |", `:38-40` "The NFR table has four columns: ID, MoSCoW priority, target, basis. The target cell carries the number the lint script requires; the basis cell says where that number came from — a short verbatim quote from the input or user answers, an `A-nn`, or a `Q-nn` with its owner.", `:97-99` "Every NFR target needs a number, and its Basis says where the number came from: a quote from the input, an `A-nn` for a working value you set, or a `Q-nn` owned by the person who can set the target."; `skills/business-analysis/templates/requirements.md:13-15` "| Actor | Does / decides / is informed | Notes | Basis |" … "| <role> | <trigger, do, decide, or informed> | <constraint or fact from the input> | <input quote, or A-nn> |" and `:40-42` "| ID | Priority | Target | Basis |" … "| NFR-001 | Must | p95 response time ≤ 2 s at 100 concurrent users | A-01 |"; `skills/business-analysis/templates/brd.md:58-61` "| ID | Priority | Target | Basis |" … "| NFR-001 | Must | p95 response time ≤ 2 s at 50 concurrent users | A-01 |" … "| NFR-002 | Must | 99.5 percent monthly availability | A-01 |" — result: pending re-run (controller)
