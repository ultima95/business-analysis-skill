# Order Cancellation After Payment — Requirements

## Context

- Problem: customers who have already paid cannot cancel their order. The ticket reports the block exists; it does not say which payment methods, order states, or channels are affected.
- Why now: not stated in the ticket. The driver and any target date are recorded as Q-01.
- Source input: ticket "Customers can't cancel orders after payment." Single stakeholder claim; no volume, no customer quotes, no current-process description supplied.

## Actors and stakeholders

| Actor | Does / decides / is informed | Notes |
|---|---|---|
| Customer | triggers the cancellation; decides to cancel | authenticated buyer of the order; sees refund status |
| Customer support agent | cancels on the customer's behalf; decides within policy | needs the `cancel-order` permission |
| Finance / refunds operator | resolves refunds that fail; informed of each cancellation | owns the manual recovery path |
| Fulfilment / warehouse | ships the order; sets the `Shipped` status | the `Shipped` status is the point after which cancellation is refused |
| Payment provider | executes the refund; external | refund can be rejected or delayed; settlement timing is outside our control |

## Scope

In scope:
- customer-initiated cancellation of a paid order that has not shipped.
- support-initiated cancellation of the same order set.
- refund of the captured amount to the payment method used for the order.
- cancellation audit record and customer notification.

Out of scope:
- cancellation of unpaid orders, which is a separate existing behaviour not analysed here.
- returns and refunds after the order has shipped or been delivered.
- exchanges, cancellations of subscriptions or recurring plans.
- cancellation by automated fraud or risk rules.
- partial refunds where the refunded amount is less than the captured amount.

## Business rules

- **BR-001**: An order is cancellable while its status is `Paid` or `Processing`; a cancellation request is refused once the status is `Shipped`, `Delivered`, or `Completed`.
- **BR-002**: A successful cancellation of a paid order refunds the full captured amount, in the original currency, to the payment method used for the order. No partial refund is issued in this release.
- **BR-003**: Only the Customer who placed the order, or a Support agent holding the `cancel-order` permission, may cancel it. Every other actor is refused.
- **BR-004**: A cancelled order accepts no second cancellation. A repeated request returns the existing cancellation record and submits no additional refund.
- **BR-005**: Each cancellation stores order ID, actor ID, actor role, request timestamp, refund amount, currency, payment provider refund reference, refund status, and, when the actor is a Support agent, the reason code.
- **BR-006**: When the payment provider rejects the refund, the order status remains `Cancelled`, the refund status becomes `Failed` with the provider reason, and the order is retrievable by Support for manual resolution.
- **BR-007**: The Customer is notified when the cancellation is accepted and again when the refund reaches a final status of `Succeeded` or `Failed`.

## Functional requirements

