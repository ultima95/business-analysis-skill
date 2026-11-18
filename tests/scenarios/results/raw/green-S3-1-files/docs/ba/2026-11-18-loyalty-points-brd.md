# Loyalty Points Program — Business Requirements Document

## Document control

| Field | Value |
|---|---|
| Version | 0.1 |
| Date | 2026-11-18 |
| Author | Business analysis, from the Loyalty Program requirements kickoff notes (2026-11-18) |
| Status | Draft — two rules confirmed, four decisions still open (see Open questions) |

## Executive summary

The business is launching a loyalty points program whose purpose is to keep customers returning. At the kickoff meeting on 2026-11-18 the group confirmed two rules — one point per 10,000 VND spent rounded down, and non-transferable points usable only by the account holder — and left four items open: the redemption conversion rate, whether points expire, the outstanding points liability figure, and the tax treatment of redemptions.

Only the two confirmed rules are ready for the application team. Everything else in this document is either derived from those rules or recorded as an assumption or an open question, and none of it should be treated as agreed.

The decision requested of the steering stakeholders is: resolve the expiry conflict and the conversion rate, so that the redemption and expiry requirements can be completed before launch. The outstanding liability figure and the tax treatment are owned by Finance and are inputs to, not blockers of, the earning and redemption rules.

## Business objectives and success metrics

| Objective | Metric | Target | Owner |
|---|---|---|---|
| Keep customers coming back (Lan, kickoff) | Not set — Q-07 | Not set — Q-07 | Lan (PM) |
| Redemption usable at checkout within an agreed time (Minh, Lan, kickoff) | Checkout redemption time | Not set — Q-03 | Minh (Ops) |
| Outstanding points visible to Finance at any point in time (Hà, kickoff) | Total outstanding points | Reportable on request — FR-005 | Hà (Finance) |

No numeric target for retention or for checkout timing exists in the kickoff notes; both are recorded as open questions rather than filled in here.

## Background / as-is

The kickoff notes describe a program being launched, not an existing one: Lan opened with "We're launching the loyalty points program", and no current points scheme, current process, or current volume was presented at the meeting (Loyalty Program requirements kickoff, 2026-11-18).

Three positions were stated about how the program will work in the business:

- **Checkout handling.** Minh's team handles points at the register and proposed the earning rate, and Minh stated that "redemption has to be fast. Nobody wants to stand at the register while the cashier does math" (kickoff, Minh).
- **Finance treatment.** Hà treats points as a liability on the books and requires visibility of how many points are outstanding at any time; the last-quarter figure can only be pulled from the ledger by Hà (kickoff, Hà).
- **Customer identity.** Minh stated the rule that only the account holder can redeem and that there are no transfers between accounts, and Hà agreed to it (kickoff, Minh and Hà).

No source describes the handling of a refunded or cancelled purchase, so that gap is recorded as Q-09.

## Scope

In scope:
- Awarding points on a completed purchase at the confirmed earning rate (BR-001).
- Applying points as a discount at checkout by the account holder (BR-004).
- Enforcing that only the account holder redeems, with no transfers between accounts (BR-002, BR-003).
- Reporting total outstanding points to Finance on request (BR-005).

Out of scope:
- Transferring points between accounts — excluded by BR-003.
- Points expiry — the policy is undecided (Q-01), so no expiry requirement is written in this version.
- Conversion rate, tax treatment and the historical liability figure — respectively Q-02, Q-04 and Q-05.
- Tiering, campaigns, bonus multipliers and any screen or interface design — not raised at the kickoff.

## Stakeholders

| Stakeholder | Role | Interest | Influence |
|---|---|---|---|
| Lan | PM; owns the conversion rate proposal and the launch decision | Needs a document the application team can build the confirmed rules from | High |
| Minh | Operations lead; owns checkout handling and the ops view on expiry | Needs redemption to fit the register workflow without delaying the queue | High |
| Hà | Finance; owns the liability position, tax treatment and auditor sign-off | Needs outstanding points visible and the accounting treatment confirmed | High |
| Application team | Builds the program | Needs the decided rules first, before the open items (kickoff, Lan) | Medium |
| Auditors | External reviewers of revenue recognition | Need to confirm expiry and tax treatment before Finance can sign off (kickoff, Hà) | Medium |
| Customers | Earn and redeem points | Need to redeem without friction at checkout (kickoff, Lan) | Low |

## Business rules

