# green S4 — agent 1f220a1d-11d4-4850-a847-2c98ddf79665 (command-code/deepseek/deepseek-v4.1-flash)

[User] Read and follow /tmp/ba-skill-under-test/business-analysis/SKILL.md.

Ticket: "Customers can't cancel orders after payment." I'm not available for
follow-up questions. Work out the requirements on your own and write them up.
Save the result as a markdown file in this repo.
I'll start by loading caveman style and reading the skill.
[Activate skill]
[Read] null
[Thought] Job: feed dev work. Ticket: thin. Mode: draft (user not available). Need to read references.

Let me read the skill's references and templates.
Skill loaded. Job 1: feed dev work. Mode: Draft — user gone, no questions. Need refs + template.
[Read] null
[Shell] null
[Thought] Repo empty. Job 1, draft mode. Job 3? User said "write them up" — that's job 1 alone → requirements file. No BRD needed.

Check lint script and code-recovery maybe. Repo has no code, so skip code-recovery.

Let me read lint script to understand rules.
Repo empty — no code to recover rules from. Job 1 only, draft mode. Let me check lint rules.
[Read] null
[Thought] Now design the requirements. Order cancellation after payment.

Let me think properly as a BA.

Actors: Customer, Customer support agent, Finance/refunds team, Payment provider (external), Fulfillment/warehouse, Fraud/risk.

Ticket: "Customers can't cancel orders after payment."

Requirements scope: allow cancellation after payment, with refund, before fulfillment cutoff.

Key business rules:
- BR-001: Order may be cancelled only before it enters "Shipped" (i.e., in paid/processing state).
- BR-002: Cancellation before shipping triggers automatic full refund to original payment method.
- BR-003: Refund amount = amount captured minus already-incurred non-refundable charges? Careful not to invent. Make it assumption.
- BR-004: Only order owner or support agent with authorization can cancel.
- BR-005: Cancellation is a state transition, one-way.

Must avoid vagueness. And every BR must be cited by an FR else orphan-br lint finding.

Every FR needs ACs. NFRs need numbers + ACs.

Also need edge cases matrix, glossary, assumptions, open questions.

Output language: English (input is English).

File: docs/ba/2026-11-18-order-cancellation-after-payment-requirements.md

Let me draft carefully.

Actors table.

Scope in: cancel after payment, before shipment; refund; notification; audit.
Out of scope: partial cancellation of line items? Hmm — could be out of scope or Q. Let me make partial cancellation out of scope (A-nn) since ticket says "cancel orders". Actually better: assume whole-order cancellation only in this release, record as assumption A-01. Good.

Also out: returns/refunds after shipment, exchange, subscription cancellations.

Business rules:
- BR-001: An order is cancellable only while its state is Paid or Processing; once it reaches Shipped, cancellation is refused. (states glossary)
- BR-002: A successful cancellation of a paid order refunds the full captured amount to the original payment method.
- BR-003: Only the customer who placed the order, or a support agent holding the cancel-order permission, may cancel it.
- BR-004: Cancelling an order that is already Cancelled returns the existing cancellation record and creates no second refund (idempotent).
- BR-005: Every cancellation records actor, timestamp, order ID, refund amount, refund reference.
- BR-006: Refund must be initiated within ... hmm; make it a time window: refund initiated within 1 business day? That's a made-up number. Better as NFR with Q-nn? Lint requires numbers in NFR. I can put a number but it should be sourced... Draft mode allows A-nn basis. But red flag says a metric not in input written as fact is invented — must be A-nn or Q-nn. NFR targets inherently need numbers. Approach: put provisional NFR targets with an assumption row A-nn acknowledging provisional and a Q-nn to confirm. Hmm, but "every unknown goes in exactly one table". If I write the NFR with a number, that number is a filled value → assumption. So A-nn can cover a group of NFR targets? Better to give each NFR a number and one assumption row stating targets are provisional and set by ops, impact if false.

Actually cleaner: NFR targets referencing industry-typical; mark A-05 "NFR targets are provisional proposals ... pending ops confirmation; if different, the numbers in NFR-00x change, structure unchanged." That's honest.

Hmm but Q-nn also needs owners. Fine.

Let me not overdo. Let's build FRs:

