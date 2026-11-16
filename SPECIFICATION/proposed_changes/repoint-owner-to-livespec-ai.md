---
topic: repoint-owner-to-livespec-ai
author: claude-sonnet-5-5
created_at: 2026-11-16T18:50:00Z
---

## Proposal: Repoint the design-record citations from the thewoolleyman account to the livespec-ai organization

### Target specification files

- SPECIFICATION/contracts.md
- SPECIFICATION/non-functional-requirements.md
- SPECIFICATION/scenarios.md
- SPECIFICATION/spec.md

### Summary

Thirteen citations in the live specification name a fleet repository under its pre-move owner (`thewoolleyman/livespec`, `thewoolleyman/livespec-orchestrator-beads-fabro`). Every fleet repository now lives under the `livespec-ai` organization. Replace the owner segment of each citation; the repository name, the cited file and the cited section stay as they are. No requirement changes meaning: these are design-record and contract-source pointers.

### Motivation

Plan stale-base-merge-options (epic livespec-dev-tooling-xowhol), Definition of Done assertion 7: the committed old-owner grep must count zero graded references in each fleet repository's master tree. The citations are live specification text, so the repoint goes through propose-change and revise rather than a direct edit. A citation that names an account the repository no longer lives under sends a reader to a redirect at best.

### Proposed Changes

In each of the following, replace the owner `thewoolleyman` with `livespec-ai` inside the backticked repository slug, changing nothing else on the line:

1. `SPECIFICATION/contracts.md`, 8 occurrences: line 121 (`thewoolleyman/livespec-orchestrator-beads-fabro`, journal invoker attribution), line 348 (`thewoolleyman/livespec`, design record), line 394 (`thewoolleyman/livespec`, design record), line 422, line 530, line 536, line 611 and line 936 (each `thewoolleyman/livespec-orchestrator-beads-fabro`).
2. `SPECIFICATION/non-functional-requirements.md`, 1 occurrence: line 267 (`thewoolleyman/livespec-orchestrator-beads-fabro`).
3. `SPECIFICATION/scenarios.md`, 1 occurrence: line 362 (`thewoolleyman/livespec-orchestrator-beads-fabro`).
4. `SPECIFICATION/spec.md`, 3 occurrences: line 368 (`thewoolleyman/livespec-orchestrator-beads-fabro`), line 370 (`thewoolleyman/livespec`, `plan/archive/autonomous-mode/handoff.md`) and line 444 (`thewoolleyman/livespec-orchestrator-beads-fabro`).

Line numbers are as of master at filing; the revise pass applies the rule by pattern (`thewoolleyman/(livespec[A-Za-z-]*)` to `livespec-ai/\1`) over those four files. No `## ` heading is added, changed or removed, so `tests/heading-coverage.json` is unaffected.
