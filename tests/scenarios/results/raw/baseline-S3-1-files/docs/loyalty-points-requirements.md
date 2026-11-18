# Loyalty Points Program — Requirements Specification (Draft v0.1)

| Field | Value |
|---|---|
| Document status | Draft — not approved for build |
| Source | Requirements kickoff meeting, 2026-11-18 |
| Attendees | Lan (Product Manager), Minh (Operations Lead), Hà (Finance) |
| Owner | Lan (Product) |
| Document date | 2026-11-18 |
| Scope of this version | Confirmed rules only. Open items are listed separately and must not be implemented on the basis of this document. |

## 1. Purpose and business objective

The program exists to increase customer retention: the stated goal is to keep
customers returning by making points easy to redeem. Ease and speed of
redemption are therefore product-level requirements, not conveniences.

Finance treats earned points as a liability and requires visibility of the
outstanding points balance at any time.

## 2. Scope

In scope: earning points at point of sale, redeeming points at checkout,
reporting on outstanding points liability.

Out of scope (not discussed, therefore not specified here): customer-facing
enrolment, programme tiers, marketing campaigns, partner or third-party
redemption, mobile/app surfaces, data retention beyond what expiry
discussions imply.

## 3. Confirmed requirements

The following two rules were explicitly stated, challenged and agreed by all
three attendees. They are the only decisions currently locked.

### FR-1 — Point earning rate

- **Statement:** Customers earn 1 point per 10,000 VND spent.
- **Rounding:** Round down (truncate) to the nearest whole point. A
  transaction of 9,999 VND earns 0 points; 19,999 VND earns 1 point.
- **Where applied:** At checkout, handled by Operations.
- **Status:** Agreed by Lan, Minh and Hà.
- **Notes / unstated:** The meeting did not define the treatment of refunds,
  voided transactions, partial returns, currency rounding on multi-line
  baskets, or whether the calculation applies per transaction or per line
  item. Points reversal on refund is therefore unspecified.

### FR-2 — Non-transferable points

- **Statement:** Only the account holder may redeem points. Transfers of
  points between accounts are not permitted.
- **Status:** Agreed by Lan, Minh and Hà.
- **Notes / unstated:** The notes do not say whether this is enforced
  technically (blocked in product) or procedurally (policy only). No error or
  messaging behaviour was defined for a blocked transfer attempt.

### FR-3 — Redemption at checkout (capability, not a rate)

- **Statement:** Customers must be able to apply points at checkout as a
  discount against the transaction.
- **Non-functional requirement:** Redemption must be fast and low-effort for
  the cashier — the meeting explicitly rejected any flow that requires the
  cashier to perform manual calculation. Speed and simplicity at the
  register are acceptance criteria for this feature.
- **Status:** Direction agreed; the conversion rate that makes it
  implementable is **not** agreed (see OI-1).
- **Notes / unstated:** No target latency figure, no minimum or maximum
  redemption threshold, no partial-redemption rule, and no handling of a
  redemption that exceeds the basket value were discussed.

## 4. Open items

These are unresolved. Each has an owner and a decision needed before launch.
They are recorded here so they are not lost; they are not requirements yet.

### OI-1 — Redemption conversion rate

- **Question:** How many VND of discount does one point buy?
- **Owner:** Lan (Product).
- **Commitment:** Lan will propose the rate next week.
- **Blocking:** Hà cannot sign off until she has reviewed the margin data.
- **Impact if unresolved:** FR-3 cannot be built or tested.

### OI-2 — Points expiry (**unresolved conflict**)

Two positions were put forward and neither was withdrawn:

- **Operations (Minh):** Points expire six months after the customer's last
  activity, to keep stale balances off the books. Minh also noted a support
  burden: customers complain when old points disappear without warning.
- **Finance (Hà):** Points should never expire. Expiry changes revenue
  recognition and would require auditor clearance first.

- **Owner:** Finance (Hà), to confirm the correct accounting treatment with
  the auditors. Minh will write up the operations view for the auditors.
- **Decision needed:** Expire vs. never expire, and if expiring, the exact
  inactivity window and the definition of "activity".
- **Impact if unresolved:** Any build that assumes expiry will produce
  balances Finance may not be able to recognise. Treat as a hard dependency
  for launch.

### OI-3 — Outstanding points liability figure

- **Question:** What is the total outstanding points liability, and how is it
  reported for any point in time?
- **Owner:** Hà (Finance) — the figure can only be pulled from the ledger by
  Finance. Hà will bring the numbers to the next meeting.
- **Related requirement:** Finance needs the outstanding balance "at any
  time". The mechanism (report, API, dashboard, frequency, granularity) was
  not specified and needs to be defined with Finance once the figure is
  available.

### OI-4 — Tax and accounting classification of redemptions

- **Question:** For tax purposes, is a redemption a discount or a separate
  payment method?
- **Owner:** Hà (Finance), to confirm.
- **Impact if unresolved:** Determines how redemption is modelled in the
  checkout transaction record and how it is reported. This may constrain the
  FR-3 implementation, so it should be resolved before development starts,
  not after.

### OI-5 — Launch date

- **Status:** Undecided. Minh stated the app work must be scheduled first;
  Hà stated launch timing is a business decision outside Finance's remit.
- **Owner:** Not assigned.
- **Dependency:** Cannot be set until OI-1 through OI-4 are resolved and
  delivery effort is estimated.

## 5. Assumptions and constraints

- Points are recorded per customer account; redemption is tied to that
  account (from FR-2).
- Point balances must be queryable for Finance reporting, but the reporting
  interface is undefined (OI-3).
- Implementation of expiry must not proceed until the conflict in OI-2 is
  closed, because the two options imply materially different data models
  (no expiry timestamp vs. expiry plus activity tracking).
- The outstanding-liability figure is not derivable by the delivery team; it
  is a Finance-led input.

## 6. Delivery sequencing (proposed, subject to OI-5)

1. Resolve OI-1, OI-2, OI-4 — these change the data model and cannot be
   retrofitted cheaply.
2. Establish the liability reporting approach (OI-3) jointly with Finance.
3. Build FR-1 (earning) and FR-2 (non-transferability), which are stable and
   independent of the open items.
4. Build FR-3 (redemption) once the conversion rate and tax classification
   are confirmed.
5. Set launch date; run acceptance against the speed/simplicity criterion in
   FR-3.

## 7. Requirements traceability

| ID | Requirement | Status | Source |
|---|---|---|---|
| FR-1 | 1 point per 10,000 VND, rounded down | Agreed | Meeting, all attendees |
| FR-2 | Non-transferable; account holder only | Agreed | Meeting, all attendees |
| FR-3 | Redeem points at checkout, fast and simple | Direction agreed, rate pending | Meeting, Minh + Lan |
| OI-1 | Redemption conversion rate | Open — Lan | Meeting |
| OI-2 | Expiry policy | Open — conflict, Finance/auditors | Meeting, Minh vs Hà |
| OI-3 | Outstanding liability figure and reporting | Open — Hà | Meeting |
| OI-4 | Redemption tax treatment | Open — Hà | Meeting |
| OI-5 | Launch date | Open — unassigned | Meeting |
