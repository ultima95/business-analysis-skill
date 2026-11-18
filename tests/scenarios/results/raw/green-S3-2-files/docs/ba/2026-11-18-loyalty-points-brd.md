# Loyalty Points Program — Business Requirements Document

## Document control

| Field | Value |
|---|---|
| Version | 0.1 |
| Date | 2026-11-18 |
| Author | Business analysis, drafted from the 2026-11-18 requirements kickoff notes |
| Status | Draft |

## Executive summary

The business is launching a loyalty points program whose purpose, in the PM's words, is to "keep customers coming back", and the program is expected to be usable at checkout without delay at the register. The stated goal is retention, and it is measured: at least 30 percent of returning customers redeem points within their first year.

Two rules are decided and agreed by all three attendees: how points are earned, and that points cannot leave the account that holds them. Everything else about the program is still open. The redemption conversion rate has no agreed value; points expiry is in direct conflict between Ops and Finance; the outstanding points liability figure has not been produced; and the tax treatment of points has not been confirmed.

This document records the decided rules as testable requirements, records the retention target and the reporting capability it needs, records the unresolved items as open questions with named owners, and marks the requirements that cannot be completed until those answers arrive. It does not choose between the conflicting positions on expiry, and it does not propose a design.

The decision requested: approve the two decided rules and the retention target as the baseline for app scheduling, and secure dates from the Ops and Finance owners for the four items they hold. Those four are open with their current owners and are expected to be answered by Minh and Hà, not by the programme owner.

## Business objectives and success metrics

| Objective | Metric | Target | Owner |
|---|---|---|---|
| Retain customers through a redeemable points balance | Share of returning customers who redeem points at least once within 12 months of their first purchase | At least 30 percent | Lan (PM) |

The target and its owner come from the programme owner. Two parts of the measurement are not yet fixed: the definition of a returning customer (A-08) and the measurement window start (A-09). FR-006 states the reporting capability the target depends on, so the number can be observed rather than asserted.

## Background / as-is

No current loyalty program is described in the input. The relevant as-is facts stated at the kickoff:

- Ops (Minh) states points can be handled at checkout and proposes the earning rate (Minh).
- Finance (Hà) treats points as a liability on the books and needs the outstanding total at any time (Hà).
- Finance states the outstanding points liability as of the last quarter can be produced only from the ledger, by Hà (Hà).
- No launch date is set; scheduling of the app work has not happened, and the launch date is described as a business decision that Finance will not make (Minh, Hà, Lan).

## Scope

In scope:
- Earning points on a purchase under the agreed earning rule (BR-001).
- Redeeming points for a discount at checkout.
- Preventing transfer of points between accounts and restricting redemption to the account holder (BR-002).
- Recording points movements so that the outstanding points liability can be reported.
- Reporting the total outstanding points at a chosen date.
- Reporting the share of returning customers who redeem points within 12 months of their first purchase, which is the measure of the retention goal.

Out of scope:
- Points expiry behaviour — no decision exists; see Q-02.
- The redemption conversion rate value — not yet proposed; see Q-01.
- Tax treatment of points — not yet confirmed; see Q-04.
- Transfers of points between accounts, which are prohibited by BR-002.
- Any programme structure not raised in the input, such as tiers, campaigns, or partner earning.

## Stakeholders

| Stakeholder | Role | Interest | Influence |
|---|---|---|---|
| Lan (PM) | Owns the program; will propose the conversion rate next week; owns the launch decision | Needs the decided rules written down and the open items tracked to closure | High |
| Minh (Ops lead) | Checkout and support operations; proposed the earning rate and the expiry position | Needs redemption to work at the register without delay and needs stale balances handled | High |
| Hà (Finance) | Owns the liability view, the expiry position, and the tax treatment | Needs the outstanding points total on demand and no change to revenue recognition without auditor clearance | High |
| App team | Receives the decided rules first, per the kickoff close | Needs unambiguous, testable rules before scheduling work | Medium |
| Customer (account holder) | Earns and redeems points | Needs redemption at checkout to work on their own account only | Medium |
| Cashier | Applies redemption at checkout | Needs the redemption step to complete without manual calculation | Medium |

