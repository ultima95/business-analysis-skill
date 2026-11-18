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
| 1 | Vietnamese document | no | Re-scored after review of regression run 2. Headings and prose are Vietnamese (`:1` "# Đăng ký nghỉ phép — Yêu cầu"), but the FR statements keep the English frame and labels: `:52` "- **FR-001**: As a nhân viên, I want gửi yêu cầu nghỉ phép gồm loại phép, ngày bắt đầu và ngày kết thúc, so that quản lý trực tiếp nhận được yêu cầu để quyết định. Fulfils [BR-001]. Priority: Must." and `:57` "- **FR-002**: As a nhân viên, I want xem số ngày phép năm còn lại trong năm hiện tại, so that biết còn bao nhiêu ngày trước khi gửi yêu cầu. Fulfils [BR-005], [BR-008]. Priority: Must." — same pattern on the non-user-facing lines ("The system shall"). |
| 2 | English IDs | yes | `:40` "**BR-001**: Một yêu cầu nghỉ phép gồm bốn trường bắt buộc…"; `:47` "**BR-008**: Quỹ phép năm của một nhân viên là 12 ngày cho mỗi năm dương lịch…"; `:52` "**FR-001**: As a nhân viên…"; `:92` "| NFR-001 | Must | p95 thời gian phản hồi ≤ 2 giây…". IDs stay `BR-nnn` / `FR-nnn` / `NFR-nnn`. |
| 3 | English Gherkin keywords | yes | `:53` "**FR-001.AC1**: Given nhân viên còn 12 ngày phép và nhập yêu cầu nghỉ từ 2026-12-01 đến 2026-12-03, When nhân viên gửi yêu cầu, Then yêu cầu được lưu ở trạng thái Chờ duyệt với số ngày nghỉ là 3." |
| 4 | Lint clean (incl. VI vague terms) | yes | Exit 0 with `0 finding(s) in 1 file(s)`; 9 BR, 9 FR and 6 NFR blocks were parsed, so `vague-term` and `missing-ac` were evaluated rather than skipped. |
| 5 | Handoff file written | yes | `_git-status.txt:2` "?? docs/ba/2026-11-18-leave-request-requirements.md". |
| 6 | Interview: one question at a time | yes | `raw/green-S6-1.md:350` "Hiện tại tài liệu giả định một yêu cầu gồm nhiều ngày liên tục và trừ theo ngày làm việc — Số ngày trừ phải tính theo ngày làm việc (bỏ cuối tuần và ngày lễ) hay theo ngày lịch?" — one question, as the last line before the turn-2 canned answer. |

**Score: 5 pass / 1 fail.**

## Remaining failures

- **S6#1 Vietnamese document** — FR statement frames and labels stay English (`:52`, `:57`
  above, and "The system shall" on the non-user-facing FRs). The check requires only IDs,
  Gherkin keywords and Mermaid syntax to stay English.

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

S6#1 was scored `yes` on first pass and re-scored `no` after review; the evidence cell and
the score below are the corrected ones.

### Rubric

| # | Check | yes/no | Evidence |
|---|---|---|---|
| 1 | Vietnamese document | no | Headings and body prose are Vietnamese (`:1` "# Đăng ký nghỉ phép — Yêu cầu"; `:39` "## Quy tắc nghiệp vụ"), but all 12 FR statement lines keep English frames and English labels: `:65` "- **FR-001**: As a nhân viên, I want gửi yêu cầu nghỉ phép gồm ngày bắt đầu, ngày kết thúc và lý do, so that xin nghỉ đúng quy trình. Fulfils [BR-001, BR-003, BR-005, BR-007]. Priority: Must."; `:93` "- **FR-008**: The system shall ghi nhật ký cho mỗi lần yêu cầu đổi trạng thái. Fulfils [BR-006]. Priority: Must."; the same pattern repeats at `:73`, `:76`, `:79`, `:82`, `:86`, `:89`, `:96`, `:99`, `:102`, `:106`. The spec's English allowlist is IDs, Gherkin keywords and Mermaid only — `skills/business-analysis/references/requirements.md:172` "Output follows the input's language; IDs and Gherkin keywords stay English." and `:174` "- Headings and prose: the input language." — so "As a …, I want …, so that …", "The system shall", "Fulfils […]" and "Priority:" are English prose in a document this check requires to be Vietnamese. |
| 2 | English IDs | yes | `:41` "- **BR-001**: Nhân viên chỉ gửi được yêu cầu nghỉ khi số ngày phép còn lại lớn hơn hoặc bằng số ngày xin nghỉ. (A-04)"; `:65` "- **FR-001**: As a nhân viên, I want gửi yêu cầu nghỉ phép gồm ngày bắt đầu, ngày kết thúc và lý do, so that xin nghỉ đúng quy trình. Fulfils [BR-001, BR-003, BR-005, BR-007]. Priority: Must."; `:114` "\| NFR-001 \| Must \| Thời gian phản hồi p95 ≤ 2 giây cho các thao tác gửi, duyệt, từ chối ở mức 200 người dùng đồng thời \| A-06 \|". IDs stay `BR-nnn` / `FR-nnn` / `NFR-nnn`. |
| 3 | English Gherkin keywords | yes | `:66` "- **FR-001.AC1**: Given nhân viên còn 12 ngày phép, When nhân viên gửi yêu cầu nghỉ 3 ngày làm việc, Then yêu cầu được ghi nhận ở trạng thái Chờ duyệt và số ngày phép còn lại vẫn là 12 ngày." — all 32 `FR-nnn.ACn` definitions open with `Given`, `When`, `Then`. |
| 4 | Lint clean (incl. VI vague terms) | yes | Exit 0 with `0 finding(s) in 1 file(s)`; 12 BR, 12 FR and 7 NFR blocks were parsed, so `vague-term` and `missing-ac` were evaluated rather than skipped. |
| 5 | Handoff file written | yes | `_git-status.txt:2` "?? docs/ba/2026-11-18-nghi-phep-requirements.md". |
| 6 | Interview: one question at a time | yes | `raw/green-S6-2.md:428` "**Câu hỏi (một câu, chặn nhiều yêu cầu nhất)**: Ai nhập hạn mức phép đầu năm và điều chỉnh số dư giữa năm — bộ phận Nhân sự hay quản lý trực tiếp?" — the last line of turn 1 (`[User]` turn 2 starts at `:429`). One question. |

