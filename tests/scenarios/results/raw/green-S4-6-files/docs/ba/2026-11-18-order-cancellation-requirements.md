# Order Cancellation After Payment — Requirements

## Context

- Problem, in the requester's words: "Customers can't cancel orders after payment."
- Why now: not stated in the ticket. No volume, cost, or deadline accompanies the claim — see [Q-01].
- Source input: the ticket text above. The repository at the time of analysis contains no application code (only `.git`), so no current rules could be recovered from source. Every rule below is therefore derived, and each one carries its assumption or open question.

The ticket reports a capability gap, not a defect report: it does not say which order states are affected, whether a refund is expected, or who the customer contacts today. This document states what "cancel after payment" has to mean to be deliverable and testable, and records what it had to assume.

## Actors and stakeholders

| Actor | Does / decides / is informed | Notes | Basis |
|---|---|---|---|
| Customer | Triggers the cancellation for their own order; is informed of the outcome and the refund | The only actor named in the ticket | "Customers can't cancel orders after payment." |
| Support agent | Cancels on a customer's behalf when the customer can no longer self-serve; decides on the recorded reason | The ticket implies a current workaround but does not name one | [A-01] |
| Finance | Reconciles refunds; receives escalations when a refund cannot be initiated | Not named in the ticket | [A-01], [A-10] |
| Fulfilment / warehouse | Stops picking and shipment of a cancelled order; is informed of the cancellation | Not named in the ticket | [A-11] |
| Payment provider | Executes the refund against the original payment method | External system; not named in the ticket | [A-07] |
| Compliance / auditor | Reads the cancellation and refund audit trail; sets the retention period | Not named in the ticket | [A-15] |

## Scope

In scope:
- Cancelling a paid order that has not yet been dispatched, by the customer and by a support agent.
- Returning the money already captured for that order to the original payment method.
- Telling the customer the outcome, the amount, and when the money arrives.
- Stopping fulfilment of the cancelled order.
- Handling a cancelled order whose refund cannot be initiated on the first attempt.

Out of scope:
- Cancelling an order before payment is completed; that path already exists and this ticket does not report it as broken ([A-05]).
- Returns, exchanges, and refunds for delivered goods; those stay in the existing returns process ([BR-002]).
- Partial cancellation of individual lines within an order — raised as [Q-04].
- Chargebacks and disputes raised by the customer with their bank.
- Pricing, promotion, or tax recalculation on cancellation.
- Choice of technology, architecture, data model, or screen design.

## Business rules

- **BR-001**: An order is eligible for customer cancellation while its payment has been captured and the order has not been dispatched. Basis: [A-03], [A-04].
- **BR-002**: An order that has been dispatched or delivered is not eligible for cancellation, and the customer is directed to the returns process instead. Basis: [A-04].
- **BR-003**: An order whose payment has not been captured is cancelled by abandoning the payment, with no refund raised. Basis: [A-05].
- **BR-004**: The refund amount equals the total captured payment for the order minus any amount already refunded against it. Basis: [A-06].
- **BR-005**: The refund is issued to the original payment method only; no alternative payout method is offered. Basis: [A-07].
- **BR-006**: A cancellation request repeated for an order that is already cancelled returns the existing cancellation record and raises no second refund. Basis: [A-08].
- **BR-007**: A customer cancellation records a reason chosen from a fixed list maintained by the business; a cancellation without a selected reason is not accepted. Basis: [Q-02].
- **BR-008**: A support agent may cancel an order that the customer can no longer self-serve only when a reason is recorded and the order has not been delivered. Basis: [A-09].
- **BR-009**: When a refund cannot be initiated, the order stays cancelled, the initiation is retried up to 3 times, and the case is escalated to Finance after the third failure. Basis: [A-10].
- **BR-010**: Cancelling an order before dispatch releases its reserved stock back to available inventory. Basis: [A-12].

### Eligibility decision table (drives BR-001, BR-002, BR-003)

| Condition / outcome | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| Payment captured | Y | Y | Y | N | – |
| Order dispatched or delivered | N | Y | N | – | – |
| Order already cancelled | N | N | Y | – | – |
| Cancellation offered to the customer | cancel + refund | refused, returns offered | refused, existing confirmation shown | abandon payment | refused |
| Enforced by | BR-001 | BR-002 | BR-006 | BR-003 | BR-006 |

