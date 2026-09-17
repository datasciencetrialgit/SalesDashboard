---
name: powerbi-performance
description: Diagnose and optimize Power BI model size, refresh, Power Query folding, DirectQuery behavior, DAX queries, visual rendering, and capacity impact. Use when measured performance misses project targets.
---

# Power BI Performance

Optimize from evidence, not intuition.

## Workflow

1. Reproduce the slow refresh, query, page, or deployment under controlled conditions.
2. Capture baseline duration, query count, model size, cardinality, source workload, cache state, and capacity context.
3. Localize the bottleneck to source, M, gateway, storage engine, formula engine, model design, visual queries, custom visuals, or capacity.
4. Apply the smallest corrective change and repeat the same measurement.
5. Check correctness, security, freshness, and user experience for regressions.
6. Record before/after results against manifest thresholds.

Typical levers include reducing high-cardinality columns, preserving folding, improving star-schema paths, limiting visuals, simplifying DAX, aggregations, incremental refresh, and source indexing. Do not change storage mode or business semantics without an architecture decision.
