---
name: powerbi-dax
description: Design, author, format, test, and optimize DAX measures, calculation items, and query-based reconciliation for Power BI semantic models. Use for calculation logic, not Power Query transformations.
---

# Power BI DAX

Start from the KPI definition, grain, filter context, time semantics, and expected examples in the project contract.

## Workflow

1. Define the base measure and its business meaning before derived measures.
2. Use explicit measures, safe division, variables, and reusable branching where they improve correctness.
3. Apply format strings, display folders, descriptions, and ownership metadata.
4. Test totals, subtotals, blanks, zero denominators, sparse periods, multiple selections, inactive relationships, and security context.
5. Reconcile representative results to a trusted source using DAX queries or an approved external calculation.
6. Measure performance before rewriting logic; then use `$powerbi-performance` when optimization is needed.

Avoid calculated columns for logic that belongs in Power Query or a measure. Do not change a business definition merely to simplify DAX.
