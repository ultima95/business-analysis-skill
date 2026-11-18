# Green S6 — Vietnamese input for job 1 (interview mode)

| Field | Value |
|---|---|
| Phase | green (skill `business-analysis` @ 54b9c11) |
| Run | 1 |
| Agent id | `f957a2d5-5330-4b77-86db-7268090bc795` |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Raw log | `raw/green-S6-1.md` |
| Saved doc | `raw/green-S6-1-files/docs/ba/2026-11-18-leave-request-requirements.md` (176 lines) |
| Git status | `raw/green-S6-1-files/_git-status.txt` |
| Lint | `python3 skills/business-analysis/scripts/lint_requirements.py <doc>` → exit 0, `0 finding(s) in 1 file(s)` — non-vacuous: 9 BR, 9 FR and 6 NFR blocks were parsed, so the VI `vague-term` rule ran |

## Rubric

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Vietnamese document | yes | `:1` "# Đăng ký nghỉ phép — Yêu cầu"; `:38` "## Quy tắc nghiệp vụ"; `:106` "## Trường hợp biên"; prose, headings and tables are Vietnamese throughout. |
| 2 | English IDs | yes | `:40` "**BR-001**: Một yêu cầu nghỉ phép gồm bốn trường bắt buộc…"; `:47` "**BR-008**: Quỹ phép năm của một nhân viên là 12 ngày cho mỗi năm dương lịch…"; `:52` "**FR-001**: As a nhân viên…"; `:92` "| NFR-001 | Must | p95 thời gian phản hồi ≤ 2 giây…". IDs stay `BR-nnn` / `FR-nnn` / `NFR-nnn`. |
| 3 | English Gherkin keywords | yes | `:53` "**FR-001.AC1**: Given nhân viên còn 12 ngày phép và nhập yêu cầu nghỉ từ 2026-12-01 đến 2026-12-03, When nhân viên gửi yêu cầu, Then yêu cầu được lưu ở trạng thái Chờ duyệt với số ngày nghỉ là 3." |
| 4 | Lint clean (incl. VI vague terms) | yes | Exit 0 with `0 finding(s) in 1 file(s)`; 9 BR, 9 FR and 6 NFR blocks were parsed, so `vague-term` and `missing-ac` were evaluated rather than skipped. |
| 5 | Handoff file written | yes | `_git-status.txt:2` "?? docs/ba/2026-11-18-leave-request-requirements.md". |
| 6 | Interview: one question at a time | yes | `raw/green-S6-1.md:350` "Hiện tại tài liệu giả định một yêu cầu gồm nhiều ngày liên tục và trừ theo ngày làm việc — Số ngày trừ phải tính theo ngày làm việc (bỏ cuối tuần và ngày lễ) hay theo ngày lịch?" — one question, as the last line before the turn-2 canned answer. |

**Score: 6 pass / 0 fail.**

## Remaining failures

None. Every S6 check passes.
