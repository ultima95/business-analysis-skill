# Order cancellation after payment — Requirements

## Context

- Problem: the ticket reports one thing only — "Customers can't cancel orders after payment."
- Why now: not stated in the ticket. No deadline, incident, volume, or cost figure was supplied.
- Source input: single-line ticket, one stakeholder, no attachments.
- Mode: draft. The requester is not available for follow-up, so every gap the ticket leaves is recorded as an assumption (A-nn) or an open question (Q-nn) in this file.

## Actors and stakeholders

| Actor | Does / decides / is informed | Notes | Basis |
|---|---|---|---|
| Customer | Requests cancellation of their own paid order | The only actor named in the ticket | Ticket: "Customers can't cancel orders" |
| Support agent | Cancels a paid order on a customer's behalf when the customer asks through support | Not in the ticket | A-05 |
| Finance user | Processes or monitors the refund created by a cancellation | Not in the ticket | A-07 |
| Product owner | Owns the cancellation cut-off, scope, and refund policy | Not in the ticket | Q-01, Q-02 |
| Finance lead | Owns refund timing and who bears the payment fee | Not in the ticket | Q-04, Q-05 |
| Compliance owner | Owns the audit retention period for cancellation and refund records | Not in the ticket | Q-08 |

## Scope

In scope:

- Cancellation of a paid order by the customer who placed it.
- Cancellation of a paid order by a support agent on a verified customer request.
- Refund record created by that cancellation, with its amount and destination visible to the customer and to finance.
- Refusal of cancellation when the order is past the fulfilment cut-off, already cancelled, or already refunded.

Out of scope:

- Cancellation of unpaid orders as a new capability. Unpaid orders already cancel through whatever path exists today (A-06).
- Returning goods after the order has been handed to the carrier. That keeps its existing returns path (A-03).
- Partial cancellation of some items in a multi-item order (Q-03, A-08).
- Dispute, chargeback, and fraud handling.
- Any change to how payment is captured in the first place.

## Business rules

- **BR-001**: A paid order may be cancelled only before the fulfilment cut-off; at or after the cut-off the cancellation is refused. Basis: A-01; exact cut-off is Q-01.
- **BR-002**: A cancelled paid order is refunded the full amount captured for that order, with no deduction other than a fee the finance lead confirms. Basis: A-02, Q-04.
- **BR-003**: When the order has already been handed to the carrier, cancellation is refused and the customer is shown the returns path instead. Basis: A-03.
- **BR-004**: A refund for a cancelled paid order is issued to the original payment method only. Basis: A-04.
- **BR-005**: Only the customer who placed the order, or a support agent acting on that customer's request, may cancel it. Basis: A-05.
- **BR-006**: A cancellation request on an order that is already cancelled or fully refunded changes no status and creates no second refund. Basis: A-07.
- **BR-007**: Each cancelled paid order produces exactly one refund entry, and later changes to that refund update the same entry rather than adding a new one. Basis: A-07.
- **BR-008**: A refund amount may never exceed the amount captured for the order. Basis: A-02.

## Functional requirements

