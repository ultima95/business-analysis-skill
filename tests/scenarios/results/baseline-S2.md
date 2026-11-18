# Baseline S2 — Invoice approval process (single turn)

| Field | Value |
|---|---|
| Phase | baseline (no skill) |
| Run | 1 |
| Agent id | `260f5089-99bb-443e-ae81-ca96a4775771` |
| Model | `command-code/deepseek/deepseek-v4.1-flash` |
| Raw log | `raw/baseline-S2-1.md` |
| Saved doc | `raw/baseline-S2-1-files/invoice-approval-process.md` (298 lines) |
| Git status | `raw/baseline-S2-1-files/_git-status.txt` |
| Lint | not part of this scenario's rubric (no run) |

## Rubric

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Process doc written | yes | `_git-status.txt:2` "?? invoice-approval-process.md". |
| 2 | As-is Mermaid swimlane | no | `invoice-approval-process.md:54` "flowchart LR" then a flat role-to-role edge list (`:55-62`) — `grep -c subgraph` → 0. Roles are node labels, not lanes. |
| 3 | To-be Mermaid swimlane | no | The to-be diagram is `invoice-approval-process.md:123` "stateDiagram-v2" — an invoice lifecycle, not a `flowchart` and with no per-role `subgraph`. |
| 4 | SIPOC present | no | `grep -iE 'SIPOC\|Suppliers'` over the doc → 0 matches. The role table at `:10-15` lists "Role / Who / What they need", which is not SIPOC. |
| 5 | Pain points tied to steps | no | Only four findings carry step refs (`:69-77` "**Steps 3–5: queue in one person's inbox.**", "**Step 8: re-keying…**"). The ten named failure modes at `:81-92` reference triggers ("Manager on leave, travelling, or inbox backlog"), never a step number, and the mapping table at `:226-236` ties fixes to pain, not to steps. |
| 6 | Root cause for top pain | yes | `:94` "### 2.5 Root causes (not symptoms)" → `:103-104` "**Approval is sequential and single-threaded** — one unavailable person blocks everything, with no delegation path", matching the top pain callout at `:69`. |

**Score: 2 pass / 4 fail.**

## Failure patterns

- **Chose diagram types by rendering convenience, not by role.** `raw/baseline-S2-1.md:106` "maybe a small mermaid diagram — GitHub renders mermaid. Could add both a numbered flow and mermaid." It produced one flat `flowchart LR` for as-is and a `stateDiagram-v2` for to-be, so neither diagram shows which role does what — the cross-role handoff, which is the whole point of the process, is invisible.
- **Replaced SIPOC with ad-hoc tables.** Its own outline (`raw/baseline-S2-1.md:27-38`) lists "Purpose/scope / Current process … Failure modes / Root causes / Future state … Mapping table as-is step → to-be / … Open questions" — SIPOC never entered the plan, and none was written.
- **Tied pain to prose, not to the step map.** `raw/baseline-S2-1.md:28` "state model of a row, exception/failure modes with frequency/impact" — the failure-modes table (`:81-92`) is organised by failure name and trigger, so a reader cannot point to the step where each pain occurs.
- **Silently invented numbers the user never gave.** `:39-43` sets success targets ("≥ 80%", "≥ 95%", "−90% vs. baseline") and `:171-177` invents threshold A/B routing without flagging any of it as assumption or question; only a later section (`:274-286`) lists open questions.
