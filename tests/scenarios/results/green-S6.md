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

## Regression run 2 (skill 6c645b2)

Re-run after the invented-name and NFR-Basis refactors (`fc908f0`, `71424bc`), with the
skill at `6c645b2`, a fresh `deepseek-v4.1-flash` agent and an isolated `/tmp` repo. Same S6
prompt and rubric, turn 2 delivered.

| Field | Value |
|---|---|
| Agent id | `20ee97e0-6395-4808-8468-af7c73e0093b` |
| Raw log | `raw/green-S6-2.md` |
| Saved doc | `raw/green-S6-2-files/docs/ba/2026-11-18-nghi-phep-requirements.md` (193 lines) |
| Git status | `raw/green-S6-2-files/_git-status.txt` |
| Lint | `python3 skills/business-analysis/scripts/lint_requirements.py <doc>` → exit 0, `0 finding(s) in 1 file(s)` — non-vacuous: 12 `BR-nnn` blocks, 12 `FR-nnn` definitions and 7 `NFR` rows were parsed, so the VI `vague-term` rule ran |

### Rubric

| # | Check | yes/no | Evidence |
|---|---|---|---|
| 1 | Vietnamese document | yes | `:1` "# Đăng ký nghỉ phép — Yêu cầu"; `:39` "## Quy tắc nghiệp vụ"; `:63` "## Yêu cầu chức năng"; headings, prose and tables are Vietnamese throughout (the `Given`/`When`/`Then` and "As a … I want … so that" frames stay English by rubric). |
| 2 | English IDs | yes | `:41` "- **BR-001**: Nhân viên chỉ gửi được yêu cầu nghỉ khi số ngày phép còn lại lớn hơn hoặc bằng số ngày xin nghỉ. (A-04)"; `:65` "- **FR-001**: As a nhân viên, I want gửi yêu cầu nghỉ phép gồm ngày bắt đầu, ngày kết thúc và lý do, so that xin nghỉ đúng quy trình. Fulfils [BR-001, BR-003, BR-005, BR-007]. Priority: Must."; `:114` "\| NFR-001 \| Must \| Thời gian phản hồi p95 ≤ 2 giây cho các thao tác gửi, duyệt, từ chối ở mức 200 người dùng đồng thời \| A-06 \|". IDs stay `BR-nnn` / `FR-nnn` / `NFR-nnn`. |
| 3 | English Gherkin keywords | yes | `:66` "- **FR-001.AC1**: Given nhân viên còn 12 ngày phép, When nhân viên gửi yêu cầu nghỉ 3 ngày làm việc, Then yêu cầu được ghi nhận ở trạng thái Chờ duyệt và số ngày phép còn lại vẫn là 12 ngày." — all 32 `FR-nnn.ACn` definitions open with `Given`, `When`, `Then`. |
| 4 | Lint clean (incl. VI vague terms) | yes | Exit 0 with `0 finding(s) in 1 file(s)`; 12 BR, 12 FR and 7 NFR blocks were parsed, so `vague-term` and `missing-ac` were evaluated rather than skipped. |
| 5 | Handoff file written | yes | `_git-status.txt:2` "?? docs/ba/2026-11-18-nghi-phep-requirements.md". |
| 6 | Interview: one question at a time | yes | `raw/green-S6-2.md:428` "**Câu hỏi (một câu, chặn nhiều yêu cầu nhất)**: Ai nhập hạn mức phép đầu năm và điều chỉnh số dư giữa năm — bộ phận Nhân sự hay quản lý trực tiếp?" — the last line of turn 1 (`[User]` turn 2 starts at `:429`). One question. |

**Score: 6 pass / 0 fail.**

### NFR Basis audit

Every NFR row carries a Basis cell that is an input quote, an `A-nn`, or a `Q-nn`:

- `:114` "| NFR-001 | Must | Thời gian phản hồi p95 ≤ 2 giây cho các thao tác gửi, duyệt, từ chối ở mức 200 người dùng đồng thời | A-06 |"
- `:115` "| NFR-002 | Must | Khả dụng ≥ 99,5% mỗi tháng trong khung giờ hành chính 08:00–18:00 | A-06 |"
- `:116` "| NFR-003 | Must | 100% yêu cầu truy cập dữ liệu nghỉ phép ngoài phạm vi quyền bị từ chối trên bộ 40 kịch bản phân quyền | A-07 |"
- `:117` "| NFR-004 | Must | Nhật ký kiểm toán được lưu 24 tháng, đọc được bởi nhân viên sở hữu yêu cầu và quản lý trực tiếp | A-07 |"
- `:118` "| NFR-005 | Must | 100% yêu cầu Đã duyệt có đúng một bút toán trừ phép; đối soát hằng ngày cho kết quả 0 sai lệch | A-04 |"
- `:119` "| NFR-006 | Must | Báo cáo nghỉ phép của một năm có 500 nhân viên trả kết quả trong p95 ≤ 5 giây | A-06 |"
- `:120` "| NFR-007 | Must | 0 trong 20 thao tác duyệt, từ chối, thu hồi do tài khoản nhân sự thực hiện được hệ thống chấp nhận | Input \"nhân sự chỉ cần xem báo cáo\" |"

### Invented-name / number audit

No actor, permission, system name, or number is stated as fact without an `A-nn`/`Q-nn` or an
input quote. The three actor rows carry input quotes: `:16` "| Nhân sự | Chỉ xem báo cáo nghỉ phép; không duyệt, không sửa yêu cầu | Không có quyền quyết định trên yêu cầu | Input: \"nhân sự chỉ cần xem báo cáo\" |" and the employee/manager rows cite "nhân viên gửi yêu cầu", "tối đa 12 ngày một năm" and "quản lý trực tiếp duyệt" at `:14`–`:15`. The 12-day quota traces to the turn-2 answer (`:49` "Nguồn: input \"tối đa 12 ngày một năm\""). One minor gap: the `20` in `NFR-007`'s target (and the `40` in `NFR-003`) is a test-batch size, and its Basis cell is the role input quote rather than a scale-specific `A-nn`; neither number states business behaviour.

### Remaining failures

None. Every S6 check scores yes. One borderline observation, scored yes:

- `:65` FR-001 and the other FR statements keep the English "As a … I want … so that" frame around Vietnamese content, and `:80`/`:100` ACs mix "When quản lý trực tiếp mở danh sách, Then hiển thị …". Check #1 asks for Vietnamese prose and headings, which holds; if it were tightened to "no English prose at all", the fixed template frames would fail it.
