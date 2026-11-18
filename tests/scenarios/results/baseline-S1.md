# Baseline S1 — Add refunds to the shop (interview mode)

| Field | Value |
|---|---|
| Phase | baseline (no skill) |
| Run | 1 |
| Agent id | `0f4680fe-2a3c-4fd8-8c09-71a4070b9ec8` |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Raw log | `raw/baseline-S1-1.md` |
| Saved doc | `raw/baseline-S1-1-files/REFUNDS.md` (146 lines) |
| Git status | `raw/baseline-S1-1-files/_git-status.txt` |
| Lint | `python3 skills/business-analysis/scripts/lint_requirements.py <REFUNDS.md>` → exit 0, `0 finding(s) in 1 file(s)` — vacuous: 0 `BR|FR|NFR-nnn` IDs parsed |

## Rubric

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Requirements IDs present | no | `REFUNDS.md:22` "**R1 — One eligibility gate.**"; `grep -cE '\b(BR\|FR\|NFR)-[0-9]{3,}' REFUNDS.md` → 0. Rules are named `R1`–`R9`, exceptions `H1`–`H9`. |
| 2 | Acceptance criteria present | no | No `FR-nnn` exists, so no `FR-nnn.ACn` can match; `grep -c '\.AC' REFUNDS.md` → 0. `§7 Tests to add` (`REFUNDS.md:131`) is prose bullets, not criteria. |
| 3 | Exception paths covered | yes | `REFUNDS.md:113` "**H8 — Fully refunded, then asked again.** Returns `ALREADY_REFUNDED`"; `REFUNDS.md:90` "## 5. Exception cases" covers non-delivered, missing date, out-of-window, over-limit approval, future date. |
| 4 | 30-day rule recovered with file:line | no | `REFUNDS.md:17` "Window is inclusive: day 30 allowed, day 31 refused \| `RETURN_WINDOW_DAYS`, tests" — window stated, but the source cell cites `RETURN_WINDOW_DAYS`/`orders.py` with no line number (see also `REFUNDS.md:14`). No `orders.py:NN` appears anywhere. |
| 5 | No tech/UI design | yes | No framework, no screen/UI text. `REFUNDS.md:18` "Refund API takes `today` too" and `REFUNDS.md:123` "`Order`: add `total` (VND int)" are contract/data-model notes, not technology choices or UI description. |
| 6 | Handoff file written | yes | `_git-status.txt:2` "?? REFUNDS.md". |
| 7 | Lint clean | no | Exit was 0, but vacuously: the doc defines no `BR-nnn`/`FR-nnn`/`NFR-nnn` block, so the linter parsed 0 requirement blocks and had nothing to check. A clean run on a doc with no IDs is not evidence of a lint-clean requirements doc. |
| 8 | Interview: one question at a time | no | `raw/baseline-S1-1.md:99-103` — "Questions:" then four numbered items: "1. Fix `can_return` for the negative-days hole, or guard only inside refunds? Literal mirroring would reproduce bug.", "2. Is `CANCELLED` already money-refunded elsewhere — refund target or hard refusal?", "3. `REFUNDED` as new `OrderStatus` member, or separate refund record while order stays `DELIVERED`?", "4. Full-total refunds only, or partials eventually needed?" |

**Score: 3 pass / 5 fail.**

## Failure patterns

- **Wrote a design note, not requirements.** Its own plan says the artefact is a "spec" of rules: `raw/baseline-S1-1.md:23` "Refund rules should mirror return rules. Write markdown doc. Include decisions/derived rules, exceptions, gaps/open questions." The result is technical design — outcome enum values (`REFUNDS.md:75-88`), a fixed check order (`REFUNDS.md:49`), a data-model section (`REFUNDS.md:118`), a "Tests to add" section (`REFUNDS.md:131`) — and no requirement IDs, so nothing is traceable.
- **Read the code, then dropped the provenance.** It did read the fixture (`raw/baseline-S1-1.md:11` "I'll read the existing code first." / `[Read]`), yet its fact table cites only bare filenames and constant names (`REFUNDS.md:14` source column "`orders.py`"), never a line number, so check 4 cannot be verified from the doc by a reader.
- **Asked a wall of questions.** `raw/baseline-S1-1.md:87` "Use plain text questions… I'll ask in text." then four numbered questions (`:99-103`), after `:105` "Stopping here." Nothing was drafted for turn 1 beyond the first doc; the interview was effectively a requirements review rather than a single blocking question.
- **Treated a code bug as a design decision to settle itself.** `raw/baseline-S1-1.md:147` "must draft now. Decide: refund path uses its own `is_within_window` helper…" — it resolved the negative-days hole by choosing an implementation refactor rather than recording it as an open business question.
