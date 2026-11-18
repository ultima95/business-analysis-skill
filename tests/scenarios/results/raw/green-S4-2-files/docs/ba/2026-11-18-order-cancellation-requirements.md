# Order Cancellation After Payment — Requirements

## Context

- Problem: customers who have already paid cannot cancel their order ("Customers can't cancel orders after payment").
- Why now: not stated in the ticket; no deadline or cost event was supplied.
- Source input: single ticket line, one stakeholder's claim. Nothing else was supplied, and the requester was unavailable for follow-up, so this document is drafted and every unknown below is an assumption (`A-nn`) or an open question (`Q-nn`).
- Repository state: this repository contains no application code (only `.git`), so no current business rules could be recovered from source. See `Q-06`.

## Actors and stakeholders

| Actor | Does / decides / is informed | Notes |
|---|---|---|
| Customer | Triggers cancellation, is informed of the outcome and refund | The only actor named in the ticket |
| Support agent | Cancels on the customer's behalf, handles refused or failed cases | Inferred, not in the ticket (`A-01`) |
| Fulfilment / warehouse | Receives the order and may already have started picking | Inferred, not in the ticket (`A-01`) |
| Payments / finance | Executes the refund and settles it with the payment provider | Inferred, not in the ticket (`A-01`) |
| Cancellation service (system) | Enforces the cut-off, calls payments, records the attempt | Derived from `A-01`; no implementation is described here |

## Scope

In scope:
- Cancelling a whole order that has been paid and not yet shipped.
- Refunding the captured payment as part of that cancellation.
- The refusal path when the cut-off has already passed.
- What the customer and support see after a cancellation.

Out of scope:
- Returns or refunds for shipped and delivered orders (`Q-07`).
- Cancelling individual line items of an order (`Q-02`).
- Charging a cancellation fee; no fee was mentioned in the input.
- Any choice of technology, architecture, schema, or screen.

## Business rules

- **BR-001**: A customer may cancel an order only while the order is in the paid state and fulfilment has not started; once fulfilment starts, cancellation is refused. Basis `A-02`, `Q-01`.
- **BR-002**: An accepted cancellation refunds the full captured amount of the order, including tax and shipping, to the original payment method. Basis `A-03`, `A-04`.
- **BR-003**: A cancelled order is never handed to fulfilment, and a fulfilment request already issued for it is withdrawn. Basis `A-01`.
- **BR-004**: Only the account that placed the order, or a support agent acting on that order, may cancel it; any other account is refused. Basis `A-01`.
- **BR-005**: A repeated cancellation request on an already-cancelled order creates no second refund and leaves the refund amount unchanged.
- **BR-006**: A cancellation requested after fulfilment has started is refused with a stated reason, and the order keeps its current state.
- **BR-007**: Every cancellation attempt is recorded with order, requester, timestamp, decision, and reason. Basis `A-09`.

## Functional requirements