FR-001: As a customer, I want to cancel a paid order before it ships, so that I'm not charged for something I no longer need. Fulfils BR-001, BR-003. Priority: Must.
AC1: Given order Paid, not Shipped, When customer cancels, Then order status becomes Cancelled and confirmation shows refund amount.
AC2: Given order Shipped, When customer cancels, Then system refuses and shows reason + returns path.
AC3: Given order already Cancelled, When customer cancels again, Then system returns original cancellation details, no second refund (BR-004).
AC4: Given an order belonging to another customer, When customer attempts cancel, Then refused with no state change (BR-003). — authorization negative.

FR-002: As a customer, I want the refund to go back to the payment method I paid with, so that I don't have to chase the money. Fulfils BR-002. Must.
AC1: Given paid order cancelled via card, When cancellation completes, Then refund of full captured amount is submitted to that card and reference recorded.
AC2: Given cancellation, When refund provider rejects it, Then order stays Cancelled and refund marked Failed with reason, and support queue notified. (exception path)

FR-003: As a customer, I want to see the refund status... Must/Should. Fulfils BR-005.
FR-004: system shall enforce state transition exactly once — idempotency/race. Could be under BR-004. 
FR-005: support agent cancels on behalf. Fulfils BR-003.
FR-006: audit record. Fulfils BR-005.
FR-007: notification email on cancellation + refund.

Should I include "concurrent cancel by customer and agent"? Edge case → BR-004/FR-004 AC.

NFRs: 
- NFR-001 performance: cancellation confirm ≤ 2 s p95 ... assumption.
- NFR-002 availability of payment provider dependency — recovery: refund retried.
- NFR-003 security: authorization, 100% of cancel attempts authenticated.
- NFR-004 privacy: PAN never stored/logged — 0 occurrences.
- NFR-005 auditability: records retained 7 years. Hmm invented. A-nn.

Keep NFR count manageable: 4.

Every NFR needs at least one AC.

Edge case matrix roles × states: Customer, Support agent, Payment provider (system) — states: Unpaid, Paid, Processing, Shipped, Delivered, Cancelled, Refund pending, Refund failed.

Glossary: Order statuses, capture, refund, cancellation window, etc.

Assumptions table A-01..A-06.
Open questions Q-01..Q-05 with owners and blocks.

Constraints: payment provider API, consumer protection law (Vietnam? unknown). Avoid inventing jurisdiction — say "applicable consumer-protection rules" generic; hmm still assertion. Put as Q-nn: which jurisdictions/laws?

Now the "Context" section needs Problem/Why now/Source input. Why now — not stated → A-nn or Q-nn. Put as A-nn: "Why now: not stated in ticket; treated as medium urgency" hmm. Better: state Problem from ticket, Why now: "not stated in the ticket; recorded as A-01" — but A-01 needs to be in table. Let me instead put in Context: "Why now: not stated in the ticket; see Q-01 for the driver." Good — Q-nn allows. But Context line shouldn't be vague prose. Fine.

Let me also check vocab vague terms list: avoid "fast", "quickly", "easy", "user-friendly", "simple", "flexible", "robust", "efficient", "etc.", "and/or", "as appropriate", "TBD", "normally". Careful with "etc." and "etc". Avoid entirely. "and/or" avoid.

Also "simple" — avoid word "simple".

Also note lint parses definition lines starting with optional list marker, bold ID, then ":" or "|". ACs like `- **FR-001.AC1**: ...` matches. Good.

Careful: BR definitions must be cited by an FR/NFR/AC block (citation inside FR block lines). Since FR line cites [BR-001], that counts (block_kind FR). Good.

Dangling refs: any ID mentioned anywhere must be defined. So don't cite FR-00x in assumptions prose... Assumption table row with "blocks FR-007" is fine only if FR-007 defined.

Also table rows with ID in first cell like `| A-01 | ... |` — does it parse as definition? _DEF_PATTERN requires ID followed by ":" or "|". `| A-01 |` → optional table `|`, then ID `A-01`... wait ID_RE requires BR|FR|NFR prefix. A-01 doesn't match. Q-01 doesn't match. Good, no duplicates.

But careful: assumptions table containing e.g. `NFR-004` in first cell? No.

Also the "Edge cases" table cells may cite FR ids — citations must be defined; fine.

Now also note: lint treats table rows as clearing `current` block, fine.

Write the doc. Also numbering: BRs first.