## Functional requirements

- **FR-001**: As a customer, I want to cancel an eligible paid order myself, so that I get my money back without contacting support. Fulfils [BR-001]. Priority: Must.
- **FR-001.AC1**: Given an order whose payment is captured and which has not been dispatched, When the customer confirms cancellation, Then the order status is Cancelled and the refund for the full captured amount is initiated in the same request.
- **FR-001.AC2**: Given an order that has been dispatched, When the customer opens the order, Then the cancel action is not offered and the returns process is offered instead.
- **FR-001.AC3**: Given a customer cancels an order, When the cancellation is recorded, Then the record holds the order reference, the acting customer, the timestamp, the refund amount, and the reason code.
- **FR-002**: As a customer, I want to see whether my order can still be cancelled and why not, before I confirm, so that I do not attempt a cancellation that will be refused. Fulfils [BR-001], [BR-002], [BR-003]. Priority: Must.
- **FR-002.AC1**: Given an eligible paid order, When the customer views the order, Then the order shows that it can be cancelled up to dispatch together with the refund amount that would be returned.
- **FR-002.AC2**: Given a dispatched or delivered order, When the customer views the order, Then the order states that cancellation is no longer available and links to the returns process.
- **FR-002.AC3**: Given an order whose payment was never captured, When the customer views the order, Then the order states that no payment was taken and offers to abandon the order.
- **FR-003**: As a customer, I want the cancellation confirmation to state the refund amount, the payment method refunded, and the arrival window, so that I know exactly what to expect. Fulfils [BR-004], [BR-005]. Priority: Must.
- **FR-003.AC1**: Given an order with captured payment of amount X and no earlier refund, When the customer cancels it, Then the confirmation states a refund of X to the original payment method and the arrival window for that method.
- **FR-003.AC2**: Given an order with an earlier partial refund of amount Y against a captured payment of X, When the customer cancels it, Then the confirmation states a refund of X minus Y.
- **FR-004**: As a customer, I want to choose a reason for cancelling, so that the business can report why orders get cancelled. Fulfils [BR-007]. Priority: Should.
- **FR-004.AC1**: Given a customer starts a cancellation, When the reason list is presented, Then the cancellation cannot be submitted until exactly one reason is selected.
- **FR-004.AC2**: Given a cancellation is recorded, When the cancellation report is produced for a period, Then each cancellation is counted under its recorded reason code.
- **FR-005**: The system shall treat a repeated cancellation request for an already cancelled order as the same cancellation and return the original confirmation. Fulfils [BR-006]. Priority: Must.
- **FR-005.AC1**: Given an order already cancelled with refund amount X, When the customer submits cancellation again, Then the original confirmation is returned and no additional refund is raised.
- **FR-005.AC2**: Given two cancellation requests for the same order arrive at the same time, When both are processed, Then exactly one cancellation record and exactly one refund exist for the order.
- **FR-006**: As a support agent, I want to cancel an order on a customer's behalf with a recorded reason, so that customers who cannot self-serve are still helped. Fulfils [BR-008]. Priority: Should.
- **FR-006.AC1**: Given an undelivered order past customer self-service eligibility, When a support agent cancels it with a reason, Then the order is cancelled, the refund is initiated, and the agent identity and reason are recorded.
- **FR-006.AC2**: Given a delivered order, When a support agent attempts cancellation, Then the request is refused and the agent is directed to the returns process.
- **FR-007**: The system shall retry a refund that cannot be initiated, escalate to Finance after the third failure, and keep the order cancelled throughout. Fulfils [BR-009]. Priority: Must.
- **FR-007.AC1**: Given a refund initiation fails, When the retry policy runs, Then 3 attempts are made and, after the third failure, an escalation record is created for Finance.
- **FR-007.AC2**: Given a refund is still failing, When the customer views the order, Then the order shows the cancellation as confirmed and the refund as pending with a next-review date, and no amount is shown as refunded.
- **FR-008**: The system shall stop fulfilment of a cancelled order and release its reserved stock to available inventory. Fulfils [BR-001], [BR-010]. Priority: Must.
- **FR-008.AC1**: Given an order is cancelled before dispatch, When the cancellation is recorded, Then the reserved stock for that order is returned to available inventory in the same transaction.
- **FR-008.AC2**: Given an order is cancelled while being picked, When fulfilment receives the cancellation, Then the order is removed from the picking queue before any shipment label is created.
- **FR-009**: As a customer, I want an email confirming the cancellation and the refund, so that I hold a record outside the site. Fulfils [BR-004], [BR-009]. Priority: Should.
- **FR-009.AC1**: Given a cancellation completes, When the cancellation is recorded, Then one email is sent within 1 minute carrying the order reference, the refund amount, the payment method, and the arrival window.
- **FR-009.AC2**: Given a refund is still failing after escalation, When Finance records the resolution, Then one further email states the final refund outcome and its date.

