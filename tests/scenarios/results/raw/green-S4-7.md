# green S4 — agent 85fabda3-0c37-4723-a72e-6cb40b6b2e66 (command-code/deepseek/deepseek-v4.1-flash)

[User] Read and follow /tmp/ba-skill-under-test/business-analysis/SKILL.md.

Ticket: "Customers can't cancel orders after payment." I'm not available for
follow-up questions. Work out the requirements on your own and write them up.
Save the result as a markdown file in this repo.
I'll start by activating caveman mode and reading the skill spec.
[Activate skill]
[Read] null
[Thought] The skill is job 1 (feed dev work). Let me read references and templates.

User says not available for follow-up questions → Draft mode.

Let me read the reference files and template.
Skill loaded. Ticket = job 1 (requirements). User unavailable → Draft mode. Let me read the reference + template files.
[Read] null
[Thought] Now I need to check the repo — the skill says job 1 inside a repo → recover current rules via code-recovery with file:line. Let me explore the repo.

Repo is /private/tmp/ba-scen-green-7/S4. Only commit "init". Let me look.
Skill says job 1 inside repo → recover current rules from code with `file:line`. Let me inspect repo.
[Shell] null
[Thought] Empty repo — no code to recover rules from. So job 1, draft mode, no code recovery possible.

Need write docs/ba/2026-11-18-order-cancellation-after-payment-requirements.md

Ticket: "Customers can't cancel orders after payment."

Draft mode: every unknown becomes A-nn or Q-nn. Ticket is one stakeholder's claim.

Must be careful: no invented facts. Every metric → A-nn/Q-nn. NFR needs number; lint requires a digit in NFR definition or AC. So can put number as working value citing A-nn.

Let me design requirements set. Domain: order cancellation after payment → refund.

Business rules:
- BR-001: Cancellation allowed by customer while order in a pre-fulfilment state (paid, not yet shipped). Hmm — the state names are invention? Ticket says "after payment". Terms: paid, fulfilment. Need glossary. I should be careful to mark inferred things as assumptions.

Let me plan the doc structure per template, deleting non-applicable sections. Which sections apply? Context, Actors, Scope, Business rules, FRs, NFRs, Edge cases, Glossary, Assumptions, Open questions, Next step. "Rules recovered from code" — no code, so delete that section.

Let me write good content.

Context:
- Problem: quoted ticket.
- Why now: not stated → A or omit. Template requires. I can say "Not stated in the ticket" — but red flag: metric/stakeholder etc not in input written as fact. Saying "not stated" is fine.
- Source input: the ticket text.

