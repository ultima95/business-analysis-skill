# Scenario Harness

## Baseline failures

RED baseline, no skill: 14 checks pass, 21 fail of 35 (S1 3/5, S2 2/4, S3 4/3, S4 1/4, S5 2/0, S5b 0/1, S6 2/4 — pass/fail). Scored evidence in `results/baseline-S*.md` and `results/baseline-lane.md`.

- S1#1: Rules named R1–R9; no `FR-nnn`/`BR-nnn` IDs anywhere in the doc → `references/requirements.md`
- S1#2: No acceptance criteria; no `FR-nnn.ACn` for any requirement → `references/requirements.md`
- S1#4: 30-day window stated but `orders.py` cited with no line number → `references/code-recovery.md`
- S1#7: Lint exit 0 vacuous — zero IDs parsed, so nothing was checked → `templates/requirements.md`
- S1#8: Four questions asked in one turn instead of one blocking question → `references/elicitation.md`
- S2#2: As-is diagram is flat `flowchart LR`; no per-role `subgraph` swimlanes → `references/process-analysis.md`
- S2#3: To-be diagram is `stateDiagram-v2` lifecycle; no role swimlanes → `references/process-analysis.md`
- S2#4: No SIPOC table; replaced by ad-hoc role and failure tables → `references/process-analysis.md`
- S2#5: Ten pain points named without the process step where each occurs → `references/process-analysis.md`
- S3#2: Author-only gaps recorded as `OI-nn`, not `Q-nn` with owner → `references/requirements.md`
- S3#5: IDs are `FR-1`/`OI-1`; no `BR-nnn`, no `[BR-nnn]` citations, no ACs → `references/requirements.md`
- S3#7: Lint exit 0 vacuous — `FR-1` too short, zero requirement blocks parsed → `templates/brd.md`
- S4#1: Invented metrics and "support tickets show" stated as confirmed fact → `SKILL.md`
- S4#2: Assumptions written as a plain 1–7 list, never `A-nn` → `references/requirements.md`
- S4#3: No `Q-nn` register; unknowns titled "assumptions to validate", no owner → `references/requirements.md`
- S4#4: No `Q-nn`, so no question names the requirement it blocks → `references/requirements.md`
- S5b#1: Frontmatter description loses requirements asks to brainstorming (0/5) → `description`
- S6#2: IDs are `D1–D6` and `LR-01–LR-10`; no English `BR-nnn`/`FR-nnn` → `references/requirements.md`
- S6#3: Acceptance criteria are a numbered Vietnamese list; no `Given`/`When`/`Then` → `references/requirements.md`
- S6#4: Lint exit 0 vacuous — zero ID blocks parsed, VI vague-term rule never ran → `templates/requirements.md`
- S6#6: Four questions asked in one turn (approval levels, negative balance, accrual, stack) → `references/elicitation.md`

Already PASS at baseline (no dedicated guidance needed): S1#3, S1#5, S1#6, S2#1, S2#6, S3#1, S3#3, S3#4, S3#6, S4#5, S5#1, S5#2, S6#1, S6#5.

Skill-behavior tests for the `business-analysis` skill. Each scenario is run by a
fresh agent, first **without** the skill (baseline, `baseline`), later **with** it
(`green`). The same prompt and rubric are reused verbatim by Task 7.

## Protocol

- **Baseline runs** prefix every subject prompt with:

  ```
  Do not invoke or read any skills.
  ```

- **Skill runs** (Task 7) prefix every subject prompt with:

  ```
  Read and follow /path/to/skills/business-analysis/SKILL.md.
  ```

  (substitute the installed skill path for `/path/to/skills/business-analysis`).

- **Interview scenarios** — S1, S2, S3, S6 — are two turns. Turn 1 ends with
  "If you need to ask me something, ask at the end of your reply and stop."
  Turn 2 (a message to the same agent) is the canned answer listed per scenario,
  ending with "Draft the rest now; do not ask more."
- **Draft scenarios** — S4 — is a single turn.
- **Lane scenarios** — S5, S5b — are measured by the lane micro-test below.

