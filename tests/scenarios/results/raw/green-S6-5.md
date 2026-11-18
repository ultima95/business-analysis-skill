# green S6 — agent f23c6285-0678-4e19-b5ab-2e5c442b1754 (command-code/deepseek/deepseek-v4.1-flash)

[User] Read and follow /tmp/ba-skill-under-test/business-analysis/SKILL.md.

Ứng dụng của chúng tôi cần thêm tính năng đăng ký nghỉ phép: nhân viên gửi yêu
cầu, quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại. Hãy viết yêu cầu
đầy đủ trước khi code. Nếu cần hỏi tôi điều gì, hãy hỏi ở cuối câu trả lời rồi
dừng lại. Lưu kết quả thành một file markdown trong repo này.
I'll start by reading the SKILL.md file and activating caveman.
[Read] null
[Activate skill]
[Thought] Skill says: request is "add feature X to app" — build request → route to brainstorming. But user explicitly asks: "Hãy viết yêu cầu đầy đủ trước khi code" (write full requirements before code). So this is job 1 (feed dev work) — requirements. The "When not to use" says a build request that merely mentions domain noun stays with brainstorming. But here user asks to write requirements, so job 1 applies.

Job: Job 1 alone → `…-requirements.md`.

I should read references/requirements.md, references/elicitation.md, maybe code-recovery.md since it's a repo (job 1 inside a repo → recover current rules via references/code-recovery.md citing file:line). Let me check the repo — there's only init commit. Let me examine the repo contents.

Mode: Interview — user present, says "If you need ask me anything, ask at the end of the answer then stop." That is explicitly asking to ask questions at end. Skill says one question per message. But user says "ask at end of the answer then stop" — the skill's interview mode: one interview message contains understanding, gap, and exactly one question. Also user asked to save result as markdown file in repo. So maybe draft + one question? Hmm.

Careful: user wants full requirements written BEFORE code, and asks questions at end. The skill says interview mode = ask one question per message and stop, don't write doc yet? Actually core loop: pick job, read input, gap-finder, pick mode, analyze, write, lint, report. In interview mode you ask one question per message before writing. But user explicitly requests the file saved in repo. Conflict: skill says "Ambigit → ask once."

Best approach: I could do gap-finder, then in interview mode ask the single highest-impact question without writing the file yet? But user asked to save results as markdown file. Hmm. Options: write draft (with unknowns as A/Q) AND ask one question at end. That satisfies both: file saved, one question asked at the end, then stop.

That's reasonable: mode hybrid-ish — produce draft with A-nn/Q-nn, ask one highest-impact question at end. But skill red flags: interview message more than one question = bad. So write doc, then ask exactly one question.

I need to read the references to follow structure properly. Let me read: references/requirements.md, references/elicitation.md, templates/requirements.md, references/code-recovery.md, scripts/lint_requirements.py.

Also explore repo.

Let me read files in parallel.
Skill says: build request → route to brainstorming, but user explicitly asks for requirements first → Job 1. Need references + templates + repo state.
[Read] null
[Read] null
[Thought] Repo empty (only .git). So no code recovery possible. Job 1 alone → `docs/ba/YYYY-MM-DD-<topic>-requirements.md`.

Mode: user present, input thin ask → Interview. But user asked to save the result as markdown file in repo. Skill says stop asking when answer recorded. Hmm. The user's instruction "Nếu cần hỏi tôi điều gì, hãy hỏi ở cuối câu trả lời rồi dừng lại" = if you need to ask me something, ask at end of answer then stop. That means write what we have (draft-ish) and ask one question at end.

Best interpretation: write draft complete doc with A/Q registers, then ask exactly one question at end. This matches "Draft" mode behavior + interview question at end. But strict interview mode would ask first without doc. User explicitly wants file saved. I'll write the doc, then one question.

Now build requirements. Domain: leave request app. Vietnamese input → Vietnamese doc.

Need to gather gaps. Input thin: "nhân viên gửi yêu cầu, quản lý duyệt, hệ thống trừ vào số ngày phép còn lại".

Actors: nhân viên, quản lý. Maybe HR. Don't invent — A/Q.

Business rules needed:
- BR-001: employee can only submit if remaining balance sufficient? That's an assumption. Must record A-01.
- BR-002: manager approves/rejects.
- BR-003: balance deduction only on approval.
- BR-004: leave types (annual, sick, unpaid) — unknown → A/Q.
- BR-005: overlap prevention.
- BR-006: cancellation after approval → refund.
- BR-007: approval window / SLA.

All these invented specifics must be A-nn or Q-nn, not confirmed prose. But BRs are requirements we need. Skill red flag: a rule not in input written as fact = invented. So BRs must be grounded: either direct from input (approval, deduction) or flag assumptions. I can write BR backed by assumption, noting "Nguồn: A-01". Hmm — canonical BR form has no source slot, but I can append "(Nguồn: A-01)". Lint may not reject. That keeps traceability.

Let me check lint script rules to avoid failures. Let me read scripts/lint_requirements.py.

Also need code-recovery reference? Repo empty, no code. Skip reading? It says job 1 inside repo → also recover current rules via code-recovery. No code exists → nothing to recover. I should note repo empty.

Let me read the lint script to know forbidden vague words (EN and VI lists).
Repo empty — no code to recover rules from. Let me check lint script rules so doc passes.
[Read] null
[Thought] Now write doc. Path: docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md

Must be careful: vague terms list includes "nhanh", "dễ dàng", "phù hợp", "hợp lý", "linh hoạt", "v.v.", also EN "simple", "TBD", "normally". Avoid those words in definition blocks (line + continuation lines until blank/heading/table). Note tables reset current block — so BR/FR definition blocks span only contiguous non-blank non-table lines. ACs follow FR lines, fine.

Careful: FR blocks include the following AC lines (continuation) if no blank line. That's fine.

Important gotcha: "v.v." avoid. "phù hợp" avoid — don't use in BR/FR/AC lines. Also "nhanh" avoid in NFR targets — use numbers.

Also `_DEF_PATTERN` matches lines starting with e.g. `| NFR-001 |`. Table rows for A/Q: `| A-01 |` doesn't match ID pattern (A not BR/FR/NFR), good.

Citations: any occurrence of FR-nnn elsewhere must be defined. Careful not to cite undefined IDs in prose. Also AC base must be defined.

Now content plan.

Context: problem in requester's words, why now, source input.

Actors table: Nhân viên (gửi yêu cầu), Quản lý trực tiếp (duyệt/từ chối), HR/admin (unknown → A), Hệ thống.