## Business rules

- **BR-001**: A purchase earns 1 point for each complete 10,000 VND of value, rounded down, so any remainder below 10,000 VND earns no point.
- **BR-002**: Points belong to the account that earned them; points cannot be transferred to another account, and only the account holder may redeem them.

Decision status of each rule:

| Rule name | Status at kickoff | Evidence |
|---|---|---|
| Earning rate (BR-001) | Decided; all three attendees agreed | "So the earning rule is one point per 10,000 VND, rounded down. Do we all agree on that?" — Minh: "Yes." Hà: "Yes." |
| Non-transferability (BR-002) | Decided; recorded by the PM as already agreed | "The second rule we already agreed on: only the account holder can redeem points. No transfers between accounts." — Hà: "Agreed." |

## Functional requirements

- **FR-001**: As a customer, I want to earn points on each purchase at the agreed rate, so that my balance grows with my spending. Fulfils [BR-001]. Priority: Must.
- **FR-001.AC1**: Given a purchase of 35,000 VND, When the transaction completes, Then 3 points are added to the account holder's balance.
- **FR-001.AC2**: Given a purchase of 19,999 VND, When the transaction completes, Then 1 point is added and the remainder of 9,999 VND earns no point.
- **FR-001.AC3**: Given a purchase of 9,000 VND, When the transaction completes, Then 0 points are added and the balance is unchanged.
- **FR-002**: As a cashier, I want to apply the account holder's points as a discount at checkout, so that the customer receives the value of the balance in the same purchase. Fulfils [BR-002]. Priority: Must.
- **FR-002.AC1**: Given the account holder has a balance above 0, When the cashier applies a redemption of that many points, Then the discount equals the redeemed points multiplied by the conversion rate in force, and the balance decreases by the same number of points.
- **FR-002.AC2**: Given the account holder's balance is 0, When the cashier attempts a redemption, Then no discount is applied and the transaction completes at the undiscounted amount.
- **FR-002.AC3**: Given a redemption request for more points than the balance holds, When the cashier applies it, Then the request is rejected and the balance is unchanged (A-04).
- **FR-003**: The system shall reject any request to move points from one account to another. Fulfils [BR-002]. Priority: Must.
- **FR-003.AC1**: Given two accounts A and B, When a transfer of points from A to B is requested, Then the request is rejected and both balances are unchanged.
- **FR-003.AC2**: Given a checkout on account A, When a redemption is attempted against points held by account B, Then the redemption is rejected and no discount is applied.
- **FR-004**: The system shall record every points earning and every points redemption as a ledger entry carrying the account, the points moved, the transaction reference, the timestamp, and the resulting balance. Fulfils [BR-002]. Priority: Must.
- **FR-004.AC1**: Given a completed transaction that earns 3 points, When the ledger is read for that account, Then one earning entry exists with 3 points and the resulting balance.
- **FR-004.AC2**: Given a transaction that is abandoned after the points were calculated, When checkout aborts, Then no earning entry is recorded for it.
- **FR-005**: As a finance user, I want the total outstanding points across all accounts for any chosen date, so that the liability on the books reflects the points customers still hold. Priority: Must.
- **FR-005.AC1**: Given ledger entries up to a chosen date, When the outstanding total is requested for that date, Then the total equals points earned minus points redeemed up to and including that date.
- **FR-005.AC2**: Given a redemption recorded on the chosen date, When the outstanding total is requested, Then the redemption is subtracted from that date's total.
- **FR-005.AC3**: Given no points activity has occurred, When the outstanding total is requested, Then the reported total is 0.
- **FR-006**: As a programme owner, I want the share of returning customers who redeemed points within 12 months of their first purchase, so that I can tell whether the programme is retaining customers. Priority: Must.
- **FR-006.AC1**: Given a group of customers who returned and purchased again, When the redemption report is produced for a 12-month window, Then it reports the count of them who redeemed at least once in that window, divided by the count of the group, as a percentage.
- **FR-006.AC2**: Given a customer redeemed points in month 13, When the report is produced for that customer's 12-month window, Then that customer is not counted as having redeemed within the window.
- **FR-006.AC3**: Given a customer redeemed points twice in the same window, When the report is produced, Then that customer is counted once.
- **FR-006.AC4**: Given no customer in the group redeemed in the window, When the report is produced, Then the reported share is 0 percent rather than an undefined value.

