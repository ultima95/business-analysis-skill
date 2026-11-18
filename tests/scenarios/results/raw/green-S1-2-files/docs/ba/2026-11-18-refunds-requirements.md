# Refunds — Requirements

## Context

- Problem: the shop can decide whether an order may be returned, but it cannot give money back. `refunds.py:1` holds only the line `Refunds: not implemented`, so a return that is allowed today has no refund behind it.
- Why now: not stated in the request (`A-08`).
- Source input: requester instruction "Add refunds to our shop. There is existing order and return logic in the code — read it first so the refund rules match what is already there", the requester's follow-up answers on refund scope and approval, plus the existing source in `orders.py`, `refunds.py`, `test_orders.py`.
- Requested outcome: the refund behaviour worked out before any code — rules, exception cases, and everything still open.

## Actors and stakeholders

| Actor | Does / decides / is informed | Notes | Basis |
|---|---|---|---|
| Customer | Requests a full or partial refund on an order they received | Only actor the existing code models (`Order` has no customer field) | `orders.py:19-21`; requester statement that refunds are full or partial |
| Shop operator | Approves or refuses a refund of 5,000,000 VND or less | Approval step is not present in the code today | `A-03` |
| Finance approver | Approves or refuses a refund above 5,000,000 VND, after the operator | Named by the requester as a required step | Requester statement "Any refund over 5,000,000 VND needs a finance approval step"; `A-12` |
| Finance | Reconciles refunded amounts against captured amounts | Not present in the code today | `A-04` |
| Product owner | Answers the remaining scope and policy questions | Named as owner of every `Q-nn` | `Q-02` … `Q-10` |

## Scope

In scope:

- Refund eligibility for a delivered order, on the return window the code already enforces.
- Full and partial refunds against the amount captured for an order.
- Two-tier approval: operator always, finance above 5,000,000 VND.
- Payout back to the original payment method, with confirmation before the refund is recorded as paid.
- Exception paths: outside the window, not delivered, no delivery date, already refunded, over-refund, refused request, cancellations.

Out of scope:

- Recovering the physical goods and inspecting them after they arrive.
- Payment-provider integration mechanics.
- Changing the 30-day return window itself.
- Refunding a paid or shipped order that has not been delivered (see FR-008).

## Business rules

Recovered from the code today:

- **BR-001**: Only an order in the delivered state is eligible for a return, and so for a refund. Source: `orders.py:25`.
- **BR-002**: A delivered order with no delivery date recorded is not eligible. Source: `orders.py:27`.
- **BR-003**: The return window is 30 days; day 30 is inside the window and day 31 is outside it. Source: `orders.py:15`, `orders.py:29`, `test_orders.py:13-14`, `test_orders.py:21-22`.
- **BR-004**: The window is counted from the delivery date, not from the order date. Source: `orders.py:29`.
- **BR-005**: Orders in pending, paid, shipped, or cancelled state are not eligible for a return or a refund. Source: `orders.py:25`, `orders.py:7-12`.

Agreed in this analysis:

- **BR-006**: A refund is either full, for the whole refundable amount of the order, or partial, for less than it. Basis: requester statement "Refunds can be full or partial".
- **BR-007**: The total refunded for an order never exceeds the amount captured for that order, across all refunds on it. Basis: `A-02`; unconfirmed until `Q-06` is answered.
- **BR-008**: No refund leaves the shop without an operator decision recorded against it. Basis: `A-03`; unconfirmed until `Q-02` is answered.
- **BR-009**: A refund is requested within the same 30-day window that governs returns, counted from the delivery date. Basis: requester statement "only within whatever window the code already sets", which is [BR-003] and [BR-004].
- **BR-010**: A refund above 5,000,000 VND needs a finance approval after the operator approval; a refund of 5,000,000 VND or less does not. Basis: requester statement "Any refund over 5,000,000 VND needs a finance approval step"; the boundary at exactly 5,000,000 VND is `A-11`.
- **BR-011**: Every refund is paid back to the original payment method used for that order, and no other payout method is offered. Basis: requester statement "they always go back to the original payment method".
- **BR-012**: Every refund keeps its amount, its state, the deciding operator, the finance approver when one was required, and its change timestamps for as long as the record exists. Basis: `A-04`.

## Functional requirements