Scope: in scope: submit, approve/reject, deduct balance, view balance/history; out of scope: payroll integration, attendance, shift scheduling (explicitly excluded? user didn't say. Mark as out of scope for this release — A-nn? Out of scope statements are decisions I make; better record as A with basis "input does not mention"). I'll keep out-of-scope minimal and cite A.

Business rules — grounded ones:
- BR-001: Leave balance counted in days. (from input "trừ vào số ngày phép còn lại") — yes grounded.
- BR-002: Deduction happens only when manager approves; rejected/cancelled request must not deduct. (grounded-ish: "quản lý duyệt, và hệ thống trừ" — sequence implies approval then deduct. Still an inference; cite A-02.)
- BR-003: Balance cannot go negative — a request exceeding remaining balance must be rejected at submit. (invention → A-03.)
- BR-004: One request covers one continuous date range. (invention → A-04)
- BR-005: An employee cannot have two overlapping requests in pending or approved state. (A-05)
- BR-006: Only direct manager (or delegated approver) can approve own team's requests; cannot approve own. (A-06)
- BR-007: Pending request can be cancelled by requester before decision, restoring nothing since not deducted. Approved leave cancellation → restore balance (A-07).
- BR-008: Balance resets per leave year. (A-08 / Q)
- BR-009: Days counted exclude weekends/holidays? Big rule. A-09.
- BR-010: Leave types and balance pools (annual/sick/unpaid) — A-10.
- BR-011: Partial-day leave (half day) — A-11.
- BR-012: Approval deadline / auto behavior — Q.

Don't over-invent. But requirements doc needs enough. Keep BRs ~8-10 with source notes.

FRs:
- FR-001 employee submit leave request (Must) — fulfils BR-001, BR-004.
- FR-002 system validate request against balance/overlap (Must) — BR-003, BR-005.
- FR-003 manager view pending requests of own team (Must) — BR-006.
- FR-004 manager approve (Must) — BR-002.
- FR-005 manager reject with reason (Must) — BR-002.
- FR-006 system deduct balance on approval atomically (Must) — BR-001, BR-002.
- FR-007 employee view remaining balance and request status (Must) — BR-001.
- FR-008 employee cancel pending request (Should) — BR-007.
- FR-009 system restore balance when approved leave cancelled (Should) — BR-007.
- FR-010 system send notification to requester on decision (Should) — BR-002? Better cite BR-002 or no BR. FRs must fulfil a BR? Template says Fulfils [BR-001] but lint doesn't require FR cite a BR. Still I'll cite where sensible. Notification → maybe BR-013 "Người gửi phải được thông báo kết quả" – but that's a rule from nowhere. Could skip "Fulfils" for FR with no BR. But every BR must be cited (orphan-br). Fine.
- FR-011 audit log of status changes (Should).
- FR-012 admin/HR adjust balance manually (Could) — hmm invented role. Mark Could, source A.

Keep it about 10-11 FRs.

Each FR needs ≥1 AC. Exception ACs for main ones.

NFRs: performance p95 ≤2s (A), availability, auditability, security (only manager of team can access), privacy. Numbers needed + basis A-nn/Q-nn.

NFR-001: p95 ≤ 2 s for submit/approve at 100 concurrent users — A-12.
NFR-002: availability 99.5%/month — A-13.
NFR-003: audit log retention 24 months — A-14.
NFR-004: every balance change traceable to request ID — grounded in input deduction? basis A.
NFR-005: TLS/authorization — no number? needs digit. lint requires digit in definition or AC. Add "0 truy cập trái phép" etc. e.g. "Given ..., Then 0 request ngoài phạm vi được duyệt" contains digit 0. Fine.

Edge cases matrix: roles × states.

Glossary: Đơn nghỉ phép, Ngày phép còn lại, Quản lý trực tiếp, Trạng thái Chờ duyệt/Đã duyệt/Từ chối/Đã hủy.

Assumptions A-01..A-12ish. Open questions Q-01..Q-06 with owner and blocks.

Every Q blocks an FR. Careful: Q rows in table; the "Blocks" cell citing FR-001 is a citation → must be defined (it will be). Good.

Language: Vietnamese. Headings translated.

Then run lint, fix.

Then report: file path, counts, top 3 risks/open questions, next step. Then one question at end, then stop.

Wait — user asked "Nếu cần hỏi tôi điều gì, hãy hỏi ở cuối câu trả lời rồi dừng lại." So exactly one question at end. Interview mode: one question. Choose highest-impact gap: approval policy — whether request exceeding balance blocked at submit, or allowed with negative/advance? Hmm highest impact likely: "đơn vị tính và cách trừ ngày phép (nghỉ nửa ngày? cuối tuần/ngày lễ? nhiều loại phép?)" That's bundling. One question: "Số ngày phép bị trừ tính theo ngày làm việc (bỏ cuối tuần/ngày lễ) hay ngày lịch?" That changes many requirements but not the most.

Highest impact: whether a request can exceed remaining balance. That drives BR-003, FR-002, and approval flow. But multiple leave types also big. I'll ask: "Đơn xin nghỉ vượt quá số ngày phép còn lại thì bị chặn ngay khi gửi, hay vẫn gửi được và quản lý quyết định?" Good single question, high impact.

Now write doc. Careful about lint's block continuation: an FR definition line followed immediately by AC lines is a single block; "Fulfils [BR-001]" citation fine.

Avoid word "phù hợp" anywhere in FR/BR/AC blocks. Also avoid "nhanh".

Careful: In BR line "không được âm" fine.

Also note: citations anywhere in the doc including prose count. E.g. mentioning "FR-001" in Next step would be a citation – fine since defined. But don't cite IDs that don't exist (e.g. FR-013).

Counts: BR, FR, NFR, AC, Q.

Let me design final lists.

BR (business rules):
BR-001: Số ngày phép còn lại của nhân viên được tính bằng đơn vị ngày và trừ khi đơn nghỉ được duyệt.
BR-002: Hệ thống chỉ trừ ngày phép khi đơn ở trạng thái Đã duyệt; đơn bị từ chối hoặc bị hủy trước khi duyệt không làm thay đổi số dư.
BR-003: Đơn nghỉ có tổng số ngày vượt quá số ngày phép còn lại bị từ chối tại thời điểm gửi. (Nguồn: A-03)
BR-004: Mỗi đơn nghỉ bao gồm đúng một khoảng ngày liên tục, có ngày bắt đầu và ngày kết thúc. (Nguồn: A-04)
BR-005: Nhân viên không được có hai đơn nghỉ ở trạng thái Chờ duyệt hoặc Đã duyệt trùng khoảng ngày. (A-05)
BR-006: Chỉ quản lý trực tiếp của nhân viên được duyệt hoặc từ chối đơn của nhân viên đó; nhân viên không tự duyệt đơn của mình. (A-06)
BR-007: Nhân viên được hủy đơn ở trạng thái Chờ duyệt; khi hủy đơn Đã duyệt, hệ thống hoàn lại số ngày phép đã trừ. (A-07)
BR-008: Số ngày phép được cấp lại theo kỳ nghỉ phép năm, mỗi kỳ bắt đầu bằng hạn mức cố định. (A-08)
BR-009: Số ngày bị trừ tính theo ngày làm việc, không tính thứ Bảy, Chủ nhật và ngày lễ. (A-09)

Hmm BR-009 says A-09 possibly false; maybe Q. It's high impact. Put as Q-01 and assumption A-09? Only one table. Make it Q with assumption working value? Rule: if you fill working value → A. I'll make A-09 and also Q about holidays calendar. Simpler: BR-009 with (Nguồn: A-09), and Q-02 asks about leave types.

BR-010: Mỗi nhân viên có hạn mức riêng cho từng loại nghỉ phép; đơn nghỉ chỉ trừ vào hạn mức của loại nghỉ tương ứng. (A-10)

Do I need 10 BRs? Fine. But every BR must be cited by FR/AC.

FRs:
FR-001: Là nhân viên, tôi muốn gửi đơn nghỉ phép với loại nghỉ, ngày bắt đầu, ngày kết thúc và lý do, để xin nghỉ đúng quy trình. Đáp ứng [BR-001], [BR-004]. Ưu tiên: Must.
AC1: Given nhân viên còn 12 ngày phép loại phép năm, When gửi đơn nghỉ 3 ngày làm việc, Then đơn được tạo ở trạng thái Chờ duyệt.
AC2: Given nhân viên nhập ngày kết thúc trước ngày bắt đầu, When gửi đơn, Then hệ thống từ chối và hiển thị lỗi khoảng ngày không hợp lệ.
AC3: Given nhân viên bỏ trống trường lý do, When gửi đơn, Then ... — depends if reason mandatory. Assumption A-11. Maybe skip? Keep AC2 only + AC3 for missing field if A says mandatory. I'll include A-11 reason mandatory and AC3.

FR-002: Hệ thống phải kiểm tra số ngày còn lại và khoảng ngày trùng trước khi tạo đơn. Đáp ứng [BR-003], [BR-005]. Ưu tiên: Must.
AC1: Given nhân viên còn 2 ngày phép, When gửi đơn nghỉ 3 ngày làm việc, Then hệ thống không tạo đơn và báo số ngày vượt quá số dư.
AC2: Given nhân viên đã có đơn Đã duyệt trùng ngày 10/12, When gửi đơn mới có ngày 10/12, Then hệ thống không tạo đơn và báo trùng khoảng ngày.
AC3: Given hai đơn Chờ duyệt trùng ngày, ... same as AC2? keep 2.

FR-003: Là quản lý trực tiếp, tôi muốn xem danh sách đơn Chờ duyệt của nhân viên trong nhóm mình, để xử lý kịp thời. Đáp ứng [BR-006]. Must.
AC1: Given quản lý A có 3 nhân viên, When mở danh sách đơn chờ duyệt, Then chỉ 3 đơn... Actually "chỉ thấy đơn của nhân viên thuộc nhóm mình" → AC2 for other team's request invisible.
AC1: Given quản lý có 3 nhân viên, When mở danh sách đơn Chờ duyệt, Then thấy đơn Chờ duyệt của 3 nhân viên đó và không thấy đơn của nhóm khác.

FR-004: Là quản lý trực tiếp, tôi muốn duyệt đơn của nhân viên, để đơn được ghi nhận là nghỉ có phép. Đáp ứng [BR-002], [BR-006]. Must.
AC1: Given đơn Chờ duyệt còn đủ số dư, When quản lý duyệt, Then đơn chuyển Đã duyệt và số dư giảm đúng số ngày.
AC2: Given đơn đã được duyệt, When quản lý duyệt lại, Then hệ thống không thay đổi trạng thái và trả lỗi đơn đã xử lý.
AC3: Given người duyệt không phải quản lý trực tiếp, When thực hiện duyệt, Then hệ thống từ chối thao tác. (permission)

FR-005: Là quản lý trực tiếp, tôi muốn từ chối đơn kèm lý do, để nhân viên biết kết quả. Đáp ứng [BR-002]. Must.
AC1: Given đơn Chờ duyệt, When quản lý từ chối với lý do bắt buộc, Then đơn chuyển Từ chối, số dư không đổi.
AC2: Given quản lý bỏ trống lý do từ chối, When xác nhận, Then hệ thống không ghi nhận và báo lỗi. (A-12 says reason required)

FR-006: Hệ thống phải ghi nhận việc trừ số ngày phép trong cùng một giao dịch với việc chuyển đơn sang Đã duyệt. Đáp ứng [BR-001], [BR-002]. Must.
AC1: Given đơn được duyệt thành công, When kiểm tra số dư, Then số dư giảm đúng số ngày của đơn và lịch sử ghi nhận mã đơn.
AC2: Given bước trừ số dư thất bại, When quản lý duyệt, Then đơn vẫn ở Chờ duyệt và số dư không đổi.

FR-007: Là nhân viên, tôi muốn xem số ngày phép còn lại theo từng loại nghỉ và trạng thái các đơn của mình, để chủ động sắp xếp. Đáp ứng [BR-001], [BR-010]. Must.
AC1: Given nhân viên có 01 đơn Chờ duyệt và 02 đơn Đã duyệt, When mở trang phép của tôi, Then thấy số dư hiện tại và toàn bộ 3 đơn kèm trạng thái.

FR-008: Là nhân viên, tôi muốn hủy đơn Chờ duyệt của mình, để rút lại yêu cầu khi kế hoạch thay đổi. Đáp ứng [BR-007]. Should.
AC1: Given đơn Chờ duyệt của chính mình, When nhân viên hủy, Then đơn chuyển Đã hủy và không ảnh hưởng số dư.
AC2: Given đơn đã Từ chối, When nhân viên hủy, Then hệ thống từ chối thao tác và giữ nguyên trạng thái.

FR-009: Hệ thống phải hoàn lại số ngày phép khi đơn Đã duyệt bị hủy. Đáp ứng [BR-007]. Should.
AC1: Given đơn Đã duyệt nghỉ 2 ngày và số dư đã bị trừ, When đơn bị hủy, Then số dư tăng 2 ngày và lịch sử ghi nhận hoàn phép.

FR-010: Hệ thống phải gửi thông báo cho nhân viên khi đơn chuyển sang Đã duyệt, Từ chối hoặc Đã hủy. Đáp ứng [BR-002]. Should.
Hmm BR-002 about deduction; notification doesn't fulfil. Just omit Fulfils? Format allows FR without? Lint fine. But maybe cite BR-002 loosely is wrong. I'll omit Fulfils line for FR-010 and FR-011.
AC1: Given đơn Chờ duyệt, When quản lý duyệt, Then nhân viên nhận 1 thông báo chứa mã đơn và kết quả trong vòng 5 phút.

FR-011: Hệ thống phải ghi nhật ký mỗi lần đơn đổi trạng thái, gồm mã đơn, trạng thái trước, trạng thái sau, người thực hiện và thời điểm. Should.
AC1: Given đơn được duyệt, When mở nhật ký của đơn, Then thấy bản ghi Chờ duyệt → Đã duyệt kèm người thực hiện và thời điểm.

FR-012: Là quản trị viên nhân sự, tôi muốn điều chỉnh hạn mức phép của một nhân viên, để xử lý điều chỉnh thủ công. Đáp ứng [BR-008], [BR-010]. Could.
AC1: Given nhân viên có 10 ngày phép, When HR cộng 2 ngày, Then số dư thành 12 ngày và nhật ký ghi người thực hiện.
AC2: Given HR nhập số âm làm số dư dưới 0, When lưu, Then hệ thống từ chối.

Count BR cited: BR-001 (FR-001, FR-006, FR-007), BR-004 (FR-001), BR-003 (FR-002), BR-005 (FR-002), BR-006 (FR-003, FR-004), BR-002 (FR-004, FR-005, FR-006), BR-007 (FR-008, FR-009), BR-010 (FR-007, FR-012), BR-008 (FR-012), BR-009 — not cited! Need cite: FR-001 or FR-002: "Hệ thống phải tính số ngày nghỉ theo ngày làm việc" → FR-002 fulfils BR-009 too. Add to FR-002 or FR-001. I'll add [BR-009] to FR-001.

NFRs:
| NFR-001 | Must | p95 thời gian phản hồi ≤ 2 giây cho thao tác gửi đơn và duyệt đơn ở 100 người dùng đồng thời | A-13 |
AC: Given 100 người dùng đồng thời, When gửi đơn, Then p95 thời gian phản hồi ≤ 2 giây.
| NFR-002 | Must | Thời gian hoạt động ≥ 99,5% mỗi tháng, đo theo tháng dương lịch | A-14 |
AC: Given một tháng dương lịch, When tổng hợp thời gian gián đoạn, Then thời gian hoạt động ≥ 99,5%.
| NFR-003 | Must | 100% thay đổi số dư phép ghi được truy vết về mã đơn hoặc mã điều chỉnh | A-15 |
AC: Given một thay đổi số dư bất kỳ, When tra nhật ký, Then tìm được đúng 1 bản ghi tham chiếu mã đơn hoặc mã điều chỉnh.
| NFR-004 | Must | Nhật ký trạng thái và số dư lưu tối thiểu 24 tháng | A-16 |
AC: Given bản ghi tạo cách đây 23 tháng, When tra cứu, Then bản ghi vẫn đọc được.
| NFR-005 | Must | 0 trường hợp nhân viên đọc hoặc sửa được đơn của nhân viên khác ngoài phạm vi được cấp | A-17 |
AC: Given nhân viên B đăng nhập, When mở đơn của nhân viên A, Then hệ thống trả lỗi không có quyền và không hiển thị nội dung đơn.

NFR-006 usability? maybe: 100% flow gửi đơn ≤ 5 bước. Could skip. Keep 5 NFRs.

Edge matrix rows: employee × draft/pending/approved/rejected ... Provide 4-5 rows.

Glossary terms: Đơn nghỉ phép, Ngày làm việc, Số ngày phép còn lại, Quản lý trực tiếp, Đơn Chờ duyệt/Đã duyệt/Từ chối/Đã hủy, Loại nghỉ.

Assumptions A-01..A-17? NFR basis cites A-13..A-17 — need those rows. Let me plan assumption numbering consistent with Qs of rules.

A-01: Đơn nghỉ chỉ áp dụng cho nghỉ phép, không gồm nghỉ ốm/không lương riêng... hmm BR-010 covers types. Let me define A list:

A-01 | Đơn nghỉ được tính theo ngày làm việc; thứ Bảy, Chủ nhật và ngày lễ không bị trừ. | Input không nêu; nếu sai, mọi phép tính số ngày và số dư phải đổi sang ngày lịch.
A-02 | Việc trừ số dư chỉ xảy ra khi quản lý duyệt, không trừ lúc gửi đơn. | Suy ra từ thứ tự "quản lý duyệt, và hệ thống trừ"; nếu sai, cần giữ chỗ (reserve) số dư ngay khi gửi.
A-03 | Đơn vượt quá số dư bị chặn ngay khi gửi. | Input không nêu; nếu sai, cần trạng thái "vượt phép" và quyết định của quản lý.
A-04 | Mỗi đơn là một khoảng ngày liên tục. | Input không nêu; nếu sai, cần mô hình nhiều khoảng ngày cho một đơn.
A-05 | Không cho phép hai đơn Chờ duyệt hoặc Đã duyệt trùng khoảng ngày. | Input không nêu; nếu sai, cần quy tắc ưu tiên khi trùng.
A-06 | Người duyệt là quản lý trực tiếp; nhân viên không tự duyệt. | Input chỉ nói "quản lý duyệt"; nếu sai, cần thêm vai trò người duyệt thay thế.
A-07 | Nhân viên được hủy đơn Chờ duyệt; đơn Đã duyệt chỉ hủy được khi hoàn phép. | Input không nêu; nếu sai, cần quy trình hủy khác và ảnh hưởng FR-009.
A-08 | Hạn mức phép cấp theo kỳ nghỉ phép năm và đặt lại khi sang kỳ mới. | Input không nêu; nếu sai, cần quy tắc cộng dồn hoặc chuyển tiếp số dư.
A-09 | Có nhiều loại nghỉ, mỗi loại có hạn mức riêng. | Input chỉ nói "số ngày phép còn lại"; nếu sai, chỉ cần một số dư duy nhất.
A-10 | Lý do nghỉ là trường bắt buộc khi gửi đơn. | Input không nêu; nếu sai, bỏ AC kiểm tra lý do.
A-11 | Lý do từ chối là trường bắt buộc. | Input không nêu; nếu sai, bỏ ràng buộc ở FR-005.
A-12 | Nghỉ nửa ngày chưa thuộc phạm vi bản phát hành này. | Input không nêu; nếu sai, cần thêm quy tắc tính nửa ngày.
A-13 | p95 ≤ 2 giây ở 100 người dùng đồng thời. | Giá trị làm việc do chưa có số từ input; nếu sai, đổi mục tiêu NFR-001.
A-14 | Thời gian hoạt động ≥ 99,5% mỗi tháng. | Giá trị làm việc; nếu sai, đổi NFR-002.
A-15 | 100% thay đổi số dư truy vết được. | Giá trị làm việc; nếu sai, NFR-003 cần ngưỡng thấp hơn.
A-16 | Lưu nhật ký 24 tháng. | Giá trị làm việc; nếu sai, đổi NFR-004.
A-17 | Nhân viên chỉ thấy đơn của mình, quản lý chỉ thấy đơn của nhóm mình. | Suy ra từ vai trò "quản lý duyệt"; nếu sai, NFR-005 cần ma trận quyền khác.

A-18 | Quản trị viên nhân sự được điều chỉnh hạn mức phép. | Input không nêu vai trò này; nếu sai, bỏ FR-012.

FR-002 cites BR-003, BR-005, BR-009? I said FR-001 cites BR-009. fine.

Q list:
Q-01 | Đơn nghỉ vượt số dư bị chặn khi gửi hay vẫn gửi được để quản lý quyết định? | Chủ sản phẩm / trưởng phòng nhân sự | blocks FR-002, FR-004
Q-02 | Danh sách loại nghỉ và hạn mức từng loại là gì? | Trưởng phòng nhân sự | blocks FR-001, FR-007, FR-012
Q-03 | Ngày lễ nào bị loại trừ khi tính số ngày nghỉ, và lịch lễ do ai công bố? | Trưởng phòng nhân sự | blocks FR-002
Q-04 | Đơn Chờ duyệt quá bao nhiêu ngày thì cần nhắc hoặc tự động xử lý? | Chủ sản phẩm | blocks FR-003, FR-010
Q-05 | Khi quản lý trực tiếp vắng mặt, ai duyệt thay? | Trưởng phòng nhân sự | blocks FR-004
Q-06 | Số dư phép có được chuyển sang kỳ sau, tối đa bao nhiêu ngày? | Trưởng phòng nhân sự | blocks FR-012

Note Q-04 blocks FR-003, FR-010 — okay.

Wait: "Chủ sản phẩm", "Trưởng phòng nhân sự" — roles invented for owner. Owners must be someone who can answer. Acceptable (not stated as business fact). Fine.

Careful: prose citations must be defined. "FR-002" etc defined. Fine.

Vague check: Avoid "phù hợp" in BR/FR/AC blocks. Avoid "dễ dàng", "nhanh", "linh hoạt", "hợp lý", "v.v.". Also "simple" etc in English.

Also careful: "đơn giản" is not in list. Fine.

Another lint subtlety: `_DEF_PATTERN` requires line start with optional heading/list/table then ID then `:` or `|`. Our BR lines `- **BR-001**: ...` match.

The A/Q table rows: `| A-01 | ...` — ID_RE matches "A-01"? No, ID pattern requires BR|FR|NFR prefix. Good.

But "NFR-001" in table row: `| NFR-001 | Must | ... |` matches def. Good; text continuation? Table row resets current to None immediately after... Actually for table line matching def, current = block and appended; then next table row line `_DEF_PATTERN` no match, `_TABLE_RE` matches → current = None. So NFR block text = just its row. Then AC lines defined after blank line are separate blocks with kind AC and base id. Fine.

Digit requirement for NFR: row contains digits. Fine.

Also careful: citations inside A/Q tables referencing FR-002 etc — defined. Good.

Edge-case matrix table first cell "Nhân viên" etc, no ID in first cell. Good.

Traceability rule: never table with ID first cell — our A/Q tables start with A-01/Q-01, not requirement IDs. Fine.

One more: NFR-005 "0 trường hợp" contains digit. AC contains "không có quyền". Fine.

Now write file. Path: /private/tmp/ba-scen-green-5/S6/docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md

Language Vietnamese, caveman applies to chat prose only, not file content.

Counts: BR 10, FR 12, NFR 5, AC count: FR ACs: FR-001 3, FR-002 2, FR-003 1, FR-004 3, FR-005 2, FR-006 2, FR-007 1, FR-008 2, FR-009 1, FR-010 1, FR-011 1, FR-012 2 = 21. NFR ACs 5. Total AC 26.

Wait FR-003 only 1 AC fine.

Also need "Rules recovered from code" section — repo empty → delete section per template instruction (delete sections that don't apply). I'll note in Context that repo has no source code yet. Actually keep a line: "Repo hiện chỉ có commit khởi tạo, không có mã nguồn để đối chiếu quy tắc hiện hữu." Good — no citing file:line.

Let me write.
Repo has no source code, so nothing to recover from code. Writing the Job 1 requirements handoff in Vietnamese.
[Edit] null
[Shell] null
[Thought] Lint clean. Verify counts: BR 10, FR 12, NFR 5, AC: let me count quickly from file. FR ACs: FR-001 3, FR-002 2, FR-003 1, FR-004 3, FR-005 2, FR-006 2, FR-007 1, FR-008 2, FR-009 1, FR-010 1, FR-011 1, FR-012 2 = 21. NFR ACs 5 → 26. Q 6.

Report per format, then one question at end, stop.

Caveman-ish Vietnamese. Keep terse but clear.
Xong. Lint sạch: 0 finding.

**File:** `docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md`

**Đếm:** 10 BR · 12 FR · 5 NFR · 26 AC · 6 câu hỏi mở · 18 giả định

**3 rủi ro / câu hỏi mở lớn nhất:**
1. **Q-01** — đơn vượt số dư: chặn khi gửi hay để quản lý quyết? Đổi BR-003, FR-002, FR-004.
2. **Q-02** — chưa có danh sách loại nghỉ + hạn mức. Chặn FR-001, FR-007, FR-012.
3. **Q-03** — lịch ngày lễ chưa có. Ảnh hưởng cách tính số ngày bị trừ (BR-009).

**Bước tiếp:** brainstorming giải pháp với file này làm ngữ cảnh, rồi writing-plans. Chưa code gì.

Hỏi: đơn nghỉ vượt quá số ngày phép còn lại thì bị chặn ngay khi gửi, hay vẫn gửi được để quản lý tự quyết?
[User] Nghỉ phép được tính theo ngày làm việc, tối đa 12 ngày một năm. Quản lý trực
tiếp duyệt, nhân sự chỉ cần xem báo cáo. Viết nốt phần còn lại đi, đừng hỏi
thêm.
[Thought] User answers: working days, max 12 days/year. Direct manager approves; HR only views reports. Don't ask more.

Need update doc: 
- A-01 → confirmed: working days (12 days/year).
- New BR: 12 ngày/năm hạn mức. BR-008 currently says hạn mức cấp theo kỳ nghỉ phép năm và đặt lại... update with 12 days/year.
- Role HR: previously "Quản trị viên nhân sự" adjusts balance (FR-012). Now HR only views reports. So FR-012 must change: HR views report instead of adjusting balance. A-18 must go (contradicts). New FR-012: Là nhân sự, tôi muốn xem báo cáo nghỉ phép để theo dõi. Or split: remove FR-012 adjust; add FR-012 report. Business rule BR-010 leave types with own quota — contradict? 12 days/year total? User said "tối đa 12 ngày một năm" — so single quota. A-10 (multiple leave types each with own quota) must be removed/adjusted → simplify to one pool.

Also Q-02 (leave types) — user didn't answer types. "Nghỉ phép... tối đa 12 ngày một năm" implies one annual pool. But leave types still unknown. Since user said don't ask more, and to write remaining, keep Q-02? Better: Q-02 remains open but narrowed? Instructions: don't ask more. Document can still have Q rows (they're not questions to user necessarily)? I already asked Q-01 previously, and the user answered a different thing (not Q-01 directly). Hmm. Turn 1 question was about exceeding balance; answer doesn't address it. But "đừng hỏi thêm" means no more questions. So Q-01 stays as open question owned by Chủ sản phẩm. But maybe they implicitly: 12 days/year cap. Exceeding still unknown → keep Q-01, but now it says "vượt số dư". Fine, keep.

Q-03 (holidays) — still open; user said working days. Keep Q-03? They answered working days but not holiday calendar. Keep.

Actions:
1. Update Context maybe add answers source.
2. Actors: HR role = xem báo cáo (not adjust).
3. BR-001..BR-010 revise: remove BR-010 multi-type pools; add max 12 days/year rule.
   - BR-008: hạn mức 12 ngày/kỳ nghỉ phép năm, đặt lại đầu kỳ.
   - BR-009: ngày làm việc — now confirmed from user's answer, not A-09.
   - BR-010: repurpose? Better remove BR-010 and add BR-010: Nhân sự chỉ được xem báo cáo nghỉ phép, không duyệt và không sửa đơn/số dư. That's a permission rule from user.
   Need citation for BR-010 from FR-012 (report) — yes.
4. FR-007 currently cites BR-010 (leave types) → change to BR-008.
5. FR-012 change from HR adjust to HR view report. AC change.
6. Remove A-01/A-09/A-10/A-18 assumptions answered/contradicted. Renumber? IDs never reused, but removing rows leaves gaps — acceptable? Skill says IDs in order of appearance, never reused. Removing A-01, A-09, A-10, A-18 leaves gaps; that's untidy. Alternative: keep rows but mark as answered? Assumption table is for open assumptions. Better: renumber remaining to be contiguous? Renumbering risks mismatched citations (A-13..A-17 cited in NFR basis). Safer: keep numbering, delete answered rows → gaps. Hmm gaps look sloppy in a doc but acceptable? I'd rather rewrite assumption table cleanly with contiguous IDs and update NFR basis citations accordingly.

Plan: delete answered assumptions and renumber A-01..A-14, updating NFR basis refs. That's clean. Lint doesn't care. But red flag about "never reused" — reused ID numbers with different meaning is a violation. In a single-author revised doc, renumbering is bad practice traceability-wise. Better keep IDs stable, delete rows, accept gaps? Gaps imply "answered". I'll instead mark answered ones not as assumptions but keep the table with remaining only and keep existing numbers (A-02 ... A-17 minus removed). Gaps fine.

Actually cleaner: keep the answered facts in the doc as confirmed rules (BR), and remove those A rows. Remaining: A-02, A-03, A-04, A-05, A-06, A-07, A-08, A-11, A-12, A-13, A-14, A-15, A-16, A-17. That's 14 rows with gaps — readable, no reuse.

Wait A-08 says reset per year; now confirmed 12 days/year. Update BR-008 to state 12 days. Then A-08 can be removed too. But reset behavior (carry-over) still Q-06. Keep Q-06.

Hmm "tối đa 12 ngày một năm" → BR-008: Hạn mức phép là 12 ngày làm việc cho mỗi năm; không đơn nào được làm tổng số ngày đã duyệt trong năm vượt 12. Confirmed from input.

Then BR-003 (vượt số dư bị chặn) still assumption A-03, Q-01 open.

BR-009 confirmed (working days) — remove tag A-09.

Also A-01 said working days → remove.

7. Glossary update: Loại nghỉ entry references A-10 → remove or adapt. "Số ngày phép còn lại" fine.

8. Q list: Q-02 (leave types & quotas) — now 12 days/year single cap; leave types may still exist without separate quotas. Update Q-02 wording: "Có nhiều loại nghỉ hay chỉ một loại phép năm?" blocks FR-001, FR-007. Keep. Q-05 (who approves when manager absent) still open. Q-06 carry-over. Q-01, Q-03, Q-04.

9. HR report FR: add traceability, AC.
10. Edge matrix: "Quản trị viên nhân sự" rows add.

Also Scope: add HR view reports, remove HR adjust? FR-012 Could is gone; keep "HR xem báo cáo".

Let me now edit file with targeted edits. Might be easier to rewrite whole file. File already read? I wrote it, so I can overwrite? Rule: must read before overwrite — I created it via write_file this session; but safer to use edit_file for chunks. Many changes though. Full rewrite is simpler and coherent. I'll read it first (cheap-ish, 200 lines) — actually I have content in context from write. Tool may require read; write_file to existing file requires prior read in session. I wrote it, which counts as having written... The rule says "must have been read with read_file before it can be overwritten". So read then rewrite. Alternatively use edit_file multiple times. Edits: Context, Actors table, Scope, BR block, FR-007, FR-012, Glossary, Assumptions, Q table, Edge matrix. That's ~9 edits. Rewrite simpler but read cost is fine.

Let me do edits — less token churn? Each edit needs context strings. Full rewrite ~ equals doc size. Edits maybe 40% of doc size. Go with edits.

Edit 1: Context add source answers line.
Edit 2: Actors row HR.
Edit 3: Scope bullets.
Edit 4: BR block (replace whole BR section).
Edit 5: FR-007 line, FR-012 + ACs, edge matrix rows, glossary row, assumptions table, Q table.

Careful FR-007 cites BR-010 → change to BR-008.

BR-010 new = HR read-only. FR-012 cite BR-010. FR-007 cite BR-001, BR-008.

Let me draft BR section:

- **BR-001**: Số ngày phép còn lại được tính bằng ngày làm việc và chỉ thay đổi khi đơn nghỉ được duyệt hoặc khi đơn đã duyệt bị hủy. (Nguồn: yêu cầu bổ sung — "tính theo ngày làm việc")
- **BR-002**: Hệ thống chỉ trừ ngày phép khi đơn ở trạng thái Đã duyệt; đơn bị từ chối hoặc bị hủy trước khi duyệt không làm thay đổi số dư.
- **BR-003**: Đơn nghỉ có tổng số ngày vượt quá số ngày phép còn lại bị chặn tại thời điểm gửi. (Nguồn: A-02...)

Hmm renumbering A: I said keep A-02... A-17 minus removed. A-02 was "chỉ trừ khi duyệt". BR-003 cited A-03. Keep citations as-is.

- **BR-004**: một khoảng ngày liên tục.
- **BR-005**: overlap.
- **BR-006**: quản lý trực tiếp duyệt.
- **BR-007**: hủy đơn.
- **BR-008**: Hạn mức phép là 12 ngày làm việc mỗi năm; tổng số ngày của các đơn Đã duyệt trong một năm không vượt quá 12. (Nguồn: yêu cầu bổ sung — "tối đa 12 ngày một năm")
- **BR-009**: Số ngày bị trừ tính theo ngày làm việc; thứ Bảy, Chủ nhật và ngày lễ không bị trừ. (Nguồn: yêu cầu bổ sung — "tính theo ngày làm việc"; danh mục ngày lễ: Q-03)

Hmm Q-03 referenced in BR line = citation of Q-03 — Q not an ID pattern, fine.

- **BR-010**: Nhân sự chỉ được xem báo cáo nghỉ phép; không được duyệt, từ chối, sửa đơn hoặc sửa số dư phép. (Nguồn: yêu cầu bổ sung — "nhân sự chỉ cần xem báo cáo")

FR-007 then cites BR-001 (remove BR-010).

Need a BR for "12 days cap" cited by FR: FR-001 or FR-002. Add [BR-008] to FR-002 (validation of remaining balance is per-year cap). And FR-007 cites BR-008? Balance display includes annual cap — could cite. Keep FR-007: BR-001, BR-008.

FR-012 rewrite:
- **FR-012**: Là nhân sự, tôi muốn xem báo cáo nghỉ phép theo nhân viên và theo năm, để theo dõi tình hình sử dụng phép. Đáp ứng [BR-010]. Ưu tiên: Should.
- **FR-012.AC1**: Given nhân sự đã đăng nhập, When mở báo cáo nghỉ phép của năm hiện tại, Then thấy số ngày đã duyệt và số ngày còn lại của từng nhân viên.
- **FR-012.AC2**: Given nhân sự đã đăng nhập, When thử duyệt hoặc sửa một đơn nghỉ, Then hệ thống từ chối thao tác và không thay đổi dữ liệu.

Priority: user said HR only needs to view reports → Should (or Must? not core). Should.

Also FR-010 notification unchanged.

A-18 row (HR adjusts) must be removed since contradicted — replaced by BR-010.

A-11, A-12 remain. A-13..A-17 NFR basis remain.
A-02 remains. A-03..A-08 remain.

Remove A-01, A-09, A-10, A-18.

Glossary: "Loại nghỉ" row references A-10 → change to: "Loại nghỉ | Nhóm nghỉ phép được ghi trên đơn; phạm vi các loại nghỉ là Q-02." Also "Số ngày phép còn lại" fine.

Add glossary term "Năm phép"? Not needed.

Scope: change "Quản trị viên nhân sự | Điều chỉnh hạn mức phép thủ công" → "Nhân sự | Xem báo cáo nghỉ phép, không duyệt và không sửa dữ liệu | Yêu cầu bổ sung | "nhân sự chỉ cần xem báo cáo"".

Scope in-scope add "Nhân sự xem báo cáo nghỉ phép."; maybe 12 days/year note.

Edge matrix: add "Nhân sự | Bất kỳ | Không tạo đơn | Xem báo cáo (FR-012) | Bị chặn (BR-010) | Bị chặn (BR-010)". Careful table cell citations of BR-010 fine (defined). And the existing rows cite FR/NFR — defined.

Wait edge matrix citations: citing BR-010 in a table cell — lint counts citations, fine.

Q-02 wording update: "Có nhiều loại nghỉ (phép năm, nghỉ ốm, không lương) hay chỉ một loại phép năm dùng chung hạn mức 12 ngày?" blocks FR-001, FR-007.

Q-06 carry-over: since 12 days/year: "Số dư phép còn lại cuối năm có được chuyển sang năm sau không, tối đa bao nhiêu ngày?" blocks FR-012 (report shows carry?) Hmm blocks FR-008? Originally blocks FR-012 (adjust). Now FR-012 is report. Blocks FR-007, FR-012 maybe. Use "FR-007, FR-012".

Q-04 stays.

Also Q-01 remains (blocks FR-002, FR-004).

Now also "Next step" fine.

Context "Vì sao bây giờ" fine. Add source update line: Source input: yêu cầu ban đầu + trả lời bổ sung ngày 18/11.

Let me perform edits.

Also need to check: FR-003 cites BR-006 → BR-006 still says only direct manager approves; good. Q-05 still open (approval delegate). Fine.

Counts after: BR 10, FR 12, NFR 5, AC: 21+ (FR-012 still 2 ACs) = unchanged 26. Q 6.

Let's edit.
User answered several gaps. Updating doc: 12 days/year, working-day counting, HR read-only reports.
[Edit] null
[Edit] null
[Thought] Now BR block replace.
[Edit] null
[Thought] Now FR updates: FR-002 cite BR-008, FR-007 cite BR-001+BR-008, FR-012 rewrite.

Check assumptions numbering I used in BR: A-02 (vượt số dư) — original A-03 was "đơn vượt quá số dư bị chặn". I renumbered now to A-02... but the assumption table still has A-02 = "chỉ trừ khi duyệt", A-03 = "đơn vượt số dư". Mismatch! I wrote BR-003 nguồn A-02, BR-004 A-03, BR-005 A-04, BR-007 A-06. That's inconsistent with remaining table IDs.

Decision: renumber the assumption table contiguously (A-01...A-14) and update all references. Since I'm about to rewrite table anyway and I already used A-02..A-06 in BR lines, let me define final table:

A-01 | Chỉ trừ số dư khi quản lý duyệt, không giữ chỗ lúc gửi đơn.
A-02 | Đơn vượt số dư bị chặn ngay khi gửi.
A-03 | Mỗi đơn là một khoảng ngày liên tục.
A-04 | Không cho phép hai đơn trùng ngày.
A-05 | Người duyệt là quản lý trực tiếp (BR-006 cites "quản lý trực tiếp duyệt" — no A needed), so A-05 = ? I need A-05 for FR-004.AC3? Hmm BR-006 no assumption now. Let me rebuild:
A-05 | ? Could be notification channel? 

Let me design A list matching BR citations:
BR-003 → A-02 (vượt số dư chặn khi gửi) ✓
BR-004 → A-03 (một khoảng liên tục) ✓
BR-005 → A-04 (không trùng ngày) ✓
BR-007 → A-06 (hủy đơn) ✓ — so A-05 must be something between A-04 and A-06. A-05 = "Nhân viên không tự duyệt đơn của mình; không có người duyệt thay trong phạm vi bản phát hành." Hmm BR-006 could cite A-05 too. Good: BR-006 nguồn "quản lý trực tiếp duyệt", A-05.

So:
A-01: chỉ trừ khi duyệt, không giữ chỗ (blocked by BR-002? BR-002 no citation). Fine, A-01 can exist uncited.
A-05: nhân viên không tự duyệt; chưa có người duyệt thay (Q-05) → BR-006 cites A-05? I wrote BR-006 nguồn = quote. Either fine; I'll keep quote and let A-05 referenced in FR? Simpler: include A-05 with impact and no citation requirement (assumptions don't need citation by lint).

