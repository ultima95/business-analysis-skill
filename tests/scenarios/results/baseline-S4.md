# Baseline S4 — Draft mode, thin ticket (single turn)

| Field | Value |
|---|---|
| Phase | baseline (no skill) |
| Run | 1 |
| Agent id | `a7760074-164c-432d-b317-bf1f8be4b4c1` |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Raw log | `raw/baseline-S4-1.md` |
| Saved doc | `raw/baseline-S4-1-files/docs/requirements/order-cancellation-after-payment.md` (343 lines) |
| Git status | `raw/baseline-S4-1-files/_git-status.txt` |
| Lint | not part of this scenario's rubric (no run) |

## Rubric

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | No invented fact stated as confirmed | no | `:16` "Support tickets show two distinct failures:" and the whole `:37-43` success table ("`≥ 80%`", "`Refund issued within 60s of confirmed cancellation \| ≥ 99%`", "`−90% vs. baseline`") are presented as the business's own targets with no assumption or question label. §5 `:83-84` does label its state-machine guesses, so the problem is not labelling as a policy but labelling only some inventions. |
| 2 | Assumptions recorded as A-nn | no | `:81` "### 5. Current-state assumptions" and `:321` "## 12. Assumptions to validate before build" are numbered `1.`–`7.`, not `A-nn`; `grep -cE '\bA-[0-9]{2,}'` → 0. |
| 3 | Open questions recorded as Q-nn with owner | no | No `Q-nn` anywhere (`grep -cE '\bQ-[0-9]{2,}'` → 0). The closest artefact, `:321-334`, is titled "Assumptions to validate" and names no owner for any item. |
| 4 | Q-nn names blocked requirement | no | No `Q-nn` exists, so none names what it blocks. `:336` does say "If any of 1–4 turn out false, the corresponding requirement above must be revised", i.e. a range of assumptions, not a per-question blocked requirement. |
| 5 | Draft mode writes anyway | yes | Full document written and saved: `_git-status.txt:2` "?? docs/requirements/order-cancellation-after-payment.md"; the reply asks nothing (`raw/baseline-S4-1.md:70-84`), consistent with "I'm not available for follow-up questions". |

**Score: 1 pass / 4 fail.**

## Failure patterns

- **Fabricated evidence to justify the feature.** `raw/baseline-S4-1.md:23` shows the agent deciding to write "problem statement, scope, personas, current-state assumptions…" from an empty repo, yet the doc asserts `:16` "Support tickets show two distinct failures" and `:25-27` "a measurable drop in repeat purchase rate" as if these were observed. Nothing in the ticket supports any of it.
- **Filled the gap with invented targets rather than flagged assumptions.** `:39-43` supplies specific numbers ("≥ 80%", "≥ 99%", "< 0.1%", "−90%") with no A-id and no question, so downstream work cannot tell a decided target from the agent's guess.
- **Used the wrong register for unknowns.** Its own plan (`raw/baseline-S4-1.md:57`) was "Open questions (documented as decisions pending vs assumed)" and `:23` "open questions (even though user unavailable — list assumptions instead)" — the two got merged into one prose list at `:321`, losing both the `A-nn` and `Q-nn` handles.
- **Pushed decisions into requirements instead of questions.** `raw/baseline-S4-1.md:76-82` "Key decisions I made on your behalf" is a table of business calls (line-item cancellation, no time window, void vs refund, fees default zero) presented in the chat reply as settled, while the doc encodes them as normative FRs (`:113-116`, `:199-201`).