- **FR-001**: As a customer, I want to request a refund for an order I received, so that I get my money back when I no longer want the goods. Fulfils [BR-001], [BR-003], [BR-004], [BR-009]. Priority: Must.
- **FR-001.AC1**: Given an order delivered 12 days ago, When the customer submits a refund request, Then the request is recorded against that order and the order shows a refund in progress.
- **FR-001.AC2**: Given an order delivered 30 days ago, When the customer submits a refund request, Then the request is accepted and recorded.
- **FR-001.AC3**: Given an order delivered 31 days ago, When the customer submits a refund request, Then the request is refused and the refusal states that the 30-day window ended on day 30.
- **FR-002**: The system shall refuse a refund request for any order that is not in the delivered state. Fulfils [BR-001], [BR-005]. Priority: Must.
- **FR-002.AC1**: Given an order in paid state, When a refund request is submitted, Then the request is refused, recorded with the reason that the order was not delivered, and no refundable amount is reserved.
- **FR-002.AC2**: Given an order in shipped state, When a refund request is submitted, Then the request is refused and the refusal names the shipped state as the reason.
- **FR-002.AC3**: Given an order in delivered state, When the customer submits a refund request, Then the request is not refused by the state check.
- **FR-003**: The system shall refuse a refund request on a delivered order whose delivery date is missing. Fulfils [BR-002]. Priority: Must.
- **FR-003.AC1**: Given an order in delivered state with no delivery date, When a refund request is submitted, Then the request is refused and the missing delivery date is recorded as the reason.
- **FR-003.AC2**: Given a delivered order whose delivery date is later recorded, When the customer submits a refund request, Then the request is accepted if the delivery date is within 30 days of the request.
- **FR-004**: As a customer, I want to choose between a full refund and a partial amount, so that a partly disputed order does not force the whole amount back. Fulfils [BR-006], [BR-007]. Priority: Must.
- **FR-004.AC1**: Given an order with 100.00 captured and nothing refunded, When the customer requests 40.00, Then the refund is recorded at 40.00 and the remaining refundable amount is 60.00.
- **FR-004.AC2**: Given an order with 100.00 captured and nothing refunded, When the customer requests the full refundable amount, Then the refund is recorded for the whole 100.00 and the remaining refundable amount is 0.00.
- **FR-004.AC3**: Given an order with 100.00 captured and 40.00 already refunded, When the customer requests 70.00, Then the request is refused, the remaining refundable amount of 60.00 is shown, and no refund is recorded.
- **FR-005**: The system shall refuse any refund that would take the total refunded for an order above the amount captured for that order. Fulfils [BR-007]. Priority: Must.
- **FR-005.AC1**: Given an order with 100.00 captured and 100.00 refunded, When another refund request arrives for that order, Then it is refused and no further refund is recorded.
- **FR-005.AC2**: Given an order with 100.00 captured and 60.00 refunded, When a payout for the same 60.00 is submitted a second time, Then the second submission is refused and the total refunded stays at 60.00.
- **FR-006**: As a shop operator, I want to approve or refuse a pending refund with a recorded reason, so that money leaves only after a decision and the reason is auditable later. Fulfils [BR-008], [BR-012]. Priority: Must.
- **FR-006.AC1**: Given a pending refund request for 5,000,000 VND, When the operator approves it, Then the refund state becomes approved and the operator and decision time are recorded against it.
- **FR-006.AC2**: Given a pending refund request, When the operator refuses it with a reason, Then the refund state becomes refused and the reason is recorded against it.
- **FR-006.AC3**: Given a pending refund request, When the operator submits a refusal with no reason, Then the refusal is rejected and the refund stays pending.
- **FR-007**: As a finance approver, I want refunds above 5,000,000 VND to wait for my approval, so that large payouts are checked twice before they leave. Fulfils [BR-010]. Priority: Must.
- **FR-007.AC1**: Given a pending refund of 5,000,000 VND, When the operator approves it, Then no finance approval is required and the refund state becomes approved.
- **FR-007.AC2**: Given a pending refund of 5,000,001 VND, When the operator approves it, Then the refund state becomes awaiting finance approval and no payout is made.
- **FR-007.AC3**: Given a refund awaiting finance approval, When the finance approver approves it, Then the refund state becomes approved and both the operator and the finance approver are recorded against it.
- **FR-007.AC4**: Given a refund awaiting finance approval, When the finance approver refuses it with a reason, Then the refund state becomes refused and the reason is recorded against it.
- **FR-008**: As a customer, I want a refund to be paid back to the method I paid with, and only show as paid once the payout is confirmed, so that I am not told money has returned before it has. Fulfils [BR-011], [BR-012]. Priority: Must.
- **FR-008.AC1**: Given a refund in approved state, When the payout to the original payment method is confirmed, Then the refund state becomes paid and the confirmation time is recorded.
- **FR-008.AC2**: Given a refund in approved state, When no payout confirmation has arrived, Then the refund still shows approved and the order does not show the amount as returned.
- **FR-008.AC3**: Given an order paid by one method, When its refund is paid out, Then the payout goes to that same method and no alternative payout method is offered.
- **FR-009**: The system shall not refund a paid, pending, shipped, or cancelled order, so that a cancellation is never a route around the delivery rule. Fulfils [BR-005]. Priority: Won't.
- **FR-009.AC1**: Given an order in paid state, When the customer cancels it and asks for the money back, Then the cancellation is recorded and the refund request is refused with the paid state named as the reason.

