# green S6 — agent 65880adb-9a74-4a2d-b97e-ea1722cacef9 (command-code/deepseek/deepseek-v4.1-flash)

[User] Read and follow /tmp/ba-skill-under-test/business-analysis/SKILL.md.

Ứng dụng của chúng tôi cần thêm tính năng đăng ký nghỉ phép: nhân viên gửi yêu
cầu, quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại. Hãy viết yêu cầu
đầy đủ trước khi code. Nếu cần hỏi tôi điều gì, hãy hỏi ở cuối câu trả lời rồi
dừng lại. Lưu kết quả thành một file markdown trong repo này.
I'll start by loading the required skill and the caveman output style.
[Activate skill]
[Read] null
[Thought] Let me read the referenced files. Also need to explore repo to recover current rules (code-recovery). Let me look at repo structure.

Skill says: Job 1 feed dev work → needs references/requirements.md, templates/requirements.md. Also references/elicitation.md, references/code-recovery.md.

Migration: user asks "viết yêu cầu đầy đủ trước khi code" — full requirements before code. That's Job 1. Mode: interview — user is present, and says "Nếu cần hỏi tôi điều gì, hãy hỏi ở cuối câu trả lời rồi dừng lại." → interview mode, one question per message.

So: read input = the request. Explore repo for current rules. Then write requirements doc with A-nn/Q-nn, ask ONE question at end and stop.

Let me read skill resources and explore repo in parallel.
Let me read skill references + templates and look at the repo.
[Read] null
[Read] null
[Thought] Repo empty (only .git). No existing code → no code recovery needed. Job: Job 1 (requirements) — user asks write full requirements before coding, save markdown in repo.

Mode: user is present, but user said "Nếu cần hỏi tôi điều gì, hãy hỏi ở cuối câu trả lời rồi dừng lại" (if need to ask, ask at end then stop). That's a permission to ask but constraints on form. Skill says interview mode = one question per message, then stop. But user also asked to save result as file and asks questions at end. Hmm. The user's requirement: write full requirements file, then ask questions at end and stop. So combine: produce document (draft-ish, with A-nn/Q-nn registers) then one question at end. Interview mode wants one question at end — that satisfies "ask at end then stop". But interview mode says ask BEFORE writing? Actually core loop: gap finder → mode → analyze → write. Interview mode asks one question at a time. But user explicitly says write the full requirements then ask questions at end. That's a user override — write complete doc, unknowns recorded as A/Q, then ask single highest-impact question at end.

Hmm, tension: the skill says one question per message. User overrides ordering. I'll write complete doc with A-nn/Q-nn, then ask exactly one question at end (highest impact).

Let me check lint script exists.

Vietnamese output. Path: repo root docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md.

Need careful: the "vague term" lint list — Vietnamese. Let me read the lint script to know banned words.
[Read] null
[Thought] Repo empty (only .git). Job 1 (requirements). User's request: "Hãy viết yêu cầu đầy đủ trước khi code" — write full requirements before code. "Nếu cần hỏi tôi điều gì, hãy hỏi ở cuối câu trả lời rồi dừng lại." So user is present → interview mode. Hmm. But they ask to save result as markdown file in repo. The skill says interview mode asks one question per message then stop. But user request is "write full requirements before code" — they want a doc. Question: should I write the doc now and ask questions at end?

Skill: mode selection — user present and has not opted out of questions → Interview mode. But user says "write full requirements... if you need to ask me something, ask at the end and stop." That's essentially: produce the doc with assumptions/open questions, ask at end. That's a hybrid: draft + one question? The skill's stop rule allows writing doc when gaps recorded as A-nn/Q-nn. The user's instruction ("hãy viết yêu cầu đầy đủ trước khi code... nếu cần hỏi thì hỏi ở cuối") reads as "just draft, ask at end" → Draft behavior with one closing question. I'll write the complete doc with A/Q registers, lint clean, then ask ONE highest-impact question at the end (as skill requires: exactly one question in a message).

Now build requirements in Vietnamese. Must satisfy lint: every BR cited by FR, every FR/NFR has AC, no dangling refs, no duplicate IDs, no vague terms, NFR with numbers.

Careful about vague terms list: "nhanh" (word-bounded), "dễ dàng", "thân thiện", "linh hoạt", "v.v.", "phù hợp", "hợp lý", "fast", "simple", "etc." Avoid those words. Note "phù hợp" — avoid entirely. "hợp lý" avoid.

Also lint: `_DEF_PATTERN` matches lines starting with optional list marker / heading / table pipe, then optional **, then ID followed by `:` or `|`. Fine.

Careful: BR definitions that appear in tables would be parsed. Avoid IDs in first cell of tables.

Also the "Rules recovered from code" section — repo empty, no code. So delete that section.

Job 1 file path: inside git repo → docs/ba/YYYY-MM-DD-<topic>-requirements.md. Date 2026-11-18. Topic: dang-ky-nghi-phep. So `docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md`.

Output language Vietnamese. FR frame: "Là <vai trò>, tôi muốn <khả năng>, để <kết quả>. Đáp ứng [BR-001]. Ưu tiên: Must."

Note lint requires "Fulfils" ... no, lint doesn't check. But skill says translate labels including `Fulfils` and `Priority:`. So "Đáp ứng [...]" and "Ưu tiên: Must." Good.

Now content design. Actors: nhân viên (employee), quản lý trực tiếp (line manager), HR/admin (unknown — Q), maybe approver chain. Input is thin: employee sends request, manager approves, system deducts remaining leave days. Gaps → A/Q.

Let me design business rules:

- BR-001: Một yêu cầu nghỉ phép chỉ được tạo khi nhân viên còn số ngày phép ≥ số ngày xin nghỉ (checked against balance). A-01/Q.
- BR-002: Quản lý trực tiếp của nhân viên là người duyệt duy nhất cho mỗi yêu cầu. (A/Q about multi-level approval)
- BR-003: Số ngày trừ = số ngày làm việc trong khoảng nghỉ, trừ ngày nghỉ tuần và ngày lễ. (A)
- BR-004: Số ngày phép chỉ bị trừ khi yêu cầu chuyển sang trạng thái Đã duyệt; không trừ khi Chờ duyệt hoặc Từ chối.
- BR-005: Khi yêu cầu bị huỷ sau khi đã duyệt, hệ thống hoàn lại đúng số ngày đã trừ.
- BR-006: Không cho phép hai yêu cầu chờ duyệt/đã duyệt trùng khoảng ngày của cùng một nhân viên.
- BR-007: Nhân viên không được tự duyệt yêu cầu của mình. (segregation)
- BR-008: Yêu cầu đã Từ chối hoặc Đã huỷ là trạng thái cuối; không đổi được nữa.
- BR-009: Ngày bắt đầu nghỉ phải sau thời điểm gửi yêu cầu ít nhất ... hmm inventing threshold → A. Better: BR with A-nn basis. Skill says thresholds not in input → A-nn. I can state rule with A reference in the A table, but BR line should be testable. I'll include BR-009: "Yêu cầu phải có ngày kết thúc ≥ ngày bắt đầu" — that's derivable, safe.
- BR-010: Số ngày phép còn lại không được âm.

Let me get a manageable set: 8-10 BRs, 10-12 FRs, 5-6 NFRs, ACs for each.

FR list:
1. FR-001: Là nhân viên, tôi muốn gửi yêu cầu nghỉ phép với ngày bắt đầu, ngày kết thúc và lý do, để xin nghỉ theo quy trình. [BR-009]
2. FR-002: Là nhân viên, tôi muốn xem số ngày phép còn lại trước khi gửi, để chọn số ngày nghỉ không vượt quá số dư. [BR-010]
3. FR-003: Là nhân viên, tôi muốn huỷ yêu cầu đang chờ duyệt, để rút lại khi không còn nhu cầu. [BR-008? or BR-005]
4. FR-004: Là quản lý, tôi muốn xem danh sách yêu cầu đang chờ duyệt của nhân viên mình, để xử lý theo thứ tự. [BR-002]
5. FR-005: Là quản lý, tôi muốn duyệt yêu cầu, để nhân viên được nghỉ và số ngày phép bị trừ. [BR-004]
6. FR-006: Là quản lý, tôi muốn từ chối yêu cầu kèm lý do, để nhân viên biết vì sao. [BR-004]
7. FR-007: Hệ thống phải trừ số ngày phép khi yêu cầu được duyệt... (system behavior) [BR-004]
8. FR-008: Hệ thống phải hoàn lại số ngày phép khi yêu cầu đã duyệt bị huỷ. [BR-005]
9. FR-009: Hệ thống phải chặn gửi yêu cầu khi số dư không đủ. [BR-001]
10. FR-010: Hệ thống phải chặn hai yêu cầu trùng khoảng ngày. [BR-006]
11. FR-011: Hệ thống phải chặn quản lý tự duyệt yêu cầu của mình. [BR-007]
12. FR-012: Là nhân viên, tôi muốn xem trạng thái yêu cầu của mình. [BR-008]
13. FR-013: Là quản lý, tôi muốn xem số ngày phép còn lại của nhân viên khi duyệt... optional. Maybe skip or include Could.

Also notifications? Not in input → Q/A. Could add FR as Could pending Q. Better keep to scope and record Q.

NFRs: response time ≤ 2s p95, availability, audit log retention, authorization (manager only sees own reports), data retention. Each with numbers and basis (A-nn).

Traceability: every BR must be cited from FR/NFR/AC blocks. Citation detection: citations inside block lines incl. AC lines under an FR block... Note the scanner: blocks are created on definition lines; citation block_kind applies when line continues current block. `cited_br` collects citations whose block_kind is FR/NFR/AC. AC definition lines get kind AC — so BR cited in an AC counts. But careful: a blank line resets `current`, so consecutive FR definitions get their own blocks; citation on FR line kind=FR ✓.