- **FR-001**: As a customer, I want to cancel my paid order before its fulfilment cut-off, so that I am not charged for goods I no longer want. Fulfils [BR-001], [BR-005]. Priority: Must.
- **FR-001.AC1**: Given my order is paid and the fulfilment cut-off has not passed, When I confirm cancellation, Then the order status becomes Cancelled and a refund entry for the captured amount is created.
- **FR-001.AC2**: Given my order is paid and the fulfilment cut-off has passed, When I request cancellation, Then the request is refused and the refusal states the cut-off reason and the returns alternative.
- **FR-001.AC3**: Given my order is paid and already Cancelled, When I request cancellation again, Then the order stays Cancelled and no additional refund entry is created.
- **FR-001.AC4**: Given my order is placed but not paid, When I cancel it, Then the order becomes Cancelled and no refund entry is created.
- **FR-001.AC5**: Given I am a customer who did not place the order, When I request cancellation of it, Then the request is refused and the refusal is recorded against my account.
- **FR-002**: As a customer, I want to see the refund amount and the destination before I confirm cancellation, so that I know exactly what I get back and where. Fulfils [BR-002], [BR-004]. Priority: Must.
- **FR-002.AC1**: Given my order is paid and cancellable, When I reach the confirmation step, Then the amount shown equals the amount captured for that order and the destination is the payment method I paid with.
- **FR-002.AC2**: Given the order was paid with two payment methods, When I reach the confirmation step, Then one refund amount is shown per method and the amounts add up to the captured total.
- **FR-003**: As a customer, I want a written confirmation of the cancellation and refund, so that I have proof of the amount and the date the money is expected. Fulfils [BR-002]. Priority: Must.
- **FR-003.AC1**: Given my cancellation succeeded, When the refund entry is created, Then I receive a confirmation stating the refund amount, the masked destination, and an expected arrival date within 5 business days.
- **FR-003.AC2**: Given my cancellation was refused, When the refusal is returned, Then I receive no refund confirmation and the refusal states the reason.
- **FR-004**: As a support agent, I want to cancel a paid order on a customer's verified request, so that a customer who cannot self-serve is still helped. Fulfils [BR-001], [BR-005]. Priority: Should.
- **FR-004.AC1**: Given a customer's order is paid and inside the cut-off, When I cancel it on their request, Then the order becomes Cancelled and the record names me as the actor and the customer as the order owner.
- **FR-004.AC2**: Given the customer's order is past the cut-off, When I attempt the cancellation, Then it is refused and I am shown the returns path for that customer.
- **FR-004.AC3**: Given I attempt to cancel an order for a customer who has not asked, When I submit it, Then the cancellation is refused and the attempt is recorded.
- **FR-005**: The system shall refuse cancellation of a paid order at or after the fulfilment cut-off and present the returns path instead. Fulfils [BR-001], [BR-003]. Priority: Must.
- **FR-005.AC1**: Given a paid order whose carrier handover is recorded, When any actor requests cancellation, Then the refusal cites the handover and offers the returns path.
- **FR-005.AC2**: Given a paid order with no carrier handover recorded, When the cut-off check runs, Then the order is treated as cancellable.
- **FR-006**: The system shall treat a repeat cancellation request on an already cancelled or fully refunded order as a no-op. Fulfils [BR-006]. Priority: Must.
- **FR-006.AC1**: Given an order is Cancelled with one refund entry, When a second cancellation arrives, Then the status stays Cancelled and the refund entry count stays at 1.
- **FR-006.AC2**: Given an order is fully Refunded, When a cancellation arrives, Then it is refused as already completed and no refund entry is created.
- **FR-007**: As a finance user, I want every cancelled paid order to appear once in the refund queue with its amount, so that no refund is missed or paid twice. Fulfils [BR-007], [BR-002]. Priority: Must.
- **FR-007.AC1**: Given a paid order is cancelled, When the cancellation completes, Then exactly one refund entry appears in the queue with the order reference, the captured amount, the destination, and the actor.
- **FR-007.AC2**: Given a refund entry already exists for the order, When the cancellation is processed again, Then the queue still holds 1 entry for that order.
- **FR-008**: The system shall reject any refund whose amount exceeds the amount captured for the order. Fulfils [BR-008]. Priority: Must.
- **FR-008.AC1**: Given an order captured at 100.00, When a refund of 120.00 is submitted, Then the refund is rejected and the excess is reported to the finance user.
- **FR-008.AC2**: Given an order captured at 100.00, When a refund of 100.00 is submitted, Then it is accepted.

## Non-functional requirements

| ID | Priority | Target | Basis |
|---|---|---|---|
| NFR-001 | Must | p95 end-to-end cancellation completes in ≤ 3 s at 50 concurrent requests | A-10 |
| NFR-002 | Must | Cancellation path available 99.5% per calendar month | A-12 |
| NFR-003 | Must | Cancellation and refund events retained 7 years and readable by finance and audit roles | A-13 |
| NFR-004 | Must | 100% of cancellation attempts by a non-owner, non-agent actor are refused and recorded | A-05 |
| NFR-005 | Must | Support agents see payment instrument masked to the last 4 digits in 100% of cancellation records | A-11 |

- **NFR-001.AC1**: Given 50 concurrent cancellation requests, When each is submitted, Then p95 completion time is ≤ 3 s.
- **NFR-002.AC1**: Given one calendar month, When availability of the cancellation path is measured, Then it is at least 99.5%.
- **NFR-003.AC1**: Given a cancellation recorded 7 years ago, When a finance or audit user queries it, Then the actor, timestamp, prior status, and refund amount are returned.
- **NFR-004.AC1**: Given a signed-in customer who does not own the order, When they submit a cancellation, Then the request is refused and the refusal appears in the audit record.
- **NFR-005.AC1**: Given a support agent opens a cancellation record, When the payment instrument is shown, Then only the last 4 digits are visible.

