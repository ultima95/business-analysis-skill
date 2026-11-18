---
name: business-analysis
description: Use when asked to analyze a business process, gather or elicit requirements, write user stories or acceptance criteria, or produce a BRD, gap analysis, process map, or stakeholder register — including turning a task, ticket, meeting transcript, or email thread into testable requirements, and analyzing non-software processes (approvals, onboarding, invoicing). Triggers on "business analysis", "BA", "requirements for…", "as-is / to-be", "phân tích nghiệp vụ", "thu thập yêu cầu". Not for designing or building the solution — hand off to brainstorming after this.
---

# Business Analysis

## Overview

Turn a thin task, ticket, transcript, or process description into complete, testable requirements and process analysis. Own **what** and **why**: problem, stakeholders, business rules, exception paths, edge cases, non-functional needs, success metrics. Never **how**: no technology, architecture, schema, screen, or UI choice. Job 1 ends by naming the handoff file and pointing to brainstorming / writing-plans with it as context.

## When not to use

| Request | Route |
|---|---|
| "build / implement / create X", "add X to the app" | brainstorming, then writing-plans — not this skill |
| validate a diff or review code | code-validate |
| "analyze this process", "gather requirements for…", "write user stories", "write a BRD", "as-is / to-be", "gap analysis", "requirements from this ticket/meeting/email", "phân tích nghiệp vụ" | this skill |

A build request that merely mentions a domain noun ("build a leave-request app") stays with brainstorming.

## Pick the job

| Job | Request looks like | Output | Load |
|---|---|---|---|
| 1 Feed dev work | task, ticket, vague ask, notes | requirements, user stories, acceptance criteria, edge cases, assumptions, open questions | `references/requirements.md`, `templates/requirements.md` |
| 2 Analyze a process | description of how the business does X today | as-is map, pain points + root causes, to-be map, gaps | `references/process-analysis.md`, `templates/process-doc.md` |
| 3 Formal artifacts | output of job 1 or 2 | BRD, gap analysis, process doc, stakeholder register | `templates/brd.md`, `templates/gap-analysis.md`, `templates/process-doc.md`, `templates/stakeholder-register.md` |

Which file each request writes:

| Request | Files |
|---|---|
| Job 1 alone | `…-requirements.md` (handoff) |
| Job 1 + 3 | `…-brd.md` **instead of** the handoff — the BRD holds the requirements and is itself the handoff brainstorming reads |
| Job 2 alone | `…-process.md` (SIPOC, as-is, pain points, root cause, to-be, gap table) |
| Job 2 + 3 | the process doc, plus `…-gap-analysis.md` and/or `…-stakeholders.md`; formal docs link to the process doc, never restate it |
| Job 2 → 1 | process doc first; requirements/BRD for the to-be cite process steps |

Requirements (BR/FR/NFR) are defined in exactly one file per analysis; every other file cites them by ID. Jobs combine. Ambiguous job → ask once.

## Pick the mode

| Mode | Predicate | Behavior |
|---|---|---|
| Interview | user is present and has not opted out of questions | ask one question per message, highest-impact gap first; play back understanding as it forms |
| Draft | user said "just draft" / "don't ask", the session is autonomous, or someone else's material is analyzed offline | write the document anyway; every unknown becomes an A-nn or Q-nn |
| Hybrid | user is present AND the input is someone else's material (transcript, email thread, ticket written by another person) | interview only on gaps the user can answer (goals, priorities, scope); author-only gaps become Q-nn with that author as owner |

Pasted transcripts default to hybrid.

**One interview message contains, in order:**

1. Your current understanding, in 2–5 lines (or the draft gap table).
2. The single gap whose answer changes the most requirements.
3. Exactly one question, as the last line.

Then stop and wait. Ask the next question only after the answer arrives or the user opts out.

## Core loop