- **FR-001**: As a customer, I want to cancel my paid order before it is fulfilled, so that I am not charged for goods I no longer want. Fulfils [BR-001], [BR-004]. Priority: Must.
- **FR-001.AC1**: Given an order in the paid state with fulfilment not started, When the customer confirms cancellation, Then the order reads Cancelled and a refund for the full captured amount is created.
- **FR-001.AC2**: Given an order whose fulfilment has started, When the customer confirms cancellation, Then the cancellation is refused with a reason naming the fulfilment start and the order state is unchanged.
- **FR-001.AC3**: Given an order already Cancelled with a refund in progress, When the customer confirms cancellation again, Then the order stays Cancelled and no second refund is created, as required by [BR-005].
- **FR-001.AC4**: Given an order placed by another account, When a customer requests cancellation, Then the request is refused and neither the order nor the refund changes.
- **FR-002**: The system shall refund the full captured amount to the original payment method when a cancellation is accepted. Fulfils [BR-002]. Priority: Must.
- **FR-002.AC1**: Given a paid order cancelled by its owner, When the refund is submitted to the payment provider, Then the refund amount equals the captured amount of that order and the refund reads Issued.
- **FR-002.AC2**: Given the payment provider rejects the refund, When the rejection is received, Then the refund reads Failed with the provider reason and the order remains Cancelled.
- **FR-003**: The system shall withdraw a cancelled order from fulfilment before any pick is confirmed. Fulfils [BR-003]. Priority: Must.
- **FR-003.AC1**: Given an order released to fulfilment and no pick confirmed, When the cancellation is accepted, Then the fulfilment request is withdrawn and the order reads Cancelled.
- **FR-003.AC2**: Given a pick was already confirmed for the order, When cancellation is requested, Then it is refused under [BR-006] and the fulfilment request stays active.
- **FR-004**: As a customer, I want to see the cancellation and refund status of my order, so that I know when my money comes back. Fulfils [BR-002]. Priority: Should.
- **FR-004.AC1**: Given a cancelled order with an issued refund, When the customer opens the order, Then the order reads Cancelled and the refund reads Issued with its amount.
- **FR-004.AC2**: Given a cancelled order whose refund failed, When the customer opens the order, Then the refund reads Failed and the customer is told support is handling it.
- **FR-005**: As a support agent, I want to cancel a paid order on a customer's behalf, so that a customer who cannot use the self-service path is still helped. Fulfils [BR-001], [BR-004]. Priority: Should.
- **FR-005.AC1**: Given a paid order whose fulfilment has not started, When a support agent cancels it with a reason, Then the order reads Cancelled, the refund is created, and the agent identity is recorded.
- **FR-005.AC2**: Given an order whose fulfilment has started, When a support agent requests cancellation, Then the request is refused with the same reason the customer would receive.
- **FR-006**: As a customer, I want a notification when my order is cancelled and when the refund is issued, so that I do not have to check the order page. Fulfils [BR-002], `A-06`. Priority: Should.
- **FR-006.AC1**: Given a cancellation accepted for an order, When the refund is issued, Then the account owner receives one notification naming the order and the refund amount.
- **FR-006.AC2**: Given a cancellation refused after fulfilment started, When the refusal is recorded, Then the account owner receives one notification stating the reason and the next step.
- **FR-007**: The system shall record every cancellation attempt with order, requester, timestamp, decision, and reason. Fulfils [BR-007]. Priority: Must.
- **FR-007.AC1**: Given a cancellation attempt, accepted or refused, When it completes, Then one audit record exists holding order, requester, timestamp, decision, and reason, and it is readable by support and finance for the retention period in [NFR-004].

## Non-functional requirements

| ID | Priority | Target |
|---|---|---|
| NFR-001 | Must | p95 cancellation response ≤ 2 s at 50 concurrent cancellation requests |
| NFR-002 | Must | refund submitted to the payment provider within 60 s of an accepted cancellation |
| NFR-003 | Must | 100% of cancellation requests authenticated, with 0 successful cross-account cancellations in the regression suite |
| NFR-004 | Must | audit records retained 24 months and readable by support lead and finance lead |
| NFR-005 | Should | cancellation endpoint available 99.9% per calendar month |

- **NFR-001.AC1**: Given 50 concurrent cancellation requests, When the load is sustained for 10 minutes, Then p95 response time is ≤ 2 s.
- **NFR-002.AC1**: Given an accepted cancellation, When 60 s have elapsed, Then the refund has been submitted to the payment provider in at least 99 of 100 sampled cancellations.
- **NFR-003.AC1**: Given an authenticated account that does not own an order, When it requests cancellation, Then the request is refused in 100% of 200 scripted attempts.
- **NFR-004.AC1**: Given audit records 24 months old, When a support lead queries them, Then the records are returned and readable.
- **NFR-005.AC1**: Given one calendar month, When the month closes, Then the cancellation endpoint has served 99.9% of requests without an unavailability error.

