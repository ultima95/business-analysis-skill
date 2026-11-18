<!-- Delete any section below that does not apply. Do not fill a section with "N/A". -->

# Refunds — Requirements

## Context

- Problem: The shop can record orders and decide whether a return is allowed, but a refund cannot be requested, approved, paid, or tracked. `refunds.py` exists as a stub with no behaviour.
- Why now: Refund handling is the missing half of the return process; without it a returned order leaves the customer unpaid and finance without a record.
- Source input: This request, plus current code in `orders.py`, `test_orders.py`, `refunds.py`, and the clarifications given on 2026-11-18: refunds may be full or partial, always return to the original payment method, apply only to delivered orders inside the existing window, and any refund over 5,000,000 VND needs finance approval.

## Actors and stakeholders

| Actor | Does / decides / is informed | Notes |
|---|---|---|
| Customer | Requests a full or partial refund; is informed of every refund state change | Must be the customer who placed the order (A-04) |
| Finance approver | Approves or rejects any refund above 5,000,000 VND | Decision gate, BR-006 |
| Finance lead | Sets the refund policy on fees, taxes, discounts, and restocking | Owns Q-01 |
| Payment operations | Owns the completion time target for payouts | Owns Q-02 |
| Payment provider | Executes the payout to the original payment method; can accept or reject it | External system; failure path in FR-006 |

## Scope

In scope:
- Refund eligibility for an order, aligned to the rules the order code enforces today.
- Full and partial refunds, bounded by the amount captured for the order.
- Refund lifecycle states, duplicate and over-refund prevention, payout, notification, audit trail.
- Finance approval for refunds over 5,000,000 VND.

Out of scope:
- Returns logistics: accepting, receiving, and inspecting the physical item.
- Exchanges and store credit.
- Refunds for orders that never reached delivered state.
- Any override of the 30-day window or of the delivered-order rule.
- Changes to the order lifecycle and to the return-window rule.

## Business rules

- **BR-001**: An order is in exactly one of five states: pending, paid, shipped, delivered, cancelled. Source: `orders.py:8`, `orders.py:12`.
- **BR-002**: A return is allowed only when the order status is delivered; any other status, including cancelled, is not returnable. Source: `orders.py:25`.
- **BR-003**: A return requires a recorded delivery date; an order with no recorded delivery date is not returnable. Source: `orders.py:27`.
- **BR-004**: A return is allowed only within 30 days of the delivery date, and day 30 is inside the window. Source: `orders.py:15`, `orders.py:29`. Evidence of intent: `test_orders.py:13` pins day 30 as allowed, `test_orders.py:21` pins day 31 as rejected.
- **BR-005**: A refund is always paid back to the payment method used for the order; no other payout method is offered.
- **BR-006**: A refund whose amount is greater than 5,000,000 VND requires approval by a finance approver before any payout is submitted.
- **BR-007**: The sum of all completed refunds for an order shall not exceed the amount captured for that order.

### Refund eligibility decision table

| Condition / action | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| Order status is delivered | Y | Y | Y | N | Y |
| Delivery date is recorded | Y | Y | N | – | Y |
| Days since delivery ≤ 30 | Y | N | – | – | Y |
| Remaining refundable balance > 0 | Y | – | – | – | N |
| Outcome | Refund accepted | Rejected: outside window | Rejected: missing delivery date | Rejected: not delivered | Rejected: nothing left to refund |

The table applies BR-001 to BR-004 and BR-007, and is cited by FR-001 and FR-002.

## Functional requirements

- **FR-001**: As a customer, I want to request a refund for a delivered order inside the return window, so that I recover money I paid. Fulfils [BR-001], [BR-002], [BR-003], [BR-004]. Priority: Must.
- **FR-001.AC1**: Given an order in delivered state with a recorded delivery date 10 days before today, When the customer requests a refund, Then a refund is created in state requested.
- **FR-001.AC2**: Given an order in delivered state with a recorded delivery date 31 days before today, When the customer requests a refund, Then the request is rejected with reason outside-window and no refund record is created.
- **FR-001.AC3**: Given an order in pending, paid, shipped, or cancelled state, When the customer requests a refund, Then the request is rejected with reason order-not-delivered and no refund record is created.
- **FR-001.AC4**: Given an order in delivered state with no recorded delivery date, When the customer requests a refund, Then the request is rejected with reason delivery-date-missing and no refund record is created.

