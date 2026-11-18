# Requirements: Customer-Initiated Order Cancellation After Payment

Status: Draft for review
Owner: Product (TBD)
Related systems: Storefront, Orders API, Payments/Refunds, Fulfillment (WMS), Notifications

---

## 1. Problem statement

Customers can place and pay for an order but have no supported way to cancel it
afterwards. Today the only paths are (a) contact support and hope an agent can
stop it manually, or (b) refuse delivery / return the goods after they arrive.
Both are expensive, slow, and opaque to the customer.

Support tickets show two distinct failures:

1. **No capability** – the customer-facing account page shows no cancel action
   once payment succeeds, and the Orders API rejects state transitions out of
   `paid`.
2. **No trustworthy outcome** – even when support does intervene, the customer
   receives no confirmation of whether the cancellation actually took effect
   (order stopped, money refunded) or whether the item simply shipped anyway.

The business cost is avoidable refunds on shipped goods, avoidable support
volume, and a measurable drop in repeat purchase rate for customers who
experience a failed cancellation attempt.

## 2. Goal and success criteria

**Goal:** A customer can cancel any part of an order that has not yet been
handed to the carrier, with a clear, immediate, and truthful answer about what
was cancelled and what money is being returned.

Success is measured on:

| Metric | Target |
| --- | --- |
| Share of eligible (unshipped, paid) orders cancelled self-service | ≥ 80% |
| Cancellation requests resolved without a support ticket | ≥ 95% |
| Refund issued within 60s of confirmed cancellation | ≥ 99% |
| Orders cancelled after handoff to carrier (i.e. we said yes, then shipped) | < 0.1% |
| Support contacts tagged "cannot cancel order" | −90% vs. baseline |

## 3. Scope

### In scope

- Cancellation of a paid order, in whole or in part (line-item level), before
  fulfillment handoff.
- Automatic refund of the cancelled amount to the original payment method.
- Customer-facing status, confirmation, and notification.
- Support-agent path to cancel on a customer's behalf using the same mechanism.
- Audit trail of who cancelled what, when, and why.

### Out of scope

- Returns / exchanges after goods leave the warehouse. Cancellation is not a
  return; a separate returns flow handles post-handoff cases and this document
  only requires that the customer be routed to it.
- Chargeback and dispute handling.
- Cancellation by the merchant for fraud, stock, or pricing reasons (existing
  merchant-side flow; it must remain compatible, but is not redesigned here).
- Subscription cancellation.
- Store credit, gift-card reissue, or any refund destination other than the
  original payment method.

## 4. Users and permissions

| Actor | May cancel |
| --- | --- |
| Authenticated customer who owns the order | Own orders only |
| Guest customer with order access token (order confirmation link) | That single order |
| Support agent | Any order, requires reason code, is audited |
| Automated system (merchant-side) | Not via this flow |

Customers must never be able to cancel another customer's order. Object-level
authorization is required on every endpoint; "not found" and "not yours" must
be indistinguishable in the response to avoid order enumeration.

## 5. Current-state assumptions

These are asserted because the ticket is thin; each must be validated against
the actual implementation before build starts. See §12.

- An order exists in a state machine that includes at minimum: `pending_payment`,
  `paid`, `fulfilling`/`picking`, `shipped`/`handed_off`, `delivered`,
  `cancelled`, `refunded`, `partially_refunded`.
- Payment is captured synchronously at checkout for most orders, but an
  authorization-only mode exists or may be introduced.
- A payment service provider (PSP) exposes a refund API and asynchronous refund
  webhooks; refunds are not guaranteed to be synchronous.
- A fulfillment system receives order lines and acknowledges picking/packing,
  but does not currently guarantee "cancel before ship" semantics.
- Line-level tax, discount, and shipping allocations are stored, or can be
  computed, per order line.

## 6. Functional requirements

### 6.1 Eligibility

**FR-1** An order is *cancellable* when all of the following hold:

- Payment is captured, or authorized but not captured.
- No line on the order has reached `handed_off` (carrier scan / dispatch)
  state in fulfillment.
- The order is not already fully cancelled or fully refunded.

**FR-2** Eligibility is evaluated per line item, not only per order. Lines that
remain unshipped are cancellable even when other lines on the same order have
shipped; the order then becomes `partially_cancelled`.

**FR-3** Any time-based cancellation window is a policy value, not a hard-coded
constant. Default policy: no time limit while the order is unshipped. Policy
must be overridable per product category (for example, made-to-order or
customized goods may be non-cancellable once production starts).