## Non-functional requirements

| ID | Priority | Target | Basis |
|---|---|---|---|
| NFR-001 | Must | Redemption at checkout completes within 2 seconds at p95, measured from the cashier starting the redemption to the discount being recorded | A-02 |
| NFR-002 | Must | Ledger entries are append-only, are never modified or deleted after recording, and are retained for at least 7 years | A-03 |
| NFR-003 | Must | The outstanding points total for any chosen past date is produced within 1 business day of the request | A-05 |
| NFR-004 | Must | 100 percent of redemption attempts require identification of the account holder, with 0 redemptions completed on an account other than the one identified | Input: "only the account holder can redeem points. No transfers between accounts" |

- **NFR-001.AC1**: Given a checkout where the cashier applies a redemption, When the redemption is confirmed, Then the discount is recorded within 2 seconds at p95.
- **NFR-002.AC1**: Given a ledger entry recorded on any date, When any user attempts to modify or delete it, Then the change is refused.
- **NFR-002.AC2**: Given 7 years have passed since an entry was recorded, When the retention period is audited, Then the entry is still present.
- **NFR-003.AC1**: Given a request for the outstanding total of a past date, When the request is raised, Then the total is delivered within 1 business day.
- **NFR-004.AC1**: Given 100 redemption attempts in a day, When the attempts are reviewed, Then every one of them is attributable to the account holder of the account redeemed from, and 0 are attributable to another account.

## Edge cases

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| Customer | Balance is 0 | Redemption request refused, no discount (FR-002.AC2) | Balance reads 0 | No change | Not permitted (BR-002) |
| Customer | Balance below one redemption unit | Earning still adds to balance (FR-001.AC3) | Balance reads the stored points | No change | Not permitted (BR-002) |
| Customer | Purchase refunded after earning | Points earned on the refunded transaction are reversed (A-01) | Ledger shows both the earning and the reversal | No change to other entries | Not permitted (NFR-002) |
| Cashier | Redeeming against another account's points | Redemption refused (FR-003.AC2) | Only the identified account's balance is visible for the redemption | No change | Not permitted (BR-002) |
| Cashier | Duplicate submission of the same redemption | Second submission refused, balance moved once (A-07) | Balance reflects one redemption | No change | Not permitted (NFR-002) |
| Finance user | Outstanding total requested for a past date | Report produced (FR-005.AC1) | Total reconciles to ledger entries | No change through the report | Not permitted (NFR-002) |
| Programme owner | Redemption report requested for a cohort window | Report produced (FR-006.AC1) | Share reconciles to the ledger entries in the window | No change through the report | Not permitted (NFR-002) |
| Programme owner | Customer redeemed for the first time in month 13 | Not counted in that customer's window (FR-006.AC2) | Report excludes the redemption | No change | Not permitted (NFR-002) |

## Assumptions, constraints, dependencies

### Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | Points are earned on the amount paid after discounts, and a refunded purchase reverses the points earned on it. | Not stated in the input; if false, balances differ on every discounted purchase and the refund path has no points treatment. |
| A-02 | Checkout redemption must complete within 2 seconds at p95. | Working value set because the input gives a qualitative need only ("Redemption has to be fast"); if the real target is tighter, the checkout design and hardware assumptions change. |
| A-03 | The points ledger is append-only and retained for at least 7 years. | Set from Hà's liability and audit concerns; if the required retention differs, the ledger design and storage sizing change. |
| A-04 | A redemption request larger than the balance is rejected rather than partially applied. | Not stated; if partial redemption is allowed, FR-002 gains a further branch and an additional acceptance criterion. |
| A-05 | The outstanding points total for a past date is available within 1 business day. | Anticipated from Hà's "I need to know how many points are outstanding at any time"; if the need is same-day, NFR-003 tightens and the reporting path changes. |
| A-06 | No baseline exists for the share of returning customers who redeem within 12 months, so the 30 percent target is stated without a current figure to compare against. | The target comes from the programme owner; the current share was not supplied. If a baseline exists, it is recorded beside the target; if the current share already exceeds 30 percent, the metric measures upkeep rather than improvement. |
| A-07 | A repeated submission of the same redemption is refused, and the balance moves once. | Not stated; if not enforced, a double submission at the register can move points twice. |
| A-08 | A "returning customer" is a customer who made at least one purchase after their first. | The input names returning customers as the population but does not define it. If the definition is narrower, the 30 percent is measured against a smaller base and FR-006 changes. |
| A-09 | The 12-month measurement window starts at the customer's first purchase, not at programme launch. | The input says "within their first year" without naming the start point. If the window starts at launch, early cohorts are measured from a different anchor and the target is only comparable across cohorts from launch onward. |

### Constraints

- Points are a liability on the books, and Finance will not accept a change to revenue recognition without auditor clearance (Hà).
- Any expiry policy is subject to auditor confirmation before it can be adopted (Hà).
- Redemption cannot require manual calculation at the register (Minh).
- No launch date is fixed; the app work must be scheduled first (Minh).

### Dependencies

- Conversion rate proposal from Lan, expected the following week.
- Auditor confirmation of the expiry treatment, owned by Finance.
- Tax treatment confirmation, owned by Finance.
- App team scheduling of the delivery work.

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | What conversion rate applies when points are redeemed for a discount, and who approves it? | Lan (PM) — proposes next week; Hà (Finance) cannot sign off until margin data is checked | FR-002 |
| Q-02 | Do points expire six months after the customer's last activity, or never expire? Verbatim conflict — Minh: "Points should expire six months after the customer's last activity." Hà: "No — that contradicts what I said earlier. Points should never expire." | Hà (Finance), pending auditor confirmation; Minh (Ops) holds the six-month position | all FRs for points expiry |
| Q-03 | What is the total outstanding points liability as of last quarter? | Hà (Finance) — from the ledger | FR-005 |
| Q-04 | Are redeemed points treated as a discount or as a separate payment method for tax purposes? | Hà (Finance) | FR-002, FR-005 |
| Q-05 | What launch date applies, and what date does the app work need in order to hit it? | Minh (Ops) and Hà (Finance) for their inputs; Lan (PM) makes the business call | all FRs for release scope |
| Q-06 | Is there a minimum or maximum number of points redeemable in a single transaction? | Hà (Finance) for the liability view; Lan (PM) for the product call | FR-002 |
| Q-07 | How does a customer come to hold a loyalty account — enrolment at checkout, an existing customer record, or another route — and does a non-account purchase earn points? | Lan (PM) — not raised at the kickoff | FR-001, FR-004, NFR-004 |

## Glossary

| Term | Meaning |
|---|---|
| Loyalty points | The unit a customer earns by purchasing and redeems for a discount. |
| Earning | Adding points to an account as a result of a completed purchase. |
| Redemption | Using points from an account to reduce the amount payable in a purchase. |
| Conversion rate | The value of one point when redeemed, which has no agreed value yet (Q-01). |
| Account holder | The customer who owns the loyalty account and the only person permitted to redeem its points. |
| Returning customer | A customer who has made at least one purchase after their first purchase (A-08). |
| Redemption report | The percentage of a returning-customer cohort that redeemed points at least once within a 12-month window, which measures the retention goal. |
| Transfers | Moving points from one account to another, which BR-002 prohibits. |
| Outstanding points liability | The total points held across all accounts, which Finance carries as a liability. |
| Ledger entry | The record of a single earning or redemption, with its account, points, transaction reference, timestamp, and resulting balance. |

## Sign-off

| Name | Role | Decision | Date |
|---|---|---|---|
| Lan | PM | | |
| Minh | Ops lead | | |
| Hà | Finance | | |
