# Loyalty Program — Requirements Kickoff

Date: 2026-11-18
Attendees: Lan (PM), Minh (Ops lead), Hà (Finance)

## Meeting Notes

Lan: We're launching the loyalty points program. The whole point is to
keep customers coming back, so it has to be easy to redeem.
Minh: From my side, we can handle points at checkout. I propose one
point per 10,000 VND spent, rounded down.
Hà: Fine, but points are a liability on our books. I need to know how
many points are outstanding at any time.
Lan: So the earning rule is one point per 10,000 VND, rounded down. Do
we all agree on that?
Minh: Yes.
Hà: Yes.
Lan: Good. Next, redemption. Customers should be able to use points at
checkout for a discount.
Minh: Redemption has to be fast. Nobody wants to stand at the register
while the cashier does math.
Lan: Right — make it fast and easy to redeem.
Hà: I can't sign off on the redemption conversion rate until I've
checked the margin data, but that's a product decision for Lan.
Lan: I'll propose the conversion rate next week. Let's move on to
expiry.
Minh: Points should expire six months after the customer's last
activity. That keeps stale balances off our books.
Hà: No — that contradicts what I said earlier. Points should never
expire. If we expire them, the revenue recognition changes and I'd have
to clear it with the auditors first.
Lan: So we have a conflict. Minh says six months after last activity;
Hà says never expire. Let me write that down.
Minh: From an ops view, six months is cleaner. Support gets complaints
when old points vanish without warning.
Hà: And from a finance view, expiry changes the liability. I need to
confirm the correct treatment with the auditors before we can decide.
Lan: OK, that's an open item owned by Finance.
Hà: Also, the total outstanding points liability as of last quarter is
something only I can pull from the ledger.
Lan: Noted. Anything else?
Minh: The second rule we already agreed on: only the account holder can
redeem points. No transfers between accounts.
Hà: Agreed. That also matters for how we account for them.
Lan: Good. So decided rules are: one point per 10,000 VND rounded down,
and points are non-transferable. Still open: conversion rate, expiry,
and the outstanding liability figure.
Hà: One more finance-only item — whether points count as a discount or
a separate payment method for tax purposes. I'll confirm that too.
Lan: So, to recap, we have two rules locked and a few open items. Let's
make sure the app team gets the decided rules first, and we resolve the
open items before launch.
Minh: Agreed. I'll write up the ops view on expiry for the auditors.
Hà: And I'll bring the liability numbers to the next meeting.
Lan: Do we have a launch date yet?
Minh: Not from my side. We need the app work scheduled first.
Hà: Launch date is a business call, not mine to make.
Lan: Great. Let's meet again next week.
