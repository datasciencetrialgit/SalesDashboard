---
name: powerbi-pbir-authoring
description: Author or modify enhanced PBIR report definitions, pages, visuals, filters, bookmarks, resources, and semantic-model references. Use after report design and model contracts are stable.
---

# Power BI PBIR Authoring

Read `docs/PBIR-GUARDRAILS.md` before writing report metadata.

## Workflow

1. Confirm the report format, semantic-model reference, schema version, and Desktop compatibility target.
2. Build and validate the report shell before resources, page shells before visuals, and visual groups before full-page changes.
3. Preserve stable page/visual IDs and unknown supported properties when modifying existing reports.
4. Register themes, images, and custom resources using the exact current schema and safe resource paths.
5. Bind only existing model fields, measures, hierarchies, or report measures.
6. Implement filters, interactions, bookmarks, drillthrough, tooltips, and mobile definitions according to the design contract.
7. Run `$powerbi-testing-validation` after every structural layer and visual group.

When exact JSON is uncertain, inspect a current Desktop-generated example and official schema. Never guess a visual property shape or claim rendering from JSON parsing alone.
