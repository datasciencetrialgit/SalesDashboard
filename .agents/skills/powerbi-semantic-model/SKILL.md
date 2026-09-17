---
name: powerbi-semantic-model
description: Design or modify Power BI semantic models in TMDL/TMSL, including tables, relationships, metadata, calculation groups, hierarchies, perspectives, cultures, and refresh policies. Use for model structure rather than report visuals.
---

# Power BI Semantic Model

Honor the manifest's model format and storage mode.

## Modeling sequence

1. Confirm business grain, keys, fact/dimension roles, cardinality, filter direction, and ambiguity risks.
2. Prefer a clear star schema unless a documented requirement justifies another design.
3. Author columns, relationships, hierarchies, formats, descriptions, folders, sort-by columns, and hidden technical fields.
4. Add date tables, calculation groups, perspectives, cultures, and incremental-refresh policies only when declared or justified.
5. Preserve lineage tags and stable object identities in existing projects.
6. Validate relationship paths, blank-row behavior, many-to-many semantics, inactive relationships, and storage-mode compatibility.
7. Hand calculation work to `$powerbi-dax` and security objects to `$powerbi-security-governance`.

Do not rely on auto date/time or implicit measures as a substitute for an intentional governed model.