- **FR-002**: The system shall allow several partial refunds on one order while a refundable balance remains, and reject a request once that balance reaches zero. Fulfils [BR-007]. Priority: Must.
- **FR-002.AC1**: Given an order with a captured total of 100.00 and one completed refund of 40.00, When the customer requests a refund of 50.00, Then the request is accepted with remaining refundable balance 10.00.
- **FR-002.AC2**: Given an order with a captured total of 100.00 and completed refunds summing to 100.00, When the customer requests a refund, Then the request is rejected with reason nothing-left-to-refund and no refund record is created.
- **FR-002.AC3**: Given an order with a captured total of 100.00 and completed refunds of 60.00, When a refund of 50.00 is validated, Then it is rejected with reason amount-exceeds-remaining and no payout is submitted.

- **FR-003**: As a customer, I want to choose a full or partial refund amount up to my remaining refundable balance, so that I can be repaid for the part I returned. Fulfils [BR-007]. Priority: Must.
- **FR-003.AC1**: Given an order with a captured total of 100.00 and no refunds, When the customer requests a full refund, Then the refund amount is 100.00 in the order currency.
- **FR-003.AC2**: Given an order with a captured total of 100.00 and no refunds, When the customer requests a partial refund of 40.00, Then the refund amount is 40.00 in the order currency.
- **FR-003.AC3**: Given an order with a captured total of 100.00 and completed refunds of 60.00, When a refund of 50.00 is submitted, Then it is rejected with reason amount-exceeds-remaining and no payout is submitted.
- **FR-003.AC4**: Given a refund amount of zero or a negative amount, When the refund is submitted, Then it is rejected with reason invalid-amount and no refund record is created.

- **FR-004**: As a customer, I want to see the current state of each refund on my order, so that I know whether my money has been returned. Priority: Must.
- **FR-004.AC1**: Given a refund in state requested, When the customer opens the order, Then the refund state, amount, and request date are shown.
- **FR-004.AC2**: Given a refund in state failed, When the customer opens the order, Then the failure reason is shown in that refund record.
- **FR-004.AC3**: Given an order with no refund, When a customer who placed that order opens it, Then no refund record is shown and the refund request action is offered only when the eligibility check passes.

- **FR-005**: As a finance approver, I want to approve or reject any refund above 5,000,000 VND, so that large payouts are checked before money leaves the business. Fulfils [BR-006]. Priority: Must.
- **FR-005.AC1**: Given a refund amount of exactly 5,000,000 VND, When the refund is validated, Then no finance approval is required and the refund proceeds to payout.
- **FR-005.AC2**: Given a refund amount of 5,000,001 VND, When the refund is validated, Then it moves to state awaiting-finance-approval and no payout is submitted.
- **FR-005.AC3**: Given a refund in state awaiting-finance-approval, When a finance approver approves it, Then the refund moves to state approved with the approver identity recorded and the payout is submitted.
- **FR-005.AC4**: Given a refund in state awaiting-finance-approval, When a finance approver rejects it with a recorded reason, Then the refund moves to state rejected and the customer is notified.

- **FR-006**: The system shall submit an approved refund to the payment provider against the original payment method, and record the provider outcome, so that a payout is never lost or duplicated. Fulfils [BR-005]. Priority: Must.
- **FR-006.AC1**: Given a refund in state approved, When the payment provider accepts the payout, Then the refund moves to state completed and the provider reference is recorded.
- **FR-006.AC2**: Given a refund in state approved, When the payment provider rejects the payout, Then the refund moves to state failed with the provider error recorded and no further attempt is made without a new request.
- **FR-006.AC3**: Given a refund in state failed with a retryable provider error, When the retry is submitted, Then the retry count increases and no more than 3 attempts are made within 24 hours.
- **FR-006.AC4**: Given an order with no recorded payment method, When the payout is submitted, Then the refund moves to state failed with reason payment-method-missing.

- **FR-007**: The system shall notify the customer by email on every refund state change, so that the customer is informed without contacting support. Priority: Should.
- **FR-007.AC1**: Given a refund moves from requested to approved, When the state change is recorded, Then one email is queued to the customer's order email address.
- **FR-007.AC2**: Given the same state change is recorded twice within one minute, When the notification is queued, Then only one email is queued for that transition.