## Edge cases

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| Customer (owner) | Paid, inside cut-off | Cancellation accepted, one refund entry created | Refund amount and destination shown | Order becomes Cancelled | Not allowed |
| Customer (owner) | Paid, past cut-off | Refused, returns path offered | Refusal reason shown | Status unchanged | Not allowed |
| Customer (owner) | Cancelled, refund pending | No second refund entry | Refund status visible | Second request is a no-op | Not allowed |
| Customer (owner) | Fully refunded | Refused as completed | Refund record visible | Status unchanged | Not allowed |
| Customer (not owner) | Any state | Refused and recorded | No cancellation control offered | Refused | Not allowed |
| Support agent | Paid, inside cut-off | Accepted with agent as actor | Amount and masked destination visible | Order becomes Cancelled | Not allowed |
| Support agent | Paid, past cut-off | Refused, returns path offered | Refusal reason visible | Status unchanged | Not allowed |
| Finance user | Cancelled, refund failed | No new entry; failure recorded on the existing entry | Failure reason and amount visible | Refund retried on the same entry | Not allowed |
| Finance user | Any state | Not allowed | Queue view across all cancelled orders | Not allowed | Not allowed |

## Glossary

| Term | Meaning |
|---|---|
| Paid order | An order whose payment has been captured, in whole or in part. |
| Fulfilment cut-off | The point after which an order can no longer be cancelled; its exact definition is open in Q-01. |
| Cancellation | A status change on the order that stops fulfilment and triggers a refund. |
| Refund | The return of a captured amount to the payment method it came from. |
| Refund entry | The single record that tracks one order's refund and its status changes. |
| Captured amount | The total the customer actually paid for the order. |
| Original payment method | The instrument the customer paid with. |
| Support agent | A staff role that acts on a verified customer request. |
| Finance user | A staff role that monitors and processes refunds. |
| No-op | A request that is accepted as received but changes no status and creates no record. |

## Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | The fulfilment cut-off is the moment the carrier records handover of the parcel. | Ticket says only "after payment"; if the cut-off is earlier, FR-001.AC2, FR-004.AC2, and FR-005 change |
| A-02 | The refund is the full captured amount, with no restocking or handling deduction. | Not stated; if a fee applies, FR-002 and FR-008 gain a fee line and BR-002 is amended |
| A-03 | Orders already handed to the carrier leave the cancellation path and follow the existing returns path. | Not stated; if they must be cancellable, FR-005 becomes a recall flow and BR-003 is dropped |
| A-04 | The refund returns to the original payment method only. | Not stated; if the customer may choose a credit or a different method, FR-002 gains a destination choice |
| A-05 | Cancellation authority is the order owner or a support agent acting on a verified request. | Ticket names only customers; if a manager approval tier is required, FR-004 gains a step |
| A-06 | Unpaid orders cancel without a refund entry, as they do today. | Not stated; if the unpaid path differs, FR-001.AC4 changes |
| A-07 | One refund entry per cancelled paid order; status changes update that entry. | Not stated; if one entry per item is required, FR-007 changes and partial cancellation comes into scope |
| A-08 | Only whole-order cancellation is in scope for this release. | Not stated; partial cancellation would add a per-item refund rule and a per-item cut-off rule |
| A-09 | Payment methods in scope are those that can refund to the original method; the rest stay out of scope. | Not stated; the surviving list is a business decision recorded in Q-02 |
| A-10 | Cancellation completes in ≤ 3 s at p95 with 50 concurrent requests. | Working value set so NFR-001 is testable; Q-05 owns the customer-facing timing |
| A-11 | Support agents see the payment instrument masked to the last 4 digits. | Working value for NFR-005; if agents need the full instrument, the privacy target changes |
| A-12 | The cancellation path is available 99.5% per calendar month. | Working value for NFR-002; a higher figure needs a scheduled-maintenance rule |
| A-13 | Cancellation and refund records are retained 7 years. | Working value for NFR-003; a different regulatory period is Q-08 |
| A-14 | The refund reaches the customer within 5 business days of cancellation. | Working value for FR-003.AC1; the real commitment is Q-05 |

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | Where exactly is the fulfilment cut-off: carrier handover, start of picking, or a fixed number of hours after payment? | Product owner | FR-001, FR-004, FR-005 |
| Q-02 | Which order channels and payment methods must support cancellation in this release? | Product owner | all FRs for cancellation |
| Q-03 | Is partial cancellation of a multi-item paid order required in this release? | Product owner | FR-002, FR-007 |
| Q-04 | Who bears the payment provider's fee on a refund: the business or the customer? | Finance lead | FR-002, FR-008 |
| Q-05 | How many business days after cancellation must the refund reach the customer? | Finance lead | FR-003, NFR-001 |
| Q-06 | Must the customer give a cancellation reason, and is it required for every order value? | Product owner | FR-001, FR-004 |
| Q-07 | Do guest-checkout orders with no account need a cancellation path in this release? | Product owner | FR-001 |
| Q-08 | What audit retention period applies to cancellation and refund records? | Compliance owner | NFR-003 |

## Next step

Brainstorm the solution with this file as context, then write the plan. Handoff file: `docs/ba/2026-11-18-order-cancellation-after-payment-requirements.md`.