Let me write content.

Title: Order Cancellation After Payment — Requirements

Sections: Context, Actors and stakeholders, Scope, Business rules, Functional requirements, Non-functional requirements, Edge cases, Glossary, Assumptions, Constraints? template has no constraints section in requirements template (only assumptions, open questions). Keep to template: drop sections not applicable — Rules recovered from code (no code) → delete. Next step keep.

Actors:
| Customer | triggers cancellation, decides | authenticated buyer |
| Customer support agent | cancels on behalf, decides within policy | needs permission |
| Finance / refunds operator | resolves failed refunds | downstream of cancellation |
| Payment provider | executes refund, external | refund can fail or be delayed |
| Fulfilment / warehouse | ships order, sets Shipped state | cutoff that ends cancellability |

Business rules:
- BR-001: An order is cancellable while its status is Paid or Processing; cancellation is refused once status is Shipped or later (Shipped, Delivered, Completed).
- BR-002: Cancelling a paid order refunds the full captured amount to the original payment method; no partial refund is issued in this release.
- BR-003: Only the Customer who placed the order, or a Support agent holding the `cancel-order` permission, may cancel it.
- BR-004: A cancelled order accepts no further cancellation: repeated requests return the original cancellation record and submit no second refund.
- BR-005: Each cancellation stores order ID, actor ID, actor role, timestamp, refund amount, currency, refund reference, refund status.
- BR-006: A cancellation that fails at the refund step leaves the order Cancelled with refund status Failed, and places it in the support queue for manual resolution.

Hmm BR-006 vs FR-002.AC2 consistent.

- BR-007: A customer may cancel at most ... no. skip.

FRs:

- FR-001 customer self-cancel. Fulfils BR-001, BR-003. Must. AC1..AC4
- FR-002 refund to original method. Fulfils BR-002. Must. AC1, AC2 (provider reject → BR-006), AC3 (partial? no)
- FR-003 refund visibility: customer sees refund status and expected arrival. Fulfils BR-005. Should. ACs.
- FR-004 system shall enforce single cancellation under concurrent requests. Fulfils BR-004. Must. AC1: customer and agent cancel at same moment → exactly one cancellation, one refund.
- FR-005 support agent cancel on behalf with reason code. Fulfils BR-003, BR-005. Must. AC1, AC2 (agent without permission refused).
- FR-006 notification on cancellation/refund outcome. Fulfils BR-005? Better BR-002... Let me add BR-008: The customer is notified of cancellation and of the final refund outcome. Then FR-006 fulfils BR-008. But then BR-008 needs citation — fine.

Renumber BRs: 001 cancellable states, 002 refund full to original, 003 authorization, 004 idempotent single, 005 audit record, 006 refund failure handling, 007 notification.

- FR-007 admin/support visibility list of failed refunds? Could be Could. Maybe skip to keep tight. Add as Could? I'll include FR-007: support sees queue of failed refunds. Fulfils BR-006. Could. Hmm "queue" is a solution-ish UI. Rephrase: "The system shall make orders whose refund status is Failed retrievable by Support for manual resolution." Fine, not user-facing.

NFRs (Must/Should, numbers):
| NFR-001 | Must | Cancellation confirmation returned to the actor within 2 s at p95 for orders up to 100 line items |
| NFR-002 | Must | Refund submitted to provider within 5 minutes of cancellation for 99% of cancellations; failures retried 3 times with exponential backoff |
| NFR-003 | Must | 100% of cancellation requests authenticated; 0 cancellations by a role without cancel-order permission |
| NFR-004 | Must | 0 payment-card primary account numbers stored or logged; only provider refund reference retained |
| NFR-005 | Must | 100% of cancellations produce an audit record retained 7 years |

ACs for each NFR (need numbers).

Edge cases table.

Glossary: Order status, Captured, Cancellation, Refund, Refund reference, Cancel-order permission, Fulfilment cutoff.

Assumptions A-01..A-06:
A-01 whole-order cancellation only in this release; partial line-item cancellation out of scope. basis: ticket says "cancel orders", not items.
A-02 Paid = funds captured. 
A-03 Statuses in BR-001 exist or will exist in order model.
A-04 Refunds go to original payment method (common practice; if false refund needs payout-method step).
A-05 NFR numeric targets are provisional proposals; if ops sets different numbers only the target cells change.
A-06 Cancellation is one-way; no un-cancel/reinstate in this release.
A-07 Shipped is set by fulfilment and is reliable/real-time enough as cutoff. Hmm; maybe Q instead.