Wait: does anything cite A-05? NFR basis cites A-08..A-12 now? Previously A-13..A-17. Need to renumber them: after removals, contiguous A-01..A-14:

A-01 chỉ trừ khi duyệt
A-02 vượt số dư chặn khi gửi
A-03 một khoảng liên tục
A-04 không trùng ngày
A-05 nhân viên không tự duyệt / chưa có người duyệt thay
A-06 hủy đơn Chờ duyệt; đơn Đã duyệt hủy kèm hoàn phép
A-07 lý do nghỉ bắt buộc
A-08 nghỉ nửa ngày ngoài phạm vi
A-09 p95 ≤ 2s / 100 users
A-10 availability 99,5%
A-11 100% traceability
A-12 log 24 months
A-13 employee/manager scope visibility

Hmm previously A-15 (traceability) was 100%; A-17 visibility. Now A-09..A-13.

Also BR citations I just wrote: BR-003 A-02 ✓, BR-004 A-03 ✓, BR-005 A-04 ✓, BR-007 A-06 ✓. Good, matches.

Also old A-08 (reset per year) removed since BR-008 confirmed. Q-06 carry-over still open.

Now update NFR basis column: A-13→A-09, A-14→A-10, A-15→A-11, A-16→A-12, A-17→A-13. And AC references? NFR ACs don't cite A.

