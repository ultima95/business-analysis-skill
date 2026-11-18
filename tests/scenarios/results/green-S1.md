# Green S1 — Add refunds to the shop (interview mode)

| Field | Value |
|---|---|
| Phase | green (skill `business-analysis` @ 54b9c11) |
| Run | 1 |
| Agent id | `4aa5d4a3-1cf3-4531-9e08-6f679c298a95` |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Raw log | `raw/green-S1-1.md` |
| Saved doc | `raw/green-S1-1-files/docs/ba/2026-11-18-refunds-requirements.md` (157 lines) |
| Git status | `raw/green-S1-1-files/_git-status.txt` |
| Lint | `python3 skills/business-analysis/scripts/lint_requirements.py <doc>` → exit 0, `0 finding(s) in 1 file(s)` — non-vacuous: 7 BR, 7 FR and 2 NFR blocks were parsed |

## Rubric

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Requirements IDs present | yes | `:38` "**BR-001**: An order is in exactly one of five states: pending, paid, shipped, delivered, cancelled."; `:60` "**FR-001**: As a customer, I want to request a refund for a delivered order inside the return window"; IDs run `BR-001`–`BR-007`, `FR-001`–`FR-007`, `NFR-001`–`NFR-002`. |
| 2 | Acceptance criteria present | yes | `:61` "**FR-001.AC1**: Given an order in delivered state with a recorded delivery date 10 days before today, When the customer requests a refund, Then a refund is created in state requested." — every FR carries `.ACn` criteria. |
| 3 | Exception paths covered | yes | `:46` "### Refund eligibility decision table" lists the outcomes "Rejected: outside window", "Rejected: missing delivery date", "Rejected: not delivered", "Rejected: nothing left to refund"; `:62` "**FR-001.AC2**: Given an order in delivered state with a recorded delivery date 31 days before today, When the customer requests a refund, Then the request is rejected with reason outside-window and no refund record is created." |
| 4 | 30-day rule recovered with file:line | yes | `:41` "**BR-004**: A return is allowed only within 30 days of the delivery date, and day 30 is inside the window. Source: `orders.py:15`, `orders.py:29`." Fixture `tests/scenarios/fixtures/shop/orders.py:15` is `RETURN_WINDOW_DAYS = 30`. |
| 5 | No tech/UI design | yes | `grep -niEc '\b(screen\|button\|framework\|react\|database\|sql\|endpoint\|api)\b'` → 0. The only channel wording is `:94` "The system shall notify the customer by email on every refund state change", a notification behaviour, not a stack or screen choice. |
| 6 | Handoff file written | yes | `_git-status.txt:2` "?? docs/ba/2026-11-18-refunds-requirements.md". |
| 7 | Lint clean | yes | Exit 0 with `0 finding(s) in 1 file(s)` on a doc that defines 7 BR, 7 FR and 2 NFR — the linter parsed real blocks, so the run is not vacuous. |
| 8 | Interview: one question at a time | yes | `raw/green-S1-1.md:287` "One question for you: **A paid order that is later cancelled never becomes delivered, so the current return check (`orders.py:25`) rejects it — should such cancelled orders be refundable anyway, or does the refund follow the return rules exactly and refuse them?**" — exactly one question, as the last line. |

**Score: 8 pass / 0 fail.**

## Remaining failures

None. Every S1 check passes.

## Regression run 2 (skill 6c645b2)

Re-run after the invented-name and NFR-Basis refactors (`fc908f0`, `71424bc`), with the
skill at `6c645b2`, a fresh `deepseek-v4.1-flash` agent and an isolated `/tmp` repo. Same S1
prompt and rubric, turn 2 delivered.

| Field | Value |
|---|---|
| Agent id | `f15083ce-2551-44c7-8f86-338d4c7657b9` |
| Raw log | `raw/green-S1-2.md` |
| Saved doc | `raw/green-S1-2-files/docs/ba/2026-11-18-refunds-requirements.md` (172 lines) |
| Git status | `raw/green-S1-2-files/_git-status.txt` |
| Lint | `python3 skills/business-analysis/scripts/lint_requirements.py <doc>` → exit 0, `0 finding(s) in 1 file(s)` — non-vacuous: 12 `BR-nnn` blocks, 9 `FR-nnn` definitions and 3 `NFR` rows were parsed |

### Rubric

