# Elicitation — gap-finder, modes, A-nn / Q-nn

Loaded for every job. The gap-finder turns the input into a gap list; the mode decides
whether a gap becomes a question or an A-nn/Q-nn row.

## Modes

| Mode | Predicate | Behavior |
|---|---|---|
| Interview | user is present and has not opted out of questions | ask one question per message, highest-impact gap first; play back understanding as it forms |
| Draft | user said "just draft" / "don't ask", the session is autonomous, or someone else's material is analyzed offline | write the document; every unknown becomes an A-nn or Q-nn |
| Hybrid | user is present AND the input is someone else's material (transcript, email thread, ticket) | interview only on gaps the user can answer (their goals, priorities, scope); record gaps only the material's authors can answer as Q-nn with that author as owner |

Pasted transcripts default to hybrid.

**One interview message contains, in order:**

1. Your current understanding, in 2–5 lines (or the draft gap table).
2. The single gap whose answer changes the most requirements.
3. Exactly one question, as the last line.

Then stop and wait. Next question only after the answer or an opt-out.

## Gap-finder — nine gaps

Check the input against all nine. A gap is anything the document needs but the input does
not supply. Ask only about gaps; never re-ask what was answered.

| # | Gap | What to extract | Questions |
|---|---|---|---|
| 1 | Actors | who triggers, decides, does the work, is informed; external roles too | Which roles touch this? Who can approve or refuse? Who only needs to know? |
| 2 | Trigger | the event that starts it, and what "done" means | What event starts it? What counts as finished? What if the trigger never arrives? |
| 3 | Happy path | the normal sequence and its handoffs | Walk me through the normal case, step by step. Who does each step? What passes to the next step? |
| 4 | Exception paths | what can fail, be skipped, or arrive late — and the required behavior | Which steps can fail or be skipped? What happens today when they do? Which failures go unnoticed? |
| 5 | Business rules | limits, thresholds, eligibility, prioritization | What limits or thresholds apply? Where are those rules written down? Which rules have exceptions? |
| 6 | Data | what is captured, by whom, where it lives, who may read it | What does a record contain at each step? Where is it stored? Which fields are mandatory? |
| 7 | Non-functional needs | measurable speed, volume, availability, privacy | What response time or volume matters, and what number? What must a given role never see? What happens at peak? |
| 8 | Constraints | regulation, policy, contracts, existing systems, fixed dates or budgets | What regulation or policy limits the options? Which existing system must this fit? What date or budget is fixed? |
| 9 | Success metric | the number the business will judge it by, and its owner | What number shows this works? Who owns that number? How is it measured today? |

## Ranking interview order

Score each open gap by **how many requirements its answer changes**; ask the highest score
first. Tie → the gap that blocks the most other gaps. After each answer, re-score: newly
answerable gaps may now outrank the rest.

One gap per message. Do not bundle gaps because they feel related.

## Stop rule

Stop asking when any of these is true:

- every gap is answered,
- every remaining gap is recorded as an A-nn or Q-nn row,
- the user opts out ("just draft", "don't ask", "not available", session is autonomous).

Then write the document. Draft mode writes a complete document, never a request for
information.

## A-nn / Q-nn formats

Both are tables with fixed columns. A prose list ("assumptions to validate") is not a
register and does not satisfy these slots.

**Assumption — something you filled to proceed:**

```
| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | Refunds go back to the original payment method. | Not stated; matches common practice; if false the refund flow gains a payout-method step. |
```

| Slot | Required content |
|---|---|
| `ID` | `A-01`, `A-02`… — two digits, in order of appearance, never reused |
| `Assumption` | one testable statement the document relies on |
| `Basis in input, or impact if false` | the input line/decision it came from, or what changes if it is wrong |

**Open question — only someone else can answer:**

```
| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | Do points expire six months after last activity, or never? | Hà (Finance) — pending auditor input | FR-004, FR-005 |
```

| Slot | Required content |
|---|---|
| `ID` | `Q-01`, `Q-02`… — two digits, in order of appearance, never reused |
| `Question` | one answerable question, no document-shaping meta-questions |
| `Owner` | a role or named person who can answer it |
| `Blocks` | at least one requirement ID (`FR-004`), or `all FRs for <area>` when the doc has none yet |

Every unknown goes in exactly one table. If it would change a requirement if false, it is a
Q-nn; if the document can proceed as written, it is an A-nn. Never present either as a
confirmed fact in prose.

## Input types

| Input | Rules |
|---|---|
| Meeting transcript | Separate **decisions** (stated, agreed, no objection) from **opinions/proposals**. Record every contradiction verbatim and resolve it as a Q-nn owned by the people who disagree — never pick a side. |
| Email thread | The latest decision wins; flag each reversal ("earlier X, now Y"). Gaps the thread leaves open become Q-nn, owner = the person who raised or owns the topic. |
| Ticket / thin ask | One stakeholder's claim, not the business's truth. Anything not stated is an A-nn or Q-nn. |
| Existing document | As-is evidence, not proof of current practice. Cite it (`file:line` or section) and question anything that looks stale. |
| Code (job 1 in a repo) | Recover current rules with `file:line` via `references/code-recovery.md`; a requirement that contradicts the code is flagged, not silently changed. |

In hybrid mode, split the gap list first: gaps the user can answer become interview
questions; gaps only the material's authors can answer become Q-nn rows with that author as
owner.
