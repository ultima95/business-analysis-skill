# Green S3 — Meeting transcript → BRD (job 1 + 3, hybrid mode)

| Field | Value |
|---|---|
| Phase | green (skill `business-analysis` @ 54b9c11) |
| Run | 1 |
| Agent id | `fb683afa-1a32-4212-83ce-9c44c6aaebde` |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Raw log | `raw/green-S3-1.md` |
| Saved doc | `raw/green-S3-1-files/docs/ba/2026-11-18-loyalty-points-brd.md` (169 lines) |
| Git status | `raw/green-S3-1-files/_git-status.txt` |
| Lint | `python3 skills/business-analysis/scripts/lint_requirements.py <doc>` → exit 0, `0 finding(s) in 1 file(s)` — non-vacuous: 5 BR and 5 FR blocks were parsed |

## Rubric

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | User asked only answerable gaps | yes | `raw/green-S3-1.md:1011` "**One question:** Should this first release ship with earning and non-transferability only, and hold FR-002 (redemption) until Lan's conversion rate lands — or is redemption a launch blocker?" — a scope/priority question Lan can answer; no question targets expiry, the liability figure, tax treatment or the conversion rate. |
| 2 | Author-only gaps become Q-nn with owner | yes | `:141` "\| Q-01 \| Do points expire? … \| Hà (Finance), pending auditor input; Minh to supply the ops view \| all FRs for expiry \|"; `:144` "\| Q-04 \| For tax purposes, is a redemption treated as a discount on the sale or as a separate payment method? \| Hà (Finance) \| FR-002 \|"; `:145` "\| Q-05 \| What was the total outstanding points liability as of last quarter, from the ledger? \| Hà (Finance) \| FR-005 \|". |
| 3 | Both decided rules captured | yes | `:69` "**BR-001**: One point is awarded for each 10,000 VND of value spent, rounded down to a whole point."; `:70` "**BR-002**: Only the account holder may redeem points from an account." and `:71` "**BR-003**: Points cannot be transferred between accounts." |
| 4 | Expiry contradiction surfaced | yes | `:141` quotes both sides: "Minh stated \"Points should expire six months after the customer's last activity\"; Hà stated \"Points should never expire\"" — recorded as Q-01, neither side chosen. |
| 5 | Traceable IDs | yes | `:77` "**FR-001**: … Fulfils [BR-001]. Priority: Must."; `:78` "**FR-001.AC1**: Given a purchase with a transaction total of 25,000 VND, When the purchase is completed, Then 2 points are added to the account holder's balance." — every FR cites a `[BR-nnn]` and every AC carries its parent ID. |
| 6 | No N/A filler | yes | `grep -c 'N/A'` over the doc → 0. The `## Non-functional requirements` section states the missing target as a Q-nn rather than an empty "N/A" section. |
| 7 | Lint clean | yes | Exit 0 with `0 finding(s) in 1 file(s)` on a doc that defines 5 BR and 5 FR — real blocks were parsed, so the run is not vacuous. |

**Score: 7 pass / 0 fail.**

## Remaining failures

None. Every S3 check passes.

## Regression run 2 (skill 6c645b2)

