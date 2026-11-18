# green lane-3 — agent 03ffd20c-ff92-473a-8c32-04c88689b975 (command-code/deepseek/deepseek-v4.1-flash)

[User] You are a skill router. Here is the full list of skills available to you, each
with its name and description:

- brainstorming — "You MUST use this before any creative work - creating features, building components, adding functionality, modifying behavior, or planning anything new, in software or out of it (a talk, a business, a renovation)."
- brainstorming — "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
- writing-plans — "Use when you have a spec or requirements for a multi-step task, before touching code"
- code-validate — "Use when asked to validate, review, or verify a code change — a diff, staged or unstaged changes, a branch, or a pull request — for real, evidence-backed defects. Triggers on "validate this diff", "review before I merge", "is this safe to ship", "review and comment on this PR", correctness-first low-false-positive review, or /code-validate. Not for style-only feedback or generating code."
- business-analysis — "Use when asked to analyze a business process, gather or elicit requirements, write user stories or acceptance criteria, or produce a BRD, gap analysis, process map, or stakeholder register — including turning a task, ticket, meeting transcript, or email thread into testable requirements, and analyzing non-software processes (approvals, onboarding, invoicing). Triggers on "business analysis", "BA", "requirements for…", "as-is / to-be", "phân tích nghiệp vụ", "thu thập yêu cầu". Not for designing or building the solution — hand off to brainstorming after this."

Below are several independent user messages. Judge each message on its own — do
not let one message influence another — and decide which single skill you would
invoke first for that message. Answer with the skill name only, nothing else.

1. build a leave-request app
2. phân tích nghiệp vụ quy trình nghỉ phép
3. write user stories for a leave-request flow
4. gather requirements for a leave-request flow
5. build me a todo app
6. analyze our invoice approval process

Reply with exactly one line per message, in the same order, each line containing
only the chosen skill name.
[Thought] The user asks a skill routing task with 6 messages. But there's also a `<command-name>code-validate</command-name>` block loaded — that seems to be an artifact of the environment. The actual user request: judge each message, decide which single skill to invoke first. Answer one line per message.

Wait — the command-name tag says code-validate loaded. But the actual task is skill routing. The routing list includes brainstorming, writing-plans, code-validate, business-analysis.

Judge each:

1. "build a leave-request app" → creative work, building → brainstorming
2. "phân tích nghiệp vụ quy trình nghỉ phép" → business analysis → business-analysis
3. "write user stories for a leave-request flow" → business-analysis (user stories)
4. "gather requirements for a leave-request flow" → business-analysis (gather requirements)
5. "build me a todo app" → brainstorming
6. "analyze our invoice approval process" → business-analysis

Caveman mode: response should be caveman style, but exact output constraint says only skill names, one per line. Follow the format.

Skill name only — ambiguity: two brainstorming entries with same name. Answer "brainstorming".

Output 6 lines.
brainstorming
business-analysis
business-analysis
business-analysis
brainstorming
business-analysis