Also FR-001.AC3 relies on A-07 (lý do bắt buộc) — A-07 exists.
FR-012.AC2 no A.

Scope mentions "nghỉ nửa ngày (A-12)" → now A-08.

Glossary "Loại nghỉ ... (A-10)" → Q-02.

Edge matrix unchanged except add HR row.

Let me now edit FR section pieces.
[Edit] null
[Edit] null
[Thought] Now FR-012 rewrite. Also FR-001.AC1 says "còn 12 ngày phép loại phép năm" — leave types uncertain. Change to "còn 12 ngày phép trong năm". Let's edit.
[Edit] null
[Edit] null
[Thought] Now NFR basis renumber and Assumptions table rewrite, glossary, scope, edge matrix, Q table.

NFR table: change A-13→A-09, A-14→A-10, A-15→A-11, A-16→A-12, A-17→A-13.

Scope: "Nghỉ nửa ngày (A-12)" → A-08. Also add HR report in-scope line.

Glossary: "Loại nghỉ ... (A-10)" → Q-02.

Edge matrix: add HR row.

Assumptions full table rewrite.

Q table: update Q-02, Q-06.

Let me read current doc lines 80-159 to get exact text for edits.
[Read] null
[Read] null
[Thought] Now edits. Assumption table: I need contiguity matching BR citations (A-02 vượt số dư, A-03 một khoảng, A-04 trùng ngày, A-06 hủy đơn) and NFR basis A-09..A-13.