Actors/stakeholders table:
- Customer (the ticket's "Customers") — requests cancellation; basis: quote.
- Customer support agent — inferred (who handles requests when self-service not available) → A-01 basis.
- Finance / payments team — processes refund → A-02.
- Warehouse / fulfilment team — must stop picking → A-03.
- Product owner — decides policy → Q-nn owner, not actor fact. Actually owner can be role placeholders.

Keep actor rows with Basis column: "input quote" or "A-0n".

Scope in/out.

Business rules — must be cited by FRs, else orphan-br lint. And no vague terms.

BR-001: A customer may cancel an order at any time between payment confirmation and the moment the order leaves the warehouse. Hmm "leaves warehouse" — invention but as rule it's a working decision; should be A-nn based. Rules themselves can encode assumptions if cited? Red flag says a rule not in input written as fact = invented. Safer: make each rule explicit about basis? The template BR line format doesn't have a Basis column. But I can add "Basis: A-02" prose? The canonical form is `- **BR-001**: <rule>.` Extra sentence after is fine but may be part of block text. I could append "Basis: A-02." That keeps traceability and avoids presenting as confirmed. Good approach — and lint won't complain.

Let me write rules:

- BR-001: A customer may request cancellation of a paid order only while the order has not yet been handed to the carrier. Basis: A-02 (cut-off chosen as working policy); ticket states only "after payment".
- BR-002: An order cancelled after payment returns the full amount the customer paid, including any payment fee charged to the customer. Hmm invented. Basis A-03.
- BR-003: A paid order that has already been handed to the carrier cannot be cancelled; the customer is directed to the returns process instead. Basis A-02/A-04.
- BR-004: A refund issued for a cancelled paid order goes back to the original payment method only. Basis A-05.
- BR-005: Each cancellation is recorded with the actor, the timestamp, the reason... reason capture — invented. Could be Q-nn. Maybe BR-005: A cancellation request is rejected when the order is already cancelled or refunded (idempotency). Basis A-06.
- BR-006: Cancellation of a paid order requires refund amount ≤ captured amount, partial refunds only when an order is partially fulfilled. Too much.

Keep 5-6 rules, each cited.

FRs (one story each, INVEST, Priority):
- FR-001: As a customer, I want to cancel a paid order from my order history before it ships, so that I am not charged for goods I no longer want. Fulfils BR-001. Priority: Must. ACs: happy path, not-yet-paid case?, already shipped, already cancelled, cancellation window closed.
- FR-002: As a customer, I want to see the refund amount and destination before confirming cancellation, so that I know what I will get back. Fulfils BR-002, BR-004. Priority: Must.
- FR-003: As a customer, I want written confirmation of my cancellation and refund, so that I have proof of the amount and expected date. Fulfils BR-007? Need BR for notification timing. Maybe BR-007: customer is informed of cancellation outcome within N minutes... that's NFR/BR.
- FR-004: As a support agent, I want to cancel a paid order on a customer's behalf... Priority: Should. Fulfils BR-001, BR-005.
- FR-005: The system shall reject a cancellation request for an order already cancelled or fully refunded with a specific outcome message. Fulfils BR-006. Priority: Must.
- FR-006: The system shall route paid orders that have already been handed to the carrier to the returns process instead of cancelling. Fulfils BR-003. Priority: Must.
- FR-007: As a finance user, I want every cancelled paid order to appear in a refund queue with its amount, so that refunds are not lost. Fulfils BR-002. Priority: Must.

Maybe also audit: FR-008 The system shall record actor, timestamp, prior state, refund amount for each cancellation. That's more NFR auditability. But template has NFR row for auditability. Hmm NFR must have number. Could have NFR for audit retention 7 years — invented number, Q-nn basis.

NFRs:
| NFR-001 | Must | Cancellation confirmation is recorded within 5 s ... | A-07 |
Let me craft with digits:
- NFR-001 Performance: p95 end-to-end cancellation request completes within 3 s at 50 concurrent requests. Basis A-07.
- NFR-002 Availability: cancellation path available 99.5% per calendar month. Basis A-08.
- NFR-003 Audit: every cancellation and refund event retained 7 years and readable by finance and audit roles. Basis A-09.
- NFR-004 Security/authorization: only the order's owning customer or a support agent may cancel; 100% of unauthorized attempts rejected. Basis BR-005 / A-10.
- NFR-005 Privacy: cancellation records show only masked payment instrument (last 4 digits) to support agents. Basis A-11.

Each NFR needs at least one AC with a number.

Edge cases matrix: roles × states. States: created (unpaid), paid, picking/packed, shipped, delivered, cancelled, refunded, refund failed. Keep matrix focused.

Glossary: order, paid order, cancellation, refund, capture, fulfilment cut-off, carrier handover, original payment method, support agent, finance user, refund queue.

Assumptions table A-01..A-11 with basis/impact.

Open questions Q-01.. with owner + blocks. Owners must be roles since no names known — role is fine.

Q-01: What is the exact cut-off for cancellation — before carrier handover, before picking starts, or a fixed hour window after payment? Owner: Product owner. Blocks FR-001, FR-004.
Q-02: Which orders are in scope: all payment methods / all channels? Owner: Product owner. Blocks all FRs.
Q-03: Partial cancellation of a multi-item order in scope? Blocks FR-002, FR-007.
Q-04: Who bears payment-gateway fee on refund? Blocks FR-002.
Q-05: Refund SLA to customer (business days) — blocks FR-003.
Q-06: Should customers supply a reason? blocks FR-001/FR-004.
Q-07: Priority order when warehouse already picked but not handed over? Hmm covered by Q-01.
Q-08: Guest checkout orders (no account) — blocks FR-001.

Number of each: BR 7, FR 8, NFR 5, AC ~20, Q ~7, A ~11.

Now careful about lint:
- Every FR/NFR needs AC.
- Every BR cited by FR/NFR/AC.
- No dangling refs.
- No duplicates.
- Vague terms: avoid "fast", "quickly", "easy", "simple", "flexible", "robust", "efficient", "etc.", "and/or", "as appropriate", "TBD", "normally", "user-friendly". Careful with word "easy" — avoid. Watch "simple".
- NFR needs digits in definition or ACs.

Also careful: definition lines must be formatted `- **BR-001**: ...`. And AC lines `- **FR-001.AC1**: Given...`. Blocks terminate at blank line or heading or table line. Continuation lines under a definition count in the block, which affects vague-term scanning and also citations. Fine.

Careful: if I write "- **BR-001**: ... Basis: A-02." on same line, the "A-02" isn't an ID pattern (only BR/FR/NFR), no conflict.

But careful: writing "Fulfils [BR-001]. Priority: Must." — citation of BR-001 in FR block → counts as cited. Good.

One more lint nuance: AC block text with "BR-00x" citations counts as citing BR (block_kind AC). Good.

Also "orphan-br" — every BR needs citation from FR/NFR/AC. I'll make sure.

Another nuance: `_DEF_PATTERN` parses a line whose first token is ID followed by `:` or `|`. In the Assumptions table, rows start `| A-01 | ...` — A-01 not in ID_RE, fine.

Careful in glossary/edge tables: no BR/FR at line start.

Watch: in the edge-case matrix table, if I write "FR-..." cells, they'd be citations — fine since defined.

Now dates: today 2026-11-18. Filename: docs/ba/2026-11-18-order-cancellation-after-payment-requirements.md

Language: input English → English doc.

Also the skill wants: draft mode — "write the document anyway; every unknown becomes an A-nn or Q-nn". Good. Also mention mode? The doc could note "Mode: draft (no follow-up available)". Yes in context.

Also: "Job 1 ends by naming the handoff file and pointing to brainstorming / writing-plans". Next step section: "Brainstorm the solution with this file as context" — mention brainstorming skill then writing-plans.

Let me be careful with red flags: no invented stakeholder names, no invented company/system names. Use roles only. Any statement about "the platform" etc. avoided.

Also should I note that requirements avoid solution design (no UI/screens/schema). Yes keep capability-level: "from the order detail page" = screen choice — avoid. Say "from their order record" — hmm "order record" is data. Keep neutral: "cancel a paid order themselves".

FR-002: "see the refund amount and destination before confirming" — that is interaction design-ish but it's a need, acceptable (not a screen). Keep.

Now write it.

Let me craft detailed ACs.

FR-001 As a customer, I want to cancel a paid order before its fulfilment cut-off, so that I am not charged for goods I no longer want. Fulfils [BR-001]. Priority: Must.
- AC1: Given my order is paid and has not passed the fulfilment cut-off, When I confirm cancellation, Then the order status becomes Cancelled and my refund is recorded.
- AC2: Given my order is paid and has already passed the fulfilment cut-off, When I request cancellation, Then the cancellation is refused and I am shown the reason and the alternative path (returns).
- AC3: Given my order is paid and already cancelled, When I request cancellation again, Then no second cancellation or refund is recorded.
- AC4: Given my order is not yet paid, When I request cancellation, Then the order is cancelled without any refund record.
  Hmm that's an "unpaid" case; maybe belongs elsewhere but fine.
- AC5: Given I am signed in as a customer who does not own the order, When I request cancellation, Then the request is refused. (authorization) — cite BR-005.

Let's structure BRs:

- BR-001: A paid order may be cancelled by the customer only before the fulfilment cut-off; at or after the cut-off the cancellation is refused. Basis A-01 (cut-off definition Q-01).
- BR-002: A cancelled paid order is refunded the full amount captured for that order. Basis A-02.
- BR-003: When the order has already been handed to the carrier, cancellation is refused and the customer is directed to the returns path. Basis A-03.
- BR-004: A refund for a cancelled paid order is issued to the original payment method only. Basis A-04.
- BR-005: Only the customer who placed the order, or a support agent acting on a verified request, may cancel it. Basis A-05.
- BR-006: A cancellation request on an order already cancelled or fully refunded has no effect and records no additional refund. Basis A-06.
- BR-007: Every cancellation of a paid order produces exactly one refund entry in the refund queue. — hmm "exactly one" good testable. Basis A-07. Cited by FR-007.

Maybe BR-008 refund amount never exceeds captured amount — cited by FR-002.

FRs:
- FR-001 customer cancel before cut-off (BR-001, BR-005)
- FR-002 customer sees refund amount + destination before confirming (BR-002, BR-004)
- FR-003 customer receives confirmation with amount and expected arrival (BR-002)
- FR-004 support agent cancels on behalf (BR-001, BR-005)
- FR-005 system refuses cancellation at/after cut-off and points to returns (BR-001, BR-003)
- FR-006 system treats repeat cancellation as no-op (BR-006)
- FR-007 finance refund queue entry per cancelled paid order (BR-007)
- FR-008 system shall cap refund at captured amount (BR-008)

Hmm FR-008 user-facing? Non-user-facing: "The system shall reject a refund whose amount exceeds the amount captured for the order." Priority Must. AC: Given captured 100.00, when refund computed 120, then rejected and flagged. Fine — number present.

NFRs as above; ensure digit in def or AC. I'll include digits in target cells.

Now edge case matrix (roles × states): columns Create/Read/Update/Delete are odd for orders; skill says keep cells revealing rules. I'll do 4 rows.

Roles: Customer (owner), Customer (non-owner), Support agent, Finance user. States: Unpaid, Paid (before cut-off), Paid (after cut-off, with carrier), Cancelled, Refunded, Refund failed.

I'll write matrix with cells concise.

Assumptions: A-01 cut-off = carrier handover... careful: BR-001 says cut-off; A-01 defines cut-off as the moment the carrier's handover scan is recorded. A-02 full refund incl. fees. etc.

List:
| A-01 | The fulfilment cut-off is the moment the carrier records handover of the parcel; before that the order can be cancelled. | Ticket says only "after payment"; Q-01 asks the owner to confirm; if the cut-off is earlier, AC2 of FR-001 and FR-005 change |
| A-02 | Refund = full amount captured, no deduction for restocking or handling fee. | Not stated; if a fee applies, FR-002 and FR-008 need a fee line |
| A-03 | Orders already handed to the carrier are outside cancellation and follow the existing returns path. | Not stated; if in scope, FR-005 becomes a cancel-with-recall flow |
| A-04 | Refund returns to original payment method only. | Not stated, matches common practice; if a credit/voucher option is required, FR-002 gains a destination choice |
| A-05 | Cancellation authority = order owner customer or support agent on a verified request. | Ticket names only "customers"; if a manager approval tier is required FR-004 gains a step |
| A-06 | Cancellation requires an order to be paid; unpaid orders are cancelled with no refund. | Not stated; if unpaid path differs, FR-006 changes |
| A-07 | One refund entry per cancelled paid order; later refund status changes update that entry rather than adding rows. | Not stated; if one entry per item is required, FR-007 changes |
| A-08 | Only full-order cancellation is in scope for the first release. | Not stated; Q-03 asks; partial cancellation would add a per-item refund rule |
| A-09 | Payment methods in scope: card and wallet payments processed by the existing payments provider; bank transfer excluded. Hmm inventing provider. Better: "All payment methods that support a refund to the original method are in scope; methods without that capability are out of scope." Basis A-09.
| A-10 | The customer is informed of the cancellation outcome within 5 minutes of the request. | working value for NFR-001; if the business needs a different number Q-05 owns it |

Q table:
| Q-01 | Where exactly is the cancellation cut-off: carrier handover, start of picking, or a fixed number of hours after payment? | Product owner | FR-001, FR-004, FR-005 |
| Q-02 | Which order channels and payment methods must support cancellation in this release? | Product owner | all FRs for cancellation |
| Q-03 | Is partial cancellation of a multi-item paid order required in this release? | Product owner | FR-002, FR-007 |
| Q-04 | Who bears the payment provider's fee on a refund: the business or the customer? | Finance lead | FR-002, FR-008 |
| Q-05 | How many business days after cancellation must the refund reach the customer? | Finance lead | FR-003, NFR-001 |
| Q-06 | Must the customer give a cancellation reason, and is it mandatory for any order value? | Product owner | FR-001, FR-004 |
| Q-07 | Do guest-checkout orders without an account need a cancellation path in this release? | Product owner | FR-001 |
| Q-08 | What is the required audit retention period for cancellation and refund records? | Compliance owner | NFR-003 |

Wait: "blocks FR-00x" — must include requirement ID. "all FRs for cancellation" allowed per elicitation. OK.

Note "duplicate-id" issue: Q references FR IDs → citations, they're defined. Good.

Now the vague-terms check: avoid words: fast, quickly, easy, user-friendly, simple, flexible, robust, efficient, etc., and/or, as appropriate, TBD, normally, plus VI words. I must avoid "and/or" — say "or". Avoid "etc." — don't use. Careful in scope lists "etc." no.

Also avoid writing "Normally". Fine.

Make sure NFR target cells have digits — yes.

Also lint: `dangling-ref` for any BR/FR/NFR mentioned that isn't defined. Eg "BR-005" defined. Good.

Also careful: the AC lines that mention "(returns)" fine.

Careful about not creating BR references in prose sections outside FR blocks (e.g., glossary) — citations fine if defined.

Now write file. Path: /private/tmp/ba-scen-green-7/S4/docs/ba/2026-11-18-order-cancellation-after-payment-requirements.md

Then run lint with the full paths of script and doc.

Let me write carefully.

Also mention in Context: mode note "Written in draft mode: no follow-up access to the requester; unknowns recorded as A-nn/Q-nn."

The "Why now" — not stated. Write "Not stated in the ticket; no deadline, cost figure, or incident is given. A-nn? " Actually it's a fact about input, fine: "Not stated in the ticket — no deadline, incident, or cost figure supplied."

Scope in/out lists.

Also: don't include "Rules recovered from code" section since repo has no code — delete (skill: delete sections that don't apply; no "N/A").