## Non-functional requirements

| ID | Priority | Target | Basis |
|---|---|---|---|
| NFR-001 | Must | Cancellation confirmation is returned within 2 s at p95 and 5 s at p99, measured over 10 000 cancellation requests | [A-13] |
| NFR-002 | Must | The refund request reaches the payment provider within 60 s of confirmation for 99% of cancellations, and within 10 min for 100% | [A-13] |
| NFR-003 | Must | 100% of cancellation attempts from an account that is neither the order's owner nor a support agent are refused and logged | [A-14] |
| NFR-004 | Must | Every cancellation and refund event is retained in the audit trail for 7 years and readable only by the Finance and Compliance roles | [A-15] |
| NFR-005 | Should | A customer reaches a completed cancellation in at most 3 actions from the order list | [A-16] |

- **NFR-001.AC1**: Given 200 concurrent cancellation requests, When the requests are processed, Then the p95 response time is at most 2 s and the p99 is at most 5 s.
- **NFR-002.AC1**: Given 1 000 cancellations in one hour, When processing completes, Then at least 990 refund requests were received by the payment provider within 60 s of their confirmation.
- **NFR-003.AC1**: Given an account that does not own the order and holds no support agent role, When it submits a cancellation for that order, Then the request is refused and one refusal entry is written to the audit trail.
- **NFR-004.AC1**: Given a cancellation recorded 7 years ago, When an authorised Finance user queries the audit trail, Then the cancellation and refund events are returned.
- **NFR-005.AC1**: Given a customer on the order list of an eligible order, When they count the actions to reach a recorded cancellation, Then the count is at most 3.

## Edge cases

| Actor | Entity state | Create (cancel request) | Read (view order) | Update (change reason) | Delete (undo cancellation) |
|---|---|---|---|---|---|
| Customer | Payment captured, not dispatched | Cancelled, full refund | Shows cancellable plus refund amount | Reason not changeable after submit; must re-cancel not supported | Not offered; a new order is the path |
| Customer | Payment captured, dispatched | Refused, returns offered | Shows returns link | Not applicable | Not offered |
| Customer | Payment captured, delivered | Refused, returns offered | Shows returns link | Not applicable | Not offered |
| Customer | Payment never captured | Abandons payment, no refund | Shows no payment taken | Not applicable | Order reopened, no refund owed |
| Customer | Already cancelled | Returns existing confirmation, no second refund | Shows cancelled plus refund status | Not offered | Not offered |
| Customer | Refund escalated to Finance | Cancellation stands, refund pending | Shows pending with next-review date | Not applicable | Not offered |
| Customer | Another customer's order | Refused, logged | Not visible | Not applicable | Not applicable |
| Support agent | Paid, not dispatched | Cancelled with reason | Full order view | Reason recorded at cancellation only | Not offered |
| Support agent | Dispatched, not delivered | Cancelled with reason, refund raised | Full order view | Reason recorded at cancellation only | Not offered |
| Support agent | Delivered | Refused, returns offered | Full order view | Not applicable | Not offered |
| Support agent | Already cancelled by customer | Returns existing confirmation | Full order view | Not applicable | Not offered |
| System (retry process) | Refund failing | Retries up to 3 times | Escalation visible to Finance | Escalation state advances | Escalation closed after Finance resolution |

## Glossary

