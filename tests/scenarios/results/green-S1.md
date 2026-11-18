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