Also the "Next step" section.

Edge case matrix header per template: Actor | Entity state | Create | Read | Update | Delete.

Write now. Also number counts afterwards.

Careful when writing `- **FR-002.AC1**: Given ... Then the confirmation shows the full refund amount of the order and the original payment method masked to its last four characters.` "masked to last four characters" is boundary detail but that's a rule — BR-004 + A-11. Fine.

Let me ensure every NFR AC includes numbers.

NFR-001: | Must | p95 end-to-end cancellation request ≤ 3 s at 50 concurrent requests | A-10 working value; Q-05 confirms |
  AC1: Given 50 concurrent cancellation requests, When each is submitted, Then p95 completes within 3 s.
  Need digit in def or AC — yes.
NFR-002 Availability: 99.5% per calendar month, measured on the cancellation path.
  AC1: Given a calendar month, When uptime is measured, Then cancellation path availability is at least 99.5%.
NFR-003 Auditability: every cancellation and refund event retained 7 years.
  AC1: Given a cancellation 7 years old, When finance or audit role queries the record, Then the actor, timestamp, prior status, and refund amount are returned.
NFR-004 Security: 100% of cancellation attempts by non-owner non-agent are refused.
  AC1: Given a signed-in customer who does not own the order, When they submit cancellation, Then the request is refused and the refusal is recorded.
  Hmm AC needs number? unmeasurable-nfr requires digit in def or AC; def has 100%. Good.