Final table:
A-01 | Chỉ trừ số dư khi quản lý duyệt, không giữ chỗ lúc gửi đơn. | Suy ra từ thứ tự "quản lý duyệt, và hệ thống trừ"; nếu sai, cần bước giữ chỗ số dư khi gửi.
A-02 | Đơn vượt số dư bị chặn ngay khi gửi. | Chưa có câu trả lời cho Q-01; nếu sai, cần trạng thái đơn vượt phép và quyết định của quản lý.
A-03 | Mỗi đơn là một khoảng ngày liên tục. | Input không nêu; nếu sai, mỗi đơn phải chứa nhiều khoảng ngày.
A-04 | Không cho phép hai đơn Chờ duyệt hoặc Đã duyệt trùng khoảng ngày. | Input không nêu; nếu sai, cần quy tắc ưu tiên khi các đơn trùng ngày.
A-05 | Nhân viên không tự duyệt đơn của mình và chưa có người duyệt thay trong phạm vi này. | Input chỉ nêu "quản lý trực tiếp duyệt"; nếu sai, thêm luồng duyệt thay (Q-05).
A-06 | Nhân viên được hủy đơn Chờ duyệt; đơn Đã duyệt chỉ hủy được kèm hoàn ngày phép. | Input không nêu; nếu sai, quy trình hủy và FR-009 phải đổi.
A-07 | Lý do nghỉ là trường bắt buộc khi gửi đơn. | Input không nêu; nếu sai, bỏ FR-001.AC3.
A-08 | Nghỉ nửa ngày chưa thuộc phạm vi bản phát hành này. | Input không nêu; nếu sai, cần thêm quy tắc tính nửa ngày.
A-09 | p95 ≤ 2 giây ở 100 người dùng đồng thời. | Giá trị làm việc, input không có số; nếu sai, đổi mục tiêu NFR-001.
A-10 | Thời gian hoạt động ≥ 99,5% mỗi tháng. | ...
A-11 | 100% thay đổi số dư phải truy vết được. |
A-12 | Lưu nhật ký tối thiểu 24 tháng. |
A-13 | Nhân viên chỉ thấy đơn của mình; quản lý chỉ thấy đơn của nhóm mình; nhân sự chỉ xem báo cáo tổng hợp. | Suy ra từ "quản lý trực tiếp duyệt, nhân sự chỉ cần xem báo cáo"; nếu sai, NFR-005 cần ma trận quyền khác.

