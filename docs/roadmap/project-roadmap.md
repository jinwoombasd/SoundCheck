# Slack Codex Bridge Detailed Plan

Created: 2026-06-26

Purpose: This operating plan is the reference Admin Main uses to inspect project status and decide the next automatic task.

## 1. Product Goal

Use Slack as the operating console for GPT, Cursor, and Admin Main agents.

Main is the overall work manager. It interprets user requests, assigns needed work to GPT and Cursor through internal runs, and sends only the final summary to the user.

## 2. Current Reference Structure

```text
User
-> Slack
-> Admin Main
-> Internal run: GPT / Cursor
-> Save Obsidian log
-> Final Slack summary
```

Direct call rules:

```text
No prefix -> Main decides
m: / a: / admin: -> Main handles directly
g: / codex: -> GPT handles directly
c: / cursor: -> Cursor handles directly
```

## 3. Agent Responsibilities

### Main

Main is the manager.

Work to do:

Confirm: Define the purpose and completion criteria for the user request.
Confirm: Decide whether approval is required.
Confirm: Split GPT/Cursor work and integrate their results.
Confirm: Send only the final summary to the user.

Work not to do:

Caution: Do not answer like Cursor Main.
Caution: Do not present subordinate-agent answers as Main's own answer without distinction.
Caution: Do not make large code changes without user approval.

### GPT

GPT owns requirements, design, implementation direction, and documentation.

Assigned work:

Confirm: Organize feature requirements.
Confirm: Propose implementation direction.
Confirm: Clean up docs, README files, and user guidance.
Confirm: Implement within the approved scope.

### Cursor

Cursor owns verification, risk, and the real development-environment perspective.

Assigned work:

Confirm: Analyze change risk.
Confirm: Propose test methods.
Confirm: Check regression risk.
Confirm: Verify issues through execution and logs.

## 4. Operating Principles

1. Main usually acts when the user sends a message.
2. Automatic checks are always on and, by default, only save to Obsidian logs.
3. Automatic checks do not modify code; they only summarize work candidates.
4. Intermediate commands are not shown to the user.
5. Only the final summary is sent to Slack.
6. Obsidian logs are saved in folders by agent.
7. Failures and successes are recorded separately.
8. When the user gives a task, Main reports after completion and then continues with the next small task within the configured step count.
9. Automatic continuation stops when approval is required, a large change appears, or a failure occurs.
10. When approval is required, Main immediately sends an approval request in Slack and saves a waiting-approval plan.

## 5. Priority Roadmap

Current status: P0 through P4 are all complete. The items below remain as completed operating standards and regression-prevention checklists.

### P0. Stabilization - Complete

Goal: Remove duplicate replies, missing replies, and role confusion in Slack.

Tasks:

Confirm: Keep `m:` requests handled directly by Main.
Confirm: Let Main judge requests without a prefix.
Confirm: Check whether GPT stdin failures recur.
Confirm: Prevent duplicate Cursor replies.
Confirm: Keep GPT/Cursor labels in Main summaries.

Completion criteria:

Confirm: `m: What is your role?` returns only the Main role.
Confirm: `c: test` is answered only by Cursor.
Confirm: `g: test` is answered only by GPT.
Confirm: Unprefixed status questions return only the Main summary.

### P1. Status Tracking Improvements - Complete

Goal: Let Main know task completion and failure accurately.

Tasks:

Confirm: Expand step status to `pending / running / complete / failed`.
Confirm: Save execution time and failure reason by agent.
Confirm: Record success/failure clearly in `current-plan.md`.
Confirm: Distinguish timeouts from real failures.

Completion criteria:

Confirm: Main does not mistake `sent` for completion.
Confirm: If GPT or Cursor fails, the Slack summary includes the failure cause.

### P2. Automatic Operation Improvements - Complete

Goal: Let Main periodically inspect project status and create work candidates.

Tasks:

