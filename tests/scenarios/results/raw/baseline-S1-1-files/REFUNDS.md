# Refund behavior

Design note for adding refunds to the shop. Derived from the existing code in
`orders.py` and `test_orders.py`, plus the agreed refund policy: full **or**
partial refunds, always to the original payment method, delivered-only, inside
the window the code already sets, with finance approval above 5,000,000 VND.

All amounts are VND, whole đồng (integers). No minor units, no other currency.

## 1. What the existing code already decides for us

| Fact | Source | Consequence for refunds |
| --- | --- | --- |
| Eligibility is `can_return(order, today)` | `orders.py` | Refunds reuse this gate. No second, looser eligibility rule. |
| Only `DELIVERED` qualifies | `can_return` | `PENDING`, `PAID`, `SHIPPED`, `CANCELLED` are refused. Confirmed by policy. |
| `delivered_on is None` is refused | `can_return` | Missing delivery date is a refusal outcome, not an assertion. |
| Window is inclusive: day 30 allowed, day 31 refused | `RETURN_WINDOW_DAYS`, tests | Refunds share the constant. No new window value. |
| `today` is injected | `can_return(order, today)` | Refund API takes `today` too; no hidden `date.today()`. |

## 2. Core rules

- **R1 — One eligibility gate.** `refund(...)` requires `can_return(order, today)`
  to be `True`. The 30-day constant is reused, never redefined.
- **R2 — Delivered only.** Non-`DELIVERED` orders are refused. `CANCELLED` is not
  a refund path; cancellation is assumed to settle its own money.
- **R3 — Window applies to every refund.** Whether it is the first refund or the
  fourth partial, the window is checked against `delivered_on` and `today`. A
  partial refund does not restart or extend the window, and an approval does not
  extend it either (§5, H4).
- **R4 — Full or partial amount.** A refund may be any amount from 1 đồng up to
  the order's remaining refundable balance.
- **R5 — Cumulative cap.** The sum of every non-rejected, non-failed refund
  (settled, in flight, and awaiting approval) must never exceed the order total.
  The refundable balance is `order.total − (settled + in-flight + approved-but-
  unsettled)`.
- **R6 — Original payment method, always.** Every refund, partial or full and
  approved or not, is returned to the payment method that funded the order. No
  store credit, no alternate destination, no choice of destination.
- **R7 — Approval gate.** A request with `amount > 5,000,000 VND` cannot settle
  immediately. It becomes `PENDING_APPROVAL`, reserving its amount against the
  balance, and only settles after finance approves. Exactly 5,000,000 needs no
  approval — the rule is strictly "over".
- **R8 — Terminal only when exhausted.** An order is fully refunded (and no
  longer refundable) when its refundable balance reaches zero. Until then,
  further partials are allowed while the window is open.
- **R9 — Idempotency.** A retried request after a provider failure never
  double-refunds; a settled refund is never repeated.

## 3. Decision order

Fixed order, so a bad input yields one deterministic reason and no provider call
or approval request happens for an ineligible refund.

1. Order exists.
2. Eligibility via `can_return` (R1, R2) — status, missing date, window (R3).
3. `delivered_on <= today` (§5, H1 guard).
4. Remaining refundable balance (R5) is greater than zero → else already fully
   refunded.
5. Requested amount is an integer, greater than 0, and no more than the balance
   (R4, R5).
6. Amount over the approval threshold → create `PENDING_APPROVAL`, reserve the
   amount, stop (R7).
7. Otherwise, call the provider for that amount against the original payment
   method (R6).
8. Persist the result; on failure persist nothing settled and leave the balance
   intact (R9).

Approved requests re-enter at step 1: eligibility and the window are re-checked
before settlement, because time has passed while waiting for finance.

## 4. Outcomes

Exactly one outcome per attempt.