| # | Check | yes/no | Evidence |
|---|---|---|---|
| 1 | Requirements IDs present | yes | `:41` "- **BR-001**: Only an order in the delivered state is eligible for a return, and so for a refund. Source: `orders.py:25`."; `:59` "- **FR-001**: As a customer, I want to request a refund for an order I received, so that I get my money back when I no longer want the goods. Fulfils [BR-001], [BR-003], [BR-004], [BR-009]. Priority: Must."; IDs run `BR-001`–`BR-012`, `FR-001`–`FR-009`. |
| 2 | Acceptance criteria present | yes | `:60` "- **FR-001.AC1**: Given an order delivered 12 days ago, When the customer submits a refund request, Then the request is recorded against that order and the order shows a refund in progress." — 24 `FR-nnn.ACn` definitions; every FR carries at least one. |
| 3 | Exception paths covered | yes | `:62` "- **FR-001.AC3**: Given an order delivered 31 days ago, When the customer submits a refund request, Then the request is refused and the refusal states that the 30-day window ended on day 30."; `:63` "- **FR-002**: The system shall refuse a refund request for any order that is not in the delivered state. Fulfils [BR-001], [BR-005]. Priority: Must."; `:83` "Given a pending refund of 5,000,001 VND, When the operator approves it, Then the refund state becomes awaiting finance approval and no payout is made."; `:75` "Given an order with 100.00 captured and 100.00 refunded, When another refund request arrives for that order, Then it is refused and no further refund is recorded." |
| 4 | 30-day rule recovered with file:line | yes | `:43` "- **BR-003**: The return window is 30 days; day 30 is inside the window and day 31 is outside it. Source: `orders.py:15`, `orders.py:29`, `test_orders.py:13-14`, `test_orders.py:21-22`." Fixture `tests/scenarios/fixtures/shop/orders.py:15` is `RETURN_WINDOW_DAYS = 30`; `orders.py:29` is the `<= RETURN_WINDOW_DAYS` comparison; `test_orders.py:13-14`/`:21-22` are the day-30-true and day-31-false assertions. |
| 5 | No tech/UI design | yes | `grep -niE '\b(screen\|button\|framework\|react\|database\|sql\|endpoint\|api\|ui\|page\|form)\b'` over the doc → 0 matches. The only storage-shaped wording is `:98` "written to an append-only log retained for 24 months", an audit property, not a framework or screen choice. |
| 6 | Handoff file written | yes | `_git-status.txt:2` "?? docs/ba/2026-11-18-refunds-requirements.md". |
| 7 | Lint clean | yes | Exit 0 with `0 finding(s) in 1 file(s)` on a doc that defines 12 BR, 9 FR and 3 NFR blocks — the linter parsed real blocks, so the run is not vacuous. |
| 8 | Interview: one question at a time | yes | `raw/green-S1-2.md:469` "**Where does the amount a refund is measured against come from, since `Order` has no amount field — is the captured amount already stored somewhere this repo does not show, or does refund eligibility first need that amount recorded per order?**" — the last line of turn 1 (`[User]` turn 2 starts at `:470`). One question. |

**Score: 8 pass / 0 fail.**

### NFR Basis audit

Every NFR row carries a Basis cell that is an input quote, an `A-nn`, or a `Q-nn`:

- `:97` "| NFR-001 | Must | An eligibility decision is returned to the customer within 2 s at 50 concurrent refund requests | A-05 |"
- `:98` "| NFR-002 | Must | 100% of refund state changes are written to an append-only log retained for 24 months | A-04, A-06 |"
- `:99` "| NFR-003 | Should | Every refund amount is held and shown in VND with 2 decimal places, with 0 rounding differences across a 1,000-refund reconciliation | Requester statement of a 5,000,000 VND threshold; `A-07` |"

The threshold number traces to the requester's own sentence through `BR-010`
("Basis: requester statement \"Any refund over 5,000,000 VND needs a finance approval step\"; the boundary at exactly 5,000,000 VND is `A-11`").

### Invented-name / number audit

No actor, permission, system name, or number is stated as fact without an `A-nn`/`Q-nn` or an
input quote. Actor rows carry a Basis cell: `:15` "| Shop operator | Approves or refuses a refund of 5,000,000 VND or less | Approval step is not present in the code today | `A-03` |"; `:16` "| Finance approver | Approves or refuses a refund above 5,000,000 VND, after the operator | Named by the requester as a required step | Requester statement \"Any refund over 5,000,000 VND needs a finance approval step\"; `A-12` |"; `:18` "| Product owner | Answers the remaining scope and policy questions | Named as owner of every `Q-nn` | `Q-02` … `Q-10` |". The customer row is grounded in code (`orders.py:19-21`) plus the requester statement. One minor gap: the test scale in `NFR-003` ("a 1,000-refund reconciliation") is a working figure whose cell cites the requester threshold and `A-07` but not a scale-specific `A-nn`; the number does not describe business behaviour.

### Remaining failures

None. Every S1 check scores yes. Two borderline observations, both scored yes:

- `:461` (raw report, not the doc) contains a rhetorical question mark — "Refund timing vs return flow undefined: request at return time, or only after goods inspected?" — inside the top-3 risk list. The turn still ends with one question (`raw/green-S1-2.md:469`), so #8 holds under "at most one question" at the end.
- `:98` "append-only log" is the closest thing to an implementation choice in the doc; it states an audit property and names no technology, so #5 holds.
