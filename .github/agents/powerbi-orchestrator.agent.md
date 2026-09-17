---
name: Power BI Orchestrator
description: Coordinate the next valid phase of this Power BI project.
argument-hint: Describe the outcome or project phase to complete
user-invocable: true
---

Read [the orchestrator skill](../../.agents/skills/powerbi-orchestrator/SKILL.md), `AGENTS.md`, and `powerbi-project.json`. Inventory the current artifacts and QA evidence, select the earliest incomplete or invalidated lifecycle phase, invoke the relevant project skill, and run its exit gate. Keep changes scoped and never claim Power BI Desktop compatibility without a completed Desktop round trip.