## Non-functional requirements

| ID | Priority | Target | Basis |
|---|---|---|---|
| NFR-001 | Must | An eligibility decision is returned to the customer within 2 s at 50 concurrent refund requests | A-05 |
| NFR-002 | Must | 100% of refund state changes are written to an append-only log retained for 24 months | A-04, A-06 |
| NFR-003 | Should | Every refund amount is held and shown in VND with 2 decimal places, with 0 rounding differences across a 1,000-refund reconciliation | Requester statement of a 5,000,000 VND threshold; `A-07` |

- **NFR-001.AC1**: Given 50 concurrent refund requests, When each is submitted, Then each eligibility decision is returned within 2 s.
- **NFR-002.AC1**: Given 100 refund state changes in a day, When the day's log is read, Then all 100 changes are present with actor and timestamp.
- **NFR-003.AC1**: Given 1,000 refunds recorded over a month, When the total refunded per order is reconciled against captured amounts in VND, Then 0 orders differ by more than 0.00.

## Edge cases

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| Customer | pending, paid, shipped, cancelled | Refund refused, per [BR-005] and FR-009 | Remaining refundable amount not shown | Not allowed | Not allowed |
| Customer | delivered, inside 30 days | Request recorded (FR-001) | Sees refund state and remaining refundable amount | Cannot change amount after a decision | Cannot delete a request (NFR-002) |
| Customer | delivered, day 30 | Request accepted (FR-001.AC2) | — | — | — |
| Customer | delivered, day 31 | Request refused (FR-001.AC3) | — | — | — |
| Customer | delivered, delivery date missing | Request refused (FR-003.AC1) | — | — | — |
| Customer | delivered, partly refunded | Second partial request accepted while refundable amount stays above 0.00 (FR-004.AC1) | Sees reduced remaining amount | — | — |
| Customer | fully refunded | Second request refused (FR-005.AC1) | Sees 0.00 remaining | — | — |
| Operator | pending refund at 5,000,000 VND | — | Sees request with amount and order | Approves or refuses with reason; approval is final (FR-006, FR-007.AC1) | — |
| Operator | pending refund above 5,000,000 VND | — | Sees request with amount and order | Approves or refuses with reason; approval moves it to awaiting finance approval (FR-007.AC2) | — |
| Finance approver | awaiting finance approval | — | Sees amount, order, and operator decision | Approves or refuses with reason (FR-007.AC3, FR-007.AC4) | — |
| Finance approver | any refund of 5,000,000 VND or less | — | Sees it only if the operator escalated it | Cannot approve or refuse | — |
| Finance | paid refund | — | Reconciles against captured amount (NFR-003) | — | — |
| Finance | refused refund | — | Sees refusal reason and refuser | — | — |

## Glossary