Re-run after the invented-name and NFR-Basis refactors (`fc908f0`, `71424bc`), with the
skill at `6c645b2`, a fresh `deepseek-v4.1-flash` agent and an isolated `/tmp` repo. This is
the first S3 run in which turn 2 was actually delivered (the earlier runs lost it to the
controller's prompt-extraction bug), so the 30-percent retention target is present.

| Field | Value |
|---|---|
| Agent id | `39944162-affb-4a00-bfd0-df8ed6e6a9ef` |
| Raw log | `raw/green-S3-2.md` |
| Saved doc | `raw/green-S3-2-files/docs/ba/2026-11-18-loyalty-points-brd.md` (196 lines) |
| Git status | `raw/green-S3-2-files/_git-status.txt` |
| Lint | `python3 skills/business-analysis/scripts/lint_requirements.py <doc>` → exit 0, `0 finding(s) in 1 file(s)` — non-vacuous: 2 `BR-nnn` blocks, 6 `FR-nnn` definitions and 4 `NFR` rows were parsed |

### Rubric

| # | Check | yes/no | Evidence |
|---|---|---|---|
| 1 | User asked only answerable gaps | yes | `raw/green-S3-2.md:945` "One question, and I'll stop there: of the open items, which ones are launch blockers versus can-ship-later — specifically, should redemption (FR-002) ship at launch at all, or is earning-only (FR-001) plus the ledger (FR-004) enough for the first release?" — a scope/sequencing question the PM can answer; no question asks for the expiry decision, the liability figure, the tax treatment, or the conversion rate value. |
| 2 | Author-only gaps become Q-nn with owner | yes | `:168` "\| Q-02 \| Do points expire six months after the customer's last activity, or never expire? Verbatim conflict — Minh: \"Points should expire six months after the customer's last activity.\" Hà: \"No — that contradicts what I said earlier. Points should never expire.\" \| Hà (Finance), pending auditor confirmation; Minh (Ops) holds the six-month position \| all FRs for points expiry \|"; `:169` "\| Q-03 \| What is the total outstanding points liability as of last quarter? \| Hà (Finance) — from the ledger \| FR-005 \|"; `:170` "\| Q-04 \| Are redeemed points treated as a discount or as a separate payment method for tax purposes? \| Hà (Finance) \| FR-002, FR-005 \|". |
| 3 | Both decided rules captured | yes | `:69` "- **BR-001**: A purchase earns 1 point for each complete 10,000 VND of value, rounded down, so any remainder below 10,000 VND earns no point."; `:70` "- **BR-002**: Points belong to the account that earned them; points cannot be transferred to another account, and only the account holder may redeem them." |
| 4 | Expiry contradiction surfaced | yes | `:168` quotes both sides verbatim: "Minh: \"Points should expire six months after the customer's last activity.\" Hà: \"No — that contradicts what I said earlier. Points should never expire.\"" and records it as Q-02, neither side chosen. |
| 5 | Traceable IDs | yes | `:81` "- **FR-001**: As a customer, I want to earn points on each purchase at the agreed rate, so that my balance grows with my spending. Fulfils [BR-001]. Priority: Must."; `:82` "- **FR-001.AC1**: Given a purchase of 35,000 VND, When the transaction completes, Then 3 points are added to the account holder's balance." — every AC carries its parent ID; 4 of 6 FRs cite a `[BR-nnn]`. |
| 6 | No N/A filler | yes | `grep -c 'N/A'` over the doc → 0. The out-of-scope section names open items by `Q-nn` reference (`:50` "Points expiry behaviour — no decision exists; see Q-02.") rather than emptying a section. |
| 7 | Lint clean | yes | Exit 0 with `0 finding(s) in 1 file(s)` on a doc that defines 2 BR, 6 FR and 4 NFR blocks — the run is not vacuous. |

**Score: 7 pass / 0 fail.**

### NFR Basis audit

Every NFR row carries a Basis cell that is an input quote, an `A-nn`, or a `Q-nn`:

- `:109` "| NFR-001 | Must | Redemption at checkout completes within 2 seconds at p95, measured from the cashier starting the redemption to the discount being recorded | A-02 |"
- `:110` "| NFR-002 | Must | Ledger entries are append-only, are never modified or deleted after recording, and are retained for at least 7 years | A-03 |"
- `:111` "| NFR-003 | Must | The outstanding points total for any chosen past date is produced within 1 business day of the request | A-05 |"
- `:112` "| NFR-004 | Must | 100 percent of redemption attempts require identification of the account holder, with 0 redemptions completed on an account other than the one identified | Input: \"only the account holder can redeem points. No transfers between accounts\" |"

The 2-second target's source quote ("Redemption has to be fast") is kept out of the NFR row
and appears only in `A-02` at `:140`, so the vague word never lands in a definition block.

### Invented-name / number audit

No actor, permission, system name, or number is stated as fact without an `A-nn`/`Q-nn` or an
input quote. Every stakeholder is named in the transcript (`:60`–`:65`), and the only
permission rule (`:70`, non-transferability and account-holder-only redemption) is the
transcript's own decided rule. The 30-percent target traces to the turn-2 answer and its two
undefined parts are labelled `A-08` and `A-09` at `:146`–`:147`. No system name is invented;
the doc refers to "the ledger" only as the term Finance used.

### Remaining failures

None. Every S3 check scores yes. Three borderline observations, all scored yes:

- `:95` "- **FR-005**: As a finance user, I want the total outstanding points across all accounts for any chosen date, so that the liability on the books reflects the points customers still hold. Priority: Must." and `:99` FR-006 cite no `[BR-nnn]`, because no decided business rule covers liability reporting or the retention metric. The rubric's "FRs cite BRs" is satisfied by the four FRs that enforce a rule; if the check is ever read as "every FR cites a BR", these two would fail it.
- `:99` FR-006 is a reporting capability created from the turn-2 metric, not from the transcript; its justification sits in the objectives table (`:26`–`:28`) rather than in a BR.
- `:171` Q-05 ("What launch date applies…") blocks "all FRs for release scope", the weakest Blocks entry in the table; the transcript does leave the date undecided, so the row is honest, but it names no single requirement.