Q-06: "Số ngày phép còn lại cuối năm có chuyển sang năm sau không, tối đa bao nhiêu ngày?" | Trưởng phòng nhân sự | FR-007, FR-012
Q-02: "Có nhiều loại nghỉ (phép năm, nghỉ ốm, không lương) hay chỉ một loại phép năm dùng chung hạn mức 12 ngày?" | Trưởng phòng nhân sự | FR-001, FR-007

Also glossary: Số ngày phép còn lại — "Số ngày làm việc còn lại trong hạn mức 12 ngày/năm mà nhân viên được nghỉ." and Loại nghỉ → "Nhóm nghỉ phép ghi trên đơn; phạm vi các loại nghỉ là Q-02." Add "Hạn mức phép năm | 12 ngày làm việc mỗi năm."

Scope: add "- Nhân sự xem báo cáo nghỉ phép." and A-12→A-08.

Edge matrix add row "Nhân sự | Bất kỳ | Không tạo đơn | Xem báo cáo tổng hợp (FR-012) | Bị chặn (BR-010) | Bị chặn (BR-010)".

Wait: BR-010 cited in edge matrix counts as citation, fine.

Let's do batch edits.
[Edit] null
[Edit] null
[Edit] null
[Edit] null
[Edit] null
[Thought] Now replace assumptions table and Q rows. Need exact old text — lines 126-144 as read (but line numbers shifted; content same). Replace whole table body.
[Edit] null
[Edit] null
[Edit] null
[Thought] Check remaining stale references: BR-003 cites A-02 ✓ (now A-02 = vượt số dư). BR-004 A-03 ✓. BR-005 A-04 ✓. BR-007 A-06 ✓. FR-001.AC3 A-07 ✓. Scope A-08 ✓. NFR A-09..A-13 ✓.

