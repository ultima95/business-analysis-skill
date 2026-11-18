# Green lane micro-test (S5, S5b) — skill routing with `business-analysis`

| Field | Value |
|---|---|
| Phase | green (`business-analysis` @ 54b9c11 present in the skill list) |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Reps | 5 |
| Raw logs | `raw/green-lane-<rep>.md`, order per rep in `raw/green-lane-<rep>.order` |
| Pass bar | 5/5 for every message |

## Per-rep answers

Each `.order` file lists the README message number (1–6) at each prompt position. Answers are
mapped back to messages through it.

### rep1 — agent `a277578c-47a6-446c-8869-f00bcb416aca`

Order: 1, 5, 3, 6, 4, 2. Replies (`raw/green-lane-1.md`, last 6 lines), position → message:

| Position | Message | Answer |
|---|---|---|
| 1 | 1 `build me a todo app` | `brainstorming` |
| 2 | 5 `phân tích nghiệp vụ quy trình nghỉ phép` | `business-analysis` |
| 3 | 3 `write user stories for a leave-request flow` | `business-analysis` |
| 4 | 6 `build a leave-request app` | `brainstorming` |
| 5 | 4 `analyze our invoice approval process` | `business-analysis` |
| 6 | 2 `gather requirements for a leave-request flow` | `business-analysis` |

### rep2 — agent `807291df-0ad5-4e48-8a2f-bf2ca124b7b1`

Order: 3, 5, 2, 6, 4, 1.

| Position | Message | Answer |
|---|---|---|
| 1 | 3 `write user stories for a leave-request flow` | `business-analysis` |
| 2 | 5 `phân tích nghiệp vụ quy trình nghỉ phép` | `business-analysis` |
| 3 | 2 `gather requirements for a leave-request flow` | `business-analysis` |
| 4 | 6 `build a leave-request app` | `brainstorming` |
| 5 | 4 `analyze our invoice approval process` | `business-analysis` |
| 6 | 1 `build me a todo app` | `brainstorming` |

### rep3 — agent `03ffd20c-ff92-473a-8c32-04c88689b975`

Order: 6, 5, 3, 2, 1, 4.

| Position | Message | Answer |
|---|---|---|
| 1 | 6 `build a leave-request app` | `brainstorming` |
| 2 | 5 `phân tích nghiệp vụ quy trình nghỉ phép` | `business-analysis` |
| 3 | 3 `write user stories for a leave-request flow` | `business-analysis` |
| 4 | 2 `gather requirements for a leave-request flow` | `business-analysis` |
| 5 | 1 `build me a todo app` | `brainstorming` |
| 6 | 4 `analyze our invoice approval process` | `business-analysis` |

### rep4 — agent `222c7df8-7ae2-40d8-8be3-05af69e0c4f1`

Order: 1, 3, 4, 2, 6, 5.

| Position | Message | Answer |
|---|---|---|
| 1 | 1 `build me a todo app` | `brainstorming` |
| 2 | 3 `write user stories for a leave-request flow` | `business-analysis` |
| 3 | 4 `analyze our invoice approval process` | `business-analysis` |
| 4 | 2 `gather requirements for a leave-request flow` | `business-analysis` |
| 5 | 6 `build a leave-request app` | `brainstorming` |
| 6 | 5 `phân tích nghiệp vụ quy trình nghỉ phép` | `business-analysis` |

### rep5 — agent `7cdb7d90-a76b-432e-8eef-90e09dbebf78`

Order: 4, 5, 2, 1, 3, 6.

| Position | Message | Answer |
|---|---|---|
| 1 | 4 `analyze our invoice approval process` | `business-analysis` |
| 2 | 5 `phân tích nghiệp vụ quy trình nghỉ phép` | `business-analysis` |
| 3 | 2 `gather requirements for a leave-request flow` | `business-analysis` |
| 4 | 1 `build me a todo app` | `brainstorming` |
| 5 | 3 `write user stories for a leave-request flow` | `business-analysis` |
| 6 | 6 `build a leave-request app` | `brainstorming` |

## Tally

| # | Message | expected (green) | rep1 | rep2 | rep3 | rep4 | rep5 | matches |
|---|---|---|---|---|---|---|---|---|
| 1 | `build me a todo app` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | 5/5 |
| 2 | `gather requirements for a leave-request flow` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | 5/5 |
| 3 | `write user stories for a leave-request flow` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | 5/5 |
| 4 | `analyze our invoice approval process` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | 5/5 |
| 5 | `phân tích nghiệp vụ quy trình nghỉ phép` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | `business-analysis` | 5/5 |
| 6 | `build a leave-request app` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | `brainstorming` | 5/5 |

Malformed replies: none. Every rep returned exactly six lines, each a bare skill name, in
prompt order. Every message meets the pass bar (5/5).

## Scenario scores derived from this file

### S5 — lane: "build me a todo app" (message 1)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Skill does not take over | yes | Chosen skill is `brainstorming` in all 5 reps; `business-analysis` was never emitted for message 1 (tally row 1). |
| 2 | Defers to brainstorming | yes | rep1–rep5 all `brainstorming` (`raw/green-lane-1..5.md` final six lines, mapped through each `.order`). |

**Score: 2 pass / 2.**

### S5b — reverse lane: "gather requirements for a leave-request flow" (message 2)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | BA picked over brainstorming | yes | 5/5 reps chose `business-analysis` (tally row 2), against the baseline 0/5. |

**Score: 1 pass / 1.**

## Notes

- `build a leave-request app` (message 6) stayed with `brainstorming` in 5/5 reps, so the
  domain noun next to the BA trigger phrases does not pull the build request into
  `business-analysis`.
- Rep1's thought at `raw/green-lane-1.md` is the clearest trace of the intended split:
  "2. \"phân tích nghiệp vụ quy trình nghỉ phép\" (analyze business process leave flow) → business-analysis"
  and "4. \"build a leave-request app\" → brainstorming".
- No rep routed a BA message to `writing-plans` or `code-validate`; the baseline's single
  `writing-plans` variance on message 6 (rep4) did not recur.