**FR-4** The customer-facing order page must show, for every order, either an
enabled cancel action or a specific reason it is unavailable ("already
shipped", "custom item — contact support", "already cancelled"). A bare missing
button is not acceptable.

### 6.2 Cancellation request

**FR-5** The customer can cancel the whole remaining unshipped portion of an
order, or select individual unshipped line items with quantities.

**FR-6** The system must re-check eligibility at the moment the request is
submitted, not only when the page was rendered.

**FR-7** Requests must be idempotent. Retries, double-clicks, and duplicate
network submissions must not produce a second cancellation or a second refund.
Clients send an idempotency key; the server deduplicates on it.

**FR-8** A cancellation request transitions the affected lines to a pending
cancellation state immediately, and the UI must show that state rather than
claiming the cancellation is complete. Terminal states are `cancelled` (and
refund may still be in flight) and `cancellation_failed`.

**FR-9** Cancellation is irreversible. The UI must make this explicit before
confirmation and must not offer "undo".

**FR-10** A reason is optional for customers and mandatory for support agents
(reason code from a fixed list plus free text).

### 6.3 Interaction with fulfillment (race conditions)

**FR-11** On acceptance, the system must notify fulfillment to stop work on the
affected lines and must receive an acknowledgement before the cancellation is
reported as confirmed.

**FR-12** If fulfillment reports that a line shipped between the eligibility
check and the cancellation, that line moves to `cancellation_failed`, the
customer is told plainly that the item is on its way, and they are offered the
post-handoff return path. No refund is issued for that line.

**FR-13** The system must prefer failing a cancellation over shipping a
cancelled item. Where the fulfillment integration supports it, a cancel request
must be able to block dispatch until resolved.

**FR-14** Fulfillment responses that time out must not leave a line in an
indeterminate state visible to the customer for more than 30 seconds; the
system reconciles asynchronously and notifies the customer of the final
outcome either way.

### 6.4 Money and refunds

**FR-15** The refund amount for a cancelled line is exactly what the customer
paid for that line, including its allocated tax, plus its share of any
order-level discounts and shipping, computed by the same allocation rules used
at checkout. Rounding must be deterministic and must never exceed the captured
amount.

**FR-16** Refunds are issued to the original payment method only, via the PSP,
automatically. No manual step is required in the happy path.

**FR-17** Refund progress is a first-class state visible to the customer:
`refund_pending` → `refund_initiated` → `refund_succeeded` /
`refund_failed`. The vocabulary should reflect that the PSP, not the merchant,
controls the final settlement timing.

**FR-18** A failed refund must not be silently swallowed. It must: raise an
alert to the payments on-call, appear in an operations queue for reconciliation,
and tell the customer that the refund is delayed — with a support route — rather
than falsely reporting success.

**FR-19** Refunds must reconcile against PSP webhooks. The system must treat the
webhook as authoritative for terminal refund status and must be tolerant of
out-of-order and duplicate webhook deliveries.

**FR-20** The system must never refund more than the order's total captured
amount, across all refills, partial cancellations, and returns. A running
refundable balance is enforced server-side.

**FR-21** For authorization-only payments, cancellation must void the
authorization rather than refund it. The customer must see "authorization
cancelled — you were not charged" instead of a refund message.

**FR-22** A configurable, policy-driven cancellation fee must be supported but
must default to zero, and if non-zero must be shown as a distinct line ("fee")
before confirmation, never silently netted out of the refund.

### 6.5 Communication

**FR-23** On confirmed cancellation, the customer receives an email (and any
enabled push/SMS channel) containing: what was cancelled, the refund amount,
the refund destination (card ending / last known payment label), and the
expected settlement window.

**FR-24** On `cancellation_failed` or `refund_failed`, a separate notification
is sent that names the failure and the next step.

**FR-25** Order confirmation emails, invoices, and shipment notifications must
reflect the cancelled state and refunded amounts; a customer must not receive a
"your order has shipped" message for a line that was successfully cancelled.

### 6.6 Support tooling and audit

**FR-26** Support agents must be able to cancel through the existing admin
surface using the same service path as customers — no parallel manual refund
process.

**FR-27** Every cancellation records: order id, affected lines and quantities,
actor (customer / guest token / agent id), reason code, timestamp, eligibility
snapshot at request time, refund ids, and final outcome. Records are
append-only and retained per the finance retention policy.

## 7. Non-functional requirements

- **Consistency:** the order's cancellable state and its refund balance are
  enforced by a single transactional service boundary; no client-side
  computation is trusted.
- **Latency:** an eligibility check returns in < 300 ms p95; an accepted
  cancellation acknowledges to the UI in < 500 ms p95 (the confirmation of
  fulfillment stop is asynchronous and may take longer).
- **Idempotency & concurrency:** concurrent cancel requests for the same line
  resolve to exactly one cancellation and one refund. Correctness under
  concurrency is a tested requirement, not a best effort.
- **Security:** object-level authorization on every endpoint; CSRF protection;
  no order data in URLs beyond a non-guessable token; all state transitions
  logged.
- **Accessibility:** the cancel flow, including the confirmation dialog and
  status states, meets WCAG 2.2 AA.
- **Localization:** refund amounts, dates, and settlement windows are
  locale- and currency-formatted; the settlement window text is translatable
  and not hard-coded per country.
- **Observability:** metrics for cancellation attempts, outcomes by reason,
  fulfillment race losses, refund latencies, and refund failures; distributed
  traces spanning storefront → orders → PSP.
- **Backward compatibility:** existing merchant-initiated cancellation and
  refund APIs keep their current contracts.

## 8. Key user flows (required behaviour)

**Happy path**
A customer opens a paid, unshipped order, chooses "Cancel order", confirms the
amount and destination, and sees "Cancelling…". Within the acknowledgement
window the order shows `Cancelled`, the refund shows `Initiated`, and an email
follows. Refund later settles and the order shows `Refunded`.

**Partial cancellation**
Order has three lines. One has shipped. Customer cancels the other two. The
order shows `Partially cancelled`; the shipped line remains with its tracking
number; refund equals the two cancelled lines including their allocated tax and
shipping share.

**Race with fulfillment**
Customer cancels; the warehouse scanned the parcel seconds earlier. The line
reports `Cancellation failed — shipped`, no refund is issued, and the return
path is offered with a one-click link.

**Refund failure**
PSP rejects the refund (expired card, unsupported method). Order stays
`Cancelled`, refund shows `Failed`, customer sees a delayed-refund message with
a support route, and the case enters the operations queue.

## 9. Acceptance criteria

1. A paid, unshipped order exposes a working cancel action to its owner; a
   shipped order does not, and states why.
2. Submitting a cancel twice produces one cancellation and one refund.
3. A cancelled unshipped line is never dispatched by fulfillment; if it already
   was, the customer is told so and refunded nothing for that line.
4. The refunded amount equals the line's paid amount including allocations, and
   the sum of all refunds for an order never exceeds the captured total.
5. Refund state changes are driven by PSP webhooks and survive duplicate and
   out-of-order deliveries.
6. A customer cannot cancel an order they do not own, and the error reveals
   nothing about its existence.
7. Every cancellation and refund has an append-only audit record.
8. Guests with a valid order access token can cancel using the same rules.
9. All customer-visible copy for success, failure, and delay is present in each
   supported locale.
10. Automated tests cover: eligibility matrix, idempotency, concurrent
    requests, race with fulfillment, PSP refund failure, and partial
    cancellation arithmetic.

## 10. Data and API implications (indicative, not prescriptive)

- Order line needs an explicit cancellation state and a `cancelled_at` /
  `cancelled_by` pair, or an equivalent event-sourced record.
- Order needs cancellability derived from line states, not stored as a single
  boolean that can drift.
- A refund record per cancellation (or per line) with status, PSP refund id,
  amount, currency, and idempotency key.
- New endpoints or operations: check eligibility, request cancellation,
  read refund status — all authorized per order ownership.
- Fulfillment integration needs a cancel operation with acknowledgement and a
  reconciliation job for timeouts.

## 11. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Fulfillment cannot stop a picked parcel | Customers told "cancelled" then receive goods | Prefer failing the cancellation; require acknowledgement before confirming |
| PSP refund latency misread as failure | Support load, double refunds | Distinguish initiated vs settled; reconcile via webhooks; idempotency keys |
| Discount/shipping allocation drift between checkout and refund | Over- or under-refund | Reuse the checkout allocation calculation; assert totals reconcile to captured amount |
| Guests using leaked order links | Data exposure, unauthorized cancellation | Non-guessable token, expiry, rate limiting, audit |
| Policy complexity (custom goods, fees) creeping into the core flow | Slow delivery, unclear behaviour | Policy evaluated in one place, defaults simple, fee defaults to zero |

## 12. Assumptions to validate before build

1. Order state machine and its exact current states, and which service owns
   transitions.
2. Whether fulfillment exposes a cancel/stop operation and what it guarantees.
3. PSP refund capability, webhook formats, idempotency support, and settle
   timing per payment method.
4. Whether line-level tax/discount/shipping allocations are persisted.
5. Whether guest checkout exists and how order access tokens are issued.
6. Whether any product categories are legally non-cancellable in target
   markets, and what local consumer law requires for the cancellation window
   and refund messaging.
7. Current support workflow for cancellation so the agent path replaces rather
   than duplicates it.

If any of 1–4 turn out false, the corresponding requirement above must be
revised rather than worked around.

## 13. Out of scope for this ticket, explicitly

Returns after delivery, exchanges, chargebacks, merchant-initiated
cancellations, subscription cancellation, alternate refund destinations,
and any change to the checkout flow itself.