Confirm: Keep Auto Main always on.
Confirm: Automatic checks read `project-roadmap.md`, `current-plan.md`, and recent logs together.
Confirm: Automatic checks only create work candidates and do not modify code.
Confirm: Split whether automatic-check results go to Slack or only Obsidian through configuration.

Completion criteria:

Confirm: Automatic checks do not change files without user approval.
Confirm: Automatic-check summaries stay within five lines.

### P3. Tests and Operation Scripts - Complete

Goal: Operate the bridge safely without manual verification each time.

Tasks:

Confirm: Add router unit tests.
Confirm: Add GPT/Cursor runner smoke tests.
Confirm: Add process restart scripts.
Confirm: Add `npm run health`.

Completion criteria:

Confirm: One command checks GPT/Cursor/Admin run status.
Confirm: Routing rules are protected by tests.

### P4. Documentation Cleanup - Complete

Goal: Let users operate the bridge directly without confusion.

Tasks:

Confirm: Update README to match the current internal-run structure.
Confirm: Keep `docs/agents/main.md` aligned with actual behavior.
Confirm: Write the operations FAQ.
Confirm: Document common commands.

Completion criteria:

Confirm: A new user can run, stop, and check status within five minutes.

## 6. Main Automatic Decision Criteria

Main judges requests in this order:

```text
1. Can Main answer directly?
2. Is it ambiguous or a large change?
3. Should GPT handle planning/implementation?
4. Should Cursor handle verification/risk review?
5. Are both needed?
6. Can it proceed without approval?
7. What is the final summary?
```

Handled directly by Main:

Confirm: Role questions
Confirm: Bridge operating explanations
Confirm: Routing-rule explanations
Confirm: Simple status summaries
Confirm: Approval request / waiting-approval guidance

Assigned to GPT:

Confirm: Requirements organization
Confirm: Implementation direction
Confirm: Documentation drafts
Confirm: Small code changes

Assigned to Cursor:

Confirm: Failure-cause investigation
Confirm: Test methods
Confirm: Change risk
Confirm: Real execution-state verification

Assigned to both:

Confirm: Feature implementation plus verification
Confirm: Design changes plus regression risk
Confirm: Operating-structure changes

## 7. Current Next Work

Completed:

1. Confirmed P0 stabilization.
2. Updated README from the old Slack relay-command explanation to the current internal-run structure.
3. Kept `current-plan.md` as the temporary request board and this document as the long-term plan.
4. Added router tests and runner smoke tests.
5. Designed the `npm run health` script.
6. Completed P1 status-tracking improvements.
7. Verified P2 automatic-check candidates, logs, and save location.
8. Cleaned up P4 operations documentation.
9. Added process restart scripts and operations documentation.
10. Reflected P0-P4 completion in the roadmap reference document.
11. Prepared public Markdown documents for upload by translating them to English and removing Korean filenames.
12. Aligned stale current-plan records with the latest English current-plan state.
13. Verified public Markdown language consistency and upload-exclusion safety.

Next candidates:

1. Close the operations-stabilization phase and proceed with product-side Week 1 from the separate 12-week plan.
2. Run an actual Slack app restart only after separate approval because it controls live operation processes.
3. Before approval, proceed only with small verification work such as documentation consistency checks, test hardening, and health-result checks.

## 8. Approval Required Criteria

Main must ask for user approval before the following work:

Caution: Many-file changes
Caution: Slack token/env changes
Caution: Changing automatic operation to default ON
Caution: Changing scheduled work to auto-post Slack messages
Caution: Changes where bridge run/stop scripts kill existing processes
Caution: Large Obsidian log path moves

## 9. Report Format

Slack reports are written without hyphen bullets.

```text
Summarize the completed work in one line.
Confirm: What was done
Caution: Risk or limitation
Next: Next action
```

Main labels GPT/Cursor results when combining them.

```text
Confirm: GPT: ...
Confirm: Cursor: ...
```
