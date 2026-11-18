# Order Cancellation After Payment — Requirements

## Context

- Problem: the ticket states "Customers can't cancel orders after payment." The complaint is that a paid order can no longer be abandoned by the customer, so the money stays committed to goods the customer no longer wants.
- Why now: not stated in the input. The ticket carries no deadline, incident, cost figure, or volume.
- Source input: a single-sentence ticket, quoted above. No transcript, email thread, or attachment accompanies it.
- Existing system: the repository contains no application code at this revision, so no current cancellation rules could be recovered from source. Every rule below is a working value adopted by this analysis and is registered in the Assumptions table — none of it is confirmed business policy.

## Actors and stakeholders

Only the customer is named in the input. The other rows are roles this analysis assumes to exist; each is registered as an assumption and is not a confirmed actor.

| Actor | Does / decides / is informed | Notes |
|---|---|---|
| Customer | Triggers cancellation of their own paid order; is informed of the outcome and the refund | The only actor stated in the ticket |
| Support agent | May cancel on the customer's behalf | Assumed; A-03 |
| Fulfilment operation | Holds the order while it is being picked and packed; its hand-off ends the cancellation window | Assumed; A-02, A-04 |
| Payment provider | Receives the void or refund instruction and settles it | Assumed; A-06, A-07 |
| Finance | Owns refund accounting and dispute handling | Assumed; owner of Q-02, Q-08 |

## Scope

In scope:

- Cancellation of a whole paid order by the customer who placed it, while the order has not been handed to fulfilment.
- The money path of a cancellation: void of an uncaptured payment, refund of a captured payment, retry when the payment provider fails, and the record of what was returned.
- Communication to the customer that the order is cancelled and that the refund was issued.
- Cancellation performed by a support agent on the customer's behalf.
- The audit record of every cancellation.

Out of scope:

- Returns and refunds after delivery; those follow the existing return process.
- Chargebacks, payment disputes, and fraud review.
- Changing the contents of an order instead of cancelling it (address change, item swap, quantity change).
- Partial cancellation of individual line items; Q-01 records the scope question.
- Pricing, promotion, and tax recalculation for cancellations.

## Business rules

These rules are not in the ticket. Each is the working value this analysis adopts so the requirements can be made testable, and each is registered in the Assumptions table with what changes if it is wrong.

- **BR-001**: A cancellation is accepted only while the order has not been handed to fulfilment; once fulfilment has received the order, cancellation is refused. Basis: A-02, working rule; A-09 defines the order statuses used here.
- **BR-002**: Only the customer who placed the order, or a support agent acting on that customer's behalf, may cancel it. No other role may cancel. Basis: A-03.
- **BR-003**: A cancellation request that reaches the system after fulfilment has marked the order as dispatched is refused, even when the customer opened the request before the dispatch was recorded. Basis: A-04.
- **BR-004**: A completed cancellation returns the full captured amount, in the order currency, to the original payment instrument; no cancellation fee is deducted. Basis: A-05, A-10.
- **BR-005**: When the order's payment is authorized but not yet captured, cancellation voids the authorization and no refund is issued. Basis: A-06.
- **BR-006**: A cancellation whose refund instruction is rejected by, or gets no answer from, the payment provider leaves the order in Cancellation Pending; the instruction is retried and the order does not return to a cancelable state. Basis: A-07.
- **BR-007**: Cancellation is idempotent per order: one order produces at most one void or one refund, however many requests arrive. Basis: A-08.
- **BR-008**: Every cancellation records the actor, the timestamp, the order, the reason code, the amount returned, and the payment provider reference. Basis: A-11.
- **BR-009**: The customer is informed twice: when the order becomes Canceled, and when the money movement is confirmed or has failed. Basis: A-12.

## Functional requirements