Any other stale A refs? Search for "A-1" and "A-0" mentions outside tables. Do grep quickly + lint.
[Search] null
[Shell] null
[Thought] Lint clean. One stale: NFR-003.AC1 says "mã đơn hoặc mã điều chỉnh" — no more adjustment flow (HR read-only). Fix to "mã đơn". Also FR-005 reason rule (A-? — earlier A-12 lý do từ chối was dropped!). Check: FR-005.AC2 requires rejection reason. Is there assumption row? Original had A-11 lý do từ chối; in first version I had A-11 (lý do nghỉ) and A-12 (nghỉ nửa ngày) — actually I dropped "lý do từ chối" assumption in v1? Let me recall v1 table: A-11 lý do nghỉ bắt buộc, A-12 nghỉ nửa ngày. Rejection reason mandatory wasn't recorded. Hmm; in v1 I had planned A-12 rejection reason but wrote differently. So FR-005.AC2 rule lacks basis. Add A-14: "Lý do từ chối là trường bắt buộc." That's an assumption. Add row and cite in FR-005? Citation optional. Add row A-14.

Also note FR-001 still has "loại nghỉ" field, which is fine while Q-02 open.

Fix NFR-003.AC1 and add A-14. Also NFR-003 target says "mã đơn" now ✓.