- **FR-001**: As a Customer, I want to cancel a paid order before it ships, so that I am not charged for an order I no longer want. Fulfils [BR-001], [BR-003]. Priority: Must.
- **FR-001.AC1**: Given an order with status `Paid` that has not shipped, When the Customer cancels it, Then the order status becomes `Cancelled` and the confirmation shows the refund amount and currency.
- **FR-001.AC2**: Given an order with status `Processing` that has not shipped, When the Customer cancels it, Then the order status becomes `Cancelled` and the refund is submitted per BR-002.
- **FR-001.AC3**: Given an order with status `Shipped`, When the Customer cancels it, Then the request is refused, the order status is unchanged, and the response states that the order has shipped and offers the returns path.
- **FR-001.AC4**: Given an order that belongs to another Customer, When a Customer requests cancellation of it, Then the request is refused with no change to the order.
- **FR-001.AC5**: Given an order already in status `Cancelled`, When the Customer cancels it again, Then the existing cancellation record is returned and no second refund is submitted.
- **FR-002**: As a Customer, I want the refund to go back to the payment method I paid with, so that I receive the money without contacting support. Fulfils [BR-002]. Priority: Must.
- **FR-002.AC1**: Given a cancelled order that was paid by payment card, When the cancellation is accepted, Then a refund of the full captured amount in the original currency is submitted to that card and its provider refund reference is stored on the order.
- **FR-002.AC2**: Given the payment provider rejects the refund, When the rejection is received, Then the order stays `Cancelled`, the refund status becomes `Failed` with the provider reason, and the order appears in the Support failed-refund view.
- **FR-002.AC3**: Given a cancelled order, When the refund succeeds, Then the stored refund amount equals the captured amount for that order.
- **FR-003**: As a Customer, I want to see whether my refund is pending, succeeded, or failed, so that I know whether to expect money and when. Fulfils [BR-005]. Priority: Should.
- **FR-003.AC1**: Given a cancelled order with refund status `Pending`, When the Customer opens the order, Then the order shows status `Cancelled`, refund status `Pending`, the refund amount, and the arrival window given by the payment provider.
- **FR-003.AC2**: Given a refund that the provider reports as `Failed`, When the Customer opens the order, Then the order shows refund status `Failed` and a contact path for Support.
- **FR-004**: The system shall accept exactly one cancellation per order when the Customer and a Support agent submit cancellation at the same time. Fulfils [BR-004]. Priority: Must.
- **FR-004.AC1**: Given one `Paid` order, When the Customer and a Support agent submit cancellation within the same second, Then exactly one cancellation record exists and exactly one refund is submitted.
- **FR-004.AC2**: Given two cancellation requests for one order arriving concurrently, When both complete, Then the second request returns the identifier of the cancellation created by the first.
- **FR-005**: As a Support agent, I want to cancel an order on a Customer's behalf and record why, so that the customer request is resolved without the customer repeating it. Fulfils [BR-003], [BR-005]. Priority: Must.
- **FR-005.AC1**: Given a `Paid` order and an agent holding the `cancel-order` permission, When the agent cancels it with a reason code, Then the order becomes `Cancelled`, the reason code is stored on the cancellation record, and the Customer is notified per BR-007.
- **FR-005.AC2**: Given an agent who does not hold the `cancel-order` permission, When the agent requests cancellation, Then the request is refused and the order is unchanged.
- **FR-005.AC3**: Given a `Shipped` order, When the agent requests cancellation, Then the request is refused with the same reason shown to the Customer.
- **FR-006**: The system shall notify the Customer when a cancellation is accepted and again when the refund reaches status `Succeeded` or `Failed`. Fulfils [BR-007]. Priority: Should.
- **FR-006.AC1**: Given an accepted cancellation, When the cancellation is committed, Then one notification stating the order ID, refund amount, and refund status `Pending` is sent to the Customer's contact address on the order.
- **FR-006.AC2**: Given a refund that reaches `Failed`, When the failure is recorded, Then a notification stating the failure and a contact path for Support is sent to the Customer.
- **FR-007**: The system shall make orders whose refund status is `Failed` retrievable by Support, together with the provider reason and the order's paid date, for manual resolution. Fulfils [BR-006]. Priority: Could.
- **FR-007.AC1**: Given three orders with refund status `Failed`, When a Support agent retrieves the failed-refund list, Then all three orders are returned with their provider reason and paid date.
- **FR-007.AC2**: Given an order whose refund is retried successfully by a Support agent, When the retry succeeds, Then the refund status becomes `Succeeded` and the order leaves the failed-refund list.

## Non-functional requirements

| ID | Priority | Target |
|---|---|---|
| NFR-001 | Must | Cancellation confirmation returned to the actor within 2 s at p95, for orders with up to 100 line items |
| NFR-002 | Must | Refund submitted to the payment provider within 5 minutes of an accepted cancellation for 99 percent of cancellations; a rejected submission is retried 3 times before the refund is marked `Failed` |
| NFR-003 | Must | 100 percent of cancellation requests authenticated; 0 order status changes caused by an actor lacking the `cancel-order` permission or order ownership |
| NFR-004 | Must | 0 payment-card primary account numbers and 0 security codes stored in cancellation records or written to logs; only the provider refund reference is retained |
| NFR-005 | Must | 100 percent of accepted cancellations produce an audit record retained for 7 years and readable by Finance and Support |

- **NFR-001.AC1**: Given orders with 100 line items and 50 concurrent cancellation requests, When each request is submitted, Then the p95 confirmation time is at most 2 s.
- **NFR-002.AC1**: Given 1,000 accepted cancellations in one day, When the day closes, Then at least 990 refunds were submitted to the provider within 5 minutes of acceptance.
- **NFR-002.AC2**: Given a provider rejection on the first attempt, When the refund is retried, Then at most 3 attempts are made before the refund is marked `Failed`.
- **NFR-003.AC1**: Given an authenticated actor without the `cancel-order` permission, When the actor submits 100 cancellation requests, Then 0 orders change status.
- **NFR-004.AC1**: Given 100 cancelled card-paid orders, When cancellation records and logs are inspected, Then 0 primary account numbers and 0 security codes are present.
- **NFR-005.AC1**: Given one year of cancellations, When the audit store is queried, Then 100 percent of accepted cancellations have an audit record, and records from 7 years ago are still readable.

