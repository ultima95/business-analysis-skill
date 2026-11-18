# Baseline S3 — Meeting transcript → BRD (hybrid, interview mode)

| Field | Value |
|---|---|
| Phase | baseline (no skill) |
| Run | 1 |
| Agent id | `dcae6fb9-e90f-48fa-97a0-20564b4d48ec` |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Raw log | `raw/baseline-S3-1.md` |
| Saved doc | `raw/baseline-S3-1-files/docs/loyalty-points-requirements.md` (166 lines) |
| Git status | `raw/baseline-S3-1-files/_git-status.txt` |
| Lint | `python3 skills/business-analysis/scripts/lint_requirements.py <doc>` → exit 0, `0 finding(s) in 1 file(s)` — vacuous: the doc's IDs are `FR-1`…`FR-3` and `OI-1`…`OI-5`, none matching `(BR\|FR\|NFR)-\d{3,}`, so 0 requirement blocks were parsed |

## Rubric

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | User asked only answerable gaps | yes | `raw/baseline-S3-1.md:95-97` asks (1) whether to split FR-3, (2) "Rounding semantics for FR-1 … Is per-transaction correct, or is this itself an open question?", (3) "Audience and tone". All three are Lan's to answer; no question targets expiry, the liability figure, tax treatment or the conversion rate. |
| 2 | Author-only gaps become Q-nn with owner | no | The gaps are recorded as `OI-nn`, not `Q-nn` (`docs/loyalty-points-requirements.md:76` "### OI-1 — Redemption conversion rate", `:84` "### OI-2 — Points expiry (**unresolved conflict**)", `:113` "### OI-4 — Tax and accounting classification"; owners are named at `:79` "**Owner:** Lan (Product)" and `:94` "**Owner:** Finance (Hà)"). Ownership is captured; the required ID form is not. |
| 3 | Both decided rules captured | yes | `:36` "### FR-1 — Point earning rate" / `:38` "Customers earn 1 point per 10,000 VND spent."; `:48` "### FR-2 — Non-transferable points" / `:50` "Only the account holder may redeem points." |
| 4 | Expiry contradiction surfaced | yes | `:84` "### OI-2 — Points expiry (**unresolved conflict**)" then `:86` "Two positions were put forward and neither was withdrawn" — neither Ops nor Finance chosen. |
| 5 | Traceable IDs | no | No `BR-nnn` anywhere (`grep -cE '\bBR-\d{3,}'` → 0), so no FR cites `[BR-nnn]`; `grep -c '\.AC'` → 0, so no `FR-nnn.ACn`. §7 "Requirements traceability" (`:155-166`) is a table keyed `FR-1`/`OI-1` with no acceptance criteria. |
| 6 | No N/A filler | yes | `grep -cE '\bN/?A\b'` over the doc → 0. Sections are either filled or absent; `:26-29` states "Out of scope (not discussed, therefore not specified here)" rather than leaving an empty section. |
| 7 | Lint clean | no | Exit 0 is vacuous: the linter parsed 0 blocks because `FR-1` lacks the three-digit form, so no `missing-ac`, `orphan-br` or `vague-term` rule could ever fire. A doc with no canonical IDs counts as failed, not clean. |

**Score: 4 pass / 3 fail.**

## Failure patterns

- **Invented its own ID scheme instead of the required one.** `raw/baseline-S3-1.md:73` "Let me produce a formal requirements doc (markdown) with sections: purpose, scope, decided requirements (FR-1 earning, FR-2 non-transferable…)" — from its first plan it chose `FR-1` and later `OI-1`, so every structural check (traceability, ACs, lint) missed. It never planned business rules or acceptance criteria at all.
- **Skipped the "why" layer entirely.** There is no business objective as a numbered rule; the goal sentence sits in prose at `:14` "The program exists to increase customer retention", so nothing can be traced upward and no FR can cite a BR.
- **Confused ownership with the required open-question register.** `:76-121` records five open items with named owners and even "blocked" impact, but because the IDs are `OI-nn` the doc does not satisfy the `Q-nn` contract that later tasks reuse.
- **Asked meta-questions about its own document.** `raw/baseline-S3-1.md:95` "Should the doc assert a status for FR-3?" and `:97` "Audience and tone — I wrote it for a mixed stakeholder group" — three document-shaping questions rather than one substantive gap, so the turn-2 canned answer (retention target) never got a place to land.
