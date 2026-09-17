---
name: powerbi-requirements-planning
description: Turn business questions and constraints into a Power BI project brief, manifest, architecture choices, acceptance criteria, and delivery plan. Use before authoring or when scope materially changes.
---

# Power BI Requirements and Planning

Capture decisions that materially affect implementation:

- audiences, decisions, questions, KPIs, definitions, grain, and time logic;
- source owners, latency, history, volume, data quality, privacy, and gateway constraints;
- report, semantic model, thin-report, embedded, paginated, or service-only deliverables;
- Import, DirectQuery, Direct Lake, Composite, or LiveConnection tradeoffs;
- RLS/OLS, sensitivity, accessibility, performance, refresh, distribution, and support expectations;
- environments, release approvals, rollback, ownership, and success measures.

Update `powerbi-project.json`, `docs/PROJECT-BRIEF.md`, and architecture decisions. Mark unknowns explicitly. Do not invent tables, measures, layouts, workspaces, or security rules. Hand off to `$powerbi-project-setup` only when the topology and acceptance criteria are sufficiently concrete.
