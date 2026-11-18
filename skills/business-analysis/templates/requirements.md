<!-- Delete any section below that does not apply. Do not fill a section with "N/A". -->

# <Topic> — Requirements

## Context

- Problem: <the problem in the requester's words>.
- Why now: <event, deadline, or cost that makes this urgent>.
- Source input: <ticket, transcript, email, or file path>.

## Actors and stakeholders

| Actor | Does / decides / is informed | Notes |
|---|---|---|
| <role> | <trigger, do, decide, or informed> | <constraint or fact from the input> |

## Scope

In scope:
- <capability or outcome included in this analysis>.

Out of scope:
- <capability or outcome explicitly excluded>.

## Business rules

- **BR-001**: <rule stated as a testable condition with its threshold or scope>.

## Functional requirements

- **FR-001**: As a <role>, I want <capability>, so that <outcome>. Fulfils [BR-001]. Priority: Must.
- **FR-001.AC1**: Given <context>, When <action>, Then <observable outcome>.
- **FR-001.AC2**: Given <exception context>, When <action>, Then <observable outcome>.
- **FR-002**: The system shall <behavior> for <actor>. Fulfils [BR-002]. Priority: Must.
- **FR-002.AC1**: Given <context>, When <action>, Then <observable outcome>.
- **FR-002.AC2**: Given <exception context>, When <action>, Then <observable outcome>.

## Non-functional requirements

| ID | Priority | Target |
|---|---|---|
| NFR-001 | Must | p95 response time ≤ 2 s at 100 concurrent users |

- **NFR-001.AC1**: Given 100 concurrent users, When <action>, Then p95 response time is ≤ 2 s.

## Edge cases

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| <role> | <state> | <expected result> | <expected result> | <expected result> | <expected result> |

## Rules recovered from code

- **BR-002**: <rule the code enforces today, in business words>. Source: `src/<module>.py:<line>`.

## Glossary

| Term | Meaning |
|---|---|
| <domain term> | <one sentence a new team member understands> |

## Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | <one testable statement the document relies on> | <input line or decision it came from, or what changes if false> |

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | <one answerable question> | <role or person who can answer> | <FR-nnn it blocks> |

## Next step

Brainstorm the solution with this file as context.