- **FR-001**: As a customer, I want to cancel a paid order before it is handed to fulfilment, so that I am not charged for goods I no longer want. Fulfils [BR-001], [BR-002]. Priority: Must.
- **FR-001.AC1**: Given my order is paid and still awaiting fulfilment, When I confirm cancellation, Then the order status becomes Canceled and the amount I was charged is queued for return.
- **FR-001.AC2**: Given my order has been handed to fulfilment, When I request cancellation, Then the request is refused with a message naming the return process as the available route.
- **FR-001.AC3**: Given my order belongs to another customer, When I request cancellation for it, Then the request is refused and the order is unchanged.
- **FR-002**: As a customer, I want to see whether my order can still be cancelled before I try, so that I do not attempt a request that will be refused. Fulfils [BR-001]. Priority: Must.
- **FR-002.AC1**: Given my order is awaiting fulfilment, When I open the order, Then a cancellation action is offered and the order's current status is shown with it.
- **FR-002.AC2**: Given my order is dispatched, When I open the order, Then the cancellation action is absent and the return route is shown instead.
- **FR-003**: As a customer, I want to see the amount that will be returned and when it is expected before I confirm, so that I know what I am agreeing to. Fulfils [BR-004]. Priority: Must.
- **FR-003.AC1**: Given an order of 49.00 USD that was fully charged, When I open the cancellation confirmation, Then I am shown 49.00 USD as the amount to be returned and the settlement window stated for that payment instrument.
- **FR-003.AC2**: Given the order's payment was authorized but not charged, When I open the cancellation confirmation, Then I am shown that 0.00 is refunded because the reservation on my funds is released instead.
- **FR-004**: The system shall return the full captured amount to the original payment instrument when a cancellation completes. Fulfils [BR-004]. Priority: Must.
- **FR-004.AC1**: Given an order charged 49.00 USD, When the cancellation completes, Then a refund instruction to the original instrument is accepted by the payment provider and the amount recorded against the order is 49.00 USD.
- **FR-004.AC2**: Given the order was paid with a payment instrument that is no longer valid, When the cancellation completes, Then the order is held in Cancellation Pending and the failure is recorded against the order.
- **FR-005**: The system shall void the payment authorization instead of issuing a refund when the order's payment has not been captured. Fulfils [BR-005]. Priority: Must.
- **FR-005.AC1**: Given an order whose payment is authorized and not captured, When the cancellation completes, Then a void instruction is sent to the payment provider and no refund instruction is sent.
- **FR-005.AC2**: Given the payment provider confirms the void, When the cancellation record is written, Then the recorded returned amount is 0.00 and the void reference is recorded instead of a refund reference.
- **FR-006**: The system shall hold a cancellation in Cancellation Pending and retry the money instruction when the payment provider rejects it or does not answer. Fulfils [BR-006]. Priority: Must.
- **FR-006.AC1**: Given the payment provider rejects the refund instruction, When the rejection is received, Then the order remains in Cancellation Pending and a retry is scheduled.
- **FR-006.AC2**: Given the payment provider does not answer within 30 seconds, When the attempt times out, Then the order remains in Cancellation Pending and the timeout is recorded against the order.
- **FR-006.AC3**: Given three failed attempts, When the last attempt fails, Then the order is flagged for support agent handling and the customer is informed that the money return is delayed.
- **FR-007**: The system shall refuse a cancellation that arrives after fulfilment has marked the order as dispatched, and point the customer to the return process. Fulfils [BR-003]. Priority: Must.
- **FR-007.AC1**: Given I opened the cancellation confirmation while the order was awaiting fulfilment, When I confirm after dispatch has been recorded, Then the cancellation is refused and no money instruction is sent.
- **FR-007.AC2**: Given dispatch is recorded at the same moment as my confirmation, When the two events are processed, Then only one outcome is recorded for the order and it is stated to me.
- **FR-008**: As a support agent, I want to cancel a paid order on a customer's behalf, so that telephone and chat requests are handled without the customer doing it themselves. Fulfils [BR-002]. Priority: Should.
- **FR-008.AC1**: Given the customer asks by telephone for an awaiting-fulfilment order to be cancelled, When I cancel it as a support agent, Then the order becomes Canceled and my identity is recorded as the actor.
- **FR-008.AC2**: Given the order has been dispatched, When I attempt cancellation, Then the request is refused with the same rule the customer meets.
- **FR-009**: The system shall produce at most one void or refund per order, whatever the number of cancellation requests received. Fulfils [BR-007]. Priority: Must.
- **FR-009.AC1**: Given an order already cancelled with a refund accepted, When a second cancellation request arrives, Then the current Canceled status is returned and no new money instruction is sent.
- **FR-009.AC2**: Given two cancellation requests for the same order arrive at the same moment, When both are processed, Then exactly one money instruction is sent and both requests report the same outcome.
- **FR-010**: The system shall record an audit entry for every cancellation, naming the actor, the order, the time, the reason code, the amount returned, and the payment provider reference. Fulfils [BR-008]. Priority: Must.
- **FR-010.AC1**: Given a customer cancels their own order, When the cancellation completes, Then the audit entry names the customer as the actor and carries the time to the second.
- **FR-010.AC2**: Given a support agent cancels an order, When the cancellation completes, Then the audit entry names the support agent as the actor and the customer as the order owner.
- **FR-011**: As a customer, I want to be told that my order is cancelled and that my money is on its way, so that I am not left checking my statement. Fulfils [BR-009]. Priority: Should.
- **FR-011.AC1**: Given my cancellation completes, When the order becomes Canceled, Then I receive one message naming the order, the amount to be returned, and the settlement window.
- **FR-011.AC2**: Given a refund fails three times, When the last attempt fails, Then I receive one message stating that the money return is delayed and that support will contact me.