## Edge cases

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| Customer | `Paid` | cancellation accepted, refund submitted | sees amount and refund status | status becomes `Cancelled` | not allowed, no hard delete |
| Customer | `Processing` | cancellation accepted, refund submitted | same as `Paid` | status becomes `Cancelled` | not allowed |
| Customer | `Shipped` | refused, returns path offered | sees shipped status | not allowed | not allowed |
| Customer | `Cancelled`, refund `Pending` | repeat request returns existing record, no second refund | sees `Pending` and arrival window | not allowed | not allowed |
| Customer | `Cancelled`, refund `Failed` | repeat request returns existing record | sees `Failed` and Support path | not allowed | not allowed |
| Customer | order owned by another Customer | refused | refused | not allowed | not allowed |
| Support agent | `Paid` with permission | accepted with reason code, refund submitted | full order and cancellation record | status becomes `Cancelled` | not allowed |
| Support agent | `Paid` without permission | refused | may read order | not allowed | not allowed |
| Support agent | `Shipped` | refused with shipped reason | sees shipped status | not allowed | not allowed |
| Support agent | refund `Failed` | retry allowed | sees provider reason and paid date | refund status becomes `Succeeded` on success | not allowed |
| Payment provider | refund submission times out | refund marked `Failed` after 3 attempts, order stays `Cancelled` | — | retried by Support | — |
| System | two concurrent requests on one `Paid` order | one cancellation and one refund only | — | — | — |

## Glossary

| Term | Meaning |
|---|---|
| Captured amount | the money actually taken from the customer for the order, in the order currency |
| Cancelled | order status meaning the order will not be fulfilled and its money is being returned |
| Cancellation record | the stored record of one accepted cancellation, holding the fields in BR-005 |
| Cancellation window | the period from payment until the order reaches `Shipped`, during which BR-001 allows cancellation |
| `cancel-order` permission | the entitlement that lets a Support agent cancel orders on a customer's behalf |
| Order status | one of `Unpaid`, `Paid`, `Processing`, `Shipped`, `Delivered`, `Completed`, `Cancelled` |
| Refund reference | the identifier the payment provider returns for one refund submission |
| Refund status | one of `Pending`, `Succeeded`, `Failed` |
| `Shipped` | order status set by Fulfilment when the order leaves the warehouse; ends the cancellation window |

## Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | This release covers whole-order cancellation only; cancelling individual line items is out of scope. | Ticket says "cancel orders", not items; if line-item cancellation is required, FR-001 and FR-002 split per item and BR-002 gains a partial-refund rule. |
| A-02 | `Paid` means the money has been captured, not merely authorised. | Not stated in the ticket; if `Paid` covers authorisations, BR-002 and FR-002 gain a void-instead-of-refund path. |
| A-03 | The order statuses named in BR-001 exist, or will exist, in the order model before FR-001 ships. | Not stated; if statuses differ, BR-001 and every AC that names a status need remapping. |
| A-04 | Refunds go back to the original payment method, not to a store balance or bank transfer. | Not stated; matches common practice; if wrong, FR-002 gains a payout-method choice step. |
| A-05 | Cancellation is one-way; reinstating a cancelled order is out of this release. | Not stated; if reinstatement is needed, BR-004 gains a reversal rule and a new FR. |
| A-06 | Reason codes for Support cancellations are supplied by Support, not defined here. | Not stated; if no reason-code set exists, FR-005.AC1 drops the stored code and BR-005 drops that field. |
| A-07 | The numeric targets in NFR-001 to NFR-005 are provisional proposals pending Finance and Support sign-off. | No target was given in the input; if the owners set different numbers, only the target cells and matching ACs change. |
| A-08 | Cancellations are submitted from the storefront order page and from the Support tool; both channels behave identically. | Ticket does not name a channel; if Support uses a different process, FR-005 gains its own channel-specific ACs. |

## Constraints

- Refund execution depends on the payment provider's API and on the provider's own settlement timing; a submitted refund can succeed days later.
- A shipped order cannot be recalled by this process, so `Shipped` is a hard end of the cancellation window.
- Failed refunds require a manual Finance or Support action; this release cannot guarantee automatic recovery.

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | What business event produced this ticket, and by what date must cancellation be live? | Ticket author / Product owner | all FRs for the cancellation release |
| Q-02 | Is cancellation of individual line items required in this release or a later one? | Product owner | FR-001, FR-002 |
| Q-03 | Which jurisdictions and consumer-protection rules set a minimum cancellation window or a mandatory refund period? | Legal / compliance | BR-001, FR-001 |
| Q-04 | Are shipping and handling charges refunded with the order total? | Finance | BR-002, FR-002 |
| Q-05 | What is the agreed resolution time for a `Failed` refund? | Finance operations | NFR-002, FR-007 |
| Q-06 | Are orders paid by cash on delivery or offline transfer in scope for this cancellation flow? | Finance | FR-002 |
| Q-07 | What volume of cancellation requests per day should the solution be sized for? | Operations | NFR-001, NFR-002 |

## Next step

Brainstorm the solution with this file as context.
