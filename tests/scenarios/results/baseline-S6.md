# Baseline S6 — Vietnamese input for job 1 (interview mode)

| Field | Value |
|---|---|
| Phase | baseline (no skill) |
| Run | 1 |
| Agent id | `122414db-7fe1-4d7b-82c4-b369696359e9` |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Raw log | `raw/baseline-S6-1.md` |
| Saved doc | `raw/baseline-S6-1-files/docs/leave-request-requirements.md` (386 lines) |
| Git status | `raw/baseline-S6-1-files/_git-status.txt` |
| Lint | `python3 skills/business-analysis/scripts/lint_requirements.py <doc>` → exit 0, `0 finding(s) in 1 file(s)` — vacuous: the doc's IDs are `D1`–`D6` and `LR-01`–`LR-10`, none matching `(BR\|FR\|NFR)-\d{3,}`, so 0 requirement blocks were parsed |

## Rubric

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Vietnamese document | yes | `:1` "# Yêu cầu chức năng: Đăng ký nghỉ phép"; `:21` "## 1. Mục tiêu"; `:48` "## 3. Vai trò và quyền". Tables and rules are written in Vietnamese throughout. |
| 2 | English IDs | no | `:10-17` uses `D1`–`D6`; `:157-168` uses `LR-01`–`LR-10` ("`\| LR-04 \| Số dư khả dụng < tổng ngày xin nghỉ \| 409 INSUFFICIENT_BALANCE \|`"). `grep -cE '\b(BR\|FR\|NFR)-[0-9]{3,}'` → 0; no `BR-nnn`/`FR-nnn`/`NFR-nnn` anywhere. |
| 3 | English Gherkin keywords | no | Acceptance criteria are a numbered Vietnamese list, `:325` "1. Nhân viên có 12 ngày phép năm, gửi đơn 3 ngày làm việc, quản lý trực tiếp duyệt → còn 9 ngày"; `grep -cE '\b(Given\|When\|Then)\b'` → 0. |
| 4 | Lint clean (incl. VI vague terms) | no | Exit 0 with `0 finding(s)`, but nothing was lintable: 0 `BR/FR/NFR-nnn` blocks parsed, so `vague-term` and `missing-ac` could not fire. `grep -iE '\b(nhanh\|dễ dàng\|thân thiện\|linh hoạt\|v\.v\.\|phù hợp\|hợp lý)\b'` → 0, i.e. the exit code says nothing about the doc. |
| 5 | Handoff file written | yes | `_git-status.txt:2` "?? docs/leave-request-requirements.md". |
| 6 | Interview: one question at a time | no | `raw/baseline-S6-1.md:77-80` asks four: "1. **Duyệt mấy cấp?** … 2. **Số dư âm?** … 3. **Cấp phép**: cấp đủ đầu năm hay cấp dần hàng tháng? … 4. **Stack**: dùng framework/ngôn ngữ gì, DB gì?" |

**Score: 2 pass / 4 fail.**

## Failure patterns

- **Mixed a requirements doc with an API/schema design.** `raw/baseline-S6-1.md:22` "keep it focused: scope, actors, user stories, **data model**, **state machine**, business rules…, **API surface (suggested, tech-agnostic)**, acceptance criteria" — delivered as `:210` "## 7. Mô hình dữ liệu" (six tables with column types), `:296` "## 8. API" (13 endpoints), `:377` "## 12. Thứ tự triển khai" (8 implementation steps). It also asked for stack details in turn 1 (`:80` "**Stack**: dùng framework/ngôn ngữ gì, DB gì?"), a technology question the BA must not be asking.
- **Invented its own business-rule vocabulary instead of `BR-nnn`/`FR-nnn`.** `:157` "### 6.3 Kiểm tra hợp lệ" defines `LR-01`–`LR-10` and `:8` "## 0. Quyết định nghiệp vụ đã chốt" defines `D1`–`D6`; no functional or business-requirement ID exists, so nothing has a parent, an AC or a lint target.
- **Wrote acceptance criteria as scenario prose, not Gherkin.** `:323` "## 9. Tiêu chí chấp nhận" is a 21-item numbered list with no `Given/When/Then`, so none of it is machine-checkable per requirement and none of it references an FR.
- **Ballparked the numbers it was missing, then asked anyway.** `raw/baseline-S6-1.md:38` "Reserve on pending (hold) to prevent overbooking — pick hold-on-submit approach? … I'll spec: soft-hold at submission, commit at approval" and the doc's `:151` "Nhân viên vào giữa năm: entitlement = `round_half_up(12 * số_tháng_còn_lại / 12)`" — pro-rata and half-day rules the user never gave, decided unilaterally, then four questions asked on top of the already-finished doc.