NFR-005 Privacy: support agents see payment instrument masked to last 4 digits in 100% of cancellation records.
  AC1: Given a support agent opens a cancellation record, When they view it, Then the instrument shows only the last 4 digits.

Basis cells: "A-10", "A-12"... let me number assumptions consistently and make NFR basis reference actual A-IDs.

Let me finalize A list:
A-01 cut-off definition
A-02 full refund, no fee deduction
A-03 carrier-handover orders excluded → returns
A-04 original payment method only
A-05 authority = owner or support agent
A-06 unpaid orders cancel with no refund
A-07 one refund entry per cancelled order
A-08 full-order cancellation only in first release
A-09 payment methods limited to those supporting refund to original method
A-10 p95 target 3 s at 50 concurrent (working value for NFR-001)
A-11 instrument masked to last 4 digits
A-12 availability 99.5% (working value NFR-002)
A-13 audit retention 7 years (working value NFR-003)
A-14 refund reaches customer within 5 business days (working value FR-003)

NFR basis: NFR-001 → A-10; NFR-002 → A-12; NFR-003 → A-13; NFR-004 → BR-005? basis column says "input quote, A-nn, or Q-nn". Use A-05. NFR-005 → A-11.

FR-003 AC1 mention 5 business days → can cite A-14 in prose? Not necessary, but helpful: "then the confirmation states an expected arrival within 5 business days". Fine.

