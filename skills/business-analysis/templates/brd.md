<!-- Delete any section below that does not apply. Do not fill a section with "N/A". -->

# <Title> — Business Requirements Document

## Document control

| Field | Value |
|---|---|
| Version | <version> |
| Date | <YYYY-MM-DD> |
| Author | <author> |
| Status | <Draft / In review / Approved> |

## Executive summary

<Five to eight lines: the problem, the decision requested, and what this document covers.>

## Business objectives and success metrics

| Objective | Metric | Target | Owner |
|---|---|---|---|
| <objective> | <metric> | <number and unit> | <owner> |

## Background / as-is

<How the business handles this today: actors, steps, systems, volumes. Cite each source.>

## Scope

In scope:
- <capability or outcome included in this release>.

Out of scope:
- <capability or outcome explicitly excluded>.

## Stakeholders

| Stakeholder | Role | Interest | Influence |
|---|---|---|---|
| <name or role> | <decision or contribution> | <what they need from this document> | <high, medium, or low> |

## Business rules

- **BR-001**: <rule stated as a testable condition with its threshold or scope>.
- **BR-002**: <rule the code enforces today, in business words>. Source: `src/<module>.py:<line>`.

## Functional requirements

- **FR-001**: As a <role>, I want <capability>, so that <outcome>. Fulfils [BR-001]. Priority: Must.
- **FR-001.AC1**: Given <context>, When <action>, Then <observable outcome>.
- **FR-001.AC2**: Given <exception context>, When <action>, Then <observable outcome>.
- **FR-002**: The system shall <behavior> for <actor>. Fulfils [BR-002]. Priority: Must.
- **FR-002.AC1**: Given <context>, When <action>, Then <observable outcome>.
- **FR-002.AC2**: Given <exception context>, When <action>, Then <observable outcome>.

## Non-functional requirements

| ID | Priority | Target | Basis |
|---|---|---|
| NFR-001 | Must | p95 response time ≤ 2 s at 50 concurrent users | A-01 |
| NFR-002 | Must | 99.5 percent monthly availability | A-01 |

- **NFR-001.AC1**: Given 50 concurrent users, When <action>, Then p95 response time is ≤ 2 s.
- **NFR-002.AC1**: Given one calendar month, When the month completes, Then availability is at least 99.5 percent.

## Edge cases

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| <role> | <state> | <expected result> | <expected result> | <expected result> | <expected result> |

## Assumptions, constraints, dependencies

### Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | <one testable statement the document relies on> | <input line or decision it came from, or what changes if false> |

### Constraints

- <regulation, policy, contract, fixed date, or fixed budget that limits the options>.

### Dependencies

- <system, team, or decision this work waits on>.

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | <one answerable question> | <role or person who can answer> | <FR-nnn it blocks> |

## Glossary

| Term | Meaning |
|---|---|
| <domain term> | <one sentence a new team member understands> |

## Sign-off

| Name | Role | Decision | Date |
|---|---|---|---|
| <name> | <role> | <Approved / Rejected / Changes requested> | <YYYY-MM-DD> |