## Edge cases

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| Customer (owner) | Paid, fulfilment not started | Cancel accepted, refund created | Sees Cancelled and refund status | No edit of a cancelled order | Cancellation is the close action; no hard delete |
| Customer (owner) | Fulfilment started | Cancel refused with reason | Sees order state and refusal reason | No change | Not allowed |
| Customer (owner) | Shipped | Cancel refused; return path out of scope (`Q-07`) | Sees shipped state | Not allowed | Not allowed |
| Customer (owner) | Cancelled, refund failed | Repeat cancel creates no new refund | Sees Failed refund | Not allowed | Not allowed |
| Customer (non-owner) | Any state | Refused, no state change | Sees nothing beyond their own orders | Refused | Refused |
| Support agent | Paid, fulfilment not started | Cancel on behalf accepted, identity recorded | Sees order and audit trail | Not allowed beyond the cancel action | Not allowed |
| Unauthenticated | Any state | Refused | Refused | Refused | Refused |

## Rules recovered from code

None. This repository holds no application code, so no rule could be cited to a `file:line`; the current behaviour is unverified and is tracked as `Q-06`.

## Glossary

| Term | Meaning |
|---|---|
| Order | One purchase placed by one account, with its own payment and its own fulfilment request. |
| Paid | The payment provider has captured money for the order. |
| Captured amount | The money actually taken for the order, including tax and shipping. |
| Fulfilment start | The moment the warehouse confirms it has begun picking the order. |
| Cancellation | Closing an unfulfilled paid order and refunding the captured amount. |
| Refund | The return of the captured amount to the original payment method. |
| Refund states | Issued (submitted to the provider), Failed (provider rejected), Settled (provider confirms the money is back). |
| Cut-off | The last moment a cancellation is accepted, defined in [BR-001]. |

## Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | Beyond the customer, support agents, fulfilment/warehouse, and payments/finance each take part in a cancellation. | Not stated. If false, the actor table shrinks and FR-005 is dropped. |
| A-02 | The cut-off is fulfilment start; cancellations before it are accepted, after it refused. | Not stated. If the cut-off is a time window instead, BR-001, FR-001.AC1, and Q-01 change together. |
| A-03 | Refunds go back to the original payment method. | Not stated; matches common practice. If false, FR-002 gains a payout-method choice. |
| A-04 | A full refund covers item price, tax, and shipping. | Not stated. If shipping is retained, BR-002 and FR-002.AC1 change. |
| A-05 | An order has one payment and one currency, so a refund has one amount. | Not stated. If split payments exist, FR-002 needs one refund per payment. |
| A-06 | The account owner is notified by email. | Not stated. If another channel is used, only FR-006 changes. |
| A-07 | Order states are Paid, fulfilment started, Shipped, Delivered, Cancelled. | Not stated. If more states exist, the edge-case matrix gains rows. |
| A-08 | The repository under analysis has no application code. | Verified: only `.git` is present. No recovered rules; current behaviour unverified (`Q-06`). |
| A-09 | Audit records are kept 24 months. | Not stated; may be set by regulation (`Q-05`). If longer, NFR-004 and its AC change. |

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | Is the cut-off fulfilment start, a fixed time window after payment, or a mix, and does the customer see it before ordering? | Product owner (ticket author) | FR-001, FR-003 |
| Q-02 | Is cancelling individual line items in scope for this release? | Product owner (ticket author) | FR-001, FR-002 |
| Q-03 | May support agents cancel an order after fulfilment has started, or only before? | Support lead | FR-005 |
| Q-04 | When a provider refund fails, how many retries happen and who owns the follow-up? | Payments/finance lead | FR-002, FR-004 |
| Q-05 | Which retention period does regulation or policy require for cancellation and refund records? | Legal/compliance | NFR-004 |
| Q-06 | Where is order and cancellation logic implemented today, and does it already block cancellation after payment as the ticket says? | Engineering lead | all FRs for order state |
| Q-07 | Should a shipped or delivered order offer a return instead of a cancellation, and is that part of this release? | Product owner (ticket author) | FR-001, FR-003 |

## Next step

Brainstorm the solution with this file as context, then turn the agreed FRs into a plan. `Q-01`, `Q-06`, and `Q-07` should be answered first because they move the cut-off, the current behaviour, and the release boundary.
