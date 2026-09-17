---
name: powerbi-testing-validation
description: Validate Power BI manifests, PBIP/TMDL/PBIR structure, data refresh, calculations, visuals, accessibility, security, performance, and Desktop round trips. Use at phase gates and before release.
---

# Power BI Testing and Validation

Match tests to the manifest topology and quality requirements.

## Test layers

1. Manifest and folder topology: run the provided validators.
2. Schema and metadata: validate JSON, TMDL/TMSL, object references, unique IDs, resources, and format consistency.
3. Data: test connectivity, types, row counts, quality rules, folding, refresh, and incremental boundaries.
4. Model and DAX: test relationships, totals, filter contexts, formats, edge cases, and reconciliation.
5. Security: execute the approved persona matrix for RLS/OLS and downstream permissions.
6. Report: verify bindings, filters, sorting, interactions, drill paths, bookmarks, tooltips, mobile layouts, and visual consistency.
7. Accessibility and performance: test manifest thresholds and record evidence.
8. Desktop round trip: open, refresh, save, close, and reopen with the intended Desktop version.
9. Deployment smoke test: validate target parameters, permissions, refresh, app/report access, and rollback readiness.

Static checks never substitute for Desktop or service tests. Record evidence in `docs/QA-RESULTS.md`.
