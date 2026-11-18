# Code recovery — current rules as-is

Loaded for job 1 when the analysis runs inside a repository. Goal: recover the business
rules the code enforces today, with provenance a reader can check, and surface every
requirement that would change existing behaviour.

Recovery is evidence gathering, not design. Never propose, plan, or write a code change.

## Where rules hide

| Place | Search for |
|---|---|
| Entities and status enums | the domain nouns from the input, `status` / `state` / `class` / `enum` declarations |
| Constants and config | thresholds, windows, limits, `*_DAYS`, `MAX_*`, `MIN_*`, feature flags |
| Validators and guards | `validate`, `check`, `can_*`, `is_*`, `raise`, error codes |
| State transitions | assignments to status fields, transition tables, workflow definitions |
| Tests | names and fixtures that pin a rule — "30 days", "insufficient balance" |

Start from the domain nouns in the input, then follow the hits:

```sh
grep -rn "refund\|return" --include='*.py' .
grep -rn "ORDER_STATUS\|DELIVERED\|CANCELLED" .
grep -rn "30\b\|WINDOW\|DAYS" .
```

Use the project's language and file extensions. Read every file that owns a hit; a constant
name alone is not a rule until you see how it is compared.

## Recovered-rule entry format

Record each rule as a `BR-nnn` in the requirements document. The source slot is required —
a rule with no line number was not recovered and must not be written as a finding.

- **BR-004**: A return is accepted only within 30 days of delivery; day 30 is inside the window. Source: `shop/orders.py:12`.

| Slot | Required content |
|---|---|
| `BR-nnn` | the next free business-rule ID in this document |
| Rule | one testable statement of the behaviour the code enforces, in business words |
| `Source:` | `path/to/file:<line>` for the exact line that enforces it; comma-separate multiple sources |

Do not paste code. Summarize the rule; the citation is the proof. The line number points at
the line a reader opens to verify the claim, not at the enclosing function.

## Conflicting requirements

When a new requirement would contradict a recovered rule, do not rewrite the rule and do
not pick a winner. Add a Q-nn owned by the person who can decide:

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-03 | Conflicts with `shop/orders.py:12` (code allows 30 days): the request allows 45-day returns. Which applies? | <product owner> | FR-002, FR-004 |

The question names the contradiction and its `file:line`; the `Blocks` column names the
requirements that wait on the answer.

## Limits

- Cite only behaviour you can point to on a line of source. An inference is an A-nn, not a BR.
- Read tests as evidence of intended behaviour and say so: "`test_orders.py:40` pins day 30".
- A missing or unreadable source means the rule is not recovered — raise a Q-nn instead.
- Never propose, plan, or write code changes. Job 1 ends at requirements and hands off to
  brainstorming.