| Term | Meaning |
|---|---|
| Order | The purchase record a customer receives after checkout, holding its lines, its payment, and its fulfilment state. |
| Captured payment | Money already taken from the customer's payment method, as opposed to an authorisation that has not been settled. |
| Cancellation | The business outcome where an order will not be fulfilled, recorded as a state on the order. |
| Refund | The return of captured money to the original payment method, distinct from the cancellation that triggers it. |
| Dispatch | The point at which an order leaves the warehouse for delivery; after it, cancellation is no longer available. |
| Reserved stock | Inventory held against an order that has not yet been shipped. |
| Reason code | The fixed, business-maintained value attached to a cancellation to explain it. |
| Escalation | The handover of a failing refund to Finance after the retry limit. |

## Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | Support agents, Finance, and fulfilment/warehouse are the roles that touch a cancellation today. | Not stated in the ticket; if false, those actors are removed from scope and [FR-006] is dropped. |
| A-02 | "After payment" means after the payment is captured, not after an authorisation. | Ticket wording; if false, cancellation must also handle authorisation-only orders and [BR-001] widens. |
| A-03 | A paid order not yet dispatched is the state the ticket refers to. | Ticket names no state; if false, the eligibility table changes and [FR-002] must explain a different boundary. |
| A-04 | Dispatch is the last point at which cancellation is possible; delivered goods go through returns. | Not stated; if false, a post-dispatch cancellation window exists and [BR-002] gains a threshold. |
| A-05 | Orders that were never paid are already cancellable and are not part of this problem. | Ticket says "after payment", implying before-payment cancelling works; if false, abandonment joins scope and [BR-003] is added to the work. |
| A-06 | Refund equals captured minus already-refunded amount, with no cancellation fee. | Not stated; if a fee applies, [BR-004] and [FR-003] need the fee rule and its threshold. |
| A-07 | Refunds return to the original payment method only. | Not stated; if alternative payouts are allowed, [BR-005] is replaced and [FR-003] loses the method statement. |
| A-08 | Cancellation is idempotent per order — one order, one cancellation, one refund. | Not stated; if false, [FR-005] is deleted and duplicate refunds become a risk to manage in [BR-009]. |
| A-09 | A support agent may cancel an undelivered order that the customer can no longer self-serve. | Not stated; if false, [FR-006] is removed and customers depend on the returns process. |
| A-10 | Failed refund initiations are retried 3 times before escalating to Finance. | Not stated; the retry count comes from [Q-03]. If a different count applies, [BR-009] and [FR-007] change with it. |
| A-11 | Fulfilment/warehouse must be told to stop picking a cancelled order. | Not stated; if cancellation and fulfilment are already coupled, [FR-008.AC2] is covered elsewhere. |
| A-12 | Cancelled orders release their reserved stock. | Not stated; if stock stays reserved, [BR-010] is void and overselling persists after cancellation. |
| A-13 | 2 s p95 confirmation and 60 s provider hand-off are the accepted targets. | Working values from [Q-05]; if the business sets different numbers, [NFR-001] and [NFR-002] change. |
| A-14 | Only the order owner or a support agent may cancel; every other account is refused. | Follows from [A-01]; if a shared-account or gift-purchase case exists, refusal needs an exception path. |
| A-15 | Cancellation and refund events are kept 7 years, readable by Finance and Compliance. | Not stated; if the retention period differs, [NFR-004] and its audit target change. |
| A-16 | Cancellation is reachable in 3 actions from the order list. | Not stated; if the flow needs more steps, [NFR-005] is dropped from this release. |

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | What volume of cancellation requests and what cost per request does the business see today, so the release can be judged? | Product owner | NFR-001, NFR-002 |
| Q-02 | Who maintains the cancellation reason list, and which values must be reportable from day one? | Operations lead | FR-004, BR-007 |
| Q-03 | How many refund retries are acceptable before Finance must intervene, and who watches the escalation queue? | Finance lead | FR-007 |
| Q-04 | Can a customer cancel part of an order — some lines but not others — or is cancellation always whole-order? | Product owner | FR-001, FR-003 |
| Q-05 | What arrival window may we promise per payment method, and what response time does the checkout path already meet? | Payments owner | NFR-001, NFR-002, FR-003 |
| Q-06 | Does the ticket reflect one complaint or a measured pattern, and does a legal cancellation right apply in the selling regions? | Compliance | all FRs for cancellation eligibility, BR-002 |

## Next step

Brainstorm the solution with this file as context.