**Score: 5 pass / 1 fail.**

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

- **S6#1 Vietnamese document** — the agent drafted the English frame itself before writing anything, `raw/green-S6-2.md:137`: "FR-001: As nhân viên, I want gửi yêu cầu nghỉ phép với ngày bắt đầu, ngày kết thúc, lý do, so that xin nghỉ đúng quy trình." It then shipped that shape at `:65`, with the frame made more English still: "- **FR-001**: As a nhân viên, I want gửi yêu cầu nghỉ phép gồm ngày bắt đầu, ngày kết thúc và lý do, so that xin nghỉ đúng quy trình. Fulfils [BR-001, BR-003, BR-005, BR-007]. Priority: Must." Its only language decision in the log is `raw/green-S6-2.md:375`: "One more: the skill says template headers translated to Vietnamese. Do it." — translation was scoped to headings, so all 12 FR statements kept "As a …" / "The system shall", "Fulfils […]" and "Priority:". The spec allows English only for IDs, Gherkin keywords and Mermaid (`skills/business-analysis/references/requirements.md:172` "Output follows the input's language; IDs and Gherkin keywords stay English." and `:174` "- Headings and prose: the input language."), so the check fails. The baseline run wrote Vietnamese prose with no such frames (`raw/baseline-S6-1-files/docs/leave-request-requirements.md:6` "Cho phép nhân viên tự gửi yêu cầu nghỉ phép, quản lý trực tiếp duyệt hoặc từ chối, và hệ thống"), so this is a with-skill regression, not a rubric artefact. S6#4's lint cannot catch it: the rules cover IDs, ACs and vague terms, not prose language.

The other five checks score yes. S6#2 passes on the same lines that fail #1 — the IDs inside them are English, which is what #2 asks for.

## REFACTOR iterations

Iteration 3 — failure: every FR statement in the Vietnamese runs keeps the English template frame and labels — `raw/green-S6-2-files/docs/ba/2026-11-18-nghi-phep-requirements.md:65` "- **FR-001**: As a nhân viên, I want gửi yêu cầu nghỉ phép gồm ngày bắt đầu, ngày kết thúc và lý do, so that xin nghỉ đúng quy trình. Fulfils [BR-001, BR-003, BR-005, BR-007]. Priority: Must." (12 FR lines incl. "The system shall", "Fulfils […]", "Priority:"), and the same in run 1 — `raw/green-S6-1-files/docs/ba/2026-11-18-leave-request-requirements.md:52` "- **FR-001**: As a nhân viên, I want gửi yêu cầu nghỉ phép gồm loại phép, ngày bắt đầu và ngày kết thúc, so that quản lý trực tiếp nhận được yêu cầu để quyết định. Fulfils [BR-001]. Priority: Must." and `:57` "- **FR-002**: As a nhân viên, I want xem số ngày phép năm còn lại trong năm hiện tại, so that biết còn bao nhiêu ngày trước khi gửi yêu cầu. Fulfils [BR-005], [BR-008]. Priority: Must." — change: `skills/business-analysis/SKILL.md:81` now reads "Output language follows the input's language (Vietnamese in → Vietnamese doc). Templates are English — when writing another language, translate headings, the FR statement frame (`As a … I want … so that …`, `The system shall …`), and labels such as `Fulfils` and `Priority:`. IDs (`FR-001`), Gherkin keywords (`Given` / `When` / `Then`), and Mermaid syntax stay English; MoSCoW values stay `Must` / `Should` / `Could` / `Won't`."; `skills/business-analysis/references/requirements.md:175-177` adds "FR statements and labels: translate the frame (`As a … I want … so that …`, `The system shall …`) and the labels (`Fulfils`, `Priority:`); MoSCoW values stay `Must`, `Should`, `Could`, `Won't`." and `:184-186` adds the canonical Vietnamese lines "**FR-001**: Là nhân viên, tôi muốn gửi đơn nghỉ phép, để được duyệt đúng quy trình. Đáp ứng [BR-001]. Ưu tiên: Must." and "**FR-002**: Hệ thống phải ghi nhật ký cho mỗi lần yêu cầu đổi trạng thái. Đáp ứng [BR-002]. Ưu tiên: Should." — result:

| Rep | S6#1 | S6#2 | S6#3 | S6#4 | S6#5 | S6#6 | Evidence |
|---|---|---|---|---|---|---|---|
| 3 (`green-S6-3`, `a0d88aa2-9663-4886-b06b-33bad60adee8`) | no | yes | yes | yes | yes | yes | #1: FR frame is Vietnamese (`:64` "- **FR-001**: Là nhân viên, tôi muốn gửi một đơn nghỉ phép … Đáp ứng [BR-004], [BR-011]. Ưu tiên: Must."), but the heading and basis label stay English — `:11` "## Actor và bên liên quan", `:13` "| Actor | Làm / quyết / được thông báo | Ghi chú | Cơ sở |", `:15` "… \| Input: \"nhân viên gửi yêu cầu\" \|", and `:175` "Brainstorm giải pháp với tài liệu này làm ngữ cảnh…". #2: `:64` FR-001, IDs English. #3: `:65` "Given … When … Then …". #4: lint exit 0, `0 finding(s) in 1 file(s)`, 12 BR / 13 FR / 5 NFR parsed. #5: `_git-status.txt:2` "?? docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md". #6: `raw/green-S6-3.md:372` "Câu hỏi (1 câu, chặn nhiều FR nhất): **Đơn vị nghỉ nhỏ nhất là 1 ngày công, hay cho phép nửa ngày / theo giờ?**" — one question, last line before turn 2 at `:373`. |
| 4 (`green-S6-4`, `65880adb-9a74-4a2d-b97e-ea1722cacef9`) | yes | yes | yes | yes | yes | yes | #1: headings and labels Vietnamese (`:36` "## Quy tắc nghiệp vụ", `:164` "## Giả định", basis column "Đầu vào"); FR frame `:68` "Là nhân viên, tôi muốn tạo và gửi đơn nghỉ phép … Đáp ứng […]. Ưu tiên: Must."; residual loanwords only (`:10` "Repo hiện chỉ có thư mục `.git`, không có mã nguồn … từ code."; `:202` "Brainstorm giải pháp với file này làm ngữ cảnh…"). #2: `:68` FR-001, IDs English. #3: `:69` "Given … When … Then …". #4: lint exit 0, `0 finding(s) in 1 file(s)`, 16 BR / 9 FR / 6 NFR parsed. #5: `_git-status.txt:2` "?? docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md". #6: `raw/green-S6-4.md:519` "**Ngày phép bị trừ lúc nhân viên gửi đơn, hay chỉ trừ khi quản lý duyệt?**" — one question, last line before turn 2 at `:520`. |
| 5 (`green-S6-5`, `f23c6285-0678-4e19-b5ab-2e5c442b1754`) | no | yes | yes | yes | yes | yes | #1: every section heading is English — `:3` "## Context", `:9` "## Actors and stakeholders", `:18` "## Scope", `:32` "## Business rules", `:45` "## Functional requirements", `:81` "## Non-functional requirements", `:97` "## Edge cases", `:110` "## Glossary", `:125` "## Assumptions", `:144` "## Open questions", `:155` "## Next step"; basis column also says "Input" (`:131-136`, `:142`) and `:7` "Repo hiện chỉ có commit khởi tạo…". Vietnamese FR frame `:47`, Gherkin `:48`. #2: `:47` FR-001, IDs English. #3: `:48` "Given … When … Then …". #4: lint exit 0, `0 finding(s) in 1 file(s)`, 10 BR / 12 FR / 5 NFR parsed. #5: `_git-status.txt:2` "?? docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md". #6: `raw/green-S6-5.md:334` "Hỏi: đơn nghỉ vượt quá số ngày phép còn lại thì bị chặn ngay khi gửi, hay vẫn gửi được để quản lý tự quyết?" — one question, last line before turn 2 at `:335`. |

Verdict: S6#1 passes **1/3** — the FR statement frame and labels are Vietnamese in all three reps, but headings and basis labels are still English in reps 3 and 5 (`Actor`, `Input`, and all eleven section headings), so the translation change did not fully hold.