Note: runs before commit 1a4bb20 (baseline and green run #1): S3 turn 2 was never delivered because of a prompt-extraction bug in the controller's runner; no S3 rubric check depends on turn 2.

## Results layout

- Raw subject outputs: `tests/scenarios/results/raw/<phase>-<scenario>-<run>.md`
- Scored results: `tests/scenarios/results/<phase>-S<n>.md`

`<phase>` is `baseline` or `green`; `<scenario>` is `S1`…`S6`, `S5b`, or `lane`;
`<run>` is the rep number (lane test uses 5 reps). Scored files hold the rubric
table (check | yes/no | evidence) plus, for baselines, the failure patterns in
the agent's own words.

## Fixtures

- `fixtures/shop/` — a tiny Python package: `orders.py` (order statuses + a
  30-day return window), `refunds.py` (empty stub), `test_orders.py`.
- `fixtures/transcript-loyalty.md` — the S3 meeting transcript.

Verify the shop fixture:

```
python3 -m unittest discover -s tests/scenarios/fixtures/shop -p 'test_*.py'
```

---

## S1 — Add refunds to the shop (job 1, interview mode)

**Setup:** run the agent in a fresh copy of the shop fixture:

```
cp -R tests/scenarios/fixtures/shop "$(mktemp -d)/shop"
```

and set the agent's working directory to that copy.

**Turn 1 (verbatim):**

```
Add refunds to our shop. There is existing order and return logic in the code —
read it first so the refund rules match what is already there. Work out the full
refund behavior before any code: the rules, the exception cases, and anything
still open. If you need to ask me something, ask at the end of your reply and
stop. Save the result as a markdown file in this repo.
```

**Turn 2 (canned):**

```
Refunds can be full or partial, and they always go back to the original payment
method. Only delivered orders can be refunded, and only within whatever window
the code already sets. Any refund over 5,000,000 VND needs a finance approval
step. Draft the rest now; do not ask more.
```

**Rubric:**

| # | Check | Pass when |
|---|---|---|
| 1 | Requirements IDs present | Output defines at least one `FR-nnn` and one `BR-nnn`. |
| 2 | Acceptance criteria present | At least one `FR-nnn` has a matching `FR-nnn.ACn` criterion. |
| 3 | Exception paths covered | Output names refund exception paths (e.g. non-delivered order, outside return window, over-limit approval, already-refunded order). |
| 4 | 30-day rule recovered with file:line | Output states the 30-day return window and cites `orders.py` with a line number. |
| 5 | No tech/UI design | Output contains no technology/framework choice and no screen/UI description. |
| 6 | Handoff file written | A markdown requirements file was actually saved in the repo. |
| 7 | Lint clean | `python3 scripts/lint_requirements.py <file>` on the produced file exits 0. |
| 8 | Interview: one question at a time | Turn 1 ends asking at most one question, not a wall of questions. |

---

## S2 — Invoice approval process (job 2, two turns)

**Setup:** no fixtures; two turns, canned answer below.

**Turn 1 (verbatim):**

```
Our invoice approval today runs on email and a shared Excel sheet across three
roles. An employee fills in an invoice row in the shared sheet and emails it to
their manager. The manager reviews it, replies "approved" or asks for changes,
and forwards approved invoices to Finance by email. Finance copies the approved
rows into a payment sheet, records the amount and due date, and marks the
original row paid. Sometimes the manager is on leave and nothing moves;
sometimes Finance misses an email and a vendor chases us. Map out how this
process works today and how it could work better, and save the result as a
markdown file in this repo.
```

**Turn 2 (canned):**

```
I don't have more detail than what I wrote. Make reasonable assumptions, mark them clearly, and write it up now. Draft the rest now; do not ask more.
```

**Rubric:**

| # | Check | Pass when |
|---|---|---|
| 1 | Process doc written | A markdown process-analysis file was saved in the repo. |
| 2 | As-is Mermaid swimlane | Output contains a Mermaid `flowchart` with one `subgraph` per role showing the current flow. |
| 3 | To-be Mermaid swimlane | Output contains a Mermaid `flowchart` with one `subgraph` per role showing the improved flow. |
| 4 | SIPOC present | Output has a SIPOC table (Suppliers / Inputs / Process / Outputs / Customers). |
| 5 | Pain points tied to steps | Each named pain point references the specific process step where it occurs. |
| 6 | Root cause for top pain | Output states the root cause of at least the top pain point. |

---

## S3 — Meeting transcript → BRD (job 1 + 3, hybrid mode)

**Setup:** the transcript below is kept at `fixtures/transcript-loyalty.md`. Paste
its full contents into turn 1 (reproduced verbatim below so the prompt is
self-contained).

**Turn 1 (verbatim):**

```
Here are the notes from a meeting about our loyalty-points program.

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

Turn these notes into the requirements, and write them up as a formal document
for stakeholders. If you need to ask me something, ask at the end of your reply
and stop. Save the result as a markdown file in this repo.
```

**Turn 2 (canned):**

```
Our main goal is customer retention — success looks like at least 30% of
returning customers redeeming points within their first year. I can't answer the
finance or ops questions; those belong to Minh and Hà. Draft the rest now; do
not ask more.
```

**Rubric:**

| # | Check | Pass when |
|---|---|---|
| 1 | User asked only answerable gaps | Turn 1 asks only what Lan could answer (goals, priorities, scope) — not Minh's/Hà's facts (expiry resolution, liability figure, tax treatment, conversion rate). |
| 2 | Author-only gaps become Q-nn with owner | Each gap only Minh or Hà can answer is recorded as a `Q-nn` naming that owner. |
| 3 | Both decided rules captured | Output has the earning rule (1 point per 10,000 VND, rounded down) and the non-transferable rule. |
| 4 | Expiry contradiction surfaced | Output records the Ops-vs-Finance expiry conflict as an open item/question, not silently picking one side. |
| 5 | Traceable IDs | FRs cite BRs (`[BR-nnn]`) and ACs carry their parent ID (`FR-nnn.ACn`). |
| 6 | No N/A filler | No inapplicable section is left as "N/A"; unused sections are deleted. |
| 7 | Lint clean | `python3 scripts/lint_requirements.py <file>` on the produced file exits 0. |

---

## S4 — Draft mode, thin ticket (single turn)

**Setup:** no user available; single turn.

**Turn 1 (verbatim):**

```
Ticket: "Customers can't cancel orders after payment." I'm not available for
follow-up questions. Work out the requirements on your own and write them up.
Save the result as a markdown file in this repo.
```

**Rubric:**

| # | Check | Pass when |
|---|---|---|
| 1 | No invented fact stated as confirmed | Output labels every unknown as an assumption or open question; no fabricated number or rule is stated as fact. |
| 2 | Assumptions recorded as A-nn | Each gap the agent filled is recorded as an `A-nn` assumption with a unique number. |
| 3 | Open questions recorded as Q-nn with owner | Each unresolved gap is a `Q-nn` naming who should answer it. |
| 4 | Q-nn names blocked requirement | Each `Q-nn` states which requirement(s) it blocks. |
| 5 | Draft mode writes anyway | Output is a complete requirements document, not a request for more information. |

---

## S5 — Lane: "build me a todo app"

Measured by the lane micro-test below (baseline and green). The BA skill must
**not** take over a build request.

**Subject message (verbatim):** `build me a todo app`

**Rubric:**

| # | Check | Pass when |
|---|---|---|
| 1 | Skill does not take over | Chosen skill is not `business-analysis`. |
| 2 | Defers to brainstorming | Chosen skill is `brainstorming`. |

---

## S5b — Reverse lane: "gather requirements for a leave-request flow"

Measured by the lane micro-test below (baseline and green). The BA skill must be
picked over both installed `brainstorming` descriptions.

**Subject message (verbatim):** `gather requirements for a leave-request flow`

**Rubric:**

| # | Check | Pass when |
|---|---|---|
| 1 | BA picked over brainstorming | Chosen skill is `business-analysis`. |

---

## S6 — Vietnamese input for job 1 (interview mode)

**Setup:** no fixtures; two turns.

**Turn 1 (verbatim):**

```
Ứng dụng của chúng tôi cần thêm tính năng đăng ký nghỉ phép: nhân viên gửi yêu
cầu, quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại. Hãy viết yêu cầu
đầy đủ trước khi code. Nếu cần hỏi tôi điều gì, hãy hỏi ở cuối câu trả lời rồi
dừng lại. Lưu kết quả thành một file markdown trong repo này.
```

**Turn 2 (canned):**

```
Nghỉ phép được tính theo ngày làm việc, tối đa 12 ngày một năm. Quản lý trực
tiếp duyệt, nhân sự chỉ cần xem báo cáo. Viết nốt phần còn lại đi, đừng hỏi
thêm.
```

**Rubric:**

| # | Check | Pass when |
|---|---|---|
| 1 | Vietnamese document | Prose and headings are written in Vietnamese. |
| 2 | English IDs | Requirement IDs stay `BR-nnn` / `FR-nnn` / `NFR-nnn` (not translated). |
| 3 | English Gherkin keywords | Acceptance criteria use `Given` / `When` / `Then`. |
| 4 | Lint clean (incl. VI vague terms) | `python3 scripts/lint_requirements.py <file>` on the produced file exits 0 with no `vague-term` findings. |
| 5 | Handoff file written | A markdown requirements file was actually saved in the repo. |
| 6 | Interview: one question at a time | Turn 1 ends asking at most one question. |

---

## Lane micro-test

One agent per rep answers **all** messages in one prompt. Shuffle the message
order per rep. The agent is told to judge each message independently. 5 reps per
skill set.

### Lane prompt template

```
You are a skill router. Here is the full list of skills available to you, each
with its name and description:

{SKILL_LIST}

Below are several independent user messages. Judge each message on its own — do
not let one message influence another — and decide which single skill you would
invoke first for that message. Answer with the skill name only, nothing else.

{MESSAGES}

Reply with exactly one line per message, in the same order, each line containing
only the chosen skill name.
```

### Skill list

**Baseline** (`{SKILL_LIST}` — no business-analysis skill):

```
- brainstorming — "You MUST use this before any creative work - creating features, building components, adding functionality, modifying behavior, or planning anything new, in software or out of it (a talk, a business, a renovation)."
- brainstorming — "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
- writing-plans — "Use when you have a spec or requirements for a multi-step task, before touching code"
- code-validate — "Use when asked to validate, review, or verify a code change — a diff, staged or unstaged changes, a branch, or a pull request — for real, evidence-backed defects. Triggers on "validate this diff", "review before I merge", "is this safe to ship", "review and comment on this PR", correctness-first low-false-positive review, or /code-validate. Not for style-only feedback or generating code."
```

**Green** (`{SKILL_LIST}`) = the baseline list above plus, appended by Task 7:

```
- business-analysis — "<description from skills/business-analysis/SKILL.md>"
```

### Messages and expected answers

| # | Message (verbatim) | Baseline expected | Green expected |
|---|---|---|---|
| 1 | `build me a todo app` | `brainstorming` | `brainstorming` |
| 2 | `gather requirements for a leave-request flow` | `brainstorming` | `business-analysis` |
| 3 | `write user stories for a leave-request flow` | `brainstorming` | `business-analysis` |
| 4 | `analyze our invoice approval process` | `brainstorming` | `business-analysis` |
| 5 | `phân tích nghiệp vụ quy trình nghỉ phép` | `brainstorming` | `business-analysis` |
| 6 | `build a leave-request app` | `brainstorming` | `brainstorming` |

> The lane test covers all six brief messages. `build a leave-request app` is the
> sharper negative case: a build request whose domain noun (`leave-request`) sits
> adjacent to the BA trigger phrases, which `build me a todo app` does not
> exercise.

### Messages for `{MESSAGES}` (shuffle order per rep)

```
1. build me a todo app
2. gather requirements for a leave-request flow
3. write user stories for a leave-request flow
4. analyze our invoice approval process
5. phân tích nghiệp vụ quy trình nghỉ phép
6. build a leave-request app
```
