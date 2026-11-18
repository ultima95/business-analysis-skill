# Order Cancellation After Payment — Requirements

## Context

- Problem: "Customers can't cancel orders after payment." — ticket text quoted verbatim; no ticket ID, reporter, or attachment was supplied.
- Source input: one-line ticket: `"Customers can't cancel orders after payment."` The ticket names no deadline, incident, or cost, so no urgency is asserted here.
- Repository state: at analysis time the repository holds no application code (git history contains a single empty commit). No current rules could therefore be recovered from source, and the "Rules recovered from code" section is dropped rather than filled from guesswork. Every rule below derives from the ticket plus the assumptions register.

## Actors and stakeholders

| Actor | Does / decides / is informed | Notes | Basis |
|---|---|---|---|
| Customer (order owner) | Triggers the cancellation, receives the outcome and the refund status | The only actor named in the ticket | Ticket |
| Support agent | Cancels on a customer's behalf; explains why a request cannot be honoured | Agent-initiated cancellation is not mentioned in the ticket | A-08, Q-08 |
| Finance team | Investigates and resolves refund failures | Needed only because a refund can fail after the cancellation stands | A-11, Q-09 |
| Fulfilment team | Advances the order through picking, packing, and handing to the carrier | The moment of handing to the carrier is what ends cancellability | A-10, Q-02 |
| Payment provider | Executes void or refund against the original payment | External party; its capability set bounds the rule in BR-003 | A-03, Q-06 |
| Legal / compliance | Owns withdrawal rights and record-retention obligations | Not mentioned in the ticket | Q-07, Q-10 |

## Scope

In scope:

- Cancellation of a paid order, or of part of one, while the order has not been handed to the carrier.
- The decision on whether a given order or line item may be cancelled, and the explanation given when it may not.
- Refund of the amount captured for the cancelled items, and the record of that refund.
- Release of the stock reservation held for the cancelled items.
- The hand-off point to the return path that applies once the order is handed to the carrier.

Out of scope:

- The post-delivery return and exchange process itself (A-10). Only the hand-off into it is in scope.
- Changing how payments are captured, authorised, or reconciled.
- Pricing, discount, and tax recalculation beyond stating the refunded amount.
- Any statement about screens, technology, or data model — solution design belongs to the next stage.

## Business rules

- **BR-001**: A cancellation is permitted only while fulfilment state is `Unfulfilled` or `Packed, not yet handed over`; at `Handed to carrier` and `Delivered` the request is refused as a cancellation. The payment state selects the mechanism, not the permission, per the decision table below.
- **BR-002**: Partial cancellation is allowed at line-item granularity only before the order is handed to the carrier; the uncancelled lines keep their original order state and ship as planned.
- **BR-003**: When payment is authorised but not captured, cancellation voids the authorisation; when payment is captured, cancellation refunds the captured amount for the cancelled items.
- **BR-004**: A line item flagged non-cancellable is never cancelled; a cancellation request covering it cancels only the cancellable lines and leaves the flagged lines in the order.
- **BR-005**: A cancelled order, or a cancelled line, is terminal: it cannot be reactivated, resumed, or un-cancelled. A new order is the only way to buy the items again.
- **BR-006**: The refunded amount for a full cancellation equals the amount captured for that order; for a partial cancellation it equals the captured amount attributable to the cancelled lines. No cancellation fee is deducted (A-04, Q-05).
- **BR-007**: Only the order owner, or a support agent holding the cancel permission, may cancel an order. Any other requester is refused.
- **BR-008**: A successful cancellation releases the stock reservation held for the cancelled items before the order leaves the picking queue.
- **BR-009**: Every cancellation records the requester, the actor who performed it, the reason, the timestamp, the cancelled lines, and the refunded amount.
- **BR-010**: A failed refund does not reverse the cancellation: the order stays cancelled and the failure is raised to the finance team as an open item (A-11, Q-09).
- **BR-011**: Elapsed time since payment does not by itself make an order non-cancellable; only fulfilment state does (Q-07 governs any legally required window).