1. **Pick job(s)** from the request. Ambiguous → ask once.
2. **Read the input** (text or file paths). Job 1 inside a repo → also recover current rules via `references/code-recovery.md`, citing `file:line`.
3. **Run the gap-finder** (`references/elicitation.md`) → gap list.
4. **Pick the mode** (table above). Interview: one question at a time by impact. Draft: record each gap as A-nn or Q-nn.
5. **Analyze** using the job's reference.
6. **Write** from the job's template; delete sections that do not apply (never "N/A").
7. **Lint** every doc that contains requirement IDs: `python3 scripts/lint_requirements.py <files…>`. Fix each finding or record why it stays (a genuinely qualitative NFR becomes a Q-nn). Pass all files of one analysis in a single call — they share one ID namespace. Lint sets that contain a requirements-bearing doc (handoff or BRD).
8. **Report** in the format below.

## Output location, names, language

| Where | Path |
|---|---|
| Inside a git repo | `docs/ba/` at the repo root |
| No repo | `./ba/` in the current directory |
| User preference | overrides both |

File names: `YYYY-MM-DD-<topic>-requirements.md`, `-brd.md`, `-process.md`, `-gap-analysis.md`, `-stakeholders.md`.

Output language follows the input's language (Vietnamese in → Vietnamese doc). Templates are English — when writing another language, translate headings, the FR statement frame (`As a … I want … so that …`, `The system shall …`), and labels such as `Fulfils` and `Priority:`. IDs (`FR-001`), Gherkin keywords (`Given` / `When` / `Then`), and Mermaid syntax stay English; MoSCoW values stay `Must` / `Should` / `Could` / `Won't`.

## Report format

Reply with: file path(s) · counts (BR / FR / NFR / AC / open questions) · top 3 risks or open questions · next step. After job 1 the next step is brainstorming (then writing-plans) with the handoff file as context. After job 2, the next step is the to-be requirements or the formal artifact the user asked for.

## Quick reference

| Element | Canonical form |
|---|---|
| Business rule | `- **BR-001**: <rule>.` |
| Functional requirement | `- **FR-001**: As a <role>, I want <capability>, so that <outcome>. Fulfils [BR-001].` |
| Non-user-facing FR | `- **FR-002**: The system shall <behavior>.` |
| Acceptance criterion | `- **FR-001.AC1**: Given <context>, When <action>, Then <outcome>.` |
| Non-functional requirement | `| NFR-001 | <priority> | <measurable target> | <basis: input quote, A-nn, or Q-nn> |` plus `- **NFR-001.AC1**: Given …, When …, Then ….` |
| Open question | `| Q-01 | <question> | <owner> | blocks FR-00x |` |
| Assumption | `| A-01 | <assumption> | <basis in input or impact if false> |` |

- IDs use three digits or more (`BR-001`, `FR-012`, `NFR-003`); acceptance criteria carry the parent ID.
- Every FR/NFR gets a MoSCoW priority. One story = one FR — no `US-nnn`.
- Process docs number steps `P1`, `P2`… in plain prose; they get BR IDs only when job 2 → 1 turns them into requirements.
- Rich detail: gap-finder and modes in `references/elicitation.md`; IDs, stories, Gherkin, edge cases, decision tables in `references/requirements.md`; repo rules in `references/code-recovery.md`; Mermaid swimlanes, SIPOC, wastes, 5 Whys in `references/process-analysis.md`.

## Red flags

Stop and fix before writing the document:

| Signal | Reality |
|---|---|
| A metric, stakeholder, rule, quote, actor, role, team, permission, or system or component name that is not in the input or the user's answers, written as fact | Invented. Every one must be an A-nn or a Q-nn, never a confirmed statement. |
| "The ticket implies…", "a sensible default…", "customers expect…" | Still an invention. Record it as A-nn. |
| More than one question in an interview message | Ask the single highest-impact one, then stop. |
| Unknowns written as prose ("assumptions to validate") | Use the A-nn and Q-nn tables; every Q-nn names an owner and the requirement it blocks. |
| A question about stack, framework, database, or screens | That is solution design — drop it. |
