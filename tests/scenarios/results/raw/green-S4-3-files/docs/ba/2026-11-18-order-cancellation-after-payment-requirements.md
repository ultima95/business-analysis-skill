# Order cancellation after payment — Requirements

## Context

- Problem: as filed, "Customers can't cancel orders after payment." A customer who has paid has no way to stop the order; the ticket names no workaround and no other actor.
- Why now: no deadline, incident, or cost is stated in the ticket (see A-01).
- Source input: ticket title only, one line. No body, no acceptance criteria, no comments.
- Repository state: the repository contains no application code (`git ls-files` returns no files, single `init` commit), so no current rules could be recovered from code. Every rule below is proposed and rests on an assumption (A-nn) or an open question (Q-nn).

## Actors and stakeholders

| Actor | Does / decides / is informed | Notes |
|---|---|---|
| Customer (order owner) | Requests cancellation, is informed of the refund outcome | The only actor named in the ticket |
| Support agent | Cancels on a customer's behalf, answers refund questions | Assumed, A-06 |
| Finance | Handles refunds the payment provider refuses | Assumed, A-08, Q-06 |
| Fulfilment / warehouse operator | Must stop picking and handover once an order is cancelled | Assumed, A-07 |
| Payment provider | Accepts or refuses the refund instruction | External; assumed, A-05 |

## Scope

In scope:
- Customer-initiated cancellation of an order whose payment has been captured, up to the carrier handover.
- Refund of the captured amount back to the original payment method.
- Cancellation and refund status the customer can observe.
- Refusing cancellation after handover, and refusing duplicate cancellations.
- Stopping fulfilment once a cancellation is recorded.

Out of scope:
- Cancellation after the order has been handed to the carrier (returns and refunds are a separate process).
- Cancellation of unpaid, authorised-but-uncaptured, or failed-payment orders.
- Line-item or partial-quantity cancellation (Q-02).
- Exchanges, replacements, and goodwill credit.
- Chargeback and dispute handling.
- Customer communication templates and tone of copy.

## Business rules

- **BR-001**: An order may be cancelled only while it has not been handed to the carrier; from handover onward, cancellation is refused and the customer is directed to the returns process. Basis: A-04, Q-03, Q-09.
- **BR-002**: Cancelling an order whose payment was captured creates a refund of the captured amount to the original payment method. Basis: A-05, Q-08.
- **BR-003**: The refund equals the full captured amount, including shipping and tax; no partial refund is produced by a cancellation. Basis: A-05, Q-02.
- **BR-004**: At most one cancellation takes effect per order; a repeated request returns the outcome of the first and creates no second refund. Basis: A-09.
- **BR-005**: An order reaches the Cancelled state only after the payment provider accepts the refund; between the request and that acceptance the order is in CancellationPending. Basis: A-10.
- **BR-006**: Once a cancellation is recorded, fulfilment may not pick, pack, or ship the order; a pick list already issued for it is withdrawn. Basis: A-07.
- **BR-007**: Only the order owner, or a support agent acting for the owner, may cancel an order. Basis: A-06.
- **BR-008**: A refund the payment provider refuses leaves the order in CancellationPending and places the case in the finance work queue; the order is never moved to Cancelled on a refused refund. Basis: A-08, Q-06.
- **BR-009**: If the provider reports the payment as already refunded or charged back, no second refund is submitted and the case is flagged to finance. Basis: A-08.

## Functional requirements