### Eligibility decision table (BR-001)

| Condition / outcome | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| Payment captured | Y | Y | Y | Y | N |
| Fulfilment state | Unfulfilled | Packed, not yet handed over | Handed to carrier | Delivered | Unfulfilled |
| All requested lines cancellable | Y | Y | – | – | Y |
| Outcome | Cancel and refund | Cancel and refund | Refuse; offer the return path | Refuse; offer the return path | Cancel and void the authorisation |

## Functional requirements

- **FR-001**: As a customer, I want to cancel my paid order while it has not been handed to the carrier, so that I am not charged for goods I no longer want. Fulfils [BR-001], [BR-011]. Priority: Must.
- **FR-001.AC1**: Given a captured payment and fulfilment state `Unfulfilled`, When I request cancellation of the whole order, Then the order state becomes `Cancelled` and the cancellation reference is shown to me.
- **FR-001.AC2**: Given fulfilment state `Handed to carrier`, When I request cancellation, Then the request is refused and I am told the order has left the warehouse.
- **FR-001.AC3**: Given an order already in state `Cancelled`, When I request cancellation again, Then the request is refused as already cancelled and the original cancellation reference is shown.
- **FR-001.AC4**: Given fulfilment state `Unfulfilled` and a payment captured 90 days earlier, When I request cancellation, Then the cancellation is accepted.

- **FR-002**: As a customer, I want to be told the specific reason when cancellation is not possible, so that I know which alternative applies to me. Fulfils [BR-001]. Priority: Must.
- **FR-002.AC1**: Given an order at `Handed to carrier`, When I open the cancellation option, Then the recorded reason names the handover to the carrier and points to the return path.
- **FR-002.AC2**: Given an order whose lines are all flagged non-cancellable, When I attempt cancellation, Then the recorded reason names the non-cancellable lines.
- **FR-002.AC3**: Given I am not the order owner and hold no cancel permission, When I attempt cancellation, Then the request is refused and the reason given to me does not reveal the order's contents (BR-007).

- **FR-003**: As a customer, I want to cancel individual line items of an unshipped order, so that I keep the items I still want. Fulfils [BR-002], [BR-006]. Priority: Should.
- **FR-003.AC1**: Given an order with three lines at `Unfulfilled`, When I cancel two of them, Then the two lines become `Cancelled`, the third stays `Unfulfilled`, and the refund covers only the two.
- **FR-003.AC2**: Given the same order, When I cancel two of three lines, Then the remaining line still ships with its original delivery address.
- **FR-003.AC3**: Given every line has been cancelled individually, When the last line is cancelled, Then the whole order state becomes `Cancelled`.

- **FR-004**: The system shall refuse cancellation once an order is handed to the carrier and record the request as an inbound return instead. Fulfils [BR-001]. Priority: Must.
- **FR-004.AC1**: Given fulfilment state changes to `Handed to carrier` while a cancellation request is open, When the request is assessed, Then it is refused and the hand-off record names the return path.
- **FR-004.AC2**: Given a request refused because the order was handed to the carrier, When the customer contacts the return path, Then the original order reference is carried into that request.

- **FR-005**: The system shall compute and submit the refund for the cancelled lines, using void before capture and refund after capture, and record the amount submitted. Fulfils [BR-003], [BR-006]. Priority: Must.
- **FR-005.AC1**: Given a captured amount of 500 and a full cancellation, When the cancellation completes, Then a refund of 500 is submitted to the original payment method and recorded.
- **FR-005.AC2**: Given an authorised but uncaptured payment, When the cancellation completes, Then the authorisation is voided and no refund is submitted.
- **FR-005.AC3**: Given a partial cancellation of two lines worth 200, When the cancellation completes, Then the refund submitted is 200.
- **FR-005.AC4**: Given a refund submission that the payment provider rejects, When the rejection is received, Then the cancellation still stands and an open finance item is created (BR-010).