| Outcome | Meaning |
| --- | --- |
| `REFUNDED` | Provider settled the amount. |
| `PENDING_APPROVAL` | Over threshold; awaiting finance. Amount reserved. |
| `APPROVAL_REJECTED` | Finance refused. Nothing moves; reservation released. |
| `APPROVAL_EXPIRED` | Approved, but the window closed before settlement (H4). |
| `ALREADY_REFUNDED` | Balance is zero. |
| `NOT_DELIVERED` | Status is not `DELIVERED`. |
| `MISSING_DELIVERY_DATE` | `DELIVERED` with `delivered_on is None`. |
| `OUTSIDE_RETURN_WINDOW` | Delivered, dated, past the window. |
| `INVALID_DELIVERY_DATE` | `delivered_on` is after `today`. |
| `INVALID_AMOUNT` | Non-integer, zero, or negative amount. |
| `EXCEEDS_REFUNDABLE` | Amount larger than the remaining balance. |
| `PAYMENT_FAILED` | Provider error; balance intact, retry safe. |

## 5. Exception cases

- **H1 — Negative day count passes `can_return`.** `(today - delivered_on).days <=
  RETURN_WINDOW_DAYS` is `True` for negative values, so a future delivery date
  looks returnable. Fix: extract the window test into a shared helper using
  `0 <= days <= RETURN_WINDOW_DAYS`, called by both `can_return` and refunds. The
  existing tests (day 30, day 31) still pass unchanged; the future-date hole
  closes for both paths.
- **H2 — Threshold boundary.** 5,000,001 VND needs approval; 5,000,000 VND does
  not. Use `amount > APPROVAL_THRESHOLD`, never `>=`.
- **H3 — Two partials that each pass but together overshoot.** Enforced by the
  balance check against settled + in-flight + reserved amounts (R5), not against
  the order total alone.
- **H4 — Approval outlives the window.** Approval does not freeze eligibility.
  Re-check at settlement; a grant redeemed after the window is
  `APPROVAL_EXPIRED` and its reservation is released.
- **H5 — Approval queue races.** The reservation must be written before the
  provider call, and approved-then-cancelled must release it exactly once, or
  concurrent partials can double-spend the balance.
- **H6 — Provider settled, persistence failed.** Record the provider reference
  before/around the call so a retry re-reads it instead of refunding again (R9).
- **H7 — Same-day delivery.** `delivered_on == today` is 0 days → refundable,
  consistent with existing window logic.
- **H8 — Fully refunded, then asked again.** Returns `ALREADY_REFUNDED`, not
  `OUTSIDE_RETURN_WINDOW` or a new approval, regardless of amount.
- **H9 — Cancelled then delivered.** `CANCELLED` never refunds; the state machine
  is refused by `can_return` first, so later refund attempts stay refused.

## 6. Data model additions

Needed before this is real; the current `Order` has only `status` and
`delivered_on`.

- `Order`: add `total` (VND int) and a stable order id.
- `Payment`: original method reference per order — the only legal refund target.
- `Refund`: refund id, order id, amount, status (`PENDING_APPROVAL`, `APPROVED`,
  `REJECTED`, `SETTLED`, `FAILED`), provider reference, requested/approved/settled
  timestamps, approver.
- Derived, not stored: `refundable_balance(order, refunds)`.
- `APPROVAL_THRESHOLD = 5_000_000`, alongside `RETURN_WINDOW_DAYS`.

## 7. Tests to add (mirroring `test_orders.py` style)

- Full refund at day 30 → `REFUNDED`; balance zero; second attempt →
  `ALREADY_REFUNDED`.
- Day 31 → `OUTSIDE_RETURN_WINDOW`.
- Each non-`DELIVERED` status → `NOT_DELIVERED`; `CANCELLED` included.
- `DELIVERED` with `delivered_on=None` → `MISSING_DELIVERY_DATE`.
- Future `delivered_on` → `INVALID_DELIVERY_DATE`.
- Partials 3,000,000 + 3,000,000 on a 6,000,000 order → both settle immediately,
  balance zero.
- Partial 3,000,000 then 4,000,000 on a 6,000,000 order → `EXCEEDS_REFUNDABLE`.
- 5,000,000 → `REFUNDED` with no approval; 5,000,001 → `PENDING_APPROVAL`.
- Approved request settles after approval; rejected releases the balance.
- Approved request settled after the window closes → `APPROVAL_EXPIRED`.
- Zero and negative amounts → `INVALID_AMOUNT`.
- Provider raises → `PAYMENT_FAILED`, balance intact, retry succeeds once.