## Non-functional requirements

| ID | Priority | Target |
|---|---|---|
| NFR-001 | Must | 100% of refund state changes recorded with actor, UTC timestamp to the second, and from-state and to-state, retained for 7 years |
| NFR-002 | Should | p95 acknowledgement of a refund request ≤ 2 s at 20 concurrent requests |

- **NFR-001.AC1**: Given any refund state change, When the change is committed, Then one audit record exists containing actor, UTC timestamp, from-state, and to-state, and that record is readable for 7 years.
- **NFR-002.AC1**: Given 20 concurrent refund requests, When all requests are submitted, Then p95 acknowledgement time is ≤ 2 s.

## Edge cases

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| Customer | delivered, day ≤ 30, balance full | Refund accepted, state requested | Refund record visible with amount | Not allowed; customer cannot approve | Not allowed |
| Customer | delivered, day ≤ 30, balance partly used | Partial refund accepted up to remaining balance | All refunds on the order visible | Not allowed | Not allowed |
| Customer | delivered, day ≤ 30, balance zero | Rejected, reason nothing-left-to-refund | Completed refunds visible | Not allowed | Not allowed |
| Customer | delivered, day 31 or later | Rejected, reason outside-window | Rejection reason visible | Not allowed | Not allowed |
| Customer | delivered, delivery date missing | Rejected, reason delivery-date-missing | No refund record | Not allowed | Not allowed |
| Customer | shipped or paid | Rejected, reason order-not-delivered | No refund record | Not allowed | Not allowed |
| Customer | cancelled | Rejected, reason order-not-delivered | No refund record | Not allowed | Not allowed |
| Customer | refund above 5,000,000 VND | Accepted into awaiting-finance-approval | Approval state visible | Not allowed | Not allowed |
| Finance approver | awaiting-finance-approval | Not allowed | Refund and order visible | Approve or reject with recorded reason | Not allowed |
| Payment provider | approved | Payout accepted or rejected | Provider reference readable | Failure reason recorded | Not allowed |

## Glossary

| Term | Meaning |
|---|---|
| Order | A purchase with a status from the order lifecycle and, once delivered, a delivery date. |
| Delivered | The order state that makes a return or refund possible; set together with the delivery date. |
| Return window | The 30-day period after the delivery date in which a return is allowed, day 30 included. |
| Refund | The repayment of captured money for an order, tracked through its own state values. |
| Partial refund | A refund whose amount is below the remaining refundable balance of the order. |
| Captured amount | The money actually collected for the order, which bounds all refunds on it. |
| Remaining refundable balance | Captured amount minus the sum of all completed refunds on the order. |
| Finance approval gate | The state a refund above 5,000,000 VND must pass before a payout is submitted. |

## Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | Refund states are requested, awaiting-finance-approval, approved, completed, failed, rejected. | Not stated, and `refunds.py` defines no states; if false, FR-004, FR-005, and NFR-001 change their state names. |
| A-02 | Audit records are retained 7 years. | Accounting practice not stated in the repo; if false, NFR-001 target and its acceptance criterion change. |
| A-03 | A refund request is acknowledged within 2 s at p95 under 20 concurrent requests. | No target in the repo; if false, NFR-002 changes. |
| A-04 | Only the customer who placed the order can request its refund. | Not stated; if false, FR-001 adds an authorisation check for another role. |
| A-05 | The 5,000,000 VND threshold applies to each refund request, not to the cumulative total for one order. | Stated threshold has no scope; if false, FR-005 evaluates the order total and FR-002 changes. |
| A-06 | An order carries one recorded payment method for the whole order. | Not stated; if false, FR-006 needs a rule for orders paid by more than one method. |

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | Are shipping fees, taxes, and discounts included in the refundable balance, and is a restocking fee deducted from a partial refund? | Finance lead | FR-003 |
| Q-02 | How many business days may a refund stay between approved and completed before it is escalated? | Payment operations | FR-006, NFR-002 |
| Q-03 | Does a partial refund require a recorded return of the related items before payout? | Product owner | FR-002, FR-003 |

## Next step

Brainstorm the solution with this file as context.