- **FR-006**: As a customer, I want non-cancellable items excluded from the cancellation instead of blocking it, so that I can still cancel the rest. Fulfils [BR-004]. Priority: Must.
- **FR-006.AC1**: Given an order with one flagged line and two cancellable lines, When I cancel the whole order, Then only the two cancellable lines are cancelled and the flagged line remains.
- **FR-006.AC2**: Given the same order, When the cancellation completes, Then I am told which lines could not be cancelled and why.
- **FR-006.AC3**: Given an order whose only line is flagged non-cancellable, When I request cancellation, Then no line is cancelled and the order keeps its current state.

- **FR-007**: As a support agent, I want to cancel an order on a customer's behalf, so that I can resolve a request received outside the self-service path. Fulfils [BR-007], [BR-009]. Priority: Should.
- **FR-007.AC1**: Given I hold the cancel permission and the customer asks by another channel, When I cancel the order, Then the order becomes `Cancelled` and my identity is recorded as the actor.
- **FR-007.AC2**: Given I hold the cancel permission, When I attempt to cancel an order, Then the order's owner is recorded as the requester and I am recorded as the actor.
- **FR-007.AC3**: Given I do not hold the cancel permission, When I attempt to cancel the order, Then the attempt is refused and logged.

- **FR-008**: The system shall release the stock reservation for cancelled lines at the moment the cancellation commits. Fulfils [BR-008]. Priority: Must.
- **FR-008.AC1**: Given two reserved units for a cancelled line, When the cancellation commits, Then both reservations are released and available to other orders.
- **FR-008.AC2**: Given a line already picked and packed, When its cancellation commits, Then the released units are recorded against that location and the release is visible to the fulfilment team.

- **FR-009**: The system shall record the requester, the performing actor, the reason, the timestamp, the cancelled lines, and the refunded amount for every cancellation. Fulfils [BR-009]. Priority: Must.
- **FR-009.AC1**: Given a completed cancellation, When an auditor reads the record, Then all six fields are present.
- **FR-009.AC2**: Given an agent-initiated cancellation, When the record is read, Then requester and performing actor differ and both are named.
- **FR-009.AC3**: Given a cancellation that produced no refund, When the record is read, Then the refunded amount reads zero rather than blank.

- **FR-010**: The system shall treat a repeated cancellation request for the same order as the original cancellation, so that no second refund is submitted. Fulfils [BR-005]. Priority: Should.
- **FR-010.AC1**: Given a completed cancellation, When the same request is submitted twice within one minute, Then one cancellation record exists and the second submission returns the original reference.
- **FR-010.AC2**: Given two requests for the same order arriving at the same moment, When both are processed, Then exactly one refund is submitted.

- **FR-011**: The system shall keep a cancelled order cancelled when its refund fails and shall raise the failure to the finance team with the amount and the failed attempt. Fulfils [BR-010]. Priority: Must.
- **FR-011.AC1**: Given a rejected refund, When the rejection is processed, Then an open finance item exists naming the order, the amount, and the rejection reason.
- **FR-011.AC2**: Given an open finance item, When finance submits the refund again successfully, Then the item closes and the order record shows the refunded amount.
- **FR-011.AC3**: Given a refund still failing, When the customer checks the order, Then the order reads `Cancelled` with refund status `Pending`, not `Failed order`.

- **FR-012**: As a customer, I want confirmation of the cancellation and of the refund state, so that I know what to expect and when. Fulfils [BR-006]. Priority: Must.
- **FR-012.AC1**: Given a completed cancellation, When I view the order, Then I see the cancelled state, the cancelled lines, and the refunded amount.
- **FR-012.AC2**: Given a refund pending with the provider, When I view the order, Then the refund status reads `Pending` and names the original payment method.
- **FR-012.AC3**: Given a refund fails and is later completed by finance, When I view the order, Then the refund status reads `Completed` without needing a new cancellation.

## Non-functional requirements