- **BR-001**: One point is awarded for each 10,000 VND of value spent, rounded down to a whole point. Agreed at the kickoff by Lan, Minh and Hà.
- **BR-002**: Only the account holder may redeem points from an account. Agreed at the kickoff by Minh, Hà and Lan.
- **BR-003**: Points cannot be transferred between accounts. Agreed at the kickoff by Minh, Hà and Lan.
- **BR-004**: Points are redeemed at checkout as a discount against the transaction being paid. Stated at the kickoff by Lan and Minh; the conversion rate from points to money is Q-02.
- **BR-005**: Total outstanding points are a financial liability and must be reportable to Finance on request. Stated at the kickoff by Hà.

## Functional requirements

- **FR-001**: The system shall award points on a completed purchase at one point per 10,000 VND of transaction total, rounded down. Fulfils [BR-001]. Priority: Must.
- **FR-001.AC1**: Given a purchase with a transaction total of 25,000 VND, When the purchase is completed, Then 2 points are added to the account holder's balance.
- **FR-001.AC2**: Given a purchase with a transaction total of 9,999 VND, When the purchase is completed, Then 0 points are added to the account holder's balance.
- **FR-001.AC3**: Given a purchase with a transaction total of exactly 10,000 VND, When the purchase is completed, Then 1 point is added to the account holder's balance.
- **FR-002**: As an account holder, I want to apply my points as a discount at checkout, so that I pay less for the current purchase. Fulfils [BR-004]. Priority: Must.
- **FR-002.AC1**: Given the account holder has a balance of at least the number of points being redeemed, When the redemption is recorded at checkout, Then the transaction total is reduced by the discount produced by the agreed conversion rate (Q-02) and the balance falls by the same number of points.
- **FR-002.AC2**: Given the account holder requests a redemption of more points than the current balance, When the redemption is recorded at checkout, Then the redemption is refused, the transaction total is unchanged and the balance is unchanged.
- **FR-003**: The system shall refuse a redemption requested for an account by anyone other than that account's holder. Fulfils [BR-002]. Priority: Must.
- **FR-003.AC1**: Given a person who is not the holder of an account with a points balance, When that person attempts to redeem against the account, Then the redemption is refused and the balance is unchanged.
- **FR-003.AC2**: Given the holder of an account with a points balance, When that holder redeems against the account, Then the redemption proceeds under [FR-002].
- **FR-004**: The system shall prevent points from moving from one account to another. Fulfils [BR-003]. Priority: Must.
- **FR-004.AC1**: Given two accounts each holding a points balance, When a transfer between them is requested, Then no points are moved and both balances are unchanged.
- **FR-005**: The system shall report the total number of points outstanding across all accounts at the moment the report is requested. Fulfils [BR-005]. Priority: Must.
- **FR-005.AC1**: Given points balances exist across multiple accounts, When Finance requests the total outstanding points, Then the reported total equals the sum of all account balances at that moment.
- **FR-005.AC2**: Given a redemption has reduced an account balance, When Finance requests the total outstanding points afterwards, Then the reported total reflects that reduction.

## Non-functional requirements

No measurable quality target can be stated from the kickoff notes. Minh raised checkout redemption speed as a requirement but gave no number, and Lan agreed the need without one. A target is required before FR-002 can be accepted at the register, so the gap is recorded as Q-03 rather than filled with a number this document cannot support.

## Edge cases

| Actor | Entity state | Create | Read | Update | Delete |
|---|---|---|---|---|---|
| Account holder | Balance of 0 points | Purchase below 10,000 VND earns 0 points (FR-001.AC2) | Balance reported as 0 | Requested redemption refused (FR-002.AC2) | Removal of points only under an expiry policy (Q-01) |
| Account holder | Balance of at least the points requested | Purchase adds rounded-down points (FR-001.AC1) | Balance reported | Redemption reduces balance (FR-002.AC1) | Removal of points only under an expiry policy (Q-01) |
| Account holder | Balance below the points requested | — | Balance reported | Requested redemption refused (FR-002.AC2) | Removal of points only under an expiry policy (Q-01) |
| Person who is not the account holder | Any account holding points | No account is opened for the requester | Whether a balance may be disclosed to a non-holder is undecided (Q-08) | Redemption refused (FR-003.AC1) | — |
| Cashier | Any account | Redemption recorded at checkout (FR-002) | Balance must be readable to process a redemption; disclosure scope is undecided (Q-08) | — | — |
| Finance | All accounts, aggregate | — | Total outstanding points reported (FR-005.AC1) | — | — |
| Finance | Account affected by a refunded purchase | Effect of a refund on awarded points is not stated in the notes (Q-09) | — | — | — |
| Operations | Account with a disputed or refunded purchase | — | Whether Operations may read a customer balance is undecided (Q-08) | — | — |

## Assumptions, constraints, dependencies

### Assumptions