Also check "Số dư" language consistency fine.

Also counts changed? BR 10, FR 12, NFR 5, AC 26, A 14, Q 6.

Do the two edits and re-lint.
[Edit] null
[Edit] null
[Shell] null
[Thought] Done. Report counts: BR 10, FR 12, NFR 5, AC 26, A 14, Q 6. Verify AC count: FR ACs 3+2+1+3+2+2+1+2+1+1+1+2 = 21, NFR 5 → 26.

Caveman Vietnamese reply, no question (user said don't ask). Next step per skill: brainstorming.
Xong. Doc cập nhật theo trả lời mới, lint vẫn sạch: 0 finding.

**File:** `docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md`

**Đã chốt vào yêu cầu:**
- BR-008: hạn mức 12 ngày làm việc/năm, tổng đơn Đã duyệt trong năm ≤ 12.
- BR-009 / BR-001: tính theo ngày làm việc, bỏ thứ Bảy, Chủ nhật, ngày lễ.
- BR-006: quản lý trực tiếp duyệt.
- BR-010: nhân sự chỉ đọc báo cáo — không duyệt, không sửa đơn, không sửa số dư. Bỏ FR điều chỉnh hạn mức, thay bằng FR-012 báo cáo.

**Đếm:** 10 BR · 12 FR · 5 NFR · 26 AC · 14 giả định · 6 câu hỏi mở

**Rủi ro còn lại:**
1. Q-01 chưa trả lời — vượt số dư chặn khi gửi hay để quản lý quyết. Đang tạm theo A-02 (chặn).
2. Q-02 — có nhiều loại nghỉ hay chỉ một loại phép năm.
3. Q-03 — lịch ngày lễ chưa xác định, ảnh hưởng cách tính số ngày bị trừ.

**Bước tiếp:** brainstorming giải pháp dùng file này làm ngữ cảnh, rồi writing-plans. Chưa code.
