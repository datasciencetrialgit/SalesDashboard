---
name: powerbi-orchestrator
description: Coordinate end-to-end Power BI project development from requirements through deployment using this repository's manifest and focused skills. Use for new projects, continuation, status, phase selection, or cross-cutting changes.
---

# Power BI Orchestrator

Treat `powerbi-project.json` as the project contract and `docs/LIFECYCLE.md` as the lifecycle map.

## Workflow

1. Validate the manifest and determine the configured topology.
2. Inventory existing artifacts and evidence before choosing a phase.
3. Select the earliest incomplete or invalidated phase and load only its focused skill.
4. Make one coherent, reversible change and run the applicable gate.
5. Record architectural decisions, tests, and exceptions under `docs/`.
6. Re-evaluate downstream phases after changes to grain, keys, storage mode, security, or deployment topology.

Route work using `AGENTS.md`. Do not force report work on model-only projects or local-model work on thin reports. Stop when a required source, credential, workspace decision, or Desktop validation must be supplied by the user.