| ID | Priority | Target | Basis |
|---|---|---|---|
| NFR-001 | Must | Cancellation eligibility decision returned within 2 s at the 95th percentile under the peak order load | A-12, Q-12 |
| NFR-002 | Must | Self-service cancellation available 99.5% of each calendar month | A-12, Q-12 |
| NFR-003 | Must | 100% of cancellation attempts by a requester who is neither owner nor permitted agent are refused; 0 accepted in the authorisation test suite | BR-007 |
| NFR-004 | Must | Cancellation and refund records retained for 7 years after the order's final state | A-12, Q-10 |
| NFR-005 | Must | 0 occurrences of another customer's order, address, or payment detail in any cancellation confirmation or eligibility reason | BR-007 |
| NFR-006 | Should | A cancellation completed in at most 3 customer actions from the order page | A-12, Q-12 |
| NFR-007 | Must | Refund submitted to the payment provider within 5 minutes of the cancellation commit at the 95th percentile | A-12, Q-12 |

- **NFR-001.AC1**: Given peak order load, When 95 of 100 eligibility checks are measured, Then each returns within 2 s.
- **NFR-002.AC1**: Given one calendar month, When cancellation is attempted at any hour, Then the service responds on at least 99.5% of attempts.
- **NFR-003.AC1**: Given a requester who is not the owner and holds no cancel permission, When cancellation is attempted for 100 orders, Then 0 attempts succeed and 100 are recorded as refused.
- **NFR-004.AC1**: Given a cancellation completed 7 years ago, When the record is queried, Then the record and its refund amount are returned.
- **NFR-005.AC1**: Given a cancellation for customer A, When the confirmation is rendered, Then no field carries customer B's order, address, or payment detail.
- **NFR-006.AC1**: Given an order eligible for cancellation, When a customer cancels it, Then at most 3 actions are recorded between opening the order and the confirmed cancellation.
- **NFR-007.AC1**: Given 100 completed cancellations, When the refund submissions are measured, Then at least 95 are submitted within 5 minutes of their cancellation commit.

## Edge cases

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| Order owner | Awaiting payment | Cancellation not needed; abandonment applies | Order visible | Not applicable | Not applicable |
| Order owner | Paid, `Unfulfilled` | Cancellation accepted (FR-001) | Refund amount shown | Order becomes `Cancelled` | Not applicable |
| Order owner | `Packed, not yet handed over` | Cancellation accepted, warehouse must be told to pull the parcel (FR-001) | Cancelled lines shown | State becomes `Cancelled` | Not applicable |
| Order owner | `Handed to carrier` | Refused as cancellation; return path offered (FR-004) | Refusal reason shown | No change | Not applicable |
| Order owner | `Delivered` | Refused; return path offered | Refusal reason shown | No change | Not applicable |
| Order owner | Partially cancelled | Further cancellation of remaining lines accepted (FR-003) | Both cancelled and open lines shown | Remaining lines unchanged | Not applicable |
| Order owner | `Cancelled` | Repeat request returns original reference (FR-010) | Cancellation and refund status shown | No reactivation (BR-005) | Not applicable |
| Order owner | Refund failed | Cancellation stands (FR-011) | Status `Pending` with reason shown | No new cancellation accepted | Not applicable |
| Other customer | Any paid state | Refused, order details not revealed (NFR-005) | Order not visible | Refused | Not applicable |
| Support agent, permitted | Any cancellable state | Accepted, actor recorded (FR-007) | Full order and prior cancellations visible | Accepted within permission | Not applicable |
| Support agent, not permitted | Any state | Refused and logged (FR-007.AC3) | Read-only view | Refused | Not applicable |
| Finance team | Refund failed | Re-submits refund (FR-011.AC2) | Refund attempt history visible | Closes the open item | Not applicable |
| Fulfilment team | `Packed` after cancellation | Must pull the parcel from the outbound flow (FR-008.AC2) | Cancellation flag visible | Marks the parcel pulled | Not applicable |

## Glossary

