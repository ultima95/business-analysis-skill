# Baseline lane micro-test (S5, S5b) — skill routing without `business-analysis`

| Field | Value |
|---|---|
| Phase | baseline (no `business-analysis` in skill list) |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Reps | 5 |
| Raw logs | `raw/baseline-lane-<rep>.md`, order per rep in `raw/baseline-lane-<rep>.order` |

## Per-rep answers

Each `.order` file lists the README message number (1–6) at each prompt position. Answers are
mapped back to messages through it.

### rep1 — agent `3600ef15-f09f-4d30-8613-13f7e87a3581`

Order: 5, 6, 1, 4, 3, 2. Replies (`raw/baseline-lane-1.md`, last 6 lines), position → message:

| Position | Message | Answer |
|---|---|---|
| 1 | 5 `phân tích nghiệp vụ quy trình nghỉ phép` | `brainstorming` |
| 2 | 6 `build a leave-request app` | `brainstorming` |
| 3 | 1 `build me a todo app` | `brainstorming` |
| 4 | 4 `analyze our invoice approval process` | `brainstorming` |
| 5 | 3 `write user stories for a leave-request flow` | `brainstorming` |
| 6 | 2 `gather requirements for a leave-request flow` | `brainstorming` |

### rep2 — agent `738597f3-6dc3-433f-97f1-c30a99d9b7b2`

Order: 4, 5, 6, 3, 1, 2.

| Position | Message | Answer |
|---|---|---|
| 1 | 4 `analyze our invoice approval process` | `brainstorming` |
| 2 | 5 `phân tích nghiệp vụ quy trình nghỉ phép` | `brainstorming` |
| 3 | 6 `build a leave-request app` | `brainstorming` |
| 4 | 3 `write user stories for a leave-request flow` | `brainstorming` |
| 5 | 1 `build me a todo app` | `brainstorming` |
| 6 | 2 `gather requirements for a leave-request flow` | `brainstorming` |

### rep3 — agent `71dd4aaf-d40a-48d1-bcf5-f338889d7065`

Order: 3, 5, 1, 4, 2, 6.

| Position | Message | Answer |
|---|---|---|
| 1 | 3 `write user stories for a leave-request flow` | `brainstorming` |
| 2 | 5 `phân tích nghiệp vụ quy trình nghỉ phép` | `brainstorming` |
| 3 | 1 `build me a todo app` | `brainstorming` |
| 4 | 4 `analyze our invoice approval process` | `brainstorming` |
| 5 | 2 `gather requirements for a leave-request flow` | `brainstorming` |
| 6 | 6 `build a leave-request app` | `brainstorming` |

### rep4 — agent `f0a5780f-ce76-4461-85a2-23bfae675fad`

Order: 4, 1, 5, 2, 6, 3.

| Position | Message | Answer |
|---|---|---|
| 1 | 4 `analyze our invoice approval process` | `brainstorming` |
| 2 | 1 `build me a todo app` | `brainstorming` |
| 3 | 5 `phân tích nghiệp vụ quy trình nghỉ phép` | `brainstorming` |
| 4 | 2 `gather requirements for a leave-request flow` | `brainstorming` |
| 5 | 6 `build a leave-request app` | `writing-plans` |
| 6 | 3 `write user stories for a leave-request flow` | `brainstorming` |

### rep5 — agent `bf2acbfb-92b8-491b-8408-7caacd851051`

Order: 6, 3, 2, 5, 1, 4.

| Position | Message | Answer |
|---|---|---|
| 1 | 6 `build a leave-request app` | `brainstorming` |
| 2 | 3 `write user stories for a leave-request flow` | `brainstorming` |
| 3 | 2 `gather requirements for a leave-request flow` | `brainstorming` |
| 4 | 5 `phân tích nghiệp vụ quy trình nghỉ phép` | `brainstorming` |
| 5 | 1 `build me a todo app` | `brainstorming` |
| 6 | 4 `analyze our invoice approval process` | `brainstorming` |

## Tally

| # | Message | expected (baseline) | rep1 | rep2 | rep3 | rep4 | rep5 | matches |
|---|---|---|---|---|---|---|---|---|
| 1 | `build me a todo app` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | 5/5 |
| 2 | `gather requirements for a leave-request flow` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | 5/5 |
| 3 | `write user stories for a leave-request flow` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | 5/5 |
| 4 | `analyze our invoice approval process` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | 5/5 |
| 5 | `phân tích nghiệp vụ quy trình nghỉ phép` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | 5/5 |
| 6 | `build a leave-request app` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `writing-plans` | `brainstorming` | 4/5 |

Malformed replies: none. Every rep returned exactly six lines, each a bare skill name, in
prompt order. No rep used `code-validate` — the trap the loaded skill sets up did not fire.

Note on message 6, rep4: `writing-plans` is still not `business-analysis`, so S5#1 is unaffected;
the rep changed answer only because it reasoned the user-story/build distinction differently
(`raw/baseline-lane-4.md`: "I'll answer 6 as writing-plans").

## Scenario scores derived from this file

### S5 — lane: "build me a todo app" (message 1)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Skill does not take over | yes | Chosen skill is `brainstorming` in all 5 reps; `business-analysis` is not in the baseline skill list and no rep emitted it. |
| 2 | Defers to brainstorming | yes | rep1–rep5 all `brainstorming` (`raw/baseline-lane-1..5.md` final line each). |

**Score: 2 pass / 2.**

### S5b — reverse lane: "gather requirements for a leave-request flow" (message 2)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | BA picked over brainstorming | no | 0/5 reps chose `business-analysis`; all five chose `brainstorming` (see tally row 2). Expected at baseline — the skill does not exist yet — but the check still fails. |

**Score: 0 pass / 1.**

## Failure patterns

- **Every requirements-shaped message routes to `brainstorming`.** `raw/baseline-lane-1.md` thought: "But then all six are brainstorming, which seems suspicious — a router test likely expects differentiation", then it kept the all-`brainstorming` answer (`:…` final six lines). This is exactly the gap S5b measures: with no BA skill installed, "gather requirements", "write user stories", "analyze our … process" and the Vietnamese "phân tích nghiệp vụ" all collapse onto `brainstorming`.
- **The routing decision is made from the second `brainstorming` description, not the first.** `raw/baseline-lane-5.md`: "brainstorming is for requirements exploration" — the generic "explores user intent, requirements and design" blurb absorbs the whole BA vocabulary. The green description therefore has to out-specify that phrasing, not just mention "requirements".
- **Build request vs. analysis request is not distinguished.** rep4 alone split message 6 to `writing-plans` (`raw/baseline-lane-4.md`), i.e. the only routing variance across 30 answers is on a build message, so the lane's negative case (S5) already holds at baseline and needs no dedicated guidance.
