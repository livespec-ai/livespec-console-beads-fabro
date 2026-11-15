---
topic: family-secret-configured-wrapper
author: claude-opus-5-5
created_at: 2026-11-15T05:29:36Z
---

## Proposal: Name the family secret convention's wrapper by interface, not by the 1Password backend

### Target specification files

- SPECIFICATION/non-functional-requirements.md

### Summary

The Beads/Fabro Family Secret Convention clause, the Contributor Scenario E flowchart and its first Gherkin scenario call the injector `the 1Password Environment wrapper`. Call it the configured credential wrapper, name the unchanged installed family interface, and name Parameter Store as the canonical source of the family password. The single bare `BEADS_DOLT_PASSWORD`, the no-per-tenant-variable rule, the never-committed/never-echoed rule and the CI-never-holds-it rule are unchanged; no converted host is asserted. Scenario names are unchanged, so `tests/heading-coverage.json` links are unaffected.

### Motivation

livespec v249 (thewoolleyman/livespec#3252, non-functional-requirements.md fleet-secrets section) makes AWS Systems Manager Parameter Store the single canonical source for fleet secrets, including fleet tenants' beads/Dolt passwords, makes the livespec 1Password Environment a temporary downstream copy, and keeps `/usr/local/bin/with-livespec-env.sh` and its calling convention for callers while only its backend becomes homelab's shared-credentials launcher at each host's conversion. A 1Password backend label in this clause would go false host by host; the interface wording stays true throughout. Plan epic overseer-iyfjbo, change-plan entry C03.

### Proposed Changes

In `SPECIFICATION/non-functional-requirements.md`:

1. In `### Beads/Fabro Family Secret Convention`, Replace

```
The console and its docs MUST use the current family secret convention:
the 1Password Environment wrapper exports one bare `BEADS_DOLT_PASSWORD`.
```

with

```
The console and its docs MUST use the current family secret convention:
the configured credential wrapper exports one bare `BEADS_DOLT_PASSWORD`.
For this family tenant that wrapper is the installed family interface
`/usr/local/bin/with-livespec-env.sh --`, whose path and calling
convention are unchanged as each host's backend converts; AWS Systems
Manager Parameter Store is the canonical source of the family password.
This clause does not assert that any host's wrapper has converted.
```

2. In `## Contributor Scenario E -- Beads/Fabro family secret convention`, in the mermaid flowchart, Replace

```
  OP["1Password Environment wrapper"]
```

with

```
  OP["configured credential wrapper"]
```

3. In the same section, in `Scenario: The console uses the single bare secret`, Replace

```
    Given the 1Password Environment wrapper
    When the console or its docs reference the work-items secret
```

with

```
    Given the configured credential wrapper
    When the console or its docs reference the work-items secret
```

Nothing else in the clause, flowchart or scenarios changes.