Careful vacancy: vague term check on words like "flexible" — I use "flexible"? no.

Write the doc.

Also add edge case matrix cells: careful not to start a table cell line with an ID — not applicable.

One risk: lint treats table lines as ending a block, and _DEF_PATTERN also matches table row starting `| BR-001 | ...`. But we only use BR definitions as bullets. In the NFR table, rows start `| NFR-001 | Must | ...` → matches `|` def pattern with `|` after ID. Good, that's the intended canonical form.

In assumptions table rows start `| A-01 |` — no match.

Edge: in the "Blocks" column I write "FR-001, FR-004" — citations to already-defined IDs. Good.

Now writing.
Repo empty — no code, so no as-is rules to recover. Job 1, draft mode (no follow-up). Writing the doc now.
[Edit] null
[Thought] I noticed a duplicate ID bug: FR-007.AC1 used twice. Fix to AC2. Then run lint.

Also check BR-003 offset by FR-005 citation structure — FR-005 is one FR citing BR-001 and BR-003, okay. BR-008 cited by FR-008. All BRs cited? BR-001 (FR-001, FR-004, FR-005), BR-002 (FR-002, FR-003, FR-007), BR-003 (FR-005), BR-004 (FR-002), BR-005 (FR-001, FR-004), BR-006 (FR-006), BR-007 (FR-007), BR-008 (FR-008). Good.