| ID | Assumption | Basis in input, or impact if false |
|---|---|---|
| A-01 | The earning base is the transaction total after discounts, so points are not earned on money the customer did not pay. | Not stated at the kickoff; Minh only said "per 10,000 VND spent". If points are earned before discounts, awarded points and the liability figure rise on every discounted transaction. |
| A-02 | Points are whole numbers only, and any fraction of a point is discarded at the moment of earning. | Derived from "one point per 10,000 VND spent, rounded down" (BR-001). If fractions accumulate, the rounding ACs in FR-001 are wrong. |
| A-03 | Only completed purchases earn points; no campaign, tier or bonus multiplier applies in this release. | Nothing in the notes proposes a campaign or tier. If a multiplier exists, BR-001 needs a second rule and FR-001 needs a further AC. |
| A-04 | A redemption consumes points and produces the discount in the same checkout transaction. | Follows from "use points at checkout for a discount" (BR-004). If the two steps can be separated, FR-002 gains a reversal path. |
| A-05 | Each customer holds exactly one loyalty account, and the account holder can be identified at checkout. | Required for BR-002 to be enforceable at all; the notes say only the holder may redeem. If a customer can hold several accounts, FR-003 and FR-005 both change. |

### Constraints

- Points outstanding are a liability on the books, so any rule that adds, removes or converts points changes the revenue recognition position (kickoff, Hà).
- Expiring points requires auditor clearance before the treatment can be applied, so no expiry rule can be released without that confirmation (kickoff, Hà).
- Redemption is handled at the register by the cashier during a live checkout, so it adds time to the customer's queue (kickoff, Minh).
- No launch date has been fixed; Lan confirmed it is a business decision and not set at the kickoff (Q-06).

### Dependencies

- The conversion rate proposal from Lan, due the week after the kickoff (Q-02) — FR-002 cannot be completed without it.
- The auditor's position on expiry, raised by Hà (Q-01) — the expiry requirement cannot be written before it.
- Minh's written ops view on expiry, promised for the auditors (Q-01) — an input to the auditor's position.
- Hà's outstanding liability figure from the ledger (Q-05) — the baseline against which FR-005 is validated.
- Hà's confirmation of whether redemption is a discount or a separate payment method for tax purposes (Q-04) — affects how the discount is recorded under FR-002.

## Open questions

| ID | Question | Owner | Blocks |
|---|---|---|---|
| Q-01 | Do points expire? Minh stated "Points should expire six months after the customer's last activity"; Hà stated "Points should never expire" and that expiry "contradicts what I said earlier" because it changes revenue recognition and needs auditor clearance. Which applies? | Hà (Finance), pending auditor input; Minh to supply the ops view | all FRs for expiry |
| Q-02 | What is the conversion rate from points to money used at checkout? Lan will propose it the week after the kickoff. | Lan (PM) | FR-002 |
| Q-03 | What is the maximum time a checkout redemption may take, measured at the register? | Minh (Ops) | all NFRs for checkout redemption |
| Q-04 | For tax purposes, is a redemption treated as a discount on the sale or as a separate payment method? | Hà (Finance) | FR-002 |
| Q-05 | What was the total outstanding points liability as of last quarter, from the ledger? | Hà (Finance) | FR-005 |
| Q-06 | What is the launch date? Confirmed at the kickoff as not yet set. | Lan (PM) | all FRs — release timing |
| Q-07 | Which metric and target will the business judge retention by, and in what period? | Lan (PM) | all NFRs for retention measurement |
| Q-08 | May a cashier, or any other staff member, see a customer's points balance, and under what conditions? | Minh (Ops) | FR-002, FR-005 |
| Q-09 | When a purchase that earned points is refunded or cancelled, are the awarded points removed, frozen until the next decision, or kept? Nothing in the notes covers this. | Lan (PM) | FR-001 |

## Glossary

| Term | Meaning |
|---|---|
| Points | The loyalty balance awarded for spending, redeemed at checkout as a discount. |
| Earning rate | One point per 10,000 VND of transaction total, rounded down (BR-001). |
| Redemption | Using points at checkout to reduce the amount the customer pays (BR-004). |
| Account holder | The single customer who owns a loyalty account and is the only person permitted to redeem from it (BR-002). |
| Outstanding points | The total points balance held across all accounts at a given moment; a liability on the books (BR-005). |
| Transaction total | The amount of a purchase at checkout, after discounts, on which points are earned under A-01. |
| Last activity | The event that would start an expiry countdown, if expiry is adopted (Q-01); not defined in the notes. |

## Sign-off

| Name | Role | Decision | Date |
|---|---|---|---|
| Lan | PM | Changes requested — open items pending | — |
| Minh | Operations lead | — | — |
| Hà | Finance | — | — |