- **FR-001**: As a customer, I want to cancel an order I have paid for while it has not shipped, so that I stop the delivery and get my money back without contacting support. Fulfils [BR-001], [BR-007]. Priority: Must.
- **FR-001.AC1**: Given an order in Paid state and not handed to the carrier, When the owner requests cancellation, Then the order moves to CancellationPending and a cancellation record is created with the requester and the request time.
- **FR-001.AC2**: Given an order already handed to the carrier, When the owner requests cancellation, Then the request is refused with a reason naming the handover and the returns process is offered.
- **FR-001.AC3**: Given an order owned by another customer, When a customer requests cancellation, Then the request is refused and no cancellation record is created.
- **FR-002**: The system shall create a refund of the full captured amount to the original payment method when a paid order is cancelled. Fulfils [BR-002], [BR-003]. Priority: Must.
- **FR-002.AC1**: Given an order with 250.00 captured including 20.00 shipping, When cancellation is recorded, Then a refund of 250.00 is submitted to the original payment method and its provider reference is stored on the order.
- **FR-002.AC2**: Given the provider refuses the refund, When the refusal is received, Then the order stays in CancellationPending and a case appears in the finance queue. Fulfils [BR-008].
- **FR-002.AC3**: Given an order with no captured payment, When cancellation is requested, Then no refund is submitted and the order is handled by the unpaid-order path.
- **FR-003**: As a customer, I want to see whether my order is cancelled and whether the refund has been confirmed, so that I know when to expect the money. Fulfils [BR-005]. Priority: Should.
- **FR-003.AC1**: Given a cancellation in progress, When the customer views the order, Then the order shows CancellationPending and that the refund is not yet confirmed.
- **FR-003.AC2**: Given the provider has accepted the refund, When the customer views the order, Then the order shows Cancelled with the refund amount and the refund reference.
- **FR-004**: The system shall reject a cancellation request on an order that already has one, returning the existing outcome without creating a second refund. Fulfils [BR-004]. Priority: Must.
- **FR-004.AC1**: Given an order in Cancelled state, When the owner requests cancellation again, Then the request is refused as already cancelled and no refund is submitted.
- **FR-004.AC2**: Given an order in CancellationPending, When the owner requests cancellation again, Then the request returns the pending outcome and no second refund is submitted.
- **FR-005**: The system shall notify fulfilment that a paid order was cancelled, and withdraw any pick list already issued for it, so that the order is not shipped. Fulfils [BR-006]. Priority: Must.
- **FR-005.AC1**: Given a pick list issued for an order, When cancellation is recorded, Then fulfilment receives a withdrawal for that order and the pick list shows as withdrawn.
- **FR-005.AC2**: Given fulfilment reports the order as handed to the carrier after the cancellation was recorded, Then the order is not set to Cancelled and a case is raised for the cancellation team.
- **FR-006**: As a customer, I want to see before requesting whether an order can still be cancelled, and why it cannot, so that I do not search for a control that is not there. Fulfils [BR-001]. Priority: Should.
- **FR-006.AC1**: Given an order not yet handed to the carrier, When the customer views the order, Then a cancellation control is offered.
- **FR-006.AC2**: Given an order handed to the carrier, When the customer views the order, Then cancellation is shown as unavailable with the handover as the reason.
- **FR-007**: The system shall not submit a refund when the provider reports the payment as already refunded or charged back, and shall flag the case to finance. Fulfils [BR-009]. Priority: Must.
- **FR-007.AC1**: Given the provider reports the payment as already refunded, When cancellation is recorded, Then no refund is submitted and a case is created in the finance queue naming the existing refund.
- **FR-007.AC2**: Given the provider reports the payment as charged back, When cancellation is recorded, Then no refund is submitted and the case is created in the finance queue as a dispute.
- **FR-008**: The system shall notify the customer when a cancellation completes or fails, naming the refund amount and the expected arrival window. Fulfils [BR-005], [BR-008]. Priority: Should.
- **FR-008.AC1**: Given a refund is accepted by the provider, When the order moves to Cancelled, Then the customer is notified with the amount and the refund reference.
- **FR-008.AC2**: Given a refund is refused by the provider, When the refusal is recorded, Then the customer is notified that the cancellation is delayed and no amount or date is promised.

## Non-functional requirements

| ID | Priority | Target |
|---|---|---|
| NFR-001 | Must | p95 cancellation request response ≤ 2 s at 50 concurrent requests (placeholder; see Q-10) |
| NFR-002 | Should | refund submitted to the payment provider within 60 s of the cancellation being recorded, for 99% of cancellations (placeholder; see Q-10) |
| NFR-003 | Should | cancellation path available 99.9% of minutes per calendar month |
| NFR-004 | Must | one audit record per cancellation attempt, retained 7 years, readable by the finance role and by the order owner for their own orders (placeholder; see Q-07) |
| NFR-005 | Must | 0 cancellations of orders owned by another customer in an authorization test suite covering owner, other customer, support agent, and anonymous requester |
| NFR-006 | Could | fewer than 1% of cancellation requests ending in an unhandled error over a calendar month |

- **NFR-001.AC1**: Given 50 concurrent cancellation requests, When the requests are processed, Then p95 response time is ≤ 2 s.
- **NFR-002.AC1**: Given 100 cancellations recorded, When the refunds are submitted, Then at least 99 of them reach the provider within 60 s.
- **NFR-003.AC1**: Given a calendar month, When availability is measured, Then the cancellation path is available for at least 99.9% of minutes.
- **NFR-004.AC1**: Given a cancellation attempt, When the audit record is read, Then it contains requester identity, order, outcome, reason, amount, and provider reference, and it is still readable after 7 years.
- **NFR-005.AC1**: Given an authorization test suite with an owner, another customer, a support agent, and an anonymous requester, When each attempts to cancel a foreign order, Then 0 succeed.
- **NFR-006.AC1**: Given one calendar month of cancellation traffic, When the error count is measured, Then fewer than 1% of requests end in an unhandled error.