Orphan BR check: each BR must be cited on a FR/NFR/AC line, not just in prose. So each BR appears in a "Đáp ứng [BR-xxx]" on an FR line. Good.

Also the BR block text continues until blank line/table/heading. Vague check runs on block text including continuation lines — so list of ACs immediately under FR with no blank line get included in FR's block text. Fine as long as no vague words.

Careful with vague term "phù hợp" — avoid. Also avoid "nhanh". Also "đơn giản" isn't in list. "dễ dàng" avoid.

NFR table format: `| NFR-001 | Must | ... | basis |`. The definition pattern requires ID followed by `:` or `|` — `| NFR-001 | Must |` → after optional `\|\s*` and optional `**`, id then `\s*[:|]` matches. Good. But NFR table row is inside a table; the `_TABLE_RE` check comes after def match, so def wins. Good.

But careful: NFR row cells contain text; vague check scans block text — the block ends at next table row? No: on next line, `_DEF_PATTERN` match if it starts with an ID; otherwise `_TABLE_RE` matches → current=None. So each NFR row is its own block. Good.

Also NFR must have "number in definition or ACs" — numbers in table row count. Fine, but I'll also add AC lines.

Now Q/A registers. Q items:
- Q-01: Nghỉ nửa ngày / nghỉ theo giờ có được phép? → blocks FR-001, FR-007.
- Q-02: Quy trình duyệt nhiều cấp? → blocks FR-004, FR-005.
- Q-03: Số dư phép: cấp theo năm dương lịch, có chuyển tiếp? → blocks FR-002, FR-007.
- Q-04: Ai được huỷ đơn đã duyệt (nhân viên hay quản lý/HR)? → blocks FR-003, FR-008.
- Q-05: Thông báo qua kênh nào (email/chat)? → blocks FR-0xx. Need an FR for notifications if Q blocks it; or "tất cả FR". Format says Blocks at least one requirement ID or "all FRs for <area>". Use "tất cả FR về thông báo" — but must be an ID? "at least one requirement ID, or `all FRs for <area>` when the doc has none yet". I'll cite a real FR. Maybe add FR for notification status change as Could? Better: Q-05 blocks FR-012 (status visibility) — meh. I'll keep Q-05 as question about notifications blocking FR-013 if I add a Could FR for notification. Hmm, avoid scope creep. Let me instead make Q-05 about ngày lễ calendar source, blocking BR-003-driven FR-007.

Should BR-003 (working days calc) be cited by an FR: FR-007 covers deduction count → cite BR-003 and BR-004.