## Non-functional requirements

All targets here are working values set by this analysis, not targets stated in the ticket.

| ID | Priority | Target |
|---|---|---|
| NFR-001 | Must | Cancellation confirmation returned to the customer in ≤ 3 s at p95, measured over 50 concurrent cancellation requests |
| NFR-002 | Must | Void or refund instruction handed to the payment provider within 60 s of cancellation confirmation |
| NFR-003 | Must | Cancellation path available 99.9% of each calendar month, measured by an external check every 60 s |
| NFR-004 | Must | Audit entries retained for 7 years and readable by Finance for the full period, with no update or delete operation permitted |
| NFR-005 | Must | Cancellation records and messages never contain the full payment instrument number; at most the last 4 digits and the payment provider reference are stored |

- **NFR-001.AC1**: Given 50 concurrent cancellation requests, When each customer confirms, Then p95 time to confirmation is ≤ 3 s.
- **NFR-001.AC2**: Given the payment provider responds in 10 s, When a cancellation is confirmed, Then the customer reaches confirmation in ≤ 3 s without waiting for the provider.
- **NFR-002.AC1**: Given a cancellation confirms at 10:00:00, When the provider log is read, Then the void or refund instruction was received by 10:01:00.
- **NFR-003.AC1**: Given one calendar month of monitoring at 60 s intervals, When the month closes, Then no more than 0.1% of checks recorded the cancellation path unavailable.
- **NFR-004.AC1**: Given an audit entry written 7 years ago, When Finance reads it, Then the entry is returned unchanged and no update or delete is permitted on it.
- **NFR-005.AC1**: Given any cancellation record or customer message, When its content is inspected, Then it holds at most the last 4 digits of the payment instrument and no security code.

## Edge cases

| Actor | Order state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| Customer | Paid, awaiting fulfilment | Cancellation accepted | Status and cancel action shown | Becomes Canceled, money instruction queued | Not permitted |
| Customer | Handed to fulfilment, not dispatched | Refused (BR-001) | Status shown without cancel action | Not permitted | Not permitted |
| Customer | Dispatched | Refused, return route offered (BR-003) | Return route shown | Not permitted | Not permitted |
| Customer | Cancellation Pending | Second request returns pending state, no new instruction (BR-007) | Pending state and delay reason shown | Not permitted | Not permitted |
| Customer | Canceled | Second request returns Canceled, no new instruction (BR-007) | Cancellation and refund outcome shown | Not permitted | Not permitted |
| Customer | Paid with authorization only | Cancellation accepted, authorization voided (BR-005) | Shows 0.00 returned | Becomes Canceled | Not permitted |
| Support agent | Paid, awaiting fulfilment | Cancellation accepted on behalf (BR-002) | Sees reason code and prior requests | Becomes Canceled with agent as actor | Not permitted |
| Support agent | Dispatched | Refused (BR-003) | Sees dispatch time | Not permitted | Not permitted |
| Support agent | Three failed refund attempts | Escalation case opened (FR-006) | Sees attempts and provider responses | Can retry or hand to Finance | Not permitted |
| Fulfilment operation | Awaiting fulfilment | Not permitted | Sees cancellation flag | Hand-off advances status | Not permitted |

## Glossary