| Term | Meaning |
|---|---|
| Order | A purchase tracked by its state: pending, paid, shipped, delivered, cancelled. |
| Return | The goods coming back; the code decides today whether this is allowed. |
| Return window | The 30 days after delivery during which a return is allowed, day 30 included. |
| Refund | Money given back against an order; this document defines it, the code does not have it. |
| Full refund | A refund for the whole refundable amount of the order. |
| Partial refund | A refund for less than the refundable amount. |
| Captured amount | The money actually taken for an order, which refunds are measured against. |
| Refundable amount | Captured amount minus everything already refunded on that order. |
| Refund state | Where a refund stands: requested, approved, awaiting finance approval, refused, or paid. |
| Operator | The shop-side person who approves or refuses a refund of 5,000,000 VND or less. |
| Finance approver | The shop-side person whose approval a refund above 5,000,000 VND needs before payout. |
| Original payment method | The method used to pay for that order; the only place its refund may be sent. |
| VND | Vietnamese dong, the currency the refund amounts are held and shown in. |

## Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-02 | Every order carries one captured amount that refunds are measured against. | No amount field exists on `Order` in `orders.py:19-21`; if false FR-004, FR-005, FR-006 and NFR-003 have nothing to compute against. |
| A-03 | The operator approval step applies to every refund, with finance added above the threshold. | Requester named finance approval only for refunds above 5,000,000 VND and never said who approves below it; if false FR-006 loses its actor and refunds auto-approve. |
| A-04 | A refund record keeps amount, state, deciding operator, finance approver, and change timestamps. | Not stated; if false finance cannot reconcile and NFR-002 loses its actor field. |
| A-05 | 2 s at 50 concurrent requests is an acceptable eligibility target. | Working value, no volume in the input; if false NFR-001 is re-targeted. |
| A-06 | Refund history is kept for 24 months. | Working value, no retention policy in the input; if false NFR-002 changes and closed-period reconciliation breaks. |
| A-07 | Amounts are held and shown in VND with 2 decimal places, and every order is captured in VND. | The 5,000,000 VND threshold implies VND; if orders are captured in another currency NFR-003 and the threshold comparison both need a conversion rule. |
| A-08 | The urgency behind this work is not stated and is not needed to state the rules. | Request gives no deadline; if a deadline exists it may cut the partial-refund split from the first release. |
| A-09 | One order may carry several partial refunds until its refundable amount reaches 0.00. | "Refunds can be full or partial" implies accumulation but not repeat requests; if false FR-004 and FR-005 collapse into one refund per order. |
| A-10 | A refused refund may be requested again while the order is still inside the 30-day window. | Not stated; if false FR-001 needs a cap on attempts and a terminal refused state. |
| A-11 | Exactly 5,000,000 VND is below the finance threshold, because the requester wrote "over 5,000,000 VND". | Requester wording; if the threshold is inclusive, FR-007.AC1 and FR-007.AC2 swap at the boundary and the comparison moves from `>` to `>=`. |
| A-12 | A finance approver role exists and is separate from the shop operator. | Requester named a finance approval step without naming who holds it; if false the operator carries both approvals and FR-007 collapses into FR-006. |

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-02 | May any shop operator approve a refund of 5,000,000 VND or less, or only named roles, and may an operator approve their own request? | Product owner | FR-006, BR-008 |
| Q-04 | Is the refund requested at the moment of the return request, or only after the goods arrive back and are inspected? | Product owner | FR-001, BR-009 |
| Q-05 | Are shipping fees and any other charges refunded along with the goods amount, and does that change the captured amount used for the threshold? | Product owner | FR-004, FR-007 |
| Q-06 | Where does the captured amount for an order come from, since `orders.py:19-21` stores no amount? | Product owner and engineering lead | FR-004, FR-005, FR-006, NFR-003 |
| Q-07 | How many days after approval must the payout be confirmed before a refund awaiting payout is escalated? | Finance lead | FR-008, NFR-002 |
| Q-08 | What happens to a refund in progress when the order's state changes underneath it, given `orders.py:25` allows only delivered orders? | Product owner | FR-002, FR-005 |
| Q-09 | Are orders ever captured in a currency other than VND, and who owns the conversion when comparing against the 5,000,000 VND threshold? | Finance lead | NFR-003, FR-007 |
| Q-10 | Is the 5,000,000 VND threshold measured per refund request or against the total refunded for the order, so that three 2,000,000 VND refunds on one order need finance approval or not? | Finance lead | FR-007, BR-010 |

## Next step

Brainstorm the solution with this file as context.