Fix dup then lint.
Caught a duplicate AC id. Fixing before lint.
[Edit] null
Now lint.
[Shell] null
[Thought] Lint clean. Check orphan BR: BR-001..008 all cited? Lint says clean, so yes.

Report format: file path, counts, top 3 risks/open questions, next step.

Counts: BR 8, FR 8, NFR 5, AC: let me count. AC1-FR001 5, FR002 2, FR003 2, FR004 3, FR005 2, FR006 2, FR007 2, FR008 2 = 20. NFR AC 5. Total AC 25. Let me verify quickly.
[Shell] null
[Thought] The FR count 28 is inflated by AC lines matching `FR-001.AC1` because my regex `^\s*(-|\|)\s*(\*\*)?FR-[0-9]{3}` matches FR-001.AC1 too. Let me count properly.
FR count inflated by AC lines. Recounting properly.
[Shell] null
[Thought] Counts: BR 8, FR 8, NFR 5, AC 25... let me check AC count: 25 seems high. Let me count per FR: FR-001 has 5, FR-002 2, FR-003 2, FR-004 3, FR-005 2, FR-006 2, FR-007 2, FR-008 2 = 20, NFR 5, total 25. Yes correct.

Now, let me double check doc quality. A concern: NFR table rows use format `| NFR-001 | Must | ... |` — lint accepted. Good.

Also glossary — fine. Let me verify no vague terms slipped (lint passed).

One issue: Edge case table row "Customer (not owner) | Any state" — fine.

Also note BR-008 says basis A-02 — good.

Should I double-check FR-003.AC1 said "within 5 business days" and A-14 says working value for FR-003.AC1 but basis column of A-14 references Q-05 — good.

Also FR-007 "Fulfils [BR-007], [BR-002]" fine.

Let me double check the FR count claim on report and mention no code recovered since repo empty.

Also check for possible issue: template asks "Rules recovered from code" section — repo empty, so omitted (delete sections that don't apply). Good.

Let me quickly verify file renders okay - maybe check the assumptions table isn't missing A-14 in table (it is there). Good.

Report output: path, counts, top 3 risks/open questions, next step.

Should I git commit? User didn't ask. No commit.

Let me verify the doc one more time briefly for internal contradictions: BR-001 says cut-off, A-01 assumes handover. FR-005.AC1/AC2 consistent.

One more check: NFR-004 basis A-05 — okay.

Lint clean. Done. Report caveman style.

Counts: BR 8, FR 8, NFR 5, AC 25, A 14, Q 8.

Let me confirm AC count exactly 25 with grep already done. Yes.

Top 3 risks: cut-off undefined (Q-01), refund fee/timing (Q-04/Q-05), partial cancellation + channels (Q-02/Q-03).

Provide brief report.
Lint clean. Writing done.

**File:** `docs/ba/2026-11-18-order-cancellation-after-payment-requirements.md`

**Counts:** 8 BR · 8 FR · 5 NFR · 25 AC · 14 assumptions · 8 open questions

**Mode:** draft — you unavailable, so no interview. Every gap became an `A-nn` or `Q-nn` row. Repo empty (no code), so no as-is rules recovered; "Rules recovered from code" section dropped.

**Top 3 risks:**
1. **Q-01 — cut-off undefined.** Ticket says only "after payment". Whole shape of FR-001/004/005 hinges on whether cut-off = carrier handover, start of picking, or fixed hours after payment.
2. **Q-04 / Q-05 — money terms missing.** Who eats payment-provider refund fee, and how many business days until refund lands. Both drive FR-002, FR-003, FR-008. I set 5 business days as A-14 working value.
3. **Q-02 / Q-03 — scope unset.** No info on channels, payment methods, or whether partial cancellation of multi-item orders is required. Assumed whole-order-only (A-08).

Worth flagging: 14 assumptions is high for one-line ticket. Most load-bearing are A-01 (cut-off = handover), A-02 (full refund, no fee), A-04 (refund to original method only).

**Next step:** brainstorming with this file as context, then writing-plans.