| Term | Meaning |
|---|---|
| Paid order | An order whose payment is either captured by the payment provider or authorized and awaiting capture. |
| Awaiting fulfilment | The order state after payment and before fulfilment has received the order; the only cancelable state (A-09). |
| Handed to fulfilment | The order state in which fulfilment has taken the order to pick and pack; cancellation is refused from here (BR-001). |
| Dispatched | The order state recorded when the shipment leaves the warehouse; cancellation is refused and the return process applies (BR-003). |
| Canceled | The order state reached when a cancellation has been accepted; no further money instruction is sent for that order (BR-007). |
| Cancellation Pending | The order state in which a cancellation is accepted but the void or refund instruction has not yet been accepted by the payment provider (BR-006). |
| Captured | The payment provider has taken the money from the customer's instrument. |
| Authorized (not captured) | The payment provider has reserved the money on the customer's instrument but not taken it (BR-005). |
| Void | An instruction that releases an authorization without moving money (BR-005). |
| Refund | An instruction that returns captured money to the original payment instrument (BR-004). |
| Reason code | A fixed value recording why the customer cancelled, captured in the audit entry (BR-008). |
| Settlement window | The number of business days a payment instrument needs to show a refund, stated to the customer before confirmation (BR-009). |

## Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | "Order" means one paid purchase with one payment; the customer cancels it whole. | Ticket says only "orders"; if orders can carry several payments or shipments, FR-001 and FR-004 split per payment. |
| A-02 | The cancellation window is governed by order status, not by elapsed time; there is no time cutoff while the order awaits fulfilment. | Not stated; if a cutoff exists, FR-001, FR-002, FR-003 gain a time condition and BR-001 is rewritten. |
| A-03 | Only the order's customer and a support agent may cancel; other staff and automated processes may not. | Not stated; if Finance or fulfilment may also cancel, FR-008 and BR-002 widen. |
| A-04 | A request overtaken by dispatch is refused rather than honoured. | Not stated; if the order must still be recalled, FR-007 becomes a recall flow and BR-003 changes. |
| A-05 | No cancellation fee and no deduction is made from the returned amount. | Not stated; if a fee applies, FR-003 and FR-004 gain an amount calculation and BR-004 changes. |
| A-06 | Authorized but uncaptured payments are voided, not refunded. | Not stated; if capture always precedes cancellation, FR-005 and BR-005 are dropped. |
| A-07 | A failed money instruction keeps the order in Cancellation Pending and is retried; the order does not revert to cancelable. | Not stated; if the order must revert, BR-006 and FR-006 change and a second cancellation becomes possible. |
| A-08 | One order yields at most one void or refund. | Follows from a cancellation being final; if support can re-issue a refund, FR-009 and BR-007 narrow to automated requests only. |
| A-09 | Order statuses are Awaiting fulfilment, Handed to fulfilment, Dispatched, Canceled, and Cancellation Pending. | Working vocabulary; if real statuses differ, every rule citing a status maps onto their names. |
| A-10 | Money returns to the original payment instrument, not to store credit. | Not stated; if store credit is allowed, FR-003 and FR-004 gain a choice and BR-004 changes. |
| A-11 | A reason code is recorded for every cancellation. | Not stated; if reasons are optional, FR-010 records an empty reason and BR-008 relaxes. |
| A-12 | The customer is informed at cancellation and again at money-movement outcome. | Not stated; if only one message is sent, FR-011 keeps the outcome message and drops the first. |
| A-13 | A support agent may retry a failed money instruction. | Not stated; if only Finance may, FR-006 escalates instead of retrying. |

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | Is cancelling individual line items of an order in scope, or only the whole order? | Product owner of the ordering journey | all FRs for cancellation scope; FR-001, FR-004 |
| Q-02 | Are delivery and handling charges returned in full on cancellation? | Finance | FR-003, FR-004 |
| Q-03 | Does a time cutoff apply, refusing cancellation after a fixed number of hours even when the order still awaits fulfilment? | Operations lead | FR-001, FR-002 |
| Q-04 | Which reason codes are permitted, and is a reason required from the customer? | Customer support lead | FR-010 |
| Q-05 | Can a customer cancel an order placed without an account, and through which route do they reach cancellation? | Product owner of the ordering journey | FR-001, FR-002 |
| Q-06 | What settlement window may be promised to customers for each payment instrument? | Finance, with the payment provider contract | FR-003, FR-011 |
| Q-07 | Which figure shows this change works, who owns it, and what is its value today — for example the share of paid orders cancelled by customers without support contact? | Head of customer operations | all FRs for order cancellation (no acceptance target can be judged without it) |
| Q-08 | Do gift card, store credit, and instalment payments return to the original instrument or another channel? | Finance | FR-004, FR-005 |
| Q-09 | Must a cancellation that arrives during pick and pack attempt to stop the shipment, or is refusal acceptable at that point? | Fulfilment manager | FR-007 |

## Next step

Brainstorm the solution with this file as context.