A items:
- A-01: Số dư phép tính theo ngày làm việc, không gồm T7/CN và ngày lễ.
- A-02: Một cấp duyệt duy nhất (quản lý trực tiếp).
- A-03: Trừ phép tại thời điểm duyệt, không trừ khi gửi.
- A-04: Nhân viên được huỷ đơn chờ duyệt; đơn đã duyệt chỉ huỷ được qua quản lý (hmm that's Q-04...). Make A-04: Ngày phép làm tròn đến 0,5 ngày.
- A-05: Không có yêu cầu nghỉ phép cho nhiều nhân viên cùng lúc (mỗi đơn một người).
- A-06: Đơn vị thời gian là ngày; nghỉ nửa ngày ngoài phạm vi (but Q-01 asks it...). Conflict: choose either Q or A. Keep Q-01 for half-day, so A-06 not needed.

Edge case matrix table — careful: table cells must not begin with IDs. Fine.

Now Context: problem in requester's words: "Ứng dụng cần thêm tính năng đăng ký nghỉ phép: nhân viên gửi yêu cầu, quản lý duyệt, hệ thống trừ vào số ngày phép còn lại." Why now: not stated → A? "Why now" unknown → record in Q or omit section. Template says delete sections that don't apply. I could state Why now as unknown → but red flags say don't invent. I'll write "Chưa được nêu trong đầu vào" — that's honest, not invented. Better: omit "Vì sao bây giờ" line? Keep it minimal: I'll say input does not state; treat as Q? Q for urgency is a document-shaping question, not allowed ("no document-shaping meta-questions"). So omit.

Source input: yêu cầu trực tiếp của người dùng trong phiên làm việc (không có ticket).

Scope in/out. Out of scope: tính lương, nghỉ ốm/thai sản (Q?), báo cáo HR, tích hợp chấm công.

Let me now count and write. IDs planned:

BR-001 số dư đủ khi gửi
BR-002 quản lý trực tiếp duyệt
BR-003 số ngày trừ = ngày làm việc
BR-004 trừ khi duyệt, hoàn khi huỷ đã duyệt? split: BR-004 trừ chỉ khi Đã duyệt; BR-005 hoàn khi huỷ đã duyệt
BR-006 không trùng khoảng ngày
BR-007 không tự duyệt
BR-008 trạng thái cuối Từ chối/Đã huỷ không đổi
BR-009 ngày kết thúc ≥ ngày bắt đầu, ngày bắt đầu ≥ hôm nay? "ngày bắt đầu không trước ngày gửi" — A basis. Keep BR-009: ngày kết thúc không trước ngày bắt đầu.
BR-010 số dư không âm

FRs 1..13 as above. Map citations:
FR-001 → BR-009
FR-002 → BR-010
FR-003 → BR-008
FR-004 → BR-002
FR-005 → BR-004 (and BR-002)
FR-006 → BR-004
FR-007 → BR-003, BR-004
FR-008 → BR-005
FR-009 → BR-001
FR-010 → BR-006
FR-011 → BR-007
FR-012 → BR-008
FR-013 → BR-005? (maybe employee sees restored balance) — Let's do FR-013: Là nhân viên, tôi muốn nhận thông báo khi yêu cầu được duyệt hoặc từ chối → cite BR-004? Hmm BR cite must be meaningful. Priority Could, basis notification gap. Actually notifications weren't in input; adding as Could is fine if marked A/Q. I'll include FR-013 as Could "xem trạng thái và lý do từ chối" instead — simpler, cite BR-008. But FR-012 already status. Merge: FR-012 covers status + reason.

Drop FR-013; instead add FR-013: Hệ thống phải ghi nhật ký mỗi lần đổi trạng thái (audit) → cite BR-004. Priority Should. Good for auditability NFR.

All 10 BRs cited? BR-001 FR-009 ✓; 002 FR-004,005 ✓; 003 FR-007 ✓; 004 FR-005/006/007/013 ✓; 005 FR-008 ✓; 006 FR-010 ✓; 007 FR-011 ✓; 008 FR-003/012 ✓; 009 FR-001 ✓; 010 FR-002 ✓.

NFR list:
- NFR-001 Must: p95 ≤ 2s cho thao tác gửi/duyệt với 200 người dùng đồng thời. Basis A-06? Use "A-07" assumption on perf target. Let me number A rows: A-01..A-07.
- NFR-002 Must: uptime 99,5%/tháng giờ làm việc.
- NFR-003 Must: quản lý chỉ xem/duyệt đơn của nhân viên thuộc quyền; truy cập chéo bị từ chối 100%.
- NFR-004 Must: lưu nhật ký thay đổi trạng thái 24 tháng.
- NFR-005 Should: giao diện dùng được bàn phím... maybe accessibility: mọi thao tác duyệt hoàn tất bằng bàn phím, tương phản ≥ 4.5:1.
- NFR-006 Should: dữ liệu nghỉ phép giữ 36 tháng sau khi nhân viên rời tổ chức? Hmm keeps privacy. Use NFR-006: không quá ... Let me do retention of personal data 24 months after employment end.

Keep 5 NFRs.

Assumption rows A-01..A-08. NFR bases cite A rows.

Now the file. Must lint clean. Watch vague words: "nhanh" appears in "nhanh chóng" — word boundary: (?<!\w)nhanh(?!\w) — "nhanh chóng" → "nhanh" followed by space → matches! Avoid "nhanh" entirely. Also avoid "dễ", "đơn giản" fine. Avoid "etc." and "v.v.".

Also careful: "phù hợp" banned — I might use "hợp lệ" (fine, not in list).

Time to write. Vietnamese prose, Gherkin keywords English.

Also note: AC IDs FR-001.AC1 etc.

Let me write the document.

One more lint subtlety: `_add_citations` records every ID mention anywhere, including in the "Assumptions" table basis column etc. If I cite FR IDs in Q table Blocks column, that's a citation of a defined ID → fine. And citations of BR only count for orphan check when block_kind in FR/NFR/AC.

Careful: in Glossary table, don't put IDs in first cell.

Also blank lines reset blocks; consecutive BR definitions each followed by blank line — BR definitions will have continuation? I'll put blank lines between BRs, otherwise a BR block text includes following BR line, fine either way but cleaner.

Write file at docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md.

Also: repo empty, no code → delete "Rules recovered from code".

Let me write it.
Repo empty (only `.git`). Job 1 (requirements) in Draft mode — you asked for the full doc and said questions can wait until the end, so every unknown becomes an A-nn/Q-nn. Let me check the templates dir once more, then write.
[Shell] null
[Thought] Interesting: templates dir exists but the read worked. Fine.

Note python 3.9 — the lint script uses `tuple[str, ...]` at module level annotation which works in 3.9? `tuple[str, ...]` as annotation at module level is evaluated... In 3.9, `tuple[str, ...]` is supported (PEP 585 in 3.9). `str | None` in function signature `def _scan_files` — annotations evaluated at def time → `str | None` in 3.9 fails? Actually `from __future__ import annotations` at top makes all annotations strings, so fine. And dataclass field `path: str` fine.

Now write the doc. Plan content.

Context: feature "đăng ký nghỉ phép": employee submits request, manager approves, system deducts remaining leave days. Input: user's message (Vietnamese). Draft mode → unknowns as A/Q.

Actors: Nhân viên (employee), Quản lý trực tiếp (manager), HR/admin (only if assumption). Careful: no invention presented as fact — actors not in input become A-nn basis or listed with basis "A-nn". Template's actor table has Basis column → I can list actors with basis "A-01".

Business rules — need to be testable, based on input only + assumptions marked. Rules:
- BR-001: Đơn nghỉ phép chỉ được duyệt bởi quản lý trực tiếp của người gửi. (input: "quản lý duyệt") — basis input. Source? no code.
- BR-002: Số ngày phép trừ vào quỹ phép chỉ khi đơn được duyệt (input: "hệ thống trừ vào số ngày phép còn lại").
- BR-003: Đơn bị từ chối không làm thay đổi số ngày phép còn lại. (derived; assumption A-02? It's a sensible derivation — must mark as A-nn per red flags. I'll make BR-003 and cite A-02 as basis? The BR format is `- **BR-001**: <rule>.` Lint doesn't check basis for BR. But honesty: mention in assumption table A-02 that rejection doesn't deduct. Better: keep BR-003 stated as rule and add A-02 covering it.)
- BR-004: Không cho gửi đơn vượt quá số ngày phép còn lại — assumption A-03.
- BR-005: Số ngày phép trừ = số ngày làm việc trong khoảng nghỉ, trừ cuối tuần/ngày lễ — assumption A-04 (big one).
- BR-006: Đơn chờ duyệt giữ (giữ chỗ) số ngày — assumption A-05.
- BR-007: Nhân viên có thể hủy đơn khi còn chờ duyệt; hủy → hoàn lại ngày — assumption A-06.
- BR-008: Không duyệt đơn của chính mình — assumption? Input didn't say. A-07.
- BR-009: đơn nghỉ phải gửi trước ngày bắt đầu ít nhất N ngày? assumption A-08 or open question Q.

Careful not to over-invent as fact. All rules beyond direct input must trace to A-nn. I'll write BR with "Cơ sở: A-03" — but canonical form is `- **BR-001**: <rule>.` Additional text fine as long as one line. I can add "(Cơ sở: A-03)" at end. Lint won't complain. Orphan-br check: each BR must be cited by FR/NFR/AC — need `Fulfils [BR-00x]` in FR.

FRs: 
1. FR-001: employee submit leave request (create draft/submit), Fulfils BR-... 
2. FR-001.AC1..n
3. FR-002: system validate insufficient balance / overlap
4. FR-003: manager view pending requests for their team
5. FR-004: manager approve
6. FR-005: manager reject with reason
7. FR-006: system deduct balance on approval (or reserve on submit)
8. FR-007: employee view remaining balance and request status
9. FR-008: employee cancel pending request → restore
10. FR-009: system notify manager / employee (Should)
11. FR-010: audit log of status changes (Should)
12. FR-011: HR adjusts/allocates annual leave quota (Could?) — not in input; hmm, quota source is a gap. Could be Q-02 "quỹ phép khởi tạo thế nào". Better Q than FR. But some FR for balance display needs a source. I'll put Q-01 about quota source and add A-09 working value.

Also: partial-day leave (nghỉ nửa ngày) — A or Q. Q about đơn vị tính (ngày/nửa ngày/giờ).

NFRs: must have numbers.
- NFR-001: performance: submit/approve p95 ≤ 2s at 200 concurrent users — basis A-11 (working value).
- NFR-002: balance consistency: không âm; sai lệch 0 khi 2 request đồng thời — measurable: "khi 2 yêu cầu duyệt đồng thời, tổng ngày trừ không vượt quá số ngày phép" → target number 0 discrepancy.
- NFR-003: audit retention ≥ 24 months? number.
- NFR-004: availability 99.5% giờ hành chính.
- NFR-005: security/authorization: 100% endpoint kiểm tra quyền, không lộ dữ liệu phép của người khác.
- NFR-006: usability: gửi đơn ≤ 5 bước / ≤ 3 phút.

Each NFR needs AC with number.

Edge cases matrix: roles × states (nháp, chờ duyệt, đã duyệt, bị từ chối, đã hủy) × CRUD.

Glossary: Đơn nghỉ phép, Quỹ phép năm, Ngày phép còn lại, Ngày làm việc, Quản lý trực tiếp, Chờ duyệt, etc.

Assumptions ~ A-01..A-12, Open questions Q-01..Q-08 with owners and blocks.

Open questions (at end, and one asked in chat at end):
- Q-01: Quỹ phép năm khởi tạo và cộng dồn thế nào (theo hợp đồng, theo thâm niên)? ai quản lý? Owner HR.
- Q-02: Đơn vị nghỉ: ngày / nửa ngày / giờ?
- Q-03: Nghỉ nửa ngày, nghỉ ngoài lịch làm việc
- Q-04: Đơn vị trừ có tính ngày lễ, cuối tuần không; lịch ngày lễ lấy từ đâu?
- Q-05: Nghỉ phép có cần gửi trước bao nhiêu ngày? nghỉ đột xuất/ốm xử lý sao?
- Q-06: Phép dư có chuyển sang năm sau không, hết hạn khi nào?
- Q-07: Ai duyệt khi quản lý trực tiếp vắng / nhân viên là quản lý cấp cao / nhiều cấp duyệt?
- Q-08: Trừ phép lúc gửi (giữ chỗ) hay lúc duyệt?
- Q-09: Nếu đơn đã duyệt rồi mới hủy/thay đổi thì hoàn phép thế nào?
- Q-10: Ngày phép âm cho phép không?
- Q-11: Thông báo qua kênh nào (email/chat/in-app)? có SLA?
- Q-12: Số liệu thành công: giảm thời gian duyệt từ bao nhiêu xuống? Owner?

Should I cite "Source input" and code recovery? No code exists — note "Repo chưa có mã nguồn nào (chỉ .git) → không có BR phục hồi từ code." That's honest.

Language: Vietnamese headings/prose; IDs + Gherkin keywords English; translated frames: "Là ..., tôi muốn ..., để ..." "Đáp ứng [BR-001]. Ưu tiên: Must." Gherkin: `Given ..., When ..., Then ...` with Vietnamese prose. Lint vague list includes "nhanh", "dễ dàng", "thân thiện", "linh hoạt", "v.v.", "phù hợp", "hợp lý" — avoid these. Careful: "phù hợp" appears easily. Also English "fast","quickly","simple","flexible","etc.".

Watch out: "v.v." avoided; use "và các trường khác" — hmm.

Also lint: each FR needs AC; every BR must be cited by some FR/NFR/AC. Every AC's base must be defined. Avoid duplicate IDs. Don't put ID in first cell of traceability table (avoid traceability tables entirely).

Also careful about the definition pattern: lines starting with `- **FR-001**:`. Within assumption tables rows start with `| A-01 |` — the def pattern requires (BR|FR|NFR)- so A-01/Q-01 rows are not definitions. Good.

NFR table row: `| NFR-001 | Must | ... | A-11 |` matches def pattern (`^\s*\|\s*` then NFR...). Good — the lint requires ID followed by `|`. Yes `| NFR-001 |` → after id, space then `|` matches `\s*[:|]`. Good.

NFR AC lines separate: `- **NFR-001.AC1**: Given ..., When ..., Then ... ≤ 2 s.` Good.

Now "Số ngày phép còn lại" deduction must be aligned with BR about reserving.

Let me define states: Nháp (draft), Chờ duyệt (pending), Đã duyệt (approved), Từ chối (rejected), Đã hủy (cancelled). Decide reservation: A-05: ngày phép được giữ (reserve) ngay khi gửi đơn; giải phóng khi từ chối/hủy. That's a decision I make → A-nn, and Q-08 asks to confirm... careful: duplicate — an unknown can be either A or Q, exactly one table. Better: A-05 = working value (reserve on submit), and no Q for it. But Q-08 listed above asked the same → remove Q-08, keep A-05. Good: every unknown exactly one table.

Similarly BR-005 (working days) → A-04 only, drop Q-04? Weekend/holiday calendar is business-critical and only business can answer (which calendar, holidays list). Hmm — the rule that only working days count is a working value I set → A-04; but "lịch ngày lễ" specifics differ per company. I'll keep Q-04 for holiday calendar source/owner, and make A-04 the assumption "trừ theo ngày làm việc, không tính T7/CN và ngày lễ". Those overlap. To keep clean: A-04 states the calculation basis; Q-04 asks who maintains holiday calendar and whether it's needed at all (blocks FR-006). Slight overlap but distinct: rule vs data source. Acceptable? Red flag says every unknown exactly one table. Overlapping partially risks. Let me structure:

A-04: Số ngày trừ = số ngày làm việc (không tính thứ Bảy, Chủ Nhật và ngày lễ trong lịch công ty) trong khoảng nghỉ.
Q-01: Ngày lễ và ngày làm việc đặc biệt lấy từ nguồn nào và ai cập nhật? Owner HR. Blocks FR-006, FR-001.

Different: assumption = rule, question = data source. Fine.

Let me choose numbering for A-nn by appearance order and Q-nn by appearance order.

Assumptions list:
A-01: Vai trò tham gia: Nhân viên (gửi đơn), Quản lý trực tiếp (duyệt/từ chối), HR (quản lý quỹ phép, xem báo cáo). Basis: input names only employee+manager; HR role inferred.
A-02: Từ chối đơn không thay đổi số ngày phép còn lại. impact: nếu sai, cần bước hoàn phép khi từ chối.
A-03: Hệ thống không cho gửi đơn vượt số ngày phép còn lại (không cho âm). input says "trừ vào số ngày phép còn lại" → nếu cho âm thì cần rule riêng.
A-04: ngày trừ tính theo ngày làm việc.
A-05: Giữ ngày phép ngay khi gửi đơn; giải phóng khi từ chối/hủy.
A-06: Nhân viên hủy được đơn khi Chờ duyệt; đơn Đã duyệt chỉ hủy được nếu quản lý/HR huỷ (hmm invent). Maybe A-06: Nhân viên hủy đơn ở trạng thái Nháp/Chờ duyệt; đơn Đã duyệt không tự hủy được. Impact if false: thêm luồng hủy sau duyệt + hoàn phép.
A-07: Một cấp duyệt duy nhất (quản lý trực tiếp), không duyệt nhiều cấp.
A-08: Không ai duyệt đơn của chính mình; nếu người gửi không có quản lý trực tiếp trong hệ thống thì đơn không gửi được. Hmm inventing. Better: A-08 "Người duyệt là quản lý trực tiếp được gán trong hồ sơ nhân viên (mỗi nhân viên có 0 hoặc 1 quản lý trực tiếp)".
A-09: Quỹ phép năm khởi tạo thủ công bởi HR theo hợp đồng, đơn vị ngày. impact...
A-10: Đơn vị nghỉ nhỏ nhất là 1 ngày (chưa hỗ trợ nửa ngày/giờ). Hmm this is what Q should ask... The doc must be coherent; I'll make A-10 = 1 ngày là đơn vị nhỏ nhất and Q ask about nửa ngày? Conflict again. Choose: A-10: Đơn nghỉ tính theo ngày, đơn vị nhỏ nhất 1 ngày; impact: nếu cần nửa ngày/giờ thì thêm trường buổi và công thức trừ theo giờ. And Q: "Có cần nghỉ nửa ngày/giờ trong phạm vi phát hành này không?" — that duplicates. Skip Q; keep A-10 only. Owner could override later. Hmm but the skill wants genuinely business-only questions in Q. Half-day is a scope question only business can answer, but I can still assume and flag impact. Both acceptable; cleaner to have fewer duplicates. I'll make it A-10.

Hmm, but the highest-impact interview question for the final chat should be the one changing most requirements. Candidates: deduction timing (reserve on submit vs approve) — I already assumed A-05; quota source (Q); holiday calendar; half-day. Which changes most requirements? Probably "đơn vị tính & cách tính ngày trừ" and "trừ lúc gửi hay lúc duyệt". Since Q table asks others, the single question at end per interview format... but we're in Draft mode — user said if I need to ask, ask at end then stop. So I should ask ONE question at the end. Skill interview = one question. The user explicitly allowed asking questions at the end. I'll ask the single highest-impact one: "Số ngày phép bị trừ (giữ) tại thời điểm gửi đơn hay tại thời điểm quản lý duyệt?" Hmm — is that the highest impact? Alternatives: quota source; multi-level approval. I think deduction timing + which days count are similar impact. Timing affects concurrency rules, cancellation, ACs heavily. Also "ai duyệt khi không có quản lý trực tiếp" affects flow.

Actually maybe highest impact: "Ngày phép trừ vào lúc gửi đơn hay lúc duyệt?" — yes, drives BR-002/BR-006, FR-006/FR-008, edge matrix. I'll ask that.

But wait — user said "Hãy viết yêu cầu đầy đủ trước khi code. Nếu cần hỏi tôi điều gì, hãy hỏi ở cuối câu trả lời rồi dừng lại." So write full doc, then ask one question at end and stop. Good.

Remaining assumptions:
A-11: p95 ≤ 2s at 200 concurrent users working value (NFR basis).
A-12: Lưu trữ nhật ký 24 tháng.
A-13: Uptime 99.5% giờ hành chính.
A-14: Email/thông báo in-app? Maybe FR for notification Should, with channel A-14 = in-app + email.
A-15: Ngày phép dư không chuyển năm (reset 1/1)? That's a business policy — better Q: "Phép dư năm trước có chuyển sang năm sau không, hạn dùng?" Owner HR, blocks FR-... Actually reset policy affects FR about balance computation. Keep as Q-0x with owner HR.

I'll finalize numbering as I write. Let me write the doc carefully, avoiding vague terms. Also avoid word "phù hợp". Avoid "nhanh". 

File path: docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md. Today's date 2026-11-18.

Let me now draft full markdown.

Sections: Context, Actors and stakeholders, Scope, Business rules, Functional requirements, NFRs, Edge cases, Decision table, Rules recovered from code (skip? code recovery: no code → delete section instead of N/A. I'll delete and mention in Context line "Repo chưa có mã nguồn"). Glossary, Assumptions, Open questions, Next step.

Decision table for approval action outcomes? Use for deduction: conditions (đơn hợp lệ?, còn đủ phép?, trạng thái) → actions. Let's build:

| Điều kiện / hành động | R1 | R2 | R3 | R4 |
| Đơn đang ở trạng thái Chờ duyệt | Y | Y | Y | N |
| Số ngày phép còn lại ≥ số ngày đơn | Y | Y | N | – |
| Quản lý quyết định | Duyệt | Từ chối | Duyệt | Duyệt |
| Kết quả | Trừ phép, đơn Đã duyệt | Không trừ, đơn Từ chối | Chặn duyệt, báo lỗi, đơn giữ Chờ duyệt | Chặn, báo đơn không còn chờ duyệt |

Give BR ID and cite from FRs. BR-006 maybe.

Business rules final list:
- BR-001: Chỉ quản lý trực tiếp của người gửi được duyệt hoặc từ chối đơn nghỉ phép của nhân viên đó. (input "quản lý duyệt" + A-07)
- BR-002: Chỉ đơn ở trạng thái Chờ duyệt mới nhận được quyết định duyệt hoặc từ chối; đơn Đã duyệt, Đã từ chối, Đã hủy không nhận quyết định lần hai.
- BR-003: Số ngày phép còn lại của nhân viên giảm đúng bằng số ngày của đơn tại thời điểm đơn chuyển sang Đã duyệt... wait, if we reserve on submit (A-05), the deduction happens at submit. Let me settle A-05: reserve at submit → "Số ngày phép khả dụng giảm ngay khi đơn được gửi; khi đơn bị từ chối hoặc hủy, số ngày được hoàn lại". Hmm but the user's stated flow: "quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại" — reads like deduction follows approval. Safer assumption aligned to input: deduct on approval, no reservation on submit; the check at submit is against remaining balance (A-03), and the balance is re-checked at approval (to handle two pending requests). That makes BR-004: Khi duyệt, hệ thống kiểm tra lại số ngày còn lại; nếu không đủ, chặn duyệt (decision table R3). This is closer to input and creates a real edge case (double booking) flagged as Q or A. Overbooking risk is a real gap → I'll make Q about "đơn chờ duyệt có giữ chỗ ngày phép không?" Owner product owner, blocks FR-004/FR-005. Then no A-05 duplicate. Good — and that Q is high impact.

So:
- BR-001: chỉ quản lý trực tiếp duyệt/từ chối (A-07 for single-level).
- BR-002: chỉ đơn Chờ duyệt nhận quyết định; quyết định lần hai bị chặn.
- BR-003: số ngày còn lại giảm đúng bằng số ngày làm việc của đơn ngay khi đơn được duyệt (input).
- BR-004: đơn bị từ chối hoặc bị hủy không làm giảm số ngày còn lại (A-02).
- BR-005: không duyệt được đơn nếu số ngày còn lại nhỏ hơn số ngày đơn tại thời điểm duyệt (A-03 + decision table).
- BR-006: số ngày trừ = số ngày làm việc trong khoảng nghỉ, không tính T7, CN và ngày lễ (A-04).
- BR-007: nhân viên chỉ hủy được đơn ở trạng thái Nháp hoặc Chờ duyệt (A-06).
- BR-008: mỗi nhân viên có tối đa một quản lý trực tiếp; người không có quản lý trực tiếp không gửi được đơn (A-08).
- BR-009: không cho gửi đơn trùng khoảng ngày với một đơn khác đang Nháp/Chờ duyệt/Đã duyệt của cùng nhân viên. (A-09 — invented, mark)
- BR-010: đơn phải có ngày bắt đầu ≤ ngày kết thúc và tổng ngày ≥ 1 (basic validity, A-10).

Each must be cited by FR/NFR/AC. I'll ensure every BR appears in some FR's `Đáp ứng [..]` list or AC text.

FRs:
1. FR-001 nhân viên tạo và gửi đơn (Must) — Đáp ứng BR-010, BR-009, BR-008.
 AC1 happy: gửi đơn 3 ngày, đơn Chờ duyệt, hiện trong danh sách chờ duyệt của quản lý.
 AC2 ngày kết thúc trước ngày bắt đầu → chặn, thông báo lỗi, đơn không được tạo.
 AC3 trùng khoảng ngày với đơn đang Chờ duyệt → chặn.
 AC4 nhân viên không có quản lý trực tiếp → chặn gửi, thông báo.
 AC5 vượt số ngày còn lại → chặn (BR-005? at submit check). Hmm BR-005 is at approval. Add BR-011: khi gửi, hệ thống chặn đơn có số ngày lớn hơn số ngày phép còn lại hiện tại. Good, cite in FR-001.AC5.
2. FR-002 nhân viên xem số ngày phép còn lại + trạng thái đơn (Must) — BR-003, BR-004.
 AC1: còn 12 ngày, xem → 12.
 AC2: đơn đã duyệt 3 ngày → còn 9.
 AC3: nhân viên không xem được số ngày phép của người khác (NFR security maybe; here 403/không hiển thị).
3. FR-003 quản lý xem danh sách đơn Chờ duyệt của nhân viên mình (Must) — BR-001.
 AC1: quản lý A thấy đơn của nhân viên trực tiếp.
 AC2: không thấy đơn của nhân viên thuộc quản lý khác.
4. FR-004 quản lý duyệt đơn (Must) — BR-002, BR-003, BR-005.
 AC1: duyệt → Đã duyệt, trừ phép, nhân viên thấy.
 AC2: duyệt đơn đã Đã duyệt → chặn, không trừ lần hai.
 AC3: duyệt khi số ngày còn lại < số ngày đơn → chặn, đơn giữ Chờ duyệt, báo lỗi.
 AC4: người không phải quản lý trực tiếp duyệt → chặn.
5. FR-005 quản lý từ chối kèm lý do (Must) — BR-002, BR-004.
 AC1: từ chối → Đã từ chối, lý do hiển thị cho nhân viên, phép không đổi.
 AC2: bỏ trống lý do → chặn (A: lý do bắt buộc? invented → A-12). Hmm. Make it A-12: lý do từ chối bắt buộc. Or Should FR for optional. Keep A-12 assumption that lý do bắt buộc.
6. FR-006 nhân viên hủy đơn (Should) — BR-007, BR-004.
 AC1: hủy đơn Chờ duyệt → Đã hủy, phép không đổi.
 AC2: hủy đơn Đã duyệt → chặn.
7. FR-007 hệ thống thông báo khi trạng thái đổi (Should) — A-13 channel.
 AC1: gửi đơn → quản lý nhận thông báo trong 60 s. Hmm that's an NFR-ish number; put 5 phút.
 AC2: quyết định → nhân viên nhận thông báo.
8. FR-008 hệ thống ghi nhật ký trạng thái (Should) — BR-002? cite.
 AC1: mỗi lần đổi trạng thái ghi ai, khi nào, trạng thái trước/sau; HR đọc được.
9. FR-009 HR xem báo cáo số ngày phép theo nhân viên/kỳ (Could) — cites BR-003.
 AC1: HR chọn kỳ 1 tháng → tổng ngày đã duyệt khớp tổng trừ.
10. FR-010 hệ thống khởi tạo quỹ phép năm (Must?) — Q-01 about source. FR-010: HR gán quỹ phép năm cho nhân viên (Must). avec ACs.

That's 10 FRs. Enough.

NFRs:
- NFR-001 | Must | p95 ≤ 2 s cho thao tác gửi/duyệt đơn ở 200 người dùng đồng thời | A-14
- NFR-002 | Must | 0 chênh lệch: tổng ngày đã trừ khớp tổng ngày đơn Đã duyệt sau 1.000 lần duyệt đồng thời (không trừ hai lần khi 2 quản lý bấm cùng lúc) | A-15
- NFR-003 | Must | 100% yêu cầu không có quyền bị từ chối; nhân viên chỉ đọc được dữ liệu phép của chính mình | A-16
- NFR-004 | Should | uptime ≥ 99,5% trong giờ hành chính mỗi tháng | A-17
- NFR-005 | Should | nhật ký giữ ≥ 24 tháng | A-18
- NFR-006 | Should | nhân viên hoàn tất gửi đơn trong ≤ 4 bước và ≤ 2 phút | A-19

Each NFR AC with numbers.

Edge cases matrix: roles (Nhân viên, Quản lý trực tiếp, Quản lý khác, HR) × states (Nháp, Chờ duyệt, Đã duyệt, Từ chối, Đã hủy) × CRUD. That's a big table; use roles × states rows and create/read/update/delete columns.

Rows: Nhân viên × Nháp; Nhân viên × Chờ duyệt; Nhân viên × Đã duyệt; Nhân viên × Từ chối; Nhân viên × Đã hủy; Quản lý trực tiếp × Chờ duyệt; Quản lý trực tiếp × Đã duyệt; Quản lý khác × Chờ duyệt; HR × Đã duyệt; HR × all.

Trailing content: Assumptions table A-01..A-19, Open questions Q-01..Q-10.

Let me assign A-ids in order of appearance in doc — "in order of appearance" likely means in the assumption table order; simpler: number sequentially in table and make sure first references roughly ascending. Fine.

Now define A entries (final):
A-01 Vai trò: Nhân viên gửi đơn, Quản lý trực tiếp duyệt, HR quản lý quỹ phép và báo cáo. Basis: input chỉ nêu nhân viên và quản lý; HR là vai trò bổ sung; nếu không có HR, FR-009/FR-010 chuyển cho quản lý.
A-02 Đơn bị từ chối không làm giảm số ngày phép. Basis: input chỉ nói trừ khi duyệt; nếu sai cần bước hoàn phép khi từ chối.
A-03 Hệ thống chặn mọi trường hợp làm số ngày phép còn lại âm. Basis: "trừ vào số ngày phép còn lại"; nếu cho phép âm, BR-005 và FR-004.AC3 đổi thành cảnh báo.
A-04 Số ngày trừ tính theo ngày làm việc, không tính thứ Bảy, Chủ Nhật và ngày lễ. Basis: input không nêu; nếu tính theo ngày lịch, mọi AC về số ngày phải tính lại.
A-05 Một cấp duyệt duy nhất. Basis: "quản lý duyệt"; nếu nhiều cấp, FR-004 tách thành nhiều bước và BR-002 đổi.
A-06 Nhân viên hủy được đơn ở Nháp và Chờ duyệt, không hủy được đơn Đã duyệt. Basis: input không nêu; nếu cho hủy sau duyệt thì cần luồng hoàn phép và AC mới.
A-07 Mỗi nhân viên có tối đa một quản lý trực tiếp trong hồ sơ. Neucs 0 → không gửi được đơn.
A-08 Không cho gửi đơn trùng khoảng ngày với đơn đang Nháp/Chờ duyệt/Đã duyệt. Nếu sai, cần rule ưu tiên khi hai đơn cùng ngày.
A-09 Đơn vị nghỉ nhỏ nhất là 1 ngày. Nếu cần nửa ngày/giờ, thêm trường buổi và công thức trừ theo giờ.
A-10 Lý do từ chối bắt buộc. Nếu không bắt buộc, FR-005.AC2 bỏ.
A-11 Quỹ phép năm do HR gán thủ công theo hợp đồng, đơn vị ngày. Nếu lấy từ hệ thống nhân sự, FR-010 thành tích hợp.
A-12 Kênh thông báo: email + thông báo trong ứng dụng. Nếu chỉ một kênh, FR-007 giảm một AC.
A-13 Quỹ phép làm mới mỗi năm dương lịch, phép dư không chuyển sang năm sau. Hmm — that's business policy; better as Q for HR. But if Q, then impact goes there. Keep as Q-? Actually pick: Q (HR decides). Then AC for balance display shouldn't rely on it. OK as Q.
A-14 p95 ≤ 2 s @200 users (NFR-001 basis).
A-15 0 chênh lệch khi duyệt đồng thời (NFR-002).
A-16 kiểm tra quyền 100% (NFR-003).
A-17 uptime 99,5% (NFR-004).
A-18 nhật ký 24 tháng (NFR-005).
A-19 ≤4 bước, ≤2 phút (NFR-006).

Hmm A-16/A-17 etc. as "assumption: target numbers chosen as working values". Basis: "Giá trị làm việc do BA đặt; nếu chưa đạt, Q với chủ sản phẩm." Fine.

Open questions:
Q-01 Trừ ngày phép tại thời điểm gửi (giữ chỗ) hay tại thời điểm duyệt? Nếu giữ chỗ khi gửi, đơn Chờ duyệt chiếm quỹ phép. Owner: chủ sản phẩm. Blocks FR-004, FR-005, FR-006, FR-001.
Q-02 Quỹ phép năm của mỗi nhân viên được xác định thế nào (số ngày theo hợp đồng/thâm niên) và ai cập nhật? Owner HR. Blocks FR-010, FR-002.
Q-03 Phép dư năm trước có chuyển sang năm sau không, hạn dùng đến ngày nào? Owner HR. Blocks FR-002, FR-010.
Q-04 Lịch ngày lễ và ngày làm việc đặc biệt lấy từ nguồn nào, ai cập nhật? Owner HR. Blocks FR-001, FR-004.
Q-05 Đơn nghỉ phép có cần gửi trước ngày bắt đầu tối thiểu bao nhiêu ngày làm việc? Owner quản lý nhân sự. Blocks FR-001.
Q-06 Nghỉ ốm/đột xuất có dùng cùng luồng và trừ cùng quỹ phép không? Owner HR. Blocks FR-001, FR-002.
Q-07 Khi quản lý trực tiếp vắng hoặc nghỉ việc thì ai duyệt? Owner HR. Blocks FR-004.
Q-08 Đơn đã duyệt muốn hủy/thay đổi thì ai được phép và hoàn phép thế nào? Owner HR + quản lý. Blocks FR-006, FR-002.
Q-09 Quản lý có được tự duyệt đơn của chính mình không? Owner HR. Blocks FR-004.
Q-10 Thông báo gửi qua kênh nào và có yêu cầu thời gian tới người nhận không? — overlaps A-12. Drop Q-10. 
Q-10 Số liệu nào dùng để đánh giá thành công (ví dụ thời gian duyệt trung bình) và ai sở hữu? Owner trưởng phòng nhân sự. Blocks — needs a requirement ID; "all FRs for báo cáo"? The rule: Blocks at least one requirement ID or "all FRs for <area>". Hmm this asks success metric which maps to FR-009. Use FR-009. Fine.

Note lint doesn't check Q tables.

Also lint: BR mentions inside Q rows "FR-004" are citations → those IDs are defined, fine. Careful: any mention of an undefined ID like "FR-011" in prose → dangling-ref. Watch out.

Also careful: "Given/When/Then" lines — no issue.

Now count BRs and make sure each is cited in some FR/AC (block_kind FR/NFR/AC). Citations from BR lines themselves don't count as citing other BRs (only block_kind in FR/NFR/AC). So each BR must appear inside an FR line or AC line or FR continuation lines (continuation lines of an FR block count with block_kind=FR). Good — ACs citation block_kind = AC.

BR list final (10-ish):
BR-001 chỉ quản lý trực tiếp duyệt/từ chối → cited FR-003, FR-004, FR-005.
BR-002 chỉ đơn Chờ duyệt nhận quyết định; chặn quyết định lần hai → FR-004, FR-004.AC2, FR-005.
BR-003 duyệt → giảm đúng số ngày làm việc của đơn (input) → FR-004, FR-002.
BR-004 từ chối/hủy không giảm → FR-005, FR-006.
BR-005 chặn duyệt khi còn lại < số ngày đơn → FR-004.AC3.
BR-006 số ngày = ngày làm việc, bỏ T7/CN/lễ → FR-001.AC1? cite in FR-004/FR-002 AC.
BR-007 nhân viên hủy được đơn Nháp/Chờ duyệt → FR-006.
BR-008 mỗi nhân viên tối đa 1 quản lý trực tiếp; 0 → không gửi được → FR-001.AC4.
BR-009 chặn đơn trùng khoảng ngày → FR-001.AC3.
BR-010 đơn phải có ngày bắt đầu ≤ ngày kết thúc và ≥1 ngày làm việc → FR-001.AC2.
BR-011 chặn gửi khi số ngày đơn > số ngày còn lại → FR-001.AC5.
BR-012 lý do từ chối bắt buộc → FR-005.AC2. (A-10)
BR-013 quỹ phép năm do HR gán, đơn vị ngày → FR-010.
BR-014 mọi thay đổi trạng thái ghi nhật ký không sửa được → FR-008.

All cited. Good.

Now write. Careful with vague terms: avoid "nhanh", "dễ dàng", "phù hợp", "hợp lý", "linh hoạt", "v.v.", "thân thiện". Check "phù hợp" — avoid. Also "etc."

Watch: "trong 2 phút" fine.

Also careful with the lint's block continuation: a BR line followed by blank then next content — blank ends block, fine.

For FR lines ending "Ưu tiên: Must." — good.

Let me write file now. Long doc. Then run lint.

One more: "Rules recovered from code" section — repo has no code, so delete section. Mention in Context "Repo hiện chỉ có .git, không có mã nguồn để phục hồi quy tắc hiện hành."

Also template's Next step: brainstorming.

Writing doc in Vietnamese.

Detail on decision table placement — put after business rules, before FRs? Template doesn't have it; requirements reference allows. I'll add as subsection in Business rules.

Now the edge case table—keep 9 rows.

Let me write.
Repo holds only `.git` — no source to recover rules from, so job 1 is pure Draft-mode requirements. Writing the doc.
[Edit] null
Now lint it.
[Shell] null
[Thought] Clean. Check line count and count IDs. Also the interview mode: user is present, has not opted out — but they said "Hãy viết yêu cầu đầy đủ trước khi code. Nếu cần hỏi tôi điều gì, hãy hỏi ở cuối câu trả lời rồi dừng lại." That means write full doc, questions at end. That's essentially draft-with-questions. Good — I wrote doc with Q table. The skill says interview mode asks one question per message. But user explicitly asked to write full doc first and ask at end. So my approach: complete doc + Q register, then one highest-impact question at end. Skill interview message format: understanding 2-5 lines, single gap, exactly one question last line. I should honor that: report format + one question. But also user asked "Nếu cần hỏi tôi điều gì" — so asking at end is allowed.

Let me count IDs quickly.
[Shell] null
Doc written and lint-clean.

**File:** `docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md`

**Counts:** 14 BR · 10 FR · 6 NFR · 35 AC · 19 assumptions · 11 open questions · lint 0 findings

**Top 3 risks:**
1. **Q-01 — WHEN to deduct leave.** Input says "trừ vào số ngày phép còn lại" but not if deduction happens at submit or at approve. This changes FR-001, FR-004, FR-005, FR-006 and the whole balance model. Biggest fork in the doc.
2. **Q-02/Q-03 — leave quota source + carry-over.** Nothing in input says where the yearly quota comes from or whether unused days roll over. FR-002 and FR-010 are blocked until HR answers.
3. **Q-04 — holiday/workday calendar source.** BR-006 counts working days only, so every day-count AC depends on a calendar nobody has specified.

**Mode note:** ran Draft mode since you asked for full doc now and deferred questions. Every unknown is an A-nn (filled value) or Q-nn (needs someone else), never stated as fact. Repo has no source code — only `.git` — so no rules recovered from code.

**Next step:** brainstorm solution with this file as context, then implementation plan.

---

Câu hỏi (một câu, quan trọng nhất — trả lời xong tôi sẽ hỏi tiếp câu kế):

**Ngày phép bị trừ lúc nhân viên gửi đơn, hay chỉ trừ khi quản lý duyệt?**
[User] Nghỉ phép được tính theo ngày làm việc, tối đa 12 ngày một năm. Quản lý trực
tiếp duyệt, nhân sự chỉ cần xem báo cáo. Viết nốt phần còn lại đi, đừng hỏi
thêm.
[Thought] User answered: leave counted in working days, max 12 days per year. Direct manager approves. HR only needs to view reports. And: write the rest, don't ask more questions.

So the key answer changed:
- A-04 confirmed: working days (now confirmed fact, not assumption)
- 12 days/year max quota — a business rule on the quota cap (not per-employee assigned by HR; it's 12 max). Q-02 partially answered: quota = 12 days/year.
- HR only views reports — so HR does NOT assign quota (FR-010 changes!), does not answer; HR is read-only. A-01 needs revision: HR is viewer only.
- No more questions — so Q-01 remains unanswered... hmm. The user didn't answer Q-01 (deduction timing). But "đừng hỏi thêm" = don't ask more. So Q-01 stays as Q-nn. But wait — the deduction timing was my top question and they didn't answer it. Per the skill: stop asking, remaining gaps become A-nn or Q-nn. Keep Q-01 as open question with owner. But maybe I should reconsider: they said "Viết nốt phần còn lại đi, đừng hỏi thêm" — meaning finish writing, no more questions. So unresolved gaps stay Q-nn.

Also since HR only views reports, FR-010 (HR assigns annual quota) must be removed/reframed. Quota is fixed at 12 days/year max. Who sets it? It's a system rule: 12 days per year. But does each employee get 12 or does max mean cap? "tối đa 12 ngày một năm" — maximum 12 days per year. So quota cap = 12. Hmm, could mean each employee is entitled to 12 days per year max, and cannot go negative. I'll encode as BR: annual quota is 12 working days per employee per calendar year; the system blocks approval that exceeds remaining.

Careful: I made 12 an assumption before? No — A-04 was working days assumption, and quota A-11 was HR-assigned. Now both resolved. Must remove A-04, A-11, and revise A-01 (HR role), and update all AC numbers that used 12 (still fine), and FR-010 becomes... nothing? FR-010 now needs replacement. Options: delete FR-010 or repurpose. The skill says delete sections that don't apply, and don't add features beyond input. HR viewing reports = FR-009 stays (that's the HR report FR). So delete FR-010. But then who assigns leave? Fixed at 12. No admin function needed. Simpler.

Also "nhân sự chỉ cần xem báo cáo" — supports FR-009 (report), FR-008 (audit log read by HR) still ok.

Also update Q-02 (quota source) — now answered: 12 days/year. But does 12 apply to every employee regardless? It says max 12 days a year. So Q-02 answer: fixed 12. Remove Q-02? The original question "on what basis is quota determined and who updates it" — now answered: 12 days/year by rule, nobody updates. I should remove Q-02 and encode as BR. But there's residual ambiguity: is 12 an entitlement for all employees including new hires (prorated?) and part-time? Hmm. I shouldn't invent. Keep a narrowed question? User said don't ask more questions — that refers to not asking them in the interview, but Q-nn rows in the doc are fine (they're written, not asked). The skill says draft mode: every unknown becomes A-nn or Q-nn. So I can keep a narrowed Q about prorating for new hires. That's legitimate and not "asking a question to the user" in the conversation. But I must not ask in the reply. Actually the final report format includes "top 3 risks or open questions" — that's reporting, not asking. Fine.

Answer to Q-01 still unknown → remains Q-01. But deduct timing... Hmm, with max 12 days/year and no HR allocation, the natural reading is still ambiguous. Keep Q-01.

Also Q-03 (carry-over) — still open, HR doesn't manage quota though. With "tối đa 12 ngày một năm" and no carry-over mention, carry-over is likely no. But don't invent → keep Q-03 as open question, but owner changes? HR no longer owns quota. Hmm, HR only views reports; owner for carry-over policy would be Trưởng phòng nhân sự (policy owner, not system role). That's fine — owner is a person/role who can answer, not necessarily system role.

Q-04 holiday calendar source — still open (who maintains). Owner HR... but HR only views reports. Calendar maintenance is still a business fact. Keep owner as "Trưởng phòng nhân sự".

Q-05 notice period, Q-06 sick leave, Q-07 manager absent, Q-08 cancel approved, Q-09 self-approve, Q-10 metric owner, Q-11 perf. Q-11 was about NFR-001 target — user gave no numbers, so A-14 stays and Q-11 stays? If A-14 exists then Q-11 duplicating. Hmm, previously I had both A-14 (filled value) and Q-11 (ask for target). Skill says every unknown in exactly one table. That's a contradiction in my own doc — A-14 is the filled working value, Q-11 asks the business to confirm. Strictly, if I filled a working value it's A-nn; asking the same as Q-nn is double-listing. Let me clean that: remove Q-11, keep A-14 with basis "input gave no number; A-14 is working value, confirm with owner". Hmm but earlier report listed Q-11. Since rewrite, better to remove Q-11 to satisfy "every unknown in exactly one table".

Similarly A-17/A-18/A-19 vs no Qs — fine.

Also A-15/A-16 fine.

Now, FR-010 removal: but then "quỹ phép" glossary term still valid (12 days/year entitlement). Rewrite glossary: Quỹ phép năm = 12 ngày làm việc mỗi nhân viên được hưởng trong một năm dương lịch, theo mức tối đa 12 ngày/năm.

FR-002 AC1 "nhân viên được gán 12 ngày phép" → "đầu năm dương lịch, nhân viên có 12 ngày phép". Better: "Given nhân viên chưa dùng ngày phép nào trong năm, When mở trang nghỉ phép, Then hiển thị 12 ngày phép còn lại."

BR-013 becomes: Quỹ phép năm của mỗi nhân viên là 12 ngày làm việc cho mỗi năm dương lịch; không ai gán riêng. Definite. And BR-016? Let's renumber carefully to avoid duplicating.

New BR set:
- BR-001 manager-only approve (unchanged)
- BR-002 state transition guard
- BR-003 deduct once on approve
- BR-004 reject/cancel no change
- BR-005 approve only if remaining >= days
- BR-006 working days only, excludes Sat/Sun/holidays → now CONFIRMED by user ("tính theo ngày làm việc")
- BR-007 employee cancel scope
- BR-008 one direct manager
- BR-009 overlap block
- BR-010 valid date range, >= 1 working day
- BR-011 submit block if days > remaining
- BR-012 reject reason required
- BR-013 annual quota = 12 working days/year, cap; system blocks any approval exceeding remaining
- BR-014 audit log immutable
- add BR-015: HR read-only — HR cannot approve/reject/modify leave, only view reports and audit log? That's a permission rule. Good, derived from "nhân sự chỉ cần xem báo cáo". Then FR-008/FR-009 cite it.

Also NFR-003 (access control) cite BR-015? NFRs can cite BRs; lint counts cited BR from FR/NFR/AC blocks. Fine.

FR list:
- FR-001 create/submit
- FR-002 view own balance+status
- FR-003 manager pending list
- FR-004 approve
- FR-005 reject
- FR-006 cancel
- FR-007 notify
- FR-008 audit log + HR read
- FR-009 HR report
- FR-010 → removed (HR assigns quota). Now 9 FRs.

Wait—should I keep FR-010 as something else? No. Delete. Renumber? IDs never reused, so FR-009 is last. Good — keep FR-001..FR-009, no FR-010.

Edge cases table: update HR row: read-only for all states; no update/delete.

Assumptions: remove A-04 (confirmed), A-05 (confirmed one level), A-11 (replaced by BR-013), A-01 revise (HR = viewer only). Renumbering assumptions: skill says IDs never reused, in order of appearance. If I remove A-04, A-11, do I renumber? Reusing/renumbering in a doc revision... "never reused" means don't recycle an ID for a different statement. Removing and renumbering would reuse. Safer: keep existing IDs for surviving assumptions, and drop removed ones, leaving gaps. Gaps in numbering are acceptable (IDs never reused). Hmm, but readability. I think preserving stable IDs across revision is the right call — gaps keep traceability from the previous version. I'll keep A-01..A-19 minus removed ones (A-04, A-05, A-11 removed; A-01 revised). Actually A-05 was "only one approval level" — user confirmed "Quản lý trực tiếp duyệt" so that's confirmed → remove A-05, and BR-001 + maybe BR-016 "single approval level".

Hmm, removing A-04/A-05/A-11 leaves gaps: A-01, A-02, A-03, A-06..A-10, A-12..A-19. Acceptable. Since these stay in doc with same meaning, IDs stable. Good.

A-01 revision: "HR chỉ xem báo cáo và nhật ký, không duyệt đơn, không gán quỹ phép" — that's now confirmed from user, so it's not an assumption at all! It becomes BR-015 + actor table. So remove A-01 entirely. Then quotes in "Basis" column of NFR etc referencing A-nn fine.

Q-02 remove (answered: 12 days). Add narrowed Q about prorating for mid-year hires? That's a genuine gap: "tối đa 12 ngày một năm" — new hire mid-year: do they get 12 or prorated? Neither stated. Options: A-nn (assume full 12 regardless) or Q-nn. Skill says if only someone else can answer → Q-nn. Business policy → Q-nn with HR policy owner. But user said "nhân sự chỉ cần xem báo cáo" — meaning HR doesn't need system functions, but HR/policy owner can still answer. I'll add Q-12 (prorating for mid-year hire/part-time) and Q-13? Keep it tight: add Q-12 only.

Hmm, but "đừng hỏi thêm" — adding new Q rows is fine (documentation, not conversation), but I shouldn't over-proliferate. Add Q-12, keep rest.

Q-03 carry-over: now with 12 days/year cap, still open. Keep.

Also Q-11 removal (duplicate of A-14).

Let me also reconsider Q-01 (deduction timing). With 12 days/year fixed and no HR admin, and the requirement "hệ thống trừ vào số ngày phép còn lại" — the user hasn't answered. Keep Q-01 as top open question. But can I reduce its blast radius? BR-011 already blocks submit if insufficient, which handles both models partially. Fine, keep.

Now count changes. Also must update the "Bối cảnh" source input quote to include second message.

Also Decision table: keep.

Let me write file fully (rewrite). Since read_file was done on this file? I created it via write_file, so writing again — the rule says overwriting a file not read in this session is rejected. I wrote it, which should count as known state? Safer to read it first. Actually I created it with write_file; the tool tracks reads. To be safe, read it then write. It's 192 lines; reading costs tokens. Alternative: use edit_file for targeted edits — several edits. The changes are substantial (remove FR-010, rewrite BR-013, assumptions, HR actor row, glossary, Q updates, plus cite BRs). Reading is safer. Let me read it — but I already have the full content in context from writing it. The tool may still reject. I'll try write_file directly; if rejected, read then write.

Let me draft the full new content.

Also NFR basis: NFR-001 basis A-14; ok.

Also FR-008/FR-009 need to cite BR-015.

Also add FR-002 AC about 12 cap? BR-013 citation.

Let me carefully write.

Language: Vietnamese, headings translated, Gherkin keywords English, MoSCoW English. Avoid vague terms list (nhanh/dễ dàng/phù hợp/hợp lý/v.v./linh hoạt/thân thiện, fast/simple/easy etc.). Note "phù hợp" — avoid. Also avoid "etc.", "TBD", "normally".

Careful: word "nhanh" appears in "nhanh chóng" — avoid entirely. Watch "phù hợp" too. I'll grep after lint anyway (lint checks these).

Write now.

FR-001 ACs keep. Update FR-002 ACs: AC1 "Given đầu năm dương lịch nhân viên có 12 ngày phép và chưa có đơn nào" etc.

BR-013 wording: "**BR-013**: Số ngày phép của mỗi nhân viên là tối đa 12 ngày làm việc trong một năm dương lịch; hệ thống không cho phép tổng số ngày của các đơn Đã duyệt trong năm vượt quá 12 ngày." Cite from FR-002, FR-004, FR-009.

BR-015: "**BR-015**: HR chỉ được đọc đơn, báo cáo và nhật ký; HR không duyệt, không từ chối, không sửa hoặc xóa đơn và không thay đổi số ngày phép của nhân viên."

BR-016: "**BR-016**: Mỗi đơn chỉ qua một cấp duyệt là quản lý trực tiếp; không có cấp duyệt thứ hai." Cite from FR-004.

Hmm BR-001 already says only direct manager approves. BR-016 adds single-level. Fine, cite from FR-004.

Edge cases HR row update.

Also "Quỹ phép năm" glossary: "Số ngày phép tối đa một nhân viên được hưởng trong một năm dương lịch, bằng 12 ngày làm việc." And remove idea of HR assignment.

Scope: remove "HR gán quỹ phép năm" → "HR xem báo cáo ngày phép và nhật ký (chỉ đọc)". Out of scope: "HR gán quỹ phép..." becomes out of scope: "Chức năng gán quỹ phép riêng cho từng nhân viên, vì mức phép là 12 ngày làm việc mỗi năm." Good — that's a Won't-ish scope note.

Actors table: HR row: "Chỉ đọc đơn, báo cáo ngày phép và nhật ký" basis: quote from user message 2.

Also add note in Context: source input second quote.

Now write the file.
Đã có câu trả lời. Mình sẽ cập nhật tài liệu theo đó — 12 ngày làm việc/năm thành quy tắc cố định, HR chỉ đọc, bỏ FR-010.
[Edit] null
[Shell] null
[Thought] Wait — Q-02 and Q-11 removed, A-01, A-04, A-05, A-11 removed. Assumptions A-05 was "only one approval level" — now answered by input, so removed and covered by BR-016. A-04 covered by BR-006 basis. A-01 roles covered by actor table. A-11 covered by BR-013.

Let me verify no dangling A-nn references in definitions that were removed. Lint reported 0 findings, but lint only checks ID patterns for BR/FR/NFR — A-nn and Q-nn refs aren't validated. Let me grep for A-01, A-04, A-05, A-11, Q-02, Q-11 references that no longer have rows.
Lint clean, but lint doesn't check A/Q references — let me verify none point at removed rows.
[Shell] null
[Thought] A refs and Q refs all defined. But skill says IDs never reused, in order of appearance — gaps A-01, A-04, A-05, A-11, Q-02, Q-11 disappeared. Skill says "two digits, in order of appearance, never reused". That's a violation-ish: I removed A-01 (HR role assumption) because now confirmed, A-04 (working days) now confirmed, A-05 (one level) now confirmed by input, A-11 (HR assigns quota) — now HR can't assign, so quota is fixed 12. Q-02 (quota basis) resolved, Q-11 (perf targets) — I folded into A-14? Actually Q-11 was about p95 target; I removed it. Hmm, that's a slight loss: NFR-001 basis is A-14 assumption. Fine, but skill says never reuse IDs. Reusing numbers could confuse traceability — but not reusing means gaps. Actually "never reused" means don't assign A-04 to a different assumption later; my remaining numbers are not reused for different meanings, they retain meanings. Removed ones aren't reused. That's acceptable but a reader may wonder about gaps. Since this is a living doc and confirmations resolved those rows, gaps are legitimate — but skill says "in order of appearance".

Better: renumber sequentially? But other refs cite A-07 etc. Renumbering risks errors but keeps convention. Hmm. Which is right per skill? "IDs `A-01`, `A-02`… — two digits, in order of appearance, never reused". Strictly, remaining should be sequential. But the semantic trace stability matters more? The skill is explicit. Let me renumber sequentially and update all references via sed carefully.

Risk: sed on "A-02"→"A-01" causes cascading collisions. Do it with python mapping one pass.

Mapping: A-02→A-01, A-03→A-02, A-06→A-03, A-07→A-04, A-08→A-05, A-09→A-06, A-10→A-07, A-12→A-08, A-13→A-09, A-14→A-10, A-15→A-11, A-16→A-12, A-17→A-13, A-18→A-14, A-19→A-15, A-20→A-16.

Q: Q-01→Q-01, Q-03→Q-02, Q-04→Q-03, Q-05→Q-04, Q-06→Q-05, Q-07→Q-06, Q-08→Q-07, Q-09→Q-08, Q-10→Q-09, Q-12→Q-10.

Wait — but does doc reference "A-05" anywhere unresolved? No. Also I removed A-01 which described HR role; HR confirmed. Also I removed assumptions about HR assigning quota (A-11) — now out of scope, correct.

Also "Q-02" removed (quota basis) — resolved by "tối đa 12 ngày". Q-11 removed — but NFR-001 target is still unknown! Actually Q-11 asked p95 target; I removed it, meaning user never gave number. A-14 says assumption for NFR-001. Skill: could keep as A-nn. Assumption is fine since I filled a working value. But then the "who owns the metric" question is lost. Hmm — should keep a question about performance target? Skill says NFR needs number + basis (A-nn or Q-nn). A-nn is fine. But losing Q-11 reduces honesty? Assumption covers it. Better: keep Q about performance target owner and restore as Q-10? That would be an open question not answerable by me. I think keep it — measurement owner is genuinely unknown. Let me add Q about success metric owner for performance/approval time. Actually the gap-finder gap #9 (success metric) is unowned. I'll keep one Q for success metric once both perf targets and approval time are covered.

Hmm, I need to weigh: user said don't ask more questions. But open questions table is for other owners, fine to include.

Decision: renumber both A and Q tables sequentially, and include an open question about success metric owner (Q-11 → renumber to Q-10 or last). Let me do:

Q rows order in table currently: Q-01, Q-03, Q-04, Q-05, Q-06, Q-07, Q-08, Q-09, Q-10, Q-12. Renumber to Q-01..Q-10. Then add success metric Q as Q-11? Then not sequential-free of gaps — it's sequential. Fine, add Q-11.

Wait Q-10 currently = approval time metric owner ("Thời gian duyệt trung bình... ai chịu trách nhiệm"). That IS the success metric question partially. So keep as is; no new Q needed.

Let me do the renumber with python.
IDs now have gaps (A-01/A-04/A-05/A-11 and Q-02/Q-11 resolved out). Skill wants sequential order-of-appearance, so let me renumber and fix every citation.
[Shell] null
[Shell] null
[Thought] Two issues: line 19 basis cites "BR-015" in the actors table (fine, it's a citation). Line 34 "Tích hợp với hệ thống nhân sự bên ngoài (xem Q-10, Q-02)" — Q-10 was Q-12 (pro-rata) and Q-02 was Q-03 (carryover). Wait original was "(xem Q-12, Q-03)" → mapped Q-12→Q-10, Q-03→Q-02. Good.

But "Bối cảnh" section removed? Also I should check Q-11 removal: originally Q-11 was p95 target, removed since NFR still cites A-14 (now A-07?) — wait A-14 → A-13? Let me check: amap order A-02→A-01, A-03→A-02, A-06→A-03, A-07→A-04, A-08→A-05, A-09→A-06, A-10→A-07, A-12→A-08, A-13→A-09, A-14→A-10, A-15→A-11, A-16→A-12, A-17→A-13, A-18→A-14, A-19→A-15, A-20→A-16.

So NFR basis A-14 → A-10 (p95). Let me verify NFR table.

Also line 19 actor table cites BR-015 — fine.

Check that Q-01 (deduction timing) still open — yes, user didn't answer that. Hmm, but user said "don't ask more" — so it stays as Q-nn. Good.

Let me check NFR table and remaining refs.

Also should verify no dangling BR refs to BR-016 etc. And check the "Bối cảnh" still present. Let me grep NFR section + count.

Also note: A-02 basis changed by renumber; text says "(Cơ sở: A-02)" for BR-005 — correct mapping of old A-03.

Let me verify NFR rows.
[Shell] null
[Thought] Everything consistent. One thing: BR-004 says "Cơ sở: A-01" which is now "Đơn bị từ chối không làm thay đổi số ngày phép còn lại" — correct. BR-016 cited by FR-004 — good. Line 34 "Tích hợp với hệ thống nhân sự bên ngoài (xem Q-10, Q-02)" — Q-10 was Q-12 (proration, employee joins mid-year) hmm. Original was "(xem Q-12, Q-03)". Q-12 → Q-10 = proration/mid-year; Q-03 → Q-02 = carry-over. Both are HR-system-ish? Mid-year join relates to HR system data. Acceptable but let me reword slightly to be accurate: "Tích hợp với hệ thống nhân sự bên ngoài (xem Q-02, Q-10)" — carry-over and proration both need HR source data. Fine.

Also check BR-008 references A-05 (quản lý trực tiếp). Let me check lines 36-53 for cơ sở correctness.

Also check role table HR row cites BR-015 - good.

Let me do a final check on the "Câu hỏi mở" Q-09 = self-approval, Q-08 = cancel approved. Verify each Q's owner/blocks sane. Also A-06 = A-07 mapping: original A-07 (quản lý trực tiếp) → A-05. Let me grep BR-001 line.

Line 38-ish should say "(Cơ sở: A-05, câu trả lời ...)". Let me check.

Also the doc's scope mentions "Q-10, Q-02" ordering; minor. Also verify no leftover reference to "nhân viên HR gán" etc. Let me grep for "gán" and "HR gán".

Also check that A-03 (trùng khoảng ngày, formerly A-08) is cited as A-03 in BR-009. Let's read lines 36-60.
[Read] null
[Shell] null
[Thought] Renumbering worked correctly. Line 34 "Tích hợp với hệ thống nhân sự bên ngoài (xem Q-10, Q-02)" — Q-02 is carry-over, not integration. Originally it was Q-12 (= employee joins mid-year) and Q-03 (carry-over). Now Q-10 is the mid-year one. Hmm, "Tích hợp với hệ thống nhân sự bên ngoài" should reference... mid-year proration and carry-over? That's a bit odd but tag: originally I wrote "(xem Q-12, Q-03)". Q-12 was proration. Fine — but a more relevant ref would be quota source. Actually out-of-scope "integration with external HR system" — the gap was about where the 12 days comes from. That's now A-16/proration Q-10. Leave it; Q-10 (proration) and Q-02 (carry-over) both need external HR data. Acceptable.

Also BR-001 basis says A-04 which is the "one direct manager" assumption — correct after renumber (A-04 = original A-07). BR-008 also A-04. Good.

Check glossary NFR basis mapping: NFR-001 → A-10 = original A-14 (p95). Good.

Now one more thing: out-of-scope mentions "Chức năng gán quỹ phép riêng cho từng nhân viên" — fine.

Also the section title "Trường hợp biên" has a row "Nhân viên | Đã dùng đủ 12 ngày". Good.

Check that "Số ngày phép còn lại" glossary consistent. Fine.

One issue: draft mode stop rule satisfied. Now: check no stale A-11 reference in prose elsewhere (docs count fine, all defined). Also Q refs in context line: line 34 fine.

Let me verify whole doc reads well around edge cases & the excluded-section note about HR only reading — and also verify the decision table row R5.

Also lint OK. Let me do final render check for line 141 row and section 'Rules recovered from code' deleted (no code). Good.

Final counts: 16 BR, 9 FR, 6 NFR, 42 AC, 16 A, 10 Q.

Let me quickly confirm AC count per FR via lint? Not needed.

Double-check FR-009.AC3 statement "hệ thống không có thao tác đó" — observable. OK.

Report now.
Renumbering + citation swap worked. Doc final.

**File:** `docs/ba/2026-11-18-dang-ky-nghi-phep-requirements.md`

**Đã chốt theo câu trả lời của bạn**
| Câu trả lời | Thành phần trong doc |
|---|---|
| "tính theo ngày làm việc" | BR-006 + FR-001.AC6/AC8 (thứ Bảy, CN, ngày lễ không tính) |
| "tối đa 12 ngày một năm" | BR-013 (chặn vượt 12 ngày/năm) + FR-001.AC7, FR-004.AC6, FR-002.AC1, FR-009.AC2 |
| "Quản lý trực tiếp duyệt" | BR-001, BR-016 (một cấp duyệt) + FR-004.AC4 |
| "nhân sự chỉ xem báo cáo" | BR-015 (chỉ đọc) + FR-004.AC7, FR-008.AC3, FR-009.AC3, NFR-003.AC2; FR-010 gán quỹ phép **đã bỏ** |

**Counts:** 16 BR · 9 FR · 6 NFR · 42 AC · 16 assumptions · 10 open questions · lint **0 findings**

**Top 3 rủi ro còn lại**
1. **Q-01 — trừ lúc gửi hay lúc duyệt?** Vẫn là fork lớn nhất; chưa trả lời. Doc hiện giả định trừ lúc duyệt (BR-003).
2. **Q-02 — phép dư năm trước** có chuyển sang không. Ảnh hưởng FR-002, FR-009.
3. **Q-10 — nhân viên vào giữa năm / bán thời gian** hưởng đủ 12 ngày hay theo tỉ lệ. BR-013 hiện đang áp cứng 12 ngày cho mọi người (A-16).

**Bước tiếp theo:** brainstorm giải pháp dùng file này làm ngữ cảnh, rồi lập kế hoạch triển khai.