## Edge cases

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| Customer (owner) | Paid, not handed to carrier | Cancellation accepted (FR-001.AC1) | Cancel control offered (FR-006.AC1) | No direct order edit; only cancellation | No hard delete; state set to CancellationPending |
| Customer (owner) | Picking or packed | Accepted only while not handed to the carrier (BR-001) | Cancel control offered with the cutoff named | Pick list withdrawn (FR-005.AC1) | Not allowed |
| Customer (owner) | Handed to carrier | Refused with handover reason (FR-001.AC2) | Shows unavailable with reason (FR-006.AC2) | Not allowed | Not allowed; returns process |
| Customer (owner) | CancellationPending | Refused as duplicate (FR-004.AC2) | Shows pending refund (FR-003.AC1) | Not allowed | Not allowed |
| Customer (owner) | Cancelled | Refused as already cancelled (FR-004.AC1) | Shows amount and reference (FR-003.AC2) | Not allowed | Not allowed |
| Customer (owner) | Refunded, or charged back at provider | No refund submitted, finance case raised (FR-007.AC1) | Shows existing refund | Not allowed | Not allowed |
| Customer (not owner) | Any state | Refused, no record (FR-001.AC3) | Sees nothing of the order | Not allowed | Not allowed |
| Support agent | Paid | Cancels for the owner (BR-007, A-06) | Reads order and refund state | No direct state edit | Not allowed |
| Finance | CancellationPending after refusal | Raises a manual refund case (BR-008) | Reads audit record (NFR-004) | Records manual resolution | Not allowed |
| Warehouse operator | CancellationPending | Not allowed | Sees withdrawal on the pick list (FR-005.AC1) | Not allowed | Not allowed |

## Glossary

| Term | Meaning |
|---|---|
| Order | A customer purchase with a set of items, a total, and a lifecycle state. |
| Captured | The state in which the payment provider has taken the money from the customer. |
| Handover (cutoff) | The moment the parcel passes to the carrier; after it, cancellation is refused (Q-03 fixes the exact event). |
| CancellationPending | The order state between a recorded cancellation and the provider accepting the refund. |
| Cancelled | The order state after the provider accepts the refund; the order is not shipped and no further work is done on it. |
| Refund | The return of the captured amount to the original payment method, referenced at the provider. |
| Provider refusal | The payment provider declining a refund instruction; the order stays in CancellationPending (BR-008). |
| Duplicate request | A cancellation request on an order that already has a recorded cancellation (BR-004). |
| Finance queue | The list of refund cases that need a human decision. |

## Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | The ticket is a feature request: cancellation after payment is not offered today, rather than a broken control. | Ticket states the outcome only; repo has no code to check. If false, FR-001 becomes a defect fix and FR-006 may be dropped. |
| A-02 | "After payment" means the money is captured, not merely authorised. | Wording is ambiguous. If false, the flow needs a void on an uncaptured payment instead of a refund; FR-002 and BR-002 change. |
| A-03 | Self-service cancellation by the customer is the goal, not a support-only process. | Ticket says "Customers can't cancel", naming the customer as actor. If false, FR-001 and FR-006 are dropped and a support-console FR becomes Must. |
| A-04 | The cancellation cutoff is the carrier handover. | Not stated; chosen because any later cutoff needs a recall process. If false, BR-001 and FR-001 change and a recall path enters scope. |
| A-05 | The refund goes to the original payment method for the full captured amount. | Not stated; assumes common refund practice. If false, BR-002, BR-003, and FR-002 gain a payout-method or partial-amount step. |
| A-06 | A support agent may cancel on the customer's behalf. | Not stated; keeps the existing support route open. If false, BR-007 loses the agent clause and the edge-case matrix drops one row. |
| A-07 | Fulfilment can receive a cancellation and withdraw a pick list. | Not stated; the repo contains no integration code. If false, FR-005 depends on a new integration and ships in a later release. |
| A-08 | Finance works a queue of refused or conflicting refunds. | Not stated; needed for BR-008 and BR-009 to have an owner. If false, refused refunds need another owner and FR-002.AC2 changes. |
| A-09 | Duplicate cancellation requests are possible in practice, so the flow must be idempotent. | Not stated; customers retry, and notification links are re-opened. If false, FR-004 drops to Could. |
| A-10 | Cancelled is reached only on provider acceptance of the refund. | Not stated; chosen so the customer is never told "cancelled" while the money is held. If false, BR-005, FR-003, and FR-008 change and the order can show Cancelled while the refund is unresolved. |

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | Does self-service cancellation replace the support-assisted route, or run alongside it? | Product owner | FR-001, FR-006 |
| Q-02 | Must cancellation support line-item (partial) cancellation, or is whole-order only enough for this release? | Product owner | FR-002, BR-003 |
| Q-03 | Which event marks the carrier handover: label printed, scan at depot, or first carrier scan? | Fulfilment lead | FR-001, BR-001, FR-005 |
| Q-04 | What refund arrival window may be promised to the customer? | Finance lead with Product owner | FR-003, FR-008 |
| Q-05 | Who bears the payment-provider refund fee on a cancellation? | Finance lead | FR-002 |
| Q-06 | How many automatic refund submissions are attempted before a refused refund goes to the finance queue? | Finance lead | FR-002, BR-008 |
| Q-07 | What retention period and read scope apply to cancellation audit records? | Compliance officer | NFR-004 |
| Q-08 | Do gift-card and store-credit payments follow the same refund path as card payments? | Finance lead | FR-002, BR-002 |
| Q-09 | Does any consumer-protection rule give a mandatory cooling-off cancellation window that overrides the handover cutoff? | Legal counsel | BR-001, FR-001 |
| Q-10 | What response time and refund-submission targets apply to the cancellation path? | Engineering lead | NFR-001, NFR-002 |

## Next step

Brainstorm the solution with this file as context, then write the plan.