| Term | Meaning |
|---|---|
| Authorised (payment) | The payment provider has reserved the funds but the merchant has not yet taken them. |
| Captured (payment) | The merchant has taken the funds; reversing it requires a refund, not a void. |
| Cancellation | The customer-initiated ending of an order or line before it is handed to the carrier, which triggers refund or void. |
| Handed to carrier | The moment the parcel passes to the delivery provider; the last point at which cancellation is possible. Prose uses this phrase; `Packed, not yet handed over` is a state name quoted as written. |
| Line item | One product quantity within an order; the smallest unit that can be cancelled separately. |
| Non-cancellable | A line flagged by merchandising policy as excluded from cancellation (Q-03). |
| Refund | Return of captured funds to the original payment method. |
| Return | The post-delivery path for goods already received; out of scope except for its entry point. |
| Void | Cancellation of an authorisation before capture, so no funds are taken. |

## Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | No cancellation path exists today once payment is taken; the ticket asks for one to be added. | Ticket wording "can't cancel"; if a path exists but is unusable, the work becomes a fix to an existing path and FR-001 shrinks. |
| A-02 | The order owner is the account that placed the order. | Not stated; if orders can be placed for another person, BR-007 gains a delegate role. |
| A-03 | Refunds go back to the original payment method. | Not stated; if store credit is offered, FR-005 gains a payout-method step. |
| A-04 | No cancellation fee is deducted from the refund. | Not stated; a fee changes BR-006 and FR-005.AC1. |
| A-05 | Partial cancellation is available only before the order is handed to the carrier. | Follows BR-001; if allowed after that point, FR-003 expands to shipped lines. |
| A-06 | Stock reservations are released automatically on cancellation. | Not stated; if release is manual, FR-008 becomes an operational task with an owner and a time limit. |
| A-07 | Refund submission is automatic on cancellation, with no approval step. | Not stated; an approval step adds a queue and changes NFR-007. |
| A-08 | Support agents hold the cancel permission by default, with no amount threshold. | Not stated; a threshold changes FR-007 and adds an approval path (Q-08). |
| A-09 | Each product carries a cancellable flag that already expresses merchandising policy. | Not stated; if policy is decided per order, FR-006 needs a decision step instead of a flag. |
| A-10 | A returns process exists for orders already handed to the carrier. | Not stated; if none exists, FR-004's hand-off has no destination and must be scoped separately. |
| A-11 | The finance team owns refund failures. | Not stated; another owner changes FR-011 and BR-010. |
| A-12 | All numeric targets in the NFR table are working values for this draft. | Not supplied by the ticket; confirm or replace via Q-12 before commitment. |

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | Does "after payment" mean after capture only, or also after authorisation without capture? | Product owner | FR-001, FR-005 |
| Q-02 | Which fulfilment states must block cancellation — only the handover to the carrier, or already picking and packing? | Fulfilment lead | FR-001, FR-002 |
| Q-03 | Which product categories are non-cancellable, and where is that policy written down? | Merchandising lead | FR-006, FR-001 |
| Q-04 | May a customer cancel the remaining lines after part of the order has been handed to the carrier? | Fulfilment lead | FR-003 |
| Q-05 | Is a cancellation fee ever charged, and if so on which cancellations? | Finance lead | FR-005 |
| Q-06 | Is a refund to the original payment method the only option, or is store credit offered as a choice? | Finance lead | FR-005, FR-012 |
| Q-07 | Which consumer-withdrawal regime applies, and does it set a window after which cancellation must be refused? | Legal | FR-001, FR-004 |
| Q-08 | What approval threshold, if any, applies to agent-initiated cancellations? | Support operations lead | FR-007 |
| Q-09 | Who owns a failed refund, and within what time must it be resolved? | Finance lead | FR-011 |
| Q-10 | How long must cancellation and refund records be retained? | Legal / compliance | NFR-004 |
| Q-11 | Is a cancellation reason mandatory for the customer, or only for agents? | Support operations lead | FR-009 |
| Q-12 | What target values apply to cancellation response time, availability, step count, and refund submission delay? | Product owner | NFR-001, NFR-002, NFR-006, NFR-007 |

## Next step

Brainstorm the solution with this file as context, then turn the chosen approach into a plan. Two decisions gate most of the build: Q-01 (what "after payment" covers) and Q-02 (which fulfilment state ends cancellability).