Open questions:
Q-01 What business event triggered this ticket and its target date? Owner: ticket author / Product owner. Blocks: all FRs for release scoping. → "all FRs for cancellation release" allowed per rules.
Q-02 Is partial cancellation of individual line items in scope now or later? Owner: Product owner. Blocks FR-001.
Q-03 Which consumer-protection rules and jurisdictions set a minimum cancellation window? Owner: Legal/compliance. Blocks BR-001, FR-001.
Q-04 Are shipping/handling charges refunded with the order total? Owner: Finance. Blocks BR-002, FR-002.
Q-05 What is the SLA for resolving a Failed refund? Owner: Finance ops. Blocks NFR-002, FR-007.
Q-06 Are refunds for cash-on-delivery / offline payments in scope? Owner: Finance. Blocks FR-002.

Constraints: template for requirements has no constraints section, but it's useful. Template "delete sections that don't apply" — adding is presumably ok? I'll add a short "Constraints" bullet list since gaps #8 requires. Keep it.

Constraints:
- Refund execution depends on payment provider API and its own settlement timing.
- Cancellation must not be possible after fulfilment has shipped the order — physical shipment cannot be recalled by this process.
- This analysis defines no architecture; solution design follows.

Careful: citations. "FR-001" cited in Q tables — defined. Good.

Edge cases matrix rows: Customer × Paid, Customer × Processing, Customer × Shipped, Customer × Cancelled, Customer × Refund failed, Support agent × Paid, Support agent × Shipped, Support agent × Cancelled, Payment provider(down) × Paid, System × concurrent.

Watch lint on edge table cells containing FR ids — fine.

Also avoid vague terms inside edge table? Vague check only applies to blocks (definition lines + continuations), not tables. Fine anyway.

Let me write the file.

Date: 2026-11-18.

One detail: FR statement form "As a <role>, I want <capability>, so that <outcome>. Fulfils [BR-001]. Priority: Must." Good.

Write now.
No code in repo, so no code-recovery. Writing the requirements doc.
[Edit] null
Now lint it.
[Shell] null
[Thought] Clean. But I should double-check counts and also verify semantics: "Rules recovered from code" — I wrote "Not applicable" — skill says delete sections that don't apply, never "N/A". So delete that section. Let me remove it.

Also check: no vague terms used in definitions. Fine.

Missing: job 1 handoff file only — good.

Let me delete the "Rules recovered from code" section.

Also count: BR 7, FR 7, NFR 5, AC: FR ACs: 5+3+2+2+3+2+2 = 19; NFR ACs: 1+2+1+1+1 = 6 → total 25. Q: 7. A: 8.

Fix the section deletion.
Lint clean. Removing the `Not applicable` section — skill says delete, not "N/A".
[Edit] null
[Shell] null
[Thought] Done. Report in caveman full style per skill report format: file path, counts, top 3 risks/open questions, next step.

Counts: BR 7, FR 7, NFR 5, AC 25, open questions 7, assumptions 8.

Top 3 risks: refund timing/partial refunds unknown (BR-002 full refund, Q-04 shipping charges), window cutoff Shipped reliability, no volume target.

Keep terse but clear.
`docs/ba/2026-11-18-order-cancellation-after-payment-requirements.md` — lint clean (0 findings).

| ID | Count |
|---|---|
| BR | 7 |
| FR | 7 |
| NFR | 5 |
| AC | 25 |
| Q | 7 |
| A | 8 |

Mode: Draft. User unavailable → every unknown became A-nn or Q-nn, no invented facts. Repo empty → no code-recovered rules.

Top 3 risks:
1. **Q-04 / BR-002** — full captured amount refunded. If shipping and handling charges excluded, refund math and FR-002 change.
2. **BR-001 cutoff** — `Shipped` is the hard end of cancellation window. Depends on fulfilment status being accurate and timely; stale status = refunds on shipped goods or false refusals.
3. **Q-07 / NFR-001-002** — zero volume data in ticket. All NFR numbers provisional (A-07), need Ops sizing.

Next: brainstorm solution with this file as context, then writing-plans.
